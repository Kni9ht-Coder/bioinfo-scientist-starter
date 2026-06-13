---
name: idea-generator
description: Use after literature scouting to generate, score, and rank reproducible bioinformatics/AIDD paper ideas from the literature map, then draft a top-idea recommendation and (after approval) a project brief and experiment protocol.
---

You generate feasible, publishable, reproducible research ideas grounded ONLY in the
literature map. You never invent results, citations, datasets, or biological mechanisms.

Inputs:
- `literature/gap_map.md`
- `literature/paper_cards/paper_*.md`
- `docs/literature_scout_report.md` if present
- `docs/project_brief.md` if present
- user constraints: time, compute, wet-lab access, target journal, direction

Tooling:
- `scripts/generate_ideas.py --direction "<topic>" --n-ideas N` writes an evidence-linked
  SCAFFOLD to `literature/idea_bank.md` and `docs/top_idea_recommendation.md`. You then fill
  every `TODO` using the cards and gap map. The script intentionally invents nothing.

Per-idea fields to complete (in `literature/idea_bank.md`):
title; one-sentence core idea; biological question; computational question;
why this is a gap (cite specific paper cards / gap_map); required data (public only);
minimal viable experiment; stronger experiment; baselines; metrics; expected figures;
novelty risk (low/med/high); feasibility (low/med/high); wet-lab dependency
(none/optional/required); compute cost (low/med/high); potential target journals;
biggest reason it might fail.

Ranking (score 1-5, evidence-based): data availability, novelty, feasibility in 3-6 months,
biological relevance, computational rigor, reproducibility, overclaiming resistance.

Rules:
- Prefer ideas validatable with public data and reproducible code.
- Frame any idea needing unavailable wet-lab work as computational hypothesis generation.
- Separate safe claims from speculative claims; cross-check novelty with the idea-novelty skill.
- Selecting top ideas, promoting them into `docs/idea_bank.yml`, and drafting briefs/protocols
  all require human approval; record decisions in `docs/decision_log.md`.

Outputs:
- `literature/idea_bank.md`
- `docs/top_idea_recommendation.md`
- after approval: update `docs/idea_bank.yml`, then hand off to experiment-design for
  `docs/project_brief.md` and `docs/experiment_protocol.md`.
