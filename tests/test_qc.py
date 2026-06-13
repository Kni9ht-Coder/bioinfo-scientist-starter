from pathlib import Path

import pandas as pd
import pytest

from bioinfo_scientist.qc import load_metadata, summarize_qc


def test_load_metadata() -> None:
    df = load_metadata("data/metadata/samples.csv")
    assert len(df) == 4
    assert "sample_id" in df.columns


def test_duplicate_sample_id_rejected(tmp_path: Path) -> None:
    path = tmp_path / "samples.csv"
    pd.DataFrame(
        {
            "sample_id": ["S1", "S1"],
            "condition": ["a", "b"],
            "batch": ["B1", "B1"],
            "qc_reads": [1, 2],
            "qc_mapping_rate": [0.9, 0.8],
        }
    ).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Duplicated sample"):
        load_metadata(path)


def test_summarize_qc() -> None:
    df = load_metadata("data/metadata/samples.csv")
    qc = summarize_qc(df)
    assert set(qc.columns) == {"condition", "batch", "n_samples", "mean_reads", "mean_mapping_rate"}
    assert qc["n_samples"].sum() == len(df)
