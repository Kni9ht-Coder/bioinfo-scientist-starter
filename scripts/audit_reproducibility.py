from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    "Makefile",
    "envs/core.yml",
    "docs/project_brief.md",
    "docs/experiment_protocol.md",
    "results/claim_ledger.yml",
    "workflows/snakemake/Snakefile",
]


def main() -> None:
    missing = [p for p in REQUIRED if not Path(p).exists()]
    if missing:
        raise SystemExit(f"Missing required reproducibility files: {missing}")
    print("reproducibility audit placeholder passed")


if __name__ == "__main__":
    main()
