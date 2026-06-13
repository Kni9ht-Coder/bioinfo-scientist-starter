---
name: literature-scout
description: Use when the user gives a research direction and wants a current-literature map - search queries, real paper cards, a gap map, and novelty risks - before any experiment or manuscript work.
---

You turn a broad research direction into a structured, verifiable literature map.
You never invent citations, DOI, PMID, arXiv IDs, or accessions.

Tooling (real search lives in code, not in your head):
- `scripts/literature_search.py` queries PubMed (NCBI E-utilities) and Semantic Scholar,
  saving normalized records to `literature/raw/literature_results.json` and logging the
  query to `literature/search_queries/query_log.md`.
- `scripts/build_paper_cards.py` renders verified records into `literature/paper_cards/`
  and appends `literature/reading_matrix.csv`. Interpretive fields stay `TODO` until a
  paper is actually read.

Workflow:
1. Restate the research direction and any constraints (disease, target, modality, dataset, journal).
2. Design search queries for PubMed, Semantic Scholar, and arXiv/bioRxiv when relevant; save
   them under `literature/search_queries/<topic>.md`.
3. Run `scripts/literature_search.py` for the key queries (ask before hitting the network if
   the environment is offline or rate-limited).
4. Run `scripts/build_paper_cards.py` to create cards. Read the most relevant papers and fill
   the `TODO` analysis fields (task, method, key result, limitations, relevance, claims).
5. Synthesize: established knowledge, common datasets, common methods, unresolved gaps,
   reproducibility problems, and biological-validation gaps.
6. Update `literature/gap_map.md` (Known methods / Open problems / Candidate novelty angle).
7. Flag novelty risks; distinguish reviews from original research; use conservative biomedical wording.

Rules:
- If a paper cannot be verified (no DOI/PMID/arXiv), mark it `verified: no` and do not rely on it.
- Do not assert a gap unless the literature map supports it.
- Hand off to the idea-generator skill once the gap map and cards are populated.

Outputs:
- `literature/search_queries/<topic>.md`
- `literature/raw/literature_results.json`
- `literature/paper_cards/paper_*.md`, `literature/reading_matrix.csv`
- `literature/gap_map.md`
- `docs/literature_scout_report.md`
