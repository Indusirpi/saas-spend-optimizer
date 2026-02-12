import pandas as pd
from backend.anomalies import detect_price_spikes, find_duplicate_vendors
from backend.config import DetectConfig

def test_price_spike_detected():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01","2025-02-01","2025-03-01","2025-04-01"]),
        "vendor_norm": ["zoom"] * 4,
        "amount": [-20, -20, -20, -40],
    })

    out = detect_price_spikes(df, DetectConfig(price_spike_pct=0.5))
    assert len(out) == 1
    assert out.loc[0, "vendor_norm"] == "zoom"

def test_duplicate_vendor_similarity():
    cfg = DetectConfig(dup_similarity_threshold=0.85)
    vendors = ["amazon web services", "amazon web service", "zoom", "slack"]
    out = find_duplicate_vendors(vendors, cfg)
    assert len(out) >= 1
