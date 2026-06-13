"""CLI: search PubMed and Semantic Scholar for a research direction.

Example:
    python scripts/literature_search.py \
        --query "anti-biofilm antimicrobial peptide machine learning" \
        --max-results 25 \
        --out literature/raw/literature_results.json

Network is only touched here. Parsing/normalization lives in
bioinfo_scientist.literature and is unit-tested without the network.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from bioinfo_scientist.literature import (
    LiteratureSearchError,
    papers_to_payload,
    search_literature,
)


def append_query_log(log_path: Path, query: str, sources: list[str], n_results: int) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    entry = f"- {stamp} | sources={','.join(sources)} | n={n_results} | query: {query}\n"
    if not log_path.exists():
        log_path.write_text("# Literature search query log\n\n", encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> None:
    parser = argparse.ArgumentParser(description="Search PubMed and Semantic Scholar.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument(
        "--sources",
        default="pubmed,semantic_scholar",
        help="Comma-separated: pubmed,semantic_scholar",
    )
    parser.add_argument("--out", default="literature/raw/literature_results.json")
    parser.add_argument(
        "--queries-log",
        default="literature/search_queries/query_log.md",
    )
    parser.add_argument("--email", default=None, help="NCBI etiquette: contact email.")
    parser.add_argument("--api-key", default=None, help="Optional NCBI API key.")
    args = parser.parse_args()

    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    try:
        papers = search_literature(
            args.query,
            args.max_results,
            sources=sources,
            email=args.email,
            api_key=args.api_key,
        )
    except LiteratureSearchError as exc:
        raise SystemExit(f"Literature search failed: {exc}") from exc

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = papers_to_payload(args.query, papers)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    append_query_log(Path(args.queries_log), args.query, sources, len(papers))
    print(f"Saved {len(papers)} records to {out}")


if __name__ == "__main__":
    main()
