from backend.ingestion import load_transactions_csv
from backend.normalization import normalize_vendor, apply_vendor_aliases
from backend.aliases import VENDOR_ALIASES
from backend.config import DetectConfig
from backend.subscription import detect_recurring_subscriptions
from backend.anomalies import detect_price_spikes, find_duplicate_vendors

cfg = DetectConfig()

txn = load_transactions_csv("database/sample_data/transactions.csv")
txn["vendor_norm"] = (
    txn["vendor_raw"]
    .apply(normalize_vendor)
    .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
)

recurring = detect_recurring_subscriptions(txn, cfg)
spikes = detect_price_spikes(txn, cfg)
dups = find_duplicate_vendors(txn["vendor_norm"].unique().tolist(), cfg)

print("Recurring detected:", len(recurring))
print("Spikes detected:", len(spikes))
print("Duplicate vendor pairs:", len(dups))

print("\nTop spikes:")
print(spikes.head(10).to_string(index=False))

print("\nTop duplicates:")
print(dups.head(10).to_string(index=False))
