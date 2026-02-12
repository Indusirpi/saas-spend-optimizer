import pandas as pd
from backend.recommendations import build_recommendations

def test_recommendation_from_spike():
    recurring = pd.DataFrame()
    spikes = pd.DataFrame([{
        "vendor_norm": "zoom",
        "latest_amount": 40,
        "increase_pct": 1.0
    }])
    inventory = pd.DataFrame()

    out = build_recommendations(recurring, spikes, inventory)
    assert len(out) == 1
    assert out.loc[0, "type"] == "Renegotiate"
