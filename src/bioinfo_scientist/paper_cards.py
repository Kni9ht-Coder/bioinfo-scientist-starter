"""Turn verified literature records into structured paper cards.

Only verifiable metadata (title, authors, year, venue, identifiers) is filled
in from the source data. Interpretive fields (task, method, key result,
limitations, relevance, supportable claims) are left as explicit ``TODO`` markers
so they are filled by a human or by Codex *after reading the paper* -- never
fabricated. This mirrors literature/paper_cards/TEMPLATE.md.
"""

from __future__ import annotations

import re

from bioinfo_scientist.literature import Paper

TODO = "TODO: read paper to fill in"


def make_citation_key(paper: Paper) -> str:
    """Build a stable citation key like ``smith2021peptide``."""
    if paper.authors:
        first_author = paper.authors[0]
        last = first_author.split()[0] if first_author.split() else first_author
    else:
        last = "anon"
    year = str(paper.year) if paper.year else "nd"
    title_word = ""
    for token in re.findall(r"[A-Za-z]+", paper.title or ""):
        if token.lower() not in {"the", "a", "an", "of", "and", "for", "to", "in", "on"}:
            title_word = token.lower()
            break
    key = f"{last}{year}{title_word}".lower()
    return re.sub(r"[^a-z0-9]", "", key) or "unknownkey"


def best_identifier(paper: Paper) -> str:
    if paper.doi:
        return f"DOI:{paper.doi}"
    if paper.pmid:
        return f"PMID:{paper.pmid}"
    if paper.arxiv_id:
        return f"arXiv:{paper.arxiv_id}"
    return "unverified"


def render_paper_card(paper: Paper) -> str:
    """Render a markdown paper card matching literature/paper_cards/TEMPLATE.md."""
    authors = ", ".join(paper.authors) if paper.authors else "TODO: confirm authors"
    lines = [
        "# Paper card",
        "",
        f"- citation_key: {make_citation_key(paper)}",
        f"- title: {paper.title}",
        f"- authors: {authors}",
        f"- year: {paper.year if paper.year is not None else 'TODO: confirm year'}",
        f"- venue: {paper.venue or 'TODO: confirm venue'}",
        f"- DOI/PMID/arXiv: {best_identifier(paper)}",
        f"- url: {paper.url or 'TODO'}",
        f"- source: {paper.source}",
        f"- verified: {'yes' if (paper.doi or paper.pmid or paper.arxiv_id) else 'no'}",
        f"- task: {TODO}",
        f"- data: {TODO}",
        f"- method: {TODO}",
        f"- key result: {TODO}",
        f"- limitations: {TODO}",
        f"- relevance to our manuscript: {TODO}",
        f"- claims it can support: {TODO}",
        f"- claims it cannot support: {TODO}",
        "",
        "## Abstract (source-provided, do not edit)",
        "",
        paper.abstract or "TODO: abstract not returned by source; confirm manually.",
        "",
    ]
    return "\n".join(lines)


def card_filename(index: int) -> str:
    return f"paper_{index:03d}.md"


def reading_matrix_row(paper: Paper) -> dict[str, str]:
    """Build one row for literature/reading_matrix.csv (interpretive cells TODO)."""
    return {
        "citation_key": make_citation_key(paper),
        "title": paper.title,
        "year": str(paper.year) if paper.year else "",
        "task": "TODO",
        "dataset": "TODO",
        "method": "TODO",
        "limitation": "TODO",
        "relevance": "TODO",
    }
