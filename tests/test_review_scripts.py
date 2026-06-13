from pathlib import Path

from scripts.review_claims import find_overclaims, validate_claims
from scripts.review_figures import review_figure_mirroring
from scripts.review_manuscript import section_status


def test_find_overclaims_detects_forbidden_phrase() -> None:
    text = "The peptide has confirmed anti-biofilm activity."
    assert find_overclaims(text) == ["confirmed anti-biofilm activity"]


def test_validate_claims_requires_verified_evidence() -> None:
    issues = validate_claims(
        [
            {
                "id": "C001",
                "status": "verified",
                "evidence": [],
                "caveat": "missing evidence",
            }
        ]
    )
    assert issues == ["C001: verified claim lacks evidence"]


def test_section_status_detects_skeleton(tmp_path: Path) -> None:
    path = tmp_path / "section.qmd"
    path.write_text("# Results\n\nTODO\n", encoding="utf-8")
    assert section_status(path) == "skeleton"


def test_review_figure_mirroring_requires_result_source(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    manuscript_dir = tmp_path / "manuscript"
    results_dir.mkdir()
    manuscript_dir.mkdir()
    (manuscript_dir / "fig1.pdf").write_text("placeholder", encoding="utf-8")
    issues = review_figure_mirroring(results_dir, manuscript_dir)
    assert issues == [
        f"{manuscript_dir / 'fig1.pdf'} has no matching generated figure in {results_dir}"
    ]
