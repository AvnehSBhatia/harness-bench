from decimal import Decimal as D
from reconcile import reconcile
from helpers_billing import INVOICES, pay


def A(p, i, amt):
    return {"payment": p, "invoice": i, "amount": D(amt)}


def test_reference_then_fifo():
    r = reconcile(INVOICES, [pay("P1", "1,250.00", "2026-04-01", " inv-2 ")])
    assert r == {"allocations": [A("P1", "INV-2", "1200"), A("P1", "INV-1", "50")],
                 "open": {"INV-1": D("50"), "INV-3": D("50"), "INV-4": D("75")}, "unapplied": {}}


def test_fifo_same_issue_date_by_id():
    r = reconcile(INVOICES, [pay("P2", "120", "2026-04-01")])
    assert r["allocations"] == [A("P2", "INV-1", "100"), A("P2", "INV-2", "20")]
    assert r["open"] == {"INV-2": D("1180"), "INV-3": D("50"), "INV-4": D("75")}


def test_reference_pass_runs_first():
    r = reconcile(INVOICES, [pay("P1", "100.00", "2026-04-01"), pay("P2", "100.00", "2026-04-05", "INV-1")])
    assert r["allocations"] == [A("P2", "INV-1", "100"), A("P1", "INV-2", "100")]
    assert r["open"]["INV-2"] == D("1100") and "INV-1" not in r["open"]


def test_currencies_kept_apart():
    r = reconcile(INVOICES, [pay("PE", "75.00", "2026-04-01", "INV-4"),
                             pay("PU", "USD 80.00", "2026-04-02", None, "USD")])
    assert r["allocations"] == [A("PE", "INV-1", "75"), A("PU", "INV-4", "75")]
    assert r["unapplied"] == {"PU": D("5.00")} and r["open"]["INV-1"] == D("25")


def test_overpayment_left_unapplied():
    r = reconcile(INVOICES, [pay("P1", "1,400.00", "2026-04-01")])
    assert r["allocations"] == [A("P1", "INV-1", "100"), A("P1", "INV-2", "1200"), A("P1", "INV-3", "50")]
    assert r["open"] == {"INV-4": D("75")} and r["unapplied"] == {"P1": D("50")}


def test_payment_order_by_date_then_id():
    r = reconcile(INVOICES, [pay("PB", "60", "2026-04-02"), pay("PA", "60", "2026-04-02"), pay("PC", "30", "2026-04-01")])
    assert r["allocations"] == [A("PC", "INV-1", "30"), A("PA", "INV-1", "60"), A("PB", "INV-1", "10"),
                                A("PB", "INV-2", "50")]


def test_partial_and_unknown_references():
    r = reconcile(INVOICES, [pay("PX", "20.00", "2026-04-01", "INV-3"), pay("PY", "10.00", "2026-04-02", "INV-99")])
    assert r["allocations"] == [A("PX", "INV-3", "20"), A("PY", "INV-1", "10")]
    assert r["open"] == {"INV-1": D("90"), "INV-2": D("1200"), "INV-3": D("30"), "INV-4": D("75")}


def test_empty_and_yen():
    assert reconcile([], []) == {"allocations": [], "open": {}, "unapplied": {}}
    inv = [{"id": "J1", "currency": "JPY", "total": "1,000", "issued": "2026-04-01", "terms": "NET0"}]
    r = reconcile(inv, [pay("PJ", "JPY 400", "2026-04-02", None, "JPY")])
    assert r == {"allocations": [A("PJ", "J1", "400")], "open": {"J1": D("600")}, "unapplied": {}}
