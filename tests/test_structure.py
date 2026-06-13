from pathlib import Path


def test_required_files_exist() -> None:
    required = [
        "AGENTS.md",
        "Makefile",
        "envs/core.yml",
        "docs/project_brief.md",
        "results/claim_ledger.yml",
        "workflows/snakemake/Snakefile",
    ]
    for item in required:
        assert Path(item).exists(), item
