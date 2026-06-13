"""CLI: scaffold an evidence-linked idea bank from the literature map.

Example:
    python scripts/generate_ideas.py \
        --direction "anti-biofilm antimicrobial peptide design with ML" \
        --n-ideas 10

This writes a STRUCTURED SCAFFOLD only. It never invents ideas, citations, or
results. Codex (idea-generator skill) or a human fills the TODO slots using the
paper cards and gap map referenced in the scaffold.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from bioinfo_scientist.ideas import (
    render_idea_bank_scaffold,
    render_top_idea_recommendation_scaffold,
)


def gap_map_is_filled(gap_map_path: Path) -> bool:
    if not gap_map_path.exists():
        return False
    text = gap_map_path.read_text(encoding="utf-8")
    body = "\n".join(line for line in text.splitlines() if not line.startswith("#"))
    return "TODO" not in body and body.strip() != ""


def list_paper_cards(cards_dir: Path) -> list[str]:
    if not cards_dir.exists():
        return []
    return [p.name for p in sorted(cards_dir.glob("paper_*.md"))]


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold an evidence-linked idea bank.")
    parser.add_argument("--direction", required=True)
    parser.add_argument("--n-ideas", type=int, default=10)
    parser.add_argument("--cards-dir", default="literature/paper_cards")
    parser.add_argument("--gap-map", default="literature/gap_map.md")
    parser.add_argument("--idea-bank-out", default="literature/idea_bank.md")
    parser.add_argument("--recommendation-out", default="docs/top_idea_recommendation.md")
    args = parser.parse_args()

    cards = list_paper_cards(Path(args.cards_dir))
    gap_present = gap_map_is_filled(Path(args.gap_map))

    idea_bank = render_idea_bank_scaffold(args.direction, args.n_ideas, cards, gap_present)
    recommendation = render_top_idea_recommendation_scaffold(args.direction)

    idea_path = Path(args.idea_bank_out)
    idea_path.parent.mkdir(parents=True, exist_ok=True)
    idea_path.write_text(idea_bank, encoding="utf-8")

    rec_path = Path(args.recommendation_out)
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(recommendation, encoding="utf-8")

    print(f"Scaffolded {args.n_ideas} idea slots in {idea_path} ({len(cards)} cards referenced)")


if __name__ == "__main__":
    main()
