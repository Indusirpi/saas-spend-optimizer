import pandas as pd
from .config import DetectConfig
from .normalization import similarity

def detect_price_spikes(txn: pd.DataFrame, cfg: DetectConfig) -> pd.DataFrame:
    """
    Flags vendors where latest payment > (1+cfg.price_spike_pct)*historical median.
    Requires columns: date, amount, vendor_norm
    """
    rows = []
    if txn.empty:
        return pd.DataFrame()

    for vendor, g in txn.groupby("vendor_norm"):
        if not vendor or len(g) < 4:
            continue

        g = g.sort_values("date")
        amounts = g["amount"].abs().reset_index(drop=True)

        hist = amounts.iloc[:-1]
        latest = float(amounts.iloc[-1])
        med = float(hist.median())
        if med <= 0:
            continue

        if latest > (1.0 + cfg.price_spike_pct) * med:
            rows.append({
                "vendor_norm": vendor,
                "latest_date": g["date"].iloc[-1],
                "latest_amount": latest,
                "historical_median": med,
                "increase_pct": (latest / med) - 1.0,
            })

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    return out.sort_values("increase_pct", ascending=False).reset_index(drop=True)

def find_duplicate_vendors(vendors: list[str], cfg: DetectConfig, max_pairs: int = 200) -> pd.DataFrame:
    """
    Pairwise similarity over normalized vendor strings.
    Portfolio-sized approach (OK for <= a few hundred vendors).
    """
    vendors = sorted(set([v for v in vendors if v]))
    pairs = []

    for i in range(len(vendors)):
        for j in range(i + 1, len(vendors)):
            a, b = vendors[i], vendors[j]
            s = similarity(a, b)
            if s >= cfg.dup_similarity_threshold:
                pairs.append({"vendor_a": a, "vendor_b": b, "similarity": float(s)})
                if len(pairs) >= max_pairs:
                    break
        if len(pairs) >= max_pairs:
            break

    out = pd.DataFrame(pairs)
    if out.empty:
        return out

    return out.sort_values("similarity", ascending=False).reset_index(drop=True)
