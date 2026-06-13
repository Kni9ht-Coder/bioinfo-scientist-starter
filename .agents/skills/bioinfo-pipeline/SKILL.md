---
name: bioinfo-pipeline
description: Use for creating or modifying Snakemake/Nextflow bioinformatics pipelines and QC steps.
---

Rules:
1. Prefer Snakemake for project-specific Python-centric workflows.
2. Prefer Nextflow/nf-core for standard RNA-seq, ATAC-seq, WGS, scRNA, metagenomics, or reusable workflows.
3. Every rule/process needs input, output, log, resources, and environment/container when possible.
4. Include dry-run support and do not overwrite raw data.
5. Record reference genome and annotation versions.

Before finishing run make snakemake-dry or equivalent.
