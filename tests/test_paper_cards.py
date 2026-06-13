"""Tests for paper card rendering and idea scaffolding. No network access."""

from __future__ import annotations

from bioinfo_scientist.ideas import (
    IDEA_FIELDS,
    render_idea_bank_scaffold,
    render_top_idea_recommendation_scaffold,
)
from bioinfo_scientist.literature import Paper
from bioinfo_scientist.paper_cards import (
    card_filename,
    make_citation_key,
    reading_matrix_row,
    render_paper_card,
)


def _paper() -> Paper:
    return Paper(
        title="A study of anti-biofilm peptides",
        source="pubmed",
        authors=["Smith J", "Doe A"],
        year=2021,
        venue="Journal of Test Biology",
        abstract="We studied peptides.",
        doi="10.1000/test.doi",
        pmid="12345678",
        url="https://pubmed.ncbi.nlm.nih.gov/12345678/",
    )


def test_make_citation_key_skips_stopwords() -> None:
    assert make_citation_key(_paper()) == "smith2021study"


def test_make_citation_key_handles_missing_fields() -> None:
    key = make_citation_key(Paper(title="", source="semantic_scholar"))
    assert key  # non-empty fallback


def test_render_paper_card_includes_verified_metadata() -> None:
    card = render_paper_card(_paper())
    assert "citation_key: smith2021study" in card
    assert "DOI/PMID/arXiv: DOI:10.1000/test.doi" in card
    assert "verified: yes" in card
    assert "TODO" in card  # interpretive fields remain TODO


def test_render_paper_card_marks_unverified() -> None:
    card = render_paper_card(Paper(title="No ids", source="semantic_scholar"))
    assert "verified: no" in card


def test_card_filename_zero_padded() -> None:
    assert card_filename(7) == "paper_007.md"


def test_reading_matrix_row_keys() -> None:
    row = reading_matrix_row(_paper())
    assert row["citation_key"] == "smith2021study"
    assert row["year"] == "2021"
    assert row["task"] == "TODO"


def test_idea_bank_scaffold_has_n_slots() -> None:
    scaffold = render_idea_bank_scaffold("anti-biofilm peptides", 3, ["paper_001.md"], True)
    assert scaffold.count("### Idea I") == 3
    assert "paper_001.md" in scaffold
    for field_name in IDEA_FIELDS:
        assert field_name in scaffold


def test_idea_bank_scaffold_warns_without_cards_or_gap() -> None:
    scaffold = render_idea_bank_scaffold("topic", 1, [], False)
    assert "no paper cards found" in scaffold
    assert "gap_map.md not filled" in scaffold


def test_top_idea_recommendation_scaffold() -> None:
    rec = render_top_idea_recommendation_scaffold("topic")
    assert "Top idea recommendation" in rec
    assert "decision: pending" in rec
