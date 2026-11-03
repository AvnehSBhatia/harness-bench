"""Reference solution: line_net (SPEC.md)."""
import re
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

MINOR = {"EUR": 2, "USD": 2, "GBP": 2, "CHF": 2, "JPY": 0, "KWD": 3}
RATES = {"DE": ("19", "7"), "FR": ("20", "5.5"), "NL": ("21", "9"), "GB": ("20", "5"), "CH": ("8.1", "2.6"), "JP": ("10", "8")}
EU = {"DE", "FR", "NL"}
CATEGORIES = {"standard", "reduced", "zero", "exempt"}
_H = {
    "DE": "01-01 04-03 04-06 05-01 05-14 05-25 10-03 12-25 12-26",
    "FR": "01-01 04-06 05-01 05-08 05-14 05-25 07-14 08-15 11-01 11-11 12-25",
    "NL": "01-01 04-03 04-06 04-27 05-14 05-25 12-25 12-26",
    "GB": "01-01 04-03 04-06 05-04 05-25 08-31 12-25 12-28",
    "CH": "01-01 01-02 04-03 04-06 05-14 05-25 08-01 12-25 12-26",
    "JP": "01-01 01-12 02-11 02-23 03-20 04-29 05-04 05-05 05-06 07-20 08-11 09-21 09-22 09-23 10-12 11-03 11-23",
}
HOL = {c: {date.fromisoformat(f"2026-{x}") for x in s.split()} for c, s in _H.items()}


def D(x):
    if isinstance(x, float):
        raise ValueError("float")
    return x if isinstance(x, Decimal) else Decimal(str(x).strip())


def ccy_ok(c):
    if c not in MINOR:
        raise ValueError(c)
    return c


def rnd(x, c):
    return D(x).quantize(Decimal(1).scaleb(-MINOR[ccy_ok(c)]), rounding=ROUND_HALF_UP)


def net_of(line, c, qty=None):
    q = D(line["qty"] if qty is None else qty)
    p = D(line["unit_price"])
    d = D(line.get("discount_pct", "0"))
    if q <= 0 or p < 0 or not (0 <= d <= 100) or line.get("category") not in CATEGORIES:
        raise ValueError("bad line")
    return rnd(q * p * (100 - d) / 100, c)


def vat(b):
    v = b.get("vat_id")
    return isinstance(v, str) and v.strip() != ""


def treatment(seller, buyer):
    if seller not in RATES:
        raise ValueError(seller)
    bc = buyer.get("country")
    if bc == seller:
        return "domestic", seller
    if seller in EU and bc in EU:
        return ("reverse_charge", None) if vat(buyer) else ("distance_sale", bc)
    return "export", None


def rate_key(line, tr):
    cat = line["category"]
    if cat == "exempt":
        return None
    kind, country = tr
    if kind in ("reverse_charge", "export") or cat == "zero":
        return "0"
    return RATES[country][0 if cat == "standard" else 1]


def per_rate(nets_keys, c):
    groups = {}
    for n, k in nets_keys:
        if k is not None:
            groups[k] = groups.get(k, Decimal(0)) + n
    return {k: rnd(s * D(k) / 100, c) for k, s in groups.items()}


def check_invoice(inv):
    ccy_ok(inv["currency"])
    if not inv.get("lines"):
        raise ValueError("no lines")
    return treatment(inv["seller"], inv["buyer"])


def totals(inv):
    c = inv["currency"]
    tr = check_invoice(inv)
    nk = [(net_of(l, c), rate_key(l, tr)) for l in inv["lines"]]
    tbr = per_rate(nk, c)
    sub = rnd(sum((n for n, _ in nk), Decimal(0)), c)
    tax = rnd(sum(tbr.values(), Decimal(0)), c)
    return {"currency": c, "treatment": tr[0], "subtotal": sub, "tax_by_rate": tbr, "tax": tax, "total": rnd(sub + tax, c)}


def eom(d):
    return (d.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)


def raw_due(issue, terms):
    if terms == "DUE":
        return issue
    if terms == "EOM":
        return eom(issue)
    m = re.fullmatch(r"(NET|EOM\+)([1-9][0-9]{0,2})", terms)
    if not m or int(m.group(2)) > 120:
        raise ValueError(terms)
    return (issue if m.group(1) == "NET" else eom(issue)) + timedelta(days=int(m.group(2)))


def business(d, country):
    return d.weekday() < 5 and d not in HOL[country]


def due(issue_iso, terms, country):
    if country not in RATES:
        raise ValueError(country)
    d = raw_due(date.fromisoformat(issue_iso), terms)
    while not business(d, country):
        d += timedelta(days=1)
    return d


def line_net(line: dict, currency: str) -> Decimal:
    return net_of(line, currency)
