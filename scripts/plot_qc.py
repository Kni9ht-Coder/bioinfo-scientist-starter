from __future__ import annotations

import argparse

import pandas as pd

from bioinfo_scientist.plotting import plot_qc_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    qc = pd.read_csv(args.input)
    plot_qc_summary(qc, args.out)


if __name__ == "__main__":
    main()
