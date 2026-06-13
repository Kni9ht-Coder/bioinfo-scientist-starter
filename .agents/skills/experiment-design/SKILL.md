---
name: experiment-design
description: Use for designing bioinformatics, ML, AIDD, omics, and statistical experiments before implementation, including project briefs, experiment protocols, study boundaries, risk controls, and approval gates before code or manuscript drafting begins.
---

Startup order:
1. Write or audit docs/project_brief.md before experiment code or manuscript claims.
2. Write or audit docs/experiment_protocol.md before data processing, modeling, figures, or Results text.
3. Keep results/claim_ledger.yml aligned with the protocol; use draft claims until real evidence exists.
4. Do not proceed to formal Results writing until generated tables, figures, or metrics exist.

Project brief must define:
1. Working title and research boundary.
2. Biological question and computational question.
3. Candidate data sources without fabricating database contents.
4. Main tasks and minimum viable paper version.
5. Stronger paper version and expected figures.
6. Main risks, mitigations, and human approval gates.

Experiment protocol must define:
1. Hypothesis.
2. Data sources.
3. Inclusion/exclusion criteria.
4. Label definitions, including unknown labels that must not be treated as negatives without justification.
5. Preprocessing and feature plan.
6. Primary endpoint or metric.
7. Baselines and negative controls.
8. Split strategy; random split alone is not sufficient for the main claim when sequence similarity leakage is plausible.
9. Leakage checks.
10. Batch/confounding checks where applicable.
11. Statistical tests and multiple-testing correction.
12. Candidate generation and multi-objective filtering plan where relevant.
13. Docking or structural analysis plan where relevant; treat docking as supportive computational evidence only.
14. Expected figures/tables.
15. Failure modes and stop criteria.

For anti-biofilm antimicrobial peptide projects:
1. Treat the study as computational prioritization unless wet-lab validation exists.
2. Prefer sequence similarity cluster splits and external database splits over simple random splits.
3. Track toxicity, hemolysis, novelty, physicochemical plausibility, and Gram-negative relevance as separate objectives.
4. Use conservative wording: candidate peptides, virtual hits, computational hypotheses, or prioritization workflow.
5. Never claim confirmed activity, drug-candidate status, clinical effectiveness, or infection cure without experimental evidence.

Outputs:
1. docs/project_brief.md
2. docs/experiment_protocol.md
3. configs/experiment.yaml when implementation parameters are needed.
