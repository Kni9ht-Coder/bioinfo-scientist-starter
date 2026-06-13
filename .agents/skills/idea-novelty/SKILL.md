---
name: idea-novelty
description: Use for generating, ranking, and auditing bioinformatics or AIDD paper ideas before experiments begin, including idea-bank entries, novelty checks, feasibility scoring, and human approval gates.
---

Workflow:
1. Read or update docs/idea_bank.yml before selecting a project direction.
2. Restate the candidate idea.
3. Identify the biological problem and computational contribution.
4. Identify closest prior work and novelty risk.
5. Identify public datasets and feasibility.
6. Score novelty, feasibility, publishability, reproducibility risk.
7. Reject or reframe ideas requiring unavailable wet-lab validation.
8. Record human_decision as pending, approved, rejected, or revise.

Borrow AI-Scientist-style ideation only for planning:
1. Generate multiple candidate ideas when the user asks for exploration.
2. Use literature search to reduce novelty risk.
3. Do not execute experiments or write Results from unapproved ideas.

Output: docs/idea_novelty_report.md, update docs/idea_bank.yml, and update docs/decision_log.md.
