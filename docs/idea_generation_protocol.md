# Idea generation protocol

End-to-end workflow that turns a research direction into ranked, reproducible
paper ideas. Every step is auditable and never fabricates citations or results
(see AGENTS.md). Human approval is required before experiments or manuscript work.

## Pipeline

1. **Research direction input** — state the topic and constraints (disease,
   target, modality, dataset, compute, wet-lab access, target journal).
2. **Search query design** (`literature-scout` skill) — write queries to
   `literature/search_queries/<topic>.md`.
3. **Literature search** —
   ```bash
   python scripts/literature_search.py \
     --query "<topic>" --max-results 25 \
     --out literature/raw/literature_results.json
   ```
   Sources: PubMed (NCBI E-utilities) and Semantic Scholar. No API key needed
   for basic use; pass `--email you@example.com` for NCBI etiquette.
4. **Paper cards** —
   ```bash
   python scripts/build_paper_cards.py \
     --input literature/raw/literature_results.json
   ```
   Verified metadata is filled automatically; read the key papers and complete
   the `TODO` analysis fields. Never invent interpretive content.
5. **Gap map** — synthesize `literature/gap_map.md` (known methods, open
   problems, candidate novelty angle) and `docs/literature_scout_report.md`.
6. **Idea scaffold** (`idea-generator` skill) —
   ```bash
   python scripts/generate_ideas.py --direction "<topic>" --n-ideas 10
   ```
   Writes `literature/idea_bank.md` (idea slots + scoring rubric) and
   `docs/top_idea_recommendation.md`. Fill every `TODO` using only the cards
   and gap map.
7. **Score and rank** — score each idea 1-5 on: data availability, novelty,
   feasibility (3-6 months), biological relevance, computational rigor,
   reproducibility, overclaiming resistance.
8. **Top ideas** — select top 3; cross-check novelty with `idea-novelty`.
9. **Promote (human approval required)** — move the chosen idea into
   `docs/idea_bank.yml`, record the decision in `docs/decision_log.md`, then use
   `experiment-design` to draft `docs/project_brief.md` and
   `docs/experiment_protocol.md`.

## Verifiability rules

- No fabricated DOI/PMID/arXiv IDs/accessions/datasets/metrics.
- A claimed gap must be supported by the literature map.
- Unverifiable papers are marked `verified: no` and not relied upon.
- Wet-lab-dependent ideas are framed as computational hypothesis generation.

## Source files

- Logic: `src/bioinfo_scientist/literature.py`, `paper_cards.py`, `ideas.py`
- CLI: `scripts/literature_search.py`, `build_paper_cards.py`, `generate_ideas.py`
- Skills: `.agents/skills/literature-scout/`, `.agents/skills/idea-generator/`
