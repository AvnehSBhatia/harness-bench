CATALOG = {
    "products": {
        "PEN": {"price": "1.20", "category": "office"},
        "LAMP": {"price": "40.00", "category": "home", "tiers": [[5, "36.00"], [20, "32.00"]]},
        "MAT": {"price": "20.00", "category": "home"},
        "BOOK": {"price": "12.50", "category": "books"},
        "CABLE": {"price": "4.99", "category": "electronics", "tiers": [[10, "4.50"]]},
    },
    "bundles": [{"id": "DESK", "items": {"LAMP": 1, "MAT": 1}, "pct": "15"},
                {"id": "CABLES", "items": {"CABLE": 3}, "pct": "10"}],
}


def cart(**skus):
    return {"lines": [{"sku": s, "qty": q} for s, q in skus.items()]}


def C(code, kind, value, exclusive=False, min_spend="0", starts="2026-03-01", ends="2026-03-31", categories=None):
    c = {"code": code, "kind": kind, "value": value, "min_spend": min_spend, "starts": starts, "ends": ends,
         "exclusive": exclusive}
    if categories is not None:
        c["categories"] = categories
    return c


TEN = C("TEN", "percent", "10")
FIVER = C("FIVER", "fixed", "5")
BIG = C("BIG", "percent", "20", exclusive=True)
TODAY = "2026-03-15"
