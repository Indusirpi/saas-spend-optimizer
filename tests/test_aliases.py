from backend.normalization import normalize_vendor, apply_vendor_aliases
from backend.aliases import VENDOR_ALIASES

def test_alias_mapping():
    raw = "Zoom Video Communications, Inc."
    norm = normalize_vendor(raw)
    canon = apply_vendor_aliases(norm, VENDOR_ALIASES)
    assert canon == "zoom"
