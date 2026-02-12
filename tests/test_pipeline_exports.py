import os
import pandas as pd
from backend.pipeline import export_reports

def test_export_reports_writes_files(tmp_path):
    results = {
        "summary": pd.DataFrame([{"a": 1}]),
        "recurring": pd.DataFrame([{"vendor_norm": "zoom"}]),
        "spikes": pd.DataFrame(),
        "duplicates": pd.DataFrame(),
        "recommendations": pd.DataFrame(),
    }

    outdir = tmp_path / "outputs"
    paths = export_reports(results, str(outdir))

    assert len(paths) == 5
    for p in paths:
        assert os.path.exists(p)
