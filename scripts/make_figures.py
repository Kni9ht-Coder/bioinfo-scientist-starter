from __future__ import annotations

from pathlib import Path

import pandas as pd

from bioinfo_scientist.plotting import plot_qc_summary
from bioinfo_scientist.qc import load_metadata, summarize_qc


def main() -> None:
    metadata = Path("data/metadata/samples.csv")
    table_out = Path("results/tables/qc_summary.csv")
    fig_out = Path("results/figures/fig1_qc.pdf")
    manuscript_fig_out = Path("manuscript/figures/fig1_qc.pdf")

    df = load_metadata(metadata)
    qc = summarize_qc(df)
    table_out.parent.mkdir(parents=True, exist_ok=True)
    qc.to_csv(table_out, index=False)
    plot_qc_summary(qc, fig_out)
    manuscript_fig_out.parent.mkdir(parents=True, exist_ok=True)
    manuscript_fig_out.write_bytes(fig_out.read_bytes())


if __name__ == "__main__":
    main()
