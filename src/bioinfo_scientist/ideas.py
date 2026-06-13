"""Scaffold research ideas from a literature map.

IMPORTANT: This module does NOT invent ideas, results, or citations. It produces
a *structured, evidence-linked scaffold* (idea slots + scoring rubric + an
inventory of available evidence). The actual idea reasoning is performed by a
human or by Codex via the idea-generator skill, which fills the TODO slots using
only the paper cards and gap map referenced here. This keeps idea generation
auditable and prevents fabricated novelty claims (see AGENTS.md).
"""

from __future__ import annotations

IDEA_FIELDS: list[str] = [
    "title",
    "one_sentence_core_idea",
    "biological_question",
    "computational_question",
    "why_this_is_a_gap (cite paper_cards / gap_map)",
    "required_data (public sources only)",
    "minimal_viable_experiment",
    "stronger_experiment",
    "baselines",
    "metrics",
    "expected_figures",
    "novelty_risk (low|medium|high)",
    "feasibility (low|medium|high)",
    "wet_lab_dependency (none|optional|required)",
    "compute_cost (low|medium|high)",
    "potential_target_journals",
    "biggest_reason_this_might_fail",
]

SCORING_CRITERIA: list[str] = [
    "data_availability",
    "novelty",
    "feasibility_3_6_months",
    "biological_relevance",
    "computational_rigor",
    "reproducibility",
    "overclaiming_resistance",
]


def render_idea_slot(idea_index: int) -> str:
    lines = [f"### Idea I{idea_index:03d}", ""]
    for field_name in IDEA_FIELDS:
        lines.append(f"- {field_name}: TODO")
    lines.append("")
    return "\n".join(lines)


def render_scoring_table() -> str:
    header = "| idea_id | " + " | ".join(SCORING_CRITERIA) + " | total | rank |"
    sep = "|" + "---|" * (len(SCORING_CRITERIA) + 3)
    note = "Score each criterion 1-5 (evidence-based). Fill after idea slots are completed."
    return "\n".join([note, "", header, sep])


def render_idea_bank_scaffold(
    direction: str,
    n_ideas: int,
    evidence_cards: list[str],
    gap_map_present: bool,
) -> str:
    """Render literature/idea_bank.md as an evidence-linked scaffold."""
    cards_block = (
        "\n".join(f"- {name}" for name in evidence_cards)
        if evidence_cards
        else "- TODO: no paper cards found; run scripts/build_paper_cards.py first."
    )
    gap_note = (
        "literature/gap_map.md is present; ground every 'why_this_is_a_gap' in it."
        if gap_map_present
        else "TODO: literature/gap_map.md not filled; complete the gap map first."
    )
    parts = [
        "# Idea bank (draft scaffold)",
        "",
        f"Research direction: {direction}",
        "",
        "> Generated as a scaffold. Fill every TODO using ONLY the evidence below.",
        "> Do not invent citations, datasets, metrics, or biological mechanisms.",
        "> Promote approved ideas into docs/idea_bank.yml after human review.",
        "",
        "## Evidence inventory",
        "",
        "Paper cards available:",
        cards_block,
        "",
        gap_note,
        "",
        "## Candidate ideas",
        "",
        *[render_idea_slot(i + 1) for i in range(n_ideas)],
        "## Ranking",
        "",
        render_scoring_table(),
        "",
    ]
    return "\n".join(parts)


def render_top_idea_recommendation_scaffold(direction: str) -> str:
    return "\n".join(
        [
            "# Top idea recommendation (draft scaffold)",
            "",
            f"Research direction: {direction}",
            "",
            "> Fill after ranking ideas in literature/idea_bank.md. Evidence-based only.",
            "",
            "## Recommended top idea",
            "- idea_id: TODO",
            "- title: TODO",
            "- why it ranks first (cite cards / gap_map): TODO",
            "",
            "## Runner-up ideas",
            "- second: TODO",
            "- third: TODO",
            "",
            "## Next steps (require human approval)",
            "- [ ] Promote top idea into docs/idea_bank.yml",
            "- [ ] Draft docs/project_brief.md (experiment-design skill)",
            "- [ ] Draft docs/experiment_protocol.md (experiment-design skill)",
            "",
            "## Human decision",
            "- decision: pending",
            "- rationale: TODO",
            "",
        ]
    )
