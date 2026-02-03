import pandas as pd
from backend.subscription import detect_recurring_subscriptions
from backend.config import DetectConfig

def test_detect_recurring_monthly():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2025-01-01","2025-02-01","2025-03-01","2025-04-01"]),
        "vendor_norm": ["zoom"] * 4,
        "amount": [-20, -20, -20, -20],
    })

    out = detect_recurring_subscriptions(df, DetectConfig())
    assert len(out) == 1
    assert out.loc[0, "cadence"] == "monthly"
    assert out.loc[0, "confidence"] > 0.7
    assert out.loc[0, "run_rate_monthly_est"] == 20.0
