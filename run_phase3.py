from backend.ingestion import load_transactions_csv
from backend.normalization import normalize_vendor, apply_vendor_aliases
from backend.aliases import VENDOR_ALIASES
from backend.config import DetectConfig
from backend.subscription import detect_recurring_subscriptions

txn = load_transactions_csv("database/sample_data/transactions.csv")

txn["vendor_norm"] = (
    txn["vendor_raw"]
    .apply(normalize_vendor)
    .apply(lambda v: apply_vendor_aliases(v, VENDOR_ALIASES))
)

out = detect_recurring_subscriptions(txn, DetectConfig())

print(out.head(15).to_string(index=False))
print("\nEstimated monthly run-rate (sum):", out["run_rate_monthly_est"].sum())
