from decimal import Decimal as D
from late_fee import late_fee


def inv(seller, buyer, ccy, issue, terms, price="1000"):
    return {"seller": seller, "buyer": buyer, "currency": ccy, "issue_date": issue, "terms": terms,
            "lines": [{"sku": "A", "qty": 1, "unit_price": price, "category": "standard"}]}


B2B = {"country": "DE", "vat_id": "DE123"}


def test_b2b_eur_with_flat_compensation():
    assert late_fee(inv("DE", B2B, "EUR", "2026-03-02", "NET30"), "2026-04-11") == D("42.93")


def test_not_late():
    i = inv("DE", B2B, "EUR", "2026-03-02", "NET30")
    assert late_fee(i, "2026-04-01") == D("0.00")
    assert late_fee(i, "2026-03-20") == D("0")


def test_no_flat_for_consumers_or_other_currencies():
    assert late_fee(inv("DE", {"country": "DE"}, "EUR", "2026-03-02", "NET30"), "2026-04-11") == D("2.93")
    assert late_fee(inv("DE", B2B, "USD", "2026-03-02", "NET30"), "2026-04-11") == D("2.93")


def test_non_eu_seller():
    assert late_fee(inv("CH", {"country": "CH", "vat_id": "CHE1"}, "CHF", "2026-06-01", "NET30"), "2026-07-31") == D("4.44")


def test_counts_from_rolled_due_date():
    assert late_fee(inv("DE", {"country": "DE"}, "EUR", "2026-04-14", "NET30"), "2026-05-25") == D("2.93")


def test_paid_after_month_end_weekend():
    assert late_fee(inv("GB", {"country": "GB", "vat_id": "GB1"}, "GBP", "2026-08-03", "EOM"), "2026-09-11") == D("2.63")
    assert late_fee(inv("DE", B2B, "EUR", "2026-05-04", "EOM"), "2026-06-11") == D("42.93")
