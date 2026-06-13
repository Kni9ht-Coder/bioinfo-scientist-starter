from __future__ import annotations

from pathlib import Path

import yaml

MANUSCRIPT_SECTIONS = [
    Path("manuscript/sections/introduction.qmd"),
    Path("manuscript/sections/methods.qmd"),
    Path("manuscript/sections/results.qmd"),
    Path("manuscript/sections/discussion.qmd"),
]

FORBIDDEN_PHRASES = [
    "confirmed anti-biofilm activity",
    "cures infection",
    "clinically effective",
    "clinical efficacy",
    "drug candidate",
]


def load_claims(path: Path = Path("results/claim_ledger.yml")) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    claims = data.get("claims", [])
    if not isinstance(claims, list):
        raise SystemExit("results/claim_ledger.yml must contain a claims list")
    return claims


def read_manuscript_text(paths: list[Path] = MANUSCRIPT_SECTIONS) -> str:
    chunks = []
    for path in paths:
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks).lower()


def find_overclaims(text: str, forbidden_phrases: list[str] = FORBIDDEN_PHRASES) -> list[str]:
    return [phrase for phrase in forbidden_phrases if phrase.lower() in text]


def validate_claims(claims: list[dict]) -> list[str]:
    issues = []
    seen_ids: set[str] = set()
    valid_statuses = {"draft", "verified", "rejected"}
    for claim in claims:
        claim_id = claim.get("id", "MISSING_ID")
        if claim_id in seen_ids:
            issues.append(f"Duplicate claim id: {claim_id}")
        seen_ids.add(claim_id)
        status = claim.get("status")
        if status not in valid_statuses:
            issues.append(f"{claim_id}: invalid status {status!r}")
        if status == "verified" and not claim.get("evidence"):
            issues.append(f"{claim_id}: verified claim lacks evidence")
        if status != "rejected" and not claim.get("caveat"):
            issues.append(f"{claim_id}: non-rejected claim lacks caveat")
    return issues


def write_report(claim_issues: list[str], overclaims: list[str]) -> None:
    status = "failed" if claim_issues or overclaims else "passed"
    lines = [
        "# Overclaiming audit",
        "",
        f"Status: {status}",
        "",
        "## Claim ledger issues",
    ]
    lines.extend(f"- {issue}" for issue in claim_issues) if claim_issues else lines.append("- None")
    lines.extend(["", "## Forbidden manuscript phrases"])
    lines.extend(f"- {phrase}" for phrase in overclaims) if overclaims else lines.append("- None")
    lines.extend(
        [
            "",
            "## Interpretation",
            "This deterministic audit only checks configured claim-ledger and overclaiming patterns.",
            "It does not replace human scientific review.",
        ]
    )
    Path("docs/overclaiming_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    claims = load_claims()
    claim_issues = validate_claims(claims)
    overclaims = find_overclaims(read_manuscript_text())
    write_report(claim_issues, overclaims)
    if claim_issues or overclaims:
        raise SystemExit("claim review failed; see docs/overclaiming_audit.md")
    print("claim review passed")


if __name__ == "__main__":
    main()
