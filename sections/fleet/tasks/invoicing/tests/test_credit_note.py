from decimal import Decimal as D
import pytest
from credit_note import credit_note


def L(sku, qty, price, cat="standard"):
    return {"sku": sku, "qty": qty, "unit_price": price, "category": cat}


def inv(seller, buyer, lines, ccy="EUR"):
    return {"seller": seller, "buyer": buyer, "currency": ccy, "issue_date": "2026-03-02", "terms": "NET30", "lines": lines}


DE = inv("DE", {"country": "DE"}, [L("A", 2, "17.99"), L("B", 1, "10", "reduced"), L("S", 5, "0.13"), L("H", 2, "2.345")])


def test_partial_return():
    c = credit_note(DE, [{"sku": "A", "qty": 1}])
    assert c == {"currency": "EUR", "treatment": "domestic", "lines": [{"sku": "A", "qty": D("1"), "net": D("-17.99")}],
                 "subtotal": D("-17.99"), "tax_by_rate": {"19": D("-3.42")}, "tax": D("-3.42"), "total": D("-21.41")}


def test_per_rate_rule_on_credit_lines():
    c = credit_note(DE, [{"sku": "S", "qty": 1}, {"sku": "S", "qty": 1}, {"sku": "S", "qty": 1}])
    assert [l["net"] for l in c["lines"]] == [D("-0.13")] * 3
    assert c["tax"] == D("-0.07") and c["total"] == D("-0.46")


def test_negative_half_away_from_zero():
    c = credit_note(DE, [{"sku": "H", "qty": 1}, {"sku": "B", "qty": 1}])
    assert c["lines"][0]["net"] == D("-2.35")
    assert c["tax_by_rate"] == {"19": D("-0.45"), "7": D("-0.70")}


def test_keeps_invoice_treatment():
    rc = inv("DE", {"country": "FR", "vat_id": "FR1"}, [L("A", 2, "50")])
    c = credit_note(rc, [{"sku": "A", "qty": 2}])
    assert c["treatment"] == "reverse_charge" and c["tax_by_rate"] == {"0": D("0")} and c["total"] == D("-100.00")


@pytest.mark.parametrize("returns", [
    [], [{"sku": "Z", "qty": 1}], [{"sku": "A", "qty": 0}], [{"sku": "A", "qty": 3}], [{"sku": "A", "qty": 1}, {"sku": "A", "qty": 2}],
])
def test_invalid_returns(returns):
    with pytest.raises(ValueError):
        credit_note(DE, returns)


def test_dutch_credit():
    nl = inv("NL", {"country": "NL"}, [L("A", 4, "25", "reduced")])
    c = credit_note(nl, [{"sku": "A", "qty": 2}])
    assert c["tax_by_rate"] == {"9": D("-4.50")} and c["total"] == D("-54.50")
