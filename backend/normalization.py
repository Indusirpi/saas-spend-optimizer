import re
import pandas as pd
from difflib import SequenceMatcher

LEGAL_SUFFIXES = r"\b(inc|ltd|pty|llc|corp|co|company|limited)\b"

def normalize_vendor(v: str) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    v = str(v).lower().strip()
    v = re.sub(r"[^\w\s]", " ", v)
    v = re.sub(LEGAL_SUFFIXES, " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v

def apply_vendor_aliases(vendor_norm: str, alias_map: dict) -> str:
    if not vendor_norm:
        return vendor_norm
    return alias_map.get(vendor_norm, vendor_norm)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()
