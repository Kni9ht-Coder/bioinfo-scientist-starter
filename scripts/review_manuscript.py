from __future__ import annotations

from pathlib import Path

SECTIONS = {
    "Introduction": Path("manuscript/sections/introduction.qmd"),
    "Methods": Path("manuscript/sections/methods.qmd"),
    "Results": Path("manuscript/sections/results.qmd"),
    "Discussion": Path("manuscript/sections/discussion.qmd"),
}


def section_status(path: Path) -> str:
    if not path.exists():
        return "missing"
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return "empty"
    if "TODO" in text:
        return "skeleton"
    return "drafted"


def write_report(statuses: dict[str, str]) -> None:
    lines = [
        "# Internal manuscript review",
        "",
        "## Section status",
    ]
    lines.extend(f"- {name}: {status}" for name, status in statuses.items())
    lines.extend(
        [
            "",
            "## Required gates",
            "- Results claims require verified entries in results/claim_ledger.yml.",
            "- Citations require verified paper cards and BibTeX entries.",
            "- Figures must be generated from data or results by code.",
            "",
            "## Reviewer note",
            "This is a structural review, not a scientific acceptance decision.",
        ]
    )
    Path("docs/internal_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    statuses = {name: section_status(path) for name, path in SECTIONS.items()}
    write_report(statuses)
    missing = [name for name, status in statuses.items() if status == "missing"]
    if missing:
        raise SystemExit(f"missing manuscript sections: {missing}")
    print("manuscript review passed")


if __name__ == "__main__":
    main()
