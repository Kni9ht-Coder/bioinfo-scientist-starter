from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_qc_summary(qc_summary: pd.DataFrame, out: str | Path) -> None:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    labels = qc_summary["condition"] + " / " + qc_summary["batch"]
    ax = qc_summary.plot.bar(x=None, y="mean_mapping_rate", legend=False)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Mean mapping rate")
    ax.set_xlabel("Group")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
