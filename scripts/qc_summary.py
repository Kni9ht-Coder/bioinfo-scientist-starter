from __future__ import annotations

import argparse
from pathlib import Path

from bioinfo_scientist.qc import load_metadata, summarize_qc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = load_metadata(args.metadata)
    qc = summarize_qc(df)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    qc.to_csv(out, index=False)


if __name__ == "__main__":
    main()
