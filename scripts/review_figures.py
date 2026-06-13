from __future__ import annotations

from pathlib import Path


def list_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(
        item for item in path.iterdir() if item.is_file() and not item.name.startswith(".")
    )


def review_figure_mirroring(
    results_dir: Path = Path("results/figures"),
    manuscript_dir: Path = Path("manuscript/figures"),
) -> list[str]:
    issues = []
    result_names = {path.name for path in list_files(results_dir)}
    for figure in list_files(manuscript_dir):
        if figure.name not in result_names:
            issues.append(f"{figure} has no matching generated figure in {results_dir}")
    return issues


def write_report(issues: list[str]) -> None:
    result_figures = list_files(Path("results/figures"))
    manuscript_figures = list_files(Path("manuscript/figures"))
    status = "failed" if issues else "passed"
    lines = [
        "# Figure review",
        "",
        f"Status: {status}",
        "",
        "## Results figures",
    ]
    (
        lines.extend(f"- {path}" for path in result_figures)
        if result_figures
        else lines.append("- None")
    )
    lines.extend(["", "## Manuscript figures"])
    (
        lines.extend(f"- {path}" for path in manuscript_figures)
        if manuscript_figures
        else lines.append("- None")
    )
    lines.extend(["", "## Issues"])
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- None")
    lines.extend(
        [
            "",
            "## Reviewer note",
            "This check verifies figure mirroring only. Scientific figure quality requires human review.",
        ]
    )
    Path("docs/figure_review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    issues = review_figure_mirroring()
    write_report(issues)
    if issues:
        raise SystemExit("figure review failed; see docs/figure_review.md")
    print("figure review passed")


if __name__ == "__main__":
    main()
