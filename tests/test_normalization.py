from backend.normalization import normalize_vendor

def test_normalize_vendor():
    assert normalize_vendor("Zoom, Inc.") == "zoom"
    assert normalize_vendor("ACME Ltd") == "acme"
