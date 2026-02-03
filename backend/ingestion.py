import pandas as pd

REQUIRED_TXN_COLS = ["date", "vendor_raw", "amount"]
REQUIRED_INV_COLS = ["product_name", "vendor", "renewal_date", "billing_cycle", "price"]

class DataValidationError(ValueError):
    pass

def _validate_cols(df, required, name):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise DataValidationError(f"{name} missing required columns: {missing}")

def load_transactions_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    _validate_cols(df, REQUIRED_TXN_COLS, "transactions")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[df["date"].notna()].copy()

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"].notna()].copy()

    df["vendor_raw"] = df["vendor_raw"].astype(str)
    return df.reset_index(drop=True)

def load_inventory_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    _validate_cols(df, REQUIRED_INV_COLS, "inventory")

    df["renewal_date"] = pd.to_datetime(df["renewal_date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.reset_index(drop=True)
