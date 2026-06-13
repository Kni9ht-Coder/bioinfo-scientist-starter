from __future__ import annotations

from pathlib import Path

from bioinfo_scientist.qc import load_metadata, summarize_qc


def main() -> None:
    df = load_metadata("data/metadata/samples.csv")
    qc = summarize_qc(df)
    assert not qc.empty
    Path("results/metrics").mkdir(parents=True, exist_ok=True)
    Path("results/metrics/smoke.txt").write_text("smoke test passed\n", encoding="utf-8")
    print("smoke test passed")


if __name__ == "__main__":
    main()
