import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

np.random.seed(42)

os.makedirs("database/sample_data", exist_ok=True)

# --- Generate Transactions ---
vendors = ["Zoom", "Slack", "AWS", "Notion", "GitHub"]
start_date = datetime(2025, 1, 1)

rows = []
for vendor in vendors:
    for month in range(12):
        date = start_date + timedelta(days=30 * month)
        amount = np.random.normal(100, 5)
        rows.append({
            "date": date.date(),
            "vendor_raw": vendor,
            "amount": -round(abs(amount), 2),
            "currency": "USD",
            "description": f"{vendor} subscription",
        })

transactions = pd.DataFrame(rows)
transactions.to_csv("database/sample_data/transactions.csv", index=False)

# --- Generate Inventory ---
inventory = pd.DataFrame({
    "product_name": vendors,
    "vendor": vendors,
    "renewal_date": [(start_date + timedelta(days=365)).date()] * len(vendors),
    "billing_cycle": ["monthly"] * len(vendors),
    "price": [100] * len(vendors),
})

inventory.to_csv("database/sample_data/inventory.csv", index=False)

print("Sample data generated successfully.")
