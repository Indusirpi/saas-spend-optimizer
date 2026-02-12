import pandas as pd

def monthly_equivalent(price: float, billing_cycle: str) -> float:
    cycle = str(billing_cycle).lower().strip()
    if cycle in ("monthly", "month"):
        return float(price)
    if cycle in ("annual", "yearly", "year"):
        return float(price) / 12.0
    return float(price)

def build_recommendations(recurring, spikes, inventory):
    """
    Generates prioritized cost-optimization recommendations.
    """

    recs = []

    # 1️⃣ Price spikes → renegotiate
    if spikes is not None and not spikes.empty:
        for _, r in spikes.iterrows():
            monthly_cost = float(r["latest_amount"])
            recs.append({
                "priority": "High",
                "type": "Renegotiate",
                "vendor": r["vendor_norm"],
                "reason": f"Latest charge is {r['increase_pct']*100:.1f}% above historical median.",
                "monthly_cost_est": monthly_cost,
                "est_monthly_savings": monthly_cost * 0.15
            })

    # 2️⃣ Orphan recurring (if inventory provided)
    if inventory is not None and not inventory.empty and recurring is not None:
        inv_vendors = set(inventory["vendor_norm"].dropna().unique())

        for _, r in recurring.iterrows():
            if r["confidence"] < 0.7:
                continue
            if r["vendor_norm"] not in inv_vendors:
                monthly_cost = r["run_rate_monthly_est"]
                if pd.notna(monthly_cost):
                    recs.append({
                        "priority": "Medium",
                        "type": "Investigate Orphan",
                        "vendor": r["vendor_norm"],
                        "reason": "Recurring subscription detected but missing in inventory.",
                        "monthly_cost_est": monthly_cost,
                        "est_monthly_savings": monthly_cost * 0.6
                    })

    out = pd.DataFrame(recs)
    if out.empty:
        return out

    priority_rank = {"High": 0, "Medium": 1, "Low": 2}
    out["priority_rank"] = out["priority"].map(priority_rank)
    out = out.sort_values(["priority_rank", "est_monthly_savings"], ascending=[True, False])
    return out.drop(columns=["priority_rank"]).reset_index(drop=True)
