"""Reference solution: base_rate (SPEC.md)."""
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP

SERV = {("SWIFT", "express"), ("SWIFT", "standard"), ("TERRA", "ground")}
DIV = {"SWIFT": Decimal(5000), "TERRA": Decimal(6000)}
MAXKG = {"SWIFT": Decimal(30), "TERRA": Decimal(50)}
TABLE = {
    ("SWIFT", "express"): ("8.00 9.50 11.00 13.00 15.50 22.00", "1.10 1.30 1.60 1.90 2.30 3.40"),
    ("SWIFT", "standard"): ("5.50 6.20 7.10 8.30 9.60 14.00", "0.70 0.85 1.00 1.20 1.45 2.20"),
    ("TERRA", "ground"): ("4.20 4.80 5.40 6.30 7.20 12.00", "0.45 0.55 0.70 0.85 1.00 1.80"),
}
FUEL = {"SWIFT": Decimal("14.5"), "TERRA": Decimal("9.25")}
OVERSIZE = {"SWIFT": Decimal("25.00"), "TERRA": Decimal("18.00")}
REMOTE = {"SWIFT": Decimal("7.50"), "TERRA": Decimal("5.00")}
RESID = {"SWIFT": Decimal("3.20"), "TERRA": Decimal("2.10")}
REMOTE_PREFIXES = ("08", "29", "59", "64", "79", "96", "97")
HOL = {date.fromisoformat(f"2026-{x}") for x in "01-01 04-03 04-06 05-01 05-14 05-25 10-03 12-25 12-26".split()}
CUTOFF = {"SWIFT": 18 * 60, "TERRA": 16 * 60}
TRANSIT = {"express": (1, 1, 1, 1, 2, 3), "standard": (2, 2, 3, 3, 4, 5), "ground": (2, 3, 4, 5, 6, 8)}


def D(x):
    if isinstance(x, float):
        raise ValueError("float")
    return x if isinstance(x, Decimal) else Decimal(str(x).strip())


def money(x):
    return D(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def metric(p):
    l, w, h, kg = (D(p[k]) for k in ("length", "width", "height", "weight"))
    if p.get("unit") == "imperial":
        l, w, h, kg = l * Decimal("2.54"), w * Decimal("2.54"), h * Decimal("2.54"), kg * Decimal("0.45359237")
    elif p.get("unit") != "metric":
        raise ValueError("unit")
    if min(l, w, h, kg) <= 0:
        raise ValueError("dims")
    return l, w, h, kg


def step_up(kg):
    return max((kg / Decimal("0.5")).to_integral_value(rounding=ROUND_CEILING), Decimal(1)) * Decimal("0.5")


def billable(p, carrier):
    if carrier not in DIV:
        raise ValueError(carrier)
    l, w, h, kg = metric(p)
    b = step_up(max(kg, l * w * h / DIV[carrier]))
    if b > MAXKG[carrier]:
        raise ValueError("too heavy")
    return b


def pc(s):
    if not (isinstance(s, str) and len(s) == 5 and s.isdigit()):
        raise ValueError(s)
    return s


def zone_of(o, d):
    pc(o); pc(d)
    if d[:2] in ("96", "97"):
        return 6
    if o[:2] == d[:2]:
        return 1
    diff = abs(int(o[0]) - int(d[0]))
    if diff == 0:
        return 2
    return 3 if diff <= 2 else 4 if diff <= 5 else 5


def base_of(carrier, service, z, kg):
    if (carrier, service) not in SERV:
        raise ValueError("service")
    if not (isinstance(z, int) and 1 <= z <= 6):
        raise ValueError("zone")
    kg = D(kg)
    steps = kg / Decimal("0.5")
    if kg <= 0 or steps != steps.to_integral_value() or kg > MAXKG[carrier]:
        raise ValueError("weight")
    first, add = (D(x.split()[z - 1]) for x in TABLE[(carrier, service)])
    return first + (steps - 1) * add


def surch(s, carrier, service):
    if (carrier, service) not in SERV:
        raise ValueError("service")
    z = zone_of(s["origin"], s["dest"])
    base = base_of(carrier, service, z, billable(s["parcel"], carrier))
    l, w, h, _ = metric(s["parcel"])
    out = {"fuel": money(base * FUEL[carrier] / 100)}
    day = date.fromisoformat(s["ship_at"][:10])
    if date(2026, 11, 23) <= day <= date(2026, 12, 24):
        out["peak"] = money(base * 6 / 100)
    if max(l, w, h) > 120 or l + 2 * (w + h) > 300:
        out["oversize"] = OVERSIZE[carrier]
    if s["dest"][:2] in REMOTE_PREFIXES:
        out["remote"] = REMOTE[carrier]
    if s.get("residential"):
        out["residential"] = RESID[carrier]
    return out


def quote_of(s, carrier, service):
    sur = surch(s, carrier, service)
    z = zone_of(s["origin"], s["dest"])
    kg = billable(s["parcel"], carrier)
    base = base_of(carrier, service, z, kg)
    return {"carrier": carrier, "service": service, "zone": z, "billable_kg": kg, "base": base,
            "surcharges": sur, "total": base + sum(sur.values(), Decimal(0))}


def pickup_ok(d):
    return d.weekday() < 5 and d not in HOL


def delivers(d, carrier):
    return d not in HOL and (d.weekday() < 6 if carrier == "SWIFT" else d.weekday() < 5)


def deliver_on(s, carrier, service):
    if (carrier, service) not in SERV:
        raise ValueError("service")
    z = zone_of(s["origin"], s["dest"])
    t = datetime.fromisoformat(s["ship_at"])
    d = t.date()
    if not (pickup_ok(d) and t.hour * 60 + t.minute < CUTOFF[carrier]):
        d += timedelta(days=1)
        while not pickup_ok(d):
            d += timedelta(days=1)
    n = TRANSIT[service][z - 1]
    while n:
        d += timedelta(days=1)
        if delivers(d, carrier):
            n -= 1
    return d


def cheapest(s, deadline):
    best = None
    for carrier, service in sorted(SERV):
        try:
            q = quote_of(s, carrier, service)
        except ValueError as e:
            if str(e) == "too heavy":
                continue
            raise
        dd = deliver_on(s, carrier, service)
        if dd > date.fromisoformat(deadline):
            continue
        key = (q["total"], dd, carrier, service)
        if best is None or key < best[0]:
            best = (key, {"carrier": carrier, "service": service, "total": q["total"], "delivery_date": dd.isoformat()})
    return None if best is None else best[1]


def base_rate(carrier: str, service: str, zone: int, billable_kg: Decimal) -> Decimal:
    return base_of(carrier, service, zone, billable_kg)
