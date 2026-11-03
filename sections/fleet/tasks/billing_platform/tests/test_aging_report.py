from decimal import Decimal as D
from aging_report import aging_report
from helpers_billing import pay

AG = [
    {"id": "A1", "currency": "EUR", "total": "100.00", "issued": "2026-01-05", "terms": "NET30"},
    {"id": "A2", "currency": "EUR", "total": "200.00", "issued": "2026-03-02", "terms": "NET30"},
    {"id": "A3", "currency": "EUR", "total": "300.00", "issued": "2026-04-15", "terms": "NET14"},
    {"id": "A4", "currency": "USD", "total": "50.00", "issued": "2026-03-02", "terms": "EOM"},
    {"id": "A5", "currency": "EUR", "total": "40.00", "issued": "2026-05-04", "terms": "NET30"},
]
Z = D("0")


def B(cur, b1, b2, b3, b4):
    return {"current": D(cur), "1-30": D(b1), "31-60": D(b2), "61-90": D(b3), "90+": D(b4)}


def test_buckets():
    assert aging_report(AG, [], "2026-05-06") == {"EUR": B("40", "300", "200", "0", "100"),
                                                  "USD": B("0", "0", "50", "0", "0")}


def test_bucket_boundaries():
    inv = [AG[1]]
    expect = {"2026-03-20": "current", "2026-04-01": "current", "2026-05-01": "1-30", "2026-05-02": "31-60",
              "2026-05-31": "31-60", "2026-06-01": "61-90", "2026-06-30": "61-90", "2026-07-01": "90+"}
    for as_of, bucket in expect.items():
        r = aging_report(inv, [], as_of)["EUR"]
        assert r[bucket] == D("200.00") and sum(r.values()) == D("200.00"), as_of


def test_payments_reduce_balances():
    pays = [pay("P1", "150.00", "2026-04-10", "a2"), pay("P2", "100.00", "2026-04-12")]
    assert aging_report(AG, pays, "2026-05-06")["EUR"] == B("40", "300", "50", "0", "0")


def test_items_after_as_of_ignored():
    pays = [pay("P3", "300.00", "2026-05-05")]
    assert aging_report(AG, pays, "2026-05-03")["EUR"] == B("0", "300", "200", "100", "0")


def test_spring_statement():
    inv = [{"id": "W1", "currency": "EUR", "total": "80.00", "issued": "2026-04-02", "terms": "NET30"},
           {"id": "W2", "currency": "EUR", "total": "20.00", "issued": "2026-01-01", "terms": "NET30"}]
    assert aging_report(inv, [], "2026-05-03") == {"EUR": B("80", "0", "0", "20", "0")}


def test_paid_currency_absent():
    r = aging_report(AG, [pay("PU", "USD 50", "2026-04-01", None, "USD")], "2026-05-06")
    assert set(r) == {"EUR"}
    assert aging_report([], [], "2026-05-06") == {}


def test_every_bucket_present():
    r = aging_report([AG[4]], [], "2026-05-06")
    assert r == {"EUR": {"current": D("40.00"), "1-30": Z, "31-60": Z, "61-90": Z, "90+": Z}}
    assert all(isinstance(v, D) for v in r["EUR"].values())


def test_yen_invoices_summed():
    inv = [{"id": "J1", "currency": "JPY", "total": "1,000", "issued": "2026-04-01", "terms": "NET0"},
           {"id": "J2", "currency": "JPY", "total": "500", "issued": "2026-04-06", "terms": "NET0"}]
    r = aging_report(inv, [pay("PJ", "300", "2026-04-07", None, "JPY")], "2026-04-20")
    assert r == {"JPY": B("0", "1200", "0", "0", "0")} and str(r["JPY"]["1-30"]) == "1200"
