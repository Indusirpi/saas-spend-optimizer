from backend.ingestion import load_transactions_csv, load_inventory_csv
from backend.normalization import normalize_vendor, apply_vendor_aliases
from backend.aliases import VENDOR_ALIASES
from backend.config import DetectConfig
from backend.subscription import detect_recurring_subscriptions
from backend.anomalies import detect_price_spikes
from backend.recommendations import build_recommendations

cfg = DetectConfig()

txn = load_transactions_csv("database/sample_data/transactions.csv")
txn["vendor_norm"] = (
    txn["vendor_raw"]
    .apply(normalize_vendor)
    .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
)

inventory = load_inventory_csv("database/sample_data/inventory.csv")
inventory["vendor_norm"] = (
    inventory["vendor"]
    .apply(normalize_vendor)
    .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
)

recurring = detect_recurring_subscriptions(txn, cfg)
spikes = detect_price_spikes(txn, cfg)

recommendations = build_recommendations(recurring, spikes, inventory)

print("\n=== RECOMMENDATIONS ===")
print(recommendations.head(10).to_string(index=False))

print("\nEstimated total monthly savings:",
      recommendations["est_monthly_savings"].sum())
