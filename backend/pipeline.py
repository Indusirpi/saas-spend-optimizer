from __future__ import annotations

import os
from dataclasses import asdict
import pandas as pd

from backend.ingestion import load_transactions_csv, load_inventory_csv
from backend.normalization import normalize_vendor, apply_vendor_aliases
from backend.aliases import VENDOR_ALIASES
from backend.config import DetectConfig
from backend.subscription import detect_recurring_subscriptions
from backend.anomalies import detect_price_spikes, find_duplicate_vendors
from backend.recommendations import build_recommendations


def _prep_transactions(txn: pd.DataFrame) -> pd.DataFrame:
    txn = txn.copy()
    txn["vendor_norm"] = (
        txn["vendor_raw"]
        .apply(normalize_vendor)
        .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
    )
    return txn


def _prep_inventory(inv: pd.DataFrame) -> pd.DataFrame:
    inv = inv.copy()
    inv["vendor_norm"] = (
        inv["vendor"]
        .apply(normalize_vendor)
        .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
    )
    return inv


def run_pipeline(
    transactions_path: str,
    inventory_path: str | None = None,
    cfg: DetectConfig | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Runs the full spend optimizer analysis and returns a dict of DataFrames.
    """
    cfg = cfg or DetectConfig()

    txn = load_transactions_csv(transactions_path)
    txn = _prep_transactions(txn)

    inv = None
    if inventory_path:
        inv = load_inventory_csv(inventory_path)
        inv = _prep_inventory(inv)

    recurring = detect_recurring_subscriptions(txn, cfg)
    spikes = detect_price_spikes(txn, cfg)
    duplicates = find_duplicate_vendors(txn["vendor_norm"].unique().tolist(), cfg)
    recommendations = build_recommendations(recurring, spikes, inv)

    # Summary table (nice for README and export)
    summary = pd.DataFrame([{
        "monthly_run_rate_est": float(recurring["run_rate_monthly_est"].sum()) if not recurring.empty else 0.0,
        "recurring_vendors": int(len(recurring)),
        "price_spikes": int(len(spikes)),
        "duplicate_vendor_pairs": int(len(duplicates)),
        "recommendations": int(len(recommendations)),
        "estimated_monthly_savings": float(recommendations["est_monthly_savings"].sum()) if not recommendations.empty else 0.0,
        **{f"cfg_{k}": v for k, v in asdict(cfg).items()},
    }])

    return {
        "summary": summary,
        "transactions": txn,
        "inventory": inv if inv is not None else pd.DataFrame(),
        "recurring": recurring,
        "spikes": spikes,
        "duplicates": duplicates,
        "recommendations": recommendations,
    }


def export_reports(results: dict[str, pd.DataFrame], output_dir: str) -> list[str]:
    """
    Exports key outputs to CSV. Returns list of exported file paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    export_map = {
        "summary": "summary.csv",
        "recurring": "recurring_subscriptions.csv",
        "spikes": "price_spikes.csv",
        "duplicates": "duplicate_vendors.csv",
        "recommendations": "recommendations.csv",
    }

    paths = []
    for key, filename in export_map.items():
        df = results.get(key)
        if df is None or df.empty:
            # still write empty files for consistency (optional)
            out_path = os.path.join(output_dir, filename)
            pd.DataFrame().to_csv(out_path, index=False)
            paths.append(out_path)
        else:
            out_path = os.path.join(output_dir, filename)
            df.to_csv(out_path, index=False)
            paths.append(out_path)

    return paths
