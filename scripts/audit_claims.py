from __future__ import annotations

from pathlib import Path

import yaml


def main() -> None:
    path = Path("results/claim_ledger.yml")
    if not path.exists():
        raise SystemExit("Missing results/claim_ledger.yml")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    claims = data.get("claims", [])
    for claim in claims:
        if claim.get("status") == "verified" and not claim.get("evidence"):
            raise SystemExit(f"Verified claim lacks evidence: {claim.get('id')}")
    print(f"claim audit passed: {len(claims)} claims checked")


if __name__ == "__main__":
    main()
