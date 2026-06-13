from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_METADATA_COLUMNS = {
    "sample_id",
    "condition",
    "batch",
    "qc_reads",
    "qc_mapping_rate",
}


def load_metadata(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_METADATA_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing metadata columns: {sorted(missing)}")
    if df["sample_id"].duplicated().any():
        duplicated = df.loc[df["sample_id"].duplicated(), "sample_id"].tolist()
        raise ValueError(f"Duplicated sample IDs: {duplicated}")
    return df


def summarize_qc(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["condition", "batch"], as_index=False)
        .agg(
            n_samples=("sample_id", "count"),
            mean_reads=("qc_reads", "mean"),
            mean_mapping_rate=("qc_mapping_rate", "mean"),
        )
        .sort_values(["condition", "batch"])
    )
