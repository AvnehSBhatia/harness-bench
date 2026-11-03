"""Reference solution: parse_usage (SPEC.md)."""
import re
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_EVEN

MINOR = {"USD": 2, "EUR": 2, "GBP": 2, "JPY": 0, "KWD": 3}
METRICS = ("api_calls", "gb_hours", "seats")
TAX = {"DE": (Decimal("19"), Decimal("7")), "FR": (Decimal("20"), Decimal("5.5")), "GB": (Decimal("20"), Decimal("0")),
       "JP": (Decimal("10"), Decimal("8")), "US": (Decimal("0"), Decimal("0"))}
CATS = {"standard": 0, "digital": 0, "books": 1, "food": 1, "exempt": None}


def _ccy(c):
    if c not in MINOR:
        raise ValueError(f"unknown currency: {c}")
    return Decimal(1).scaleb(-MINOR[c])


def _D(x):
    if isinstance(x, float):
        raise TypeError("float not allowed")
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _round(x, c):
    return _D(x).quantize(_ccy(c), rounding=ROUND_HALF_EVEN)


_N = r"(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?"
_AMT = re.compile(rf"(?:([A-Z]{{3}}) )?(?:(-)?{_N}|\({_N}\))")


def _parse_amount(text, currency):
    q = _ccy(currency)
    m = _AMT.fullmatch(text.strip())
    if not m:
        raise ValueError(f"bad amount: {text}")
    code, minus, i1, f1, i2, f2 = m.groups()
    if code is not None and code != currency:
        raise ValueError("currency mismatch")
    neg = minus is not None or i2 is not None
    ip, fp = (i1, f1) if i2 is None else (i2, f2)
    fp = fp or ""
    if len(fp) > MINOR[currency]:
        raise ValueError("too many decimals")
    v = Decimal(ip.replace(",", "") + ("." + fp if fp else "")).quantize(q)
    return -v if neg else v


_TS = re.compile(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(Z|[+-]\d{2}:\d{2})")


def _ts(s):
    m = _TS.fullmatch(s)
    if not m:
        raise ValueError(f"bad timestamp: {s}")
    y, mo, d, h, mi, se, tz = m.groups()
    try:
        dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(se))
    except ValueError:
        raise ValueError(f"bad timestamp: {s}") from None
    off = 0
    if tz != "Z":
        hh, mm = int(tz[1:3]), int(tz[4:6])
        if hh > 23 or mm > 59:
            raise ValueError(f"bad timestamp: {s}")
        off = (hh * 60 + mm) * (1 if tz[0] == "+" else -1)
    return dt - timedelta(minutes=off)


def _parse_usage(line):
    parts = line.split("|")
    if len(parts) != 5:
        raise ValueError("bad line: expected 5 fields")
    eid, acct, metric, qty, ts = (p.strip() for p in parts)
    if not eid or not acct:
        raise ValueError("bad line: empty field")
    if metric not in METRICS:
        raise ValueError(f"unknown metric: {metric}")
    if not re.fullmatch(r"[0-9]+", qty):
        raise ValueError(f"bad quantity: {qty}")
    t = _ts(ts)
    return {"id": eid, "account": acct, "metric": metric, "quantity": int(qty), "ts": t.strftime("%Y-%m-%dT%H:%M:%SZ")}


def _in_period(ts, start, end):
    return _ts(start) <= _ts(ts) < _ts(end)


def _aggregate(lines, start, end):
    if _ts(start) >= _ts(end):
        raise ValueError("empty period")
    seen = set()
    out = {}
    for line in lines:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        ev = _parse_usage(line)
        if ev["id"] in seen:
            continue
        seen.add(ev["id"])
        if _in_period(ev["ts"], start, end):
            acc = out.setdefault(ev["account"], {})
            acc[ev["metric"]] = acc.get(ev["metric"], 0) + ev["quantity"]
    return out


def _rated(q, plan):
    if not isinstance(q, int) or isinstance(q, bool) or q < 0:
        raise ValueError("bad quantity")
    ccy = plan["currency"]
    _ccy(ccy)
    total = Decimal(0)
    lower = 0
    for t in plan["tiers"]:
        up = t["up_to"]
        hi = q if up is None else min(q, up)
        if hi > lower:
            total += (hi - lower) * _D(t["unit"])
        if up is None:
            break
        lower = up
    else:
        if q > lower:
            raise ValueError("quantity exceeds tiers")
    if q == 0:
        return _round(0, ccy)
    charge = _round(total, ccy)
    mn = plan.get("minimum")
    if mn is not None and charge < _D(mn):
        charge = _round(mn, ccy)
    return charge


def _convert(amount, src, dst, rates):
    _ccy(src)
    _ccy(dst)
    if src == dst:
        return _round(amount, dst)
    for c in (src, dst):
        if c not in rates:
            raise ValueError(f"no rate for {c}")
    return _round(_D(amount) * _D(rates[dst]) / _D(rates[src]), dst)


def _tax(net, currency, country, category):
    _ccy(currency)
    if country not in TAX:
        raise ValueError(f"unknown country: {country}")
    if category not in CATS:
        raise ValueError(f"unknown category: {category}")
    idx = CATS[category]
    rate = Decimal(0) if idx is None else TAX[country][idx]
    return _round(_D(net) * rate / 100, currency)


def _fraction(period_start, period_end, change):
    s, e, c = date.fromisoformat(period_start), date.fromisoformat(period_end), date.fromisoformat(change)
    return (e - c).days, (e - s).days


def _prorate(amount, currency, period_start, period_end, change):
    _ccy(currency)
    s, e, c = date.fromisoformat(period_start), date.fromisoformat(period_end), date.fromisoformat(change)
    if s >= e:
        raise ValueError("empty period")
    if not (s <= c < e):
        raise ValueError("change outside period")
    rem, days = _fraction(period_start, period_end, change)
    return _round(_D(amount) * rem / days, currency)


def _weekend_roll(d):
    if d.weekday() == 5:
        return d + timedelta(days=2)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def _due(issued, terms):
    d = date.fromisoformat(issued)
    m = re.fullmatch(r"NET([0-9]{1,3})", terms)
    if m and int(m.group(1)) <= 120:
        raw = d + timedelta(days=int(m.group(1)))
    elif terms == "EOM":
        nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        raw = nxt - timedelta(days=1)
    else:
        raise ValueError(f"bad terms: {terms}")
    return _weekend_roll(raw).isoformat()


def _invoice(account, usage_lines, period, rates):
    ccy = account["currency"]
    _ccy(ccy)
    plan = account["plan"]
    pc = plan["currency"]
    lines = []
    ch = account.get("change")
    if not ch:
        lines.append({"kind": "subscription", "net": _convert(_round(plan["price"], pc), pc, ccy, rates)})
    else:
        old = _round(plan["price"], pc) - _prorate(plan["price"], pc, period["start"], period["end"], ch["date"])
        new = _prorate(ch["price"], pc, period["start"], period["end"], ch["date"])
        lines.append({"kind": "subscription", "net": _convert(old, pc, ccy, rates)})
        lines.append({"kind": "subscription_change", "net": _convert(new, pc, ccy, rates)})
    ups = account.get("usage_plans") or {}
    if ups:
        agg = _aggregate(usage_lines, period["start"] + "T00:00:00Z", period["end"] + "T00:00:00Z").get(account["id"], {})
        for m in sorted(ups):
            q = agg.get(m, 0)
            if q == 0:
                continue
            up = ups[m]
            lines.append({"kind": "usage", "metric": m, "quantity": q,
                          "net": _convert(_rated(q, up), up["currency"], ccy, rates)})
    for ln in lines:
        ln["tax"] = _tax(ln["net"], ccy, account["country"], "digital")
    net = sum((ln["net"] for ln in lines), _round(0, ccy))
    tax = sum((ln["tax"] for ln in lines), _round(0, ccy))
    return {"account": account["id"], "currency": ccy, "lines": lines, "net": net, "tax": tax, "total": net + tax}


def _credits(total, currency, credits, today):
    total = _round(total, currency)
    if total < 0:
        raise ValueError("negative total")
    t = date.fromisoformat(today)
    usable = [c for c in credits if c["currency"] == currency
              and (c.get("expires") is None or date.fromisoformat(c["expires"]) >= t)]
    usable.sort(key=lambda c: (c.get("expires") is None, c.get("expires") or "", c["id"]))
    due = total
    applied = []
    remaining = {}
    for c in usable:
        bal = _parse_amount(c["amount"], currency)
        take = min(bal, due)
        if take > 0:
            applied.append({"id": c["id"], "amount": take})
            due -= take
            bal -= take
        remaining[c["id"]] = bal
    return {"applied": applied, "due": due, "remaining": remaining}


def _reconcile(invoices, payments):
    inv = sorted(invoices, key=lambda i: (i["issued"], i["id"]))
    pays = sorted(payments, key=lambda p: (p["date"], p["id"]))
    open_ = {i["id"]: _parse_amount(i["total"], i["currency"]) for i in inv}
    left = {p["id"]: _parse_amount(p["amount"], p["currency"]) for p in pays}
    allocs = []
    by_id = {i["id"].lower(): i for i in inv}
    for p in pays:
        ref = p.get("reference")
        if ref is None:
            continue
        i = by_id.get(ref.strip().lower())
        if i is None or i["currency"] != p["currency"]:
            continue
        amt = min(left[p["id"]], open_[i["id"]])
        if amt > 0:
            allocs.append({"payment": p["id"], "invoice": i["id"], "amount": amt})
            left[p["id"]] -= amt
            open_[i["id"]] -= amt
    for p in pays:
        for i in inv:
            if left[p["id"]] <= 0:
                break
            if i["currency"] != p["currency"] or open_[i["id"]] <= 0:
                continue
            amt = min(left[p["id"]], open_[i["id"]])
            allocs.append({"payment": p["id"], "invoice": i["id"], "amount": amt})
            left[p["id"]] -= amt
            open_[i["id"]] -= amt
    return {"allocations": allocs, "open": {k: v for k, v in open_.items() if v > 0},
            "unapplied": {k: v for k, v in left.items() if v > 0}}


BUCKETS = ("current", "1-30", "31-60", "61-90", "90+")


def _aging(invoices, payments, as_of):
    a = date.fromisoformat(as_of)
    inv = [i for i in invoices if date.fromisoformat(i["issued"]) <= a]
    pays = [p for p in payments if date.fromisoformat(p["date"]) <= a]
    rec = _reconcile(inv, pays)
    out = {}
    for i in inv:
        bal = rec["open"].get(i["id"])
        if bal is None:
            continue
        days = (a - date.fromisoformat(_due(i["issued"], i["terms"]))).days
        b = "current" if days <= 0 else "1-30" if days <= 30 else "31-60" if days <= 60 else "61-90" if days <= 90 else "90+"
        cur = out.setdefault(i["currency"], {k: _round(0, i["currency"]) for k in BUCKETS})
        cur[b] += bal
    return out


def parse_usage(line: str) -> dict:
    return _parse_usage(line)
