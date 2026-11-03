"""Reference solution: line_price (SPEC.md)."""
from datetime import date
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
from itertools import combinations

CAP = {"basic": Decimal("0.20"), "silver": Decimal("0.30"), "gold": Decimal("0.50")}
MULT = {"basic": Decimal("1"), "silver": Decimal("1.25"), "gold": Decimal("1.5")}
BLOCK = 200
BLOCK_VALUE = Decimal("1.00")


def D(x):
    if isinstance(x, float):
        raise ValueError("float")
    return x if isinstance(x, Decimal) else Decimal(str(x).strip())


def money(x):
    return D(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def merged(cart):
    out = {}
    for l in cart["lines"]:
        q = l["qty"]
        if not isinstance(q, int) or isinstance(q, bool) or q < 1:
            raise ValueError("qty")
        out[l["sku"]] = out.get(l["sku"], 0) + q
    return out


def prod(catalog, sku):
    p = catalog["products"].get(sku)
    if p is None:
        raise ValueError(sku)
    return p


def price_of(sku, qty, catalog):
    if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
        raise ValueError("qty")
    p = prod(catalog, sku)
    bands = [(1, D(p["price"]))] + [(int(m), D(x)) for m, x in p.get("tiers") or []]
    total = Decimal(0)
    for i, (start, unit) in enumerate(bands):
        end = bands[i + 1][0] - 1 if i + 1 < len(bands) else qty
        n = min(end, qty) - start + 1
        if n > 0:
            total += n * unit
    return money(total)


def subtotal(cart, catalog):
    return sum((price_of(s, q, catalog) for s, q in merged(cart).items()), Decimal(0))


def bundles(cart, catalog):
    left = merged(cart)
    for s in left:
        prod(catalog, s)
    disc = Decimal(0)
    for b in catalog.get("bundles") or []:
        items = b["items"]
        while all(left.get(s, 0) >= n for s, n in items.items()):
            for s, n in items.items():
                left[s] -= n
            disc += money(sum(D(prod(catalog, s)["price"]) * n for s, n in items.items()) * D(b["pct"]) / 100)
    return disc


def one_coupon(cart, catalog, c, today):
    if c.get("kind") not in ("percent", "fixed"):
        raise ValueError("kind")
    sub = subtotal(cart, catalog)
    t = date.fromisoformat(today)
    if not (date.fromisoformat(c["starts"]) <= t <= date.fromisoformat(c["ends"])) or sub < D(c.get("min_spend", 0)):
        return Decimal("0.00")
    cats = c.get("categories")
    elig = sum((price_of(s, q, catalog) for s, q in merged(cart).items()
                if cats is None or prod(catalog, s)["category"] in cats), Decimal(0))
    if c["kind"] == "percent":
        return money(elig * D(c["value"]) / 100)
    return money(min(D(c["value"]), elig))


def combinable(a, b):
    return not a.get("exclusive") and not b.get("exclusive")


def best(cart, catalog, coupons, today):
    cap = subtotal(cart, catalog) - bundles(cart, catalog)
    uniq = {}
    for c in coupons:
        uniq.setdefault(c["code"], c)
    valid = {k: (c, one_coupon(cart, catalog, c, today)) for k, c in uniq.items()}
    valid = {k: v for k, v in valid.items() if v[1] > 0 or _is_valid(cart, catalog, v[0], today)}
    combos = [()] + [(k,) for k in valid] + [tuple(p) for p in combinations(sorted(valid), 2)
                                              if combinable(valid[p[0]][0], valid[p[1]][0])]
    def disc(cmb):
        return min(sum((valid[k][1] for k in cmb), Decimal(0)), cap)
    chosen = min(combos, key=lambda cmb: (-disc(cmb), len(cmb), sorted(cmb)))
    return sorted(chosen), disc(chosen)


def _is_valid(cart, catalog, c, today):
    t = date.fromisoformat(today)
    return date.fromisoformat(c["starts"]) <= t <= date.fromisoformat(c["ends"]) and subtotal(cart, catalog) >= D(c.get("min_spend", 0))


def redeem(amount, points, tier):
    amount = D(amount)
    if tier not in CAP or points < 0 or amount < 0:
        raise ValueError("bad redemption")
    cap = amount * CAP[tier]
    blocks = min(points // BLOCK, int((cap / BLOCK_VALUE).to_integral_value(rounding=ROUND_FLOOR)))
    return {"points_used": blocks * BLOCK, "discount": money(blocks * BLOCK_VALUE)}


def price(cart, catalog, coupons, customer, today):
    sub = subtotal(cart, catalog)
    bd = bundles(cart, catalog)
    codes, cd = best(cart, catalog, coupons, today)
    if customer.get("redeem"):
        r = redeem(sub - bd - cd, customer.get("points", 0), customer["tier"])
    else:
        r = {"points_used": 0, "discount": Decimal("0.00")}
    return {"subtotal": sub, "bundle_discount": bd, "coupons": codes, "coupon_discount": cd,
            "points_used": r["points_used"], "points_discount": r["discount"],
            "total": sub - bd - cd - r["discount"]}


def line_price(sku: str, qty: int, catalog: dict) -> Decimal:
    return price_of(sku, qty, catalog)
