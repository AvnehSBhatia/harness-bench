from decimal import Decimal as D
from apply_credits import apply_credits
from helpers_billing import raises_msg

CREDITS = [
    {"id": "C3", "currency": "EUR", "amount": "20.00", "expires": None},
    {"id": "C1", "currency": "EUR", "amount": "50.00", "expires": "2026-06-30"},
    {"id": "C2", "currency": "EUR", "amount": "1,000.00", "expires": "2026-05-31"},
    {"id": "C4", "currency": "USD", "amount": "USD 30", "expires": "2026-12-31"},
    {"id": "C0", "currency": "EUR", "amount": "15.00", "expires": "2026-04-30"},
]


def test_soonest_expiry_first():
    r = apply_credits("1060.00", "EUR", CREDITS, "2026-05-15")
    assert r["applied"] == [{"id": "C2", "amount": D("1000.00")}, {"id": "C1", "amount": D("50.00")},
                            {"id": "C3", "amount": D("10.00")}]
    assert r["due"] == D("0") and r["remaining"] == {"C2": D("0"), "C1": D("0"), "C3": D("10.00")}


def test_partial_use():
    r = apply_credits(D("30"), "EUR", CREDITS, "2026-05-15")
    assert r == {"applied": [{"id": "C2", "amount": D("30.00")}], "due": D("0"),
                 "remaining": {"C2": D("970.00"), "C1": D("50.00"), "C3": D("20.00")}}


def test_usable_on_expiry_day():
    r = apply_credits("10.00", "EUR", CREDITS, "2026-04-30")
    assert r["applied"] == [{"id": "C0", "amount": D("10.00")}]
    assert r["remaining"] == {"C0": D("5.00"), "C2": D("1000.00"), "C1": D("50.00"), "C3": D("20.00")}


def test_same_expiry_by_id():
    cr = [{"id": "B", "currency": "GBP", "amount": "5", "expires": "2026-06-01"},
          {"id": "A", "currency": "GBP", "amount": "5", "expires": "2026-06-01"}]
    r = apply_credits(7, "GBP", cr, "2026-05-01")
    assert r["applied"] == [{"id": "A", "amount": D("5.00")}, {"id": "B", "amount": D("2.00")}]
    assert r["remaining"] == {"A": D("0"), "B": D("3.00")}


def test_other_currencies_ignored():
    r = apply_credits("45.00", "USD", CREDITS, "2026-05-15")
    assert r == {"applied": [{"id": "C4", "amount": D("30.00")}], "due": D("15.00"), "remaining": {"C4": D("0")}}


def test_credits_run_out():
    r = apply_credits("2000.00", "EUR", CREDITS, "2026-05-15")
    assert r["due"] == D("930.00") and len(r["applied"]) == 3
    assert r["remaining"] == {"C2": D("0"), "C1": D("0"), "C3": D("0")}


def test_zero_total_and_errors():
    r = apply_credits("0", "EUR", CREDITS, "2026-07-01")
    assert r == {"applied": [], "due": D("0"), "remaining": {"C3": D("20.00")}}
    raises_msg(lambda: apply_credits("-5.00", "EUR", CREDITS, "2026-05-15"), "negative total")
    raises_msg(lambda: apply_credits(1.5, "EUR", CREDITS, "2026-05-15"), "float not allowed", TypeError)
    raises_msg(lambda: apply_credits("5", "CHF", CREDITS, "2026-05-15"), "unknown currency: CHF")


def test_amount_text_and_rounding():
    cr = [{"id": "Y1", "currency": "JPY", "amount": "JPY 1,500", "expires": None}]
    r = apply_credits("2000", "JPY", cr, "2026-05-15")
    assert str(r["due"]) == "500" and r["remaining"] == {"Y1": D("0")}
    r = apply_credits("12.506", "EUR", [{"id": "E", "currency": "EUR", "amount": "EUR 12.5", "expires": None}], "2026-05-15")
    assert r["due"] == D("0.01") and r["applied"] == [{"id": "E", "amount": D("12.50")}]
    bad = [{"id": "E", "currency": "EUR", "amount": "12.345", "expires": None}]
    raises_msg(lambda: apply_credits("1", "EUR", bad, "2026-05-15"), "too many decimals")
