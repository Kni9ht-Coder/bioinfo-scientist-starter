---
name: bioinfo-pipeline
description: Use for creating or modifying Snakemake/Nextflow bioinformatics pipelines, QC steps, peptide data schemas, toy datasets, preprocessing, feature extraction, baseline models, and reproducible bioinformatics/AIDD code tasks.
---

Rules:
1. Prefer Snakemake for project-specific Python-centric workflows.
2. Prefer Nextflow/nf-core for standard RNA-seq, ATAC-seq, WGS, scRNA, metagenomics, or reusable workflows.
3. Every rule/process needs input, output, log, resources, and environment/container when possible.
4. Include dry-run support and do not overwrite raw data.
5. Record reference genome and annotation versions.
6. Keep code tasks small: one schema, loader, cleaning step, feature extractor, baseline, figure, or audit at a time.
7. Do not start advanced generation models or docking before the minimal data schema, validation, cleaning, features, baseline, and first dataset figure exist.

First code sequence for peptide/AIDD projects:
1. Define peptide data schema.
2. Add toy dataset.
3. Add validation script and tests.
4. Add data cleaning functions.
5. Add feature extraction functions.
6. Add a simple baseline model.
7. Generate the first dataset composition figure from saved data.
8. Update claim_ledger only after outputs exist.

Minimum peptide schema fields:
1. peptide_id
2. sequence
3. source
4. target_organism
5. antibiofilm_label
6. toxicity_label
7. hemolysis_label
8. reference_id

Minimum peptide validation rules:
1. sequence must not be empty.
2. sequence must contain only the standard 20 amino acids unless the protocol explicitly supports normalization.
3. antibiofilm_label must be positive, negative, or unknown.
4. unknown labels must not be silently converted to negatives.
5. duplicate and near-duplicate sequences must be considered leakage risks before modeling.

Before finishing run make snakemake-dry or equivalent.
