---
name: manuscript-writing
description: Use for manuscript planning, claim-ledger-controlled drafting, manuscript skeletons, and manuscript sections from verified claims, results, and literature only. Trigger when asked to write project brief-to-manuscript scaffolds, Introduction/Methods/Results/Discussion text, claim ledgers, or paper drafts.
---

Evidence rules:
1. Use only docs/project_brief.md, docs/experiment_protocol.md, results/claim_ledger.yml, literature/paper_cards, literature/bib/library.bib, generated results tables/figures, and verified metrics.
2. Do not invent results, citations, DOI/PMID/accession IDs, biological mechanisms, wet-lab validation, clinical conclusions, or database contents.
3. Use conservative biomedical language.
4. Mark missing evidence as TODO: evidence needed.
5. Keep claims traceable to results/claim_ledger.yml.
6. Update docs/ai_use_log.md after substantial writing unless the user explicitly requests read-only review.

Startup chain:
1. Establish docs/project_brief.md.
2. Establish docs/experiment_protocol.md.
3. Initialize or update results/claim_ledger.yml with draft, verified, or rejected claims.
4. Create manuscript/sections/*.qmd as skeletons only when results are not available.
5. Generate code, tables, metrics, and figures before converting draft claims into verified Results text.

Allowed before experimental results exist:
1. Project brief.
2. Experiment protocol.
3. Claim ledger with draft and rejected claims.
4. Introduction skeleton without unsupported specific citations.
5. Methods plan or planned workflow wording.
6. Results placeholders with TODO lines only.
7. Discussion/Limitations skeleton that explicitly states computational-only status.

Not allowed before experimental results exist:
1. Formal Results claims.
2. Performance comparisons.
3. Dataset statistics as facts.
4. Candidate peptide efficacy claims.
5. Docking interpretations as biological proof.
6. Abstract conclusions that imply completed experiments.

Claim ledger rules:
1. Use draft for planned method or workflow claims.
2. Use verified only when supported by generated tables, figures, metrics, scripts, or verified references.
3. Use rejected for tempting but unsupported claims that must not enter the manuscript.
4. Include evidence paths, manuscript location, and caveats for every claim.

Manuscript skeleton policy:
1. Introduction may state background and study objective conservatively; add citations later through literature-audit.
2. Methods may describe planned or implemented workflow, clearly distinguishing planned from completed steps.
3. Results must remain TODO placeholders until real outputs exist.
4. Discussion may include limitations and future validation needs, but must not imply biological validation.

Preferred full writing order after evidence exists:
1. Methods.
2. Results.
3. Figure legends.
4. Discussion.
5. Introduction with verified citations.
6. Abstract.
7. Title.

For anti-biofilm antimicrobial peptide projects:
1. Describe outputs as prioritized candidates, virtual hits, or computational hypotheses.
2. Do not write that a peptide has confirmed anti-biofilm activity, cures infection, is clinically effective, or is a drug candidate without wet-lab evidence.
3. Treat docking as structural hypothesis generation, not activity proof.
4. State that future synthesis, anti-biofilm assays, hemolysis assays, cytotoxicity testing, and mechanistic validation are needed when relevant.
