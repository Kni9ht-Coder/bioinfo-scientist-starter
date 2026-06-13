"""Literature search helpers for the Literature Scout / Idea Generator module.

Design goals (see AGENTS.md):
- Never fabricate citations. Every record keeps verifiable identifiers
  (DOI / PMID / arXiv ID / URL) straight from the source API.
- Parsing logic is pure (text/JSON in, structured records out) so it can be
  unit-tested without touching the network.
- Network access lives in thin wrapper functions that fail with clear errors.

Supported sources (public, no API key required for basic use):
- PubMed via NCBI E-utilities (esearch + efetch).
- Semantic Scholar Academic Graph API (paper search).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field

PUBMED_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = "title,abstract,year,venue,authors,externalIds,url"
DEFAULT_TOOL = "bioinfo-scientist"
DEFAULT_TIMEOUT = 30


class LiteratureSearchError(RuntimeError):
    """Raised when a literature source cannot be reached or returns bad data."""


@dataclass
class Paper:
    """A normalized literature record shared across all sources."""

    title: str
    source: str
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    abstract: str | None = None
    doi: str | None = None
    pmid: str | None = None
    arxiv_id: str | None = None
    url: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


# ---------------------------------------------------------------------------
# URL builders (pure)
# ---------------------------------------------------------------------------
def pubmed_esearch_url(
    query: str,
    max_results: int,
    *,
    email: str | None = None,
    api_key: str | None = None,
    tool: str = DEFAULT_TOOL,
) -> str:
    params: dict[str, str] = {
        "db": "pubmed",
        "term": query,
        "retmax": str(max_results),
        "retmode": "json",
        "tool": tool,
    }
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key
    return f"{PUBMED_EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"


def pubmed_efetch_url(
    pmids: list[str],
    *,
    email: str | None = None,
    api_key: str | None = None,
    tool: str = DEFAULT_TOOL,
) -> str:
    params: dict[str, str] = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "rettype": "abstract",
        "tool": tool,
    }
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key
    return f"{PUBMED_EUTILS}/efetch.fcgi?{urllib.parse.urlencode(params)}"


def semantic_scholar_search_url(query: str, max_results: int) -> str:
    params = {
        "query": query,
        "limit": str(max_results),
        "fields": SEMANTIC_SCHOLAR_FIELDS,
    }
    return f"{SEMANTIC_SCHOLAR_SEARCH}?{urllib.parse.urlencode(params)}"


# ---------------------------------------------------------------------------
# Parsers (pure: no network)
# ---------------------------------------------------------------------------
def parse_pubmed_esearch_json(payload: str) -> list[str]:
    """Return the list of PMIDs from an esearch JSON response."""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise LiteratureSearchError(f"Invalid PubMed esearch JSON: {exc}") from exc
    idlist = data.get("esearchresult", {}).get("idlist", [])
    return [str(pmid) for pmid in idlist]


def _text(element: ET.Element | None) -> str | None:
    if element is None:
        return None
    text = "".join(element.itertext()).strip()
    return text or None


def parse_pubmed_efetch_xml(xml_text: str) -> list[Paper]:
    """Parse an efetch ``PubmedArticleSet`` XML document into ``Paper`` records."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise LiteratureSearchError(f"Invalid PubMed efetch XML: {exc}") from exc

    papers: list[Paper] = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find("./MedlineCitation")
        if medline is None:
            continue
        pmid = _text(medline.find("./PMID"))
        art = medline.find("./Article")
        if art is None:
            continue
        title = _text(art.find("./ArticleTitle")) or "Untitled"

        abstract_parts = [
            txt for node in art.findall("./Abstract/AbstractText") if (txt := _text(node))
        ]
        abstract = " ".join(abstract_parts) if abstract_parts else None

        authors: list[str] = []
        for author in art.findall("./AuthorList/Author"):
            last = _text(author.find("./LastName"))
            initials = _text(author.find("./Initials"))
            collective = _text(author.find("./CollectiveName"))
            if last:
                authors.append(f"{last} {initials}".strip() if initials else last)
            elif collective:
                authors.append(collective)

        venue = _text(art.find("./Journal/Title"))
        year = _text(art.find("./Journal/JournalIssue/PubDate/Year"))
        if year is None:
            medline_date = _text(art.find("./Journal/JournalIssue/PubDate/MedlineDate"))
            if medline_date:
                year = medline_date[:4]

        doi = None
        for elocation in art.findall("./ELocationID"):
            if elocation.get("EIdType") == "doi":
                doi = _text(elocation)
                break
        if doi is None:
            for article_id in article.findall("./PubmedData/ArticleIdList/ArticleId"):
                if article_id.get("IdType") == "doi":
                    doi = _text(article_id)
                    break

        url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None
        papers.append(
            Paper(
                title=title,
                source="pubmed",
                authors=authors,
                year=int(year) if year and year.isdigit() else None,
                venue=venue,
                abstract=abstract,
                doi=doi,
                pmid=pmid,
                url=url,
            )
        )
    return papers


def parse_semantic_scholar_json(payload: str) -> list[Paper]:
    """Parse a Semantic Scholar paper-search JSON response into ``Paper`` records."""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise LiteratureSearchError(f"Invalid Semantic Scholar JSON: {exc}") from exc

    papers: list[Paper] = []
    for item in data.get("data", []) or []:
        external = item.get("externalIds") or {}
        authors = [a.get("name", "").strip() for a in (item.get("authors") or []) if a.get("name")]
        year_raw = item.get("year")
        papers.append(
            Paper(
                title=item.get("title") or "Untitled",
                source="semantic_scholar",
                authors=authors,
                year=int(year_raw) if isinstance(year_raw, int) else None,
                venue=item.get("venue") or None,
                abstract=item.get("abstract") or None,
                doi=external.get("DOI"),
                pmid=str(external["PubMed"]) if external.get("PubMed") else None,
                arxiv_id=external.get("ArXiv"),
                url=item.get("url") or None,
            )
        )
    return papers


# ---------------------------------------------------------------------------
# Deduplication (pure)
# ---------------------------------------------------------------------------
def _dedupe_key(paper: Paper) -> str:
    if paper.doi:
        return f"doi:{paper.doi.lower()}"
    if paper.pmid:
        return f"pmid:{paper.pmid}"
    if paper.arxiv_id:
        return f"arxiv:{paper.arxiv_id.lower()}"
    return f"title:{' '.join(paper.title.lower().split())}"


def dedupe_papers(papers: list[Paper]) -> list[Paper]:
    """Drop duplicate papers, preferring the first occurrence of each key."""
    seen: dict[str, Paper] = {}
    for paper in papers:
        key = _dedupe_key(paper)
        if key not in seen:
            seen[key] = paper
    return list(seen.values())


# ---------------------------------------------------------------------------
# Network wrappers (thin; clear failures)
# ---------------------------------------------------------------------------
def fetch_url(url: str, *, timeout: int = DEFAULT_TIMEOUT) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": f"{DEFAULT_TOOL}/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise LiteratureSearchError(f"HTTP {exc.code} for {url}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise LiteratureSearchError(f"Network error for {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise LiteratureSearchError(f"Timed out after {timeout}s for {url}") from exc


def search_pubmed(
    query: str,
    max_results: int,
    *,
    email: str | None = None,
    api_key: str | None = None,
    pause: float = 0.34,
) -> list[Paper]:
    esearch = fetch_url(pubmed_esearch_url(query, max_results, email=email, api_key=api_key))
    pmids = parse_pubmed_esearch_json(esearch)
    if not pmids:
        return []
    time.sleep(pause)
    efetch = fetch_url(pubmed_efetch_url(pmids, email=email, api_key=api_key))
    return parse_pubmed_efetch_xml(efetch)


def search_semantic_scholar(query: str, max_results: int) -> list[Paper]:
    payload = fetch_url(semantic_scholar_search_url(query, max_results))
    return parse_semantic_scholar_json(payload)


def search_literature(
    query: str,
    max_results: int,
    *,
    sources: list[str] | None = None,
    email: str | None = None,
    api_key: str | None = None,
) -> list[Paper]:
    """Search the requested sources and return a deduplicated list of papers."""
    sources = sources or ["pubmed", "semantic_scholar"]
    collected: list[Paper] = []
    errors: list[str] = []
    for source in sources:
        try:
            if source == "pubmed":
                collected.extend(search_pubmed(query, max_results, email=email, api_key=api_key))
            elif source == "semantic_scholar":
                collected.extend(search_semantic_scholar(query, max_results))
            else:
                raise LiteratureSearchError(f"Unknown source: {source}")
        except LiteratureSearchError as exc:
            errors.append(str(exc))
    if not collected and errors:
        raise LiteratureSearchError("; ".join(errors))
    return dedupe_papers(collected)


def papers_to_payload(query: str, papers: list[Paper]) -> dict[str, object]:
    return {
        "query": query,
        "n_results": len(papers),
        "results": [p.to_dict() for p in papers],
    }
