"""CLI: turn literature_search.py output into structured paper cards.

Example:
    python scripts/build_paper_cards.py \
        --input literature/raw/literature_results.json \
        --cards-dir literature/paper_cards \
        --matrix literature/reading_matrix.csv

Only verifiable metadata is written. Interpretive fields stay as TODO markers.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from bioinfo_scientist.literature import Paper
from bioinfo_scientist.paper_cards import (
    card_filename,
    reading_matrix_row,
    render_paper_card,
)

MATRIX_COLUMNS = [
    "citation_key",
    "title",
    "year",
    "task",
    "dataset",
    "method",
    "limitation",
    "relevance",
]


def load_papers(input_path: Path) -> list[Paper]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    records = data.get("results", data) if isinstance(data, dict) else data
    return [Paper(**record) for record in records]


def next_card_index(cards_dir: Path) -> int:
    existing = sorted(cards_dir.glob("paper_*.md"))
    return len(existing) + 1


def append_matrix_rows(matrix_path: Path, papers: list[Paper]) -> None:
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not matrix_path.exists() or matrix_path.stat().st_size == 0
    with matrix_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MATRIX_COLUMNS)
        if write_header:
            writer.writeheader()
        for paper in papers:
            writer.writerow(reading_matrix_row(paper))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build paper cards from search results.")
    parser.add_argument("--input", default="literature/raw/literature_results.json")
    parser.add_argument("--cards-dir", default="literature/paper_cards")
    parser.add_argument("--matrix", default="literature/reading_matrix.csv")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    papers = load_papers(Path(args.input))
    if args.limit is not None:
        papers = papers[: args.limit]

    cards_dir = Path(args.cards_dir)
    cards_dir.mkdir(parents=True, exist_ok=True)
    start = next_card_index(cards_dir)
    for offset, paper in enumerate(papers):
        path = cards_dir / card_filename(start + offset)
        path.write_text(render_paper_card(paper), encoding="utf-8")

    append_matrix_rows(Path(args.matrix), papers)
    print(f"Wrote {len(papers)} paper cards to {cards_dir}")


if __name__ == "__main__":
    main()
