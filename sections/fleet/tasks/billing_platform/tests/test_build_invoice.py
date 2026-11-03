from decimal import Decimal as D
from build_invoice import build_invoice
from helpers_billing import ACME, APRIL, API_PLAN, RATES, raises_msg

USAGE = [
    "u1|acme|api_calls|8000|2026-04-03T10:00:00Z",
    "u2|acme|api_calls|5000|2026-04-20T10:00:00+02:00",
    "u3|acme|gb_hours|126|2026-04-05T00:00:00Z",
    "u4|other|api_calls|99999|2026-04-05T00:00:00Z",
    "u1|acme|api_calls|8000|2026-04-03T10:00:00Z",
    "u5|acme|gb_hours|40|2026-03-31T23:00:00Z",
]


def test_month_with_usage():
    inv = build_invoice(ACME, USAGE, APRIL, RATES)
    assert inv["lines"] == [
        {"kind": "subscription", "net": D("150.00"), "tax": D("28.50")},
        {"kind": "usage", "metric": "api_calls", "quantity": 13000, "net": D("11.25"), "tax": D("2.14")},
        {"kind": "usage", "metric": "gb_hours", "quantity": 126, "net": D("12.60"), "tax": D("2.39")},
    ]
    assert (inv["account"], inv["currency"]) == ("acme", "EUR")
    assert (inv["net"], inv["tax"], inv["total"]) == (D("173.85"), D("33.03"), D("206.88"))


def test_tax_summed_per_line():
    acct = {"id": "tiny", "currency": "GBP", "country": "GB", "plan": {"currency": "GBP", "price": "0.02"},
            "usage_plans": {"seats": {"currency": "GBP", "tiers": [{"up_to": None, "unit": "0.02"}]},
                            "gb_hours": {"currency": "GBP", "tiers": [{"up_to": None, "unit": "0.01"}]}}}
    usage = ["t1|tiny|seats|1|2026-04-02T00:00:00Z", "t2|tiny|gb_hours|2|2026-04-02T00:00:00Z"]
    inv = build_invoice(acct, usage, APRIL, RATES)
    assert [ln["kind"] for ln in inv["lines"]] == ["subscription", "usage", "usage"]
    assert [ln.get("metric") for ln in inv["lines"]] == [None, "gb_hours", "seats"]
    assert (inv["net"], inv["tax"], inv["total"]) == (D("0.06"), D("0"), D("0.06"))


def test_upgrade_mid_april():
    acct = dict(ACME, usage_plans={}, change={"date": "2026-04-16", "price": "460.00"})
    inv = build_invoice(acct, USAGE, APRIL, RATES)
    assert inv["lines"] == [
        {"kind": "subscription", "net": D("75.00"), "tax": D("14.25")},
        {"kind": "subscription_change", "net": D("115.00"), "tax": D("21.85")},
    ]
    assert inv["total"] == D("226.10")


def test_plan_change_in_may():
    acct = dict(ACME, plan={"currency": "USD", "price": "310.00"}, usage_plans={},
                change={"date": "2026-05-22", "price": "620.00"})
    inv = build_invoice(acct, [], {"start": "2026-05-01", "end": "2026-06-01"}, RATES)
    assert [ln["net"] for ln in inv["lines"]] == [D("105.00"), D("100.00")]
    assert (inv["net"], inv["tax"], inv["total"]) == (D("205.00"), D("38.95"), D("243.95"))


def test_month_end_usage():
    usage = ["b1|acme|gb_hours|10|2026-04-30T23:59:59Z", "b2|acme|gb_hours|1000|2026-05-01T00:00:00Z",
             "b3|acme|api_calls|50000|2026-05-01T02:00:00+02:00"]
    inv = build_invoice(ACME, usage, APRIL, RATES)
    assert inv["lines"][1:] == [{"kind": "usage", "metric": "gb_hours", "quantity": 10, "net": D("1.00"), "tax": D("0.19")}]
    assert inv["total"] == D("179.69")


def test_yen_account():
    acct = {"id": "kaito", "currency": "JPY", "country": "JP", "plan": {"currency": "USD", "price": "49.98"},
            "usage_plans": {"api_calls": API_PLAN}}
    inv = build_invoice(acct, ["j1|kaito|api_calls|2000|2026-04-10T00:00:00+09:00"], APRIL, RATES)
    assert [(ln["net"], ln["tax"]) for ln in inv["lines"]] == [(D("7497"), D("750")), (D("750"), D("75"))]
    assert (inv["net"], inv["tax"], inv["total"]) == (D("8247"), D("825"), D("9072"))


def test_lines_only_for_used_metrics():
    inv = build_invoice(ACME, ["z1|acme|api_calls|0|2026-04-02T00:00:00Z", "z2|beta|gb_hours|9|2026-04-02T00:00:00Z"],
                        APRIL, RATES)
    assert inv["lines"] == [{"kind": "subscription", "net": D("150.00"), "tax": D("28.50")}]
    plain = {k: v for k, v in ACME.items() if k != "usage_plans"}
    assert build_invoice(plain, USAGE, APRIL, RATES)["total"] == D("178.50")


def test_same_currency_plan_and_errors():
    acct = {"id": "lune", "currency": "EUR", "country": "FR", "plan": {"currency": "EUR", "price": "99.90"},
            "change": None, "usage_plans": {}}
    assert build_invoice(acct, [], APRIL, {})["total"] == D("119.88")
    raises_msg(lambda: build_invoice(dict(acct, currency="CHF"), [], APRIL, RATES), "unknown currency: CHF")
    raises_msg(lambda: build_invoice(ACME, ["broken line"], APRIL, RATES), "bad line: expected 5 fields")
