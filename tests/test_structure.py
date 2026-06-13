from pathlib import Path


def test_required_files_exist() -> None:
    required = [
        "AGENTS.md",
        "Makefile",
        "configs/agent_workflow.yaml",
        "envs/core.yml",
        "docs/idea_bank.yml",
        "docs/project_brief.md",
        "results/claim_ledger.yml",
        "results/run_registry.yml",
        "workflows/snakemake/Snakefile",
    ]
    for item in required:
        assert Path(item).exists(), item
