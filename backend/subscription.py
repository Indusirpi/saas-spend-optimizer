import numpy as np
import pandas as pd
from .config import DetectConfig

def detect_recurring_subscriptions(txn: pd.DataFrame, cfg: DetectConfig) -> pd.DataFrame:
    """
    Expects txn with columns: date (datetime), amount (numeric), vendor_norm (string).
    Returns vendor-level recurring subscription candidates with cadence + confidence + run-rate estimate.
    """
    rows = []
    if txn.empty:
        return pd.DataFrame()

    for vendor, g in txn.groupby("vendor_norm"):
        if not vendor:
            continue

        g = g.sort_values("date")
        if len(g) < cfg.min_occurrences:
            continue

        dates = g["date"].values
        intervals = np.diff(dates).astype("timedelta64[D]").astype(int)
        if len(intervals) == 0:
            continue

        med_int = float(np.median(intervals))

        if cfg.monthly_interval_min_days <= med_int <= cfg.monthly_interval_max_days:
            cadence = "monthly"
        elif cfg.annual_interval_min_days <= med_int <= cfg.annual_interval_max_days:
            cadence = "annual"
        else:
            cadence = "other"

        amt = g["amount"].abs().to_numpy()
        median_amt = float(np.median(amt))
        if median_amt <= 0:
            continue

        # Stability: median relative deviation from median amount
        dev = float(np.median(np.abs(amt - median_amt) / median_amt))

        # Simple confidence score (0..1)
        cadence_score = 1.0 if cadence in ("monthly", "annual") else 0.5
        stability_score = max(0.0, 1.0 - dev * 2.0)  # dev=0.1 -> 0.8
        freq_score = min(1.0, len(g) / 12.0)         # more occurrences -> more confidence
        confidence = 0.45 * cadence_score + 0.35 * stability_score + 0.20 * freq_score

        # Monthly run-rate estimate
        run_rate = np.nan
        if cadence == "monthly":
            run_rate = median_amt
        elif cadence == "annual":
            run_rate = median_amt / 12.0

        rows.append({
            "vendor_norm": vendor,
            "first_seen": g["date"].min(),
            "last_seen": g["date"].max(),
            "transactions": int(len(g)),
            "cadence": cadence,
            "median_amount": median_amt,
            "amount_dev_median": dev,
            "confidence": float(confidence),
            "run_rate_monthly_est": float(run_rate) if run_rate == run_rate else np.nan,
        })

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    return out.sort_values(["confidence", "run_rate_monthly_est"], ascending=[False, False]).reset_index(drop=True)
