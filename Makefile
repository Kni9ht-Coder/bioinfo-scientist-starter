SHELL := /bin/bash
export PYTHONPATH := src:$(PYTHONPATH)

.PHONY: lint format test smoke snakemake-dry snakemake-run figures audit paper-html paper-pdf mlflow clean

lint:
	ruff check src tests scripts
	black --check src tests scripts

format:
	ruff check src tests scripts --fix
	black src tests scripts

test:
	pytest tests -q

smoke:
	python scripts/smoke_test.py

snakemake-dry:
	snakemake -s workflows/snakemake/Snakefile -n --cores 1

snakemake-run:
	snakemake -s workflows/snakemake/Snakefile --cores 4

figures:
	python scripts/make_figures.py

audit:
	python scripts/audit_claims.py
	python scripts/audit_citations.py
	python scripts/audit_reproducibility.py

paper-html:
	quarto render manuscript/main.qmd --to html

paper-pdf:
	quarto render manuscript/main.qmd --to pdf

mlflow:
	mlflow ui --backend-store-uri results/mlflow

clean:
	rm -rf .pytest_cache .ruff_cache .quarto manuscript/_site
