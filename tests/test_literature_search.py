"""Tests for literature search parsing/normalization. No network access."""

from __future__ import annotations

import pytest

from bioinfo_scientist.literature import (
    LiteratureSearchError,
    Paper,
    dedupe_papers,
    parse_pubmed_efetch_xml,
    parse_pubmed_esearch_json,
    parse_semantic_scholar_json,
    pubmed_efetch_url,
    pubmed_esearch_url,
    semantic_scholar_search_url,
)

PUBMED_XML = """<?xml version="1.0"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <Journal>
          <Title>Journal of Test Biology</Title>
          <JournalIssue><PubDate><Year>2021</Year></PubDate></JournalIssue>
        </Journal>
        <ArticleTitle>Machine learning for antimicrobial peptides</ArticleTitle>
        <Abstract>
          <AbstractText Label="BACKGROUND">Peptides matter.</AbstractText>
          <AbstractText Label="RESULTS">A model worked.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author><LastName>Smith</LastName><Initials>J</Initials></Author>
          <Author><LastName>Doe</LastName><Initials>A</Initials></Author>
        </AuthorList>
        <ELocationID EIdType="doi">10.1000/test.doi</ELocationID>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""

S2_JSON = """
{
  "data": [
    {
      "title": "Generative design of peptides",
      "abstract": "We generate peptides.",
      "year": 2023,
      "venue": "Nature Test",
      "authors": [{"name": "Jane Roe"}, {"name": "Bob Lee"}],
      "externalIds": {"DOI": "10.1000/s2.doi", "ArXiv": "2301.00001", "PubMed": 999},
      "url": "https://example.org/paper"
    }
  ]
}
"""


def test_pubmed_esearch_url_contains_query() -> None:
    url = pubmed_esearch_url("biofilm peptide", 10, email="a@b.com")
    assert "esearch.fcgi" in url
    assert "term=biofilm+peptide" in url
    assert "retmax=10" in url
    assert "email=a%40b.com" in url


def test_pubmed_efetch_and_s2_urls() -> None:
    efetch = pubmed_efetch_url(["1", "2"])
    assert "efetch.fcgi" in efetch and "id=1%2C2" in efetch
    s2 = semantic_scholar_search_url("peptide", 5)
    assert "paper/search" in s2 and "limit=5" in s2


def test_parse_pubmed_esearch_json() -> None:
    payload = '{"esearchresult": {"idlist": ["111", "222"]}}'
    assert parse_pubmed_esearch_json(payload) == ["111", "222"]


def test_parse_pubmed_efetch_xml() -> None:
    papers = parse_pubmed_efetch_xml(PUBMED_XML)
    assert len(papers) == 1
    paper = papers[0]
    assert paper.pmid == "12345678"
    assert paper.title == "Machine learning for antimicrobial peptides"
    assert paper.year == 2021
    assert paper.venue == "Journal of Test Biology"
    assert paper.doi == "10.1000/test.doi"
    assert paper.authors == ["Smith J", "Doe A"]
    assert paper.abstract is not None and "model worked" in paper.abstract
    assert paper.source == "pubmed"


def test_parse_semantic_scholar_json() -> None:
    papers = parse_semantic_scholar_json(S2_JSON)
    assert len(papers) == 1
    paper = papers[0]
    assert paper.title == "Generative design of peptides"
    assert paper.year == 2023
    assert paper.doi == "10.1000/s2.doi"
    assert paper.arxiv_id == "2301.00001"
    assert paper.pmid == "999"
    assert paper.authors == ["Jane Roe", "Bob Lee"]
    assert paper.source == "semantic_scholar"


def test_parse_invalid_xml_raises() -> None:
    with pytest.raises(LiteratureSearchError):
        parse_pubmed_efetch_xml("<not valid")


def test_dedupe_papers_by_doi_and_title() -> None:
    papers = [
        Paper(title="A", source="pubmed", doi="10.1/x"),
        Paper(title="A copy", source="semantic_scholar", doi="10.1/X"),
        Paper(title="Same Title", source="pubmed"),
        Paper(title="same title", source="semantic_scholar"),
        Paper(title="Unique", source="pubmed", pmid="42"),
    ]
    deduped = dedupe_papers(papers)
    assert len(deduped) == 3
