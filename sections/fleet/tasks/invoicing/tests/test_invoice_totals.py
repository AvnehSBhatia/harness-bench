from decimal import Decimal as D
import pytest
from invoice_totals import invoice_totals


def L(sku, qty, price, cat="standard", disc=None):
    d = {"sku": sku, "qty": qty, "unit_price": price, "category": cat}
    if disc:
        d["discount_pct"] = disc
    return d


def inv(seller, buyer, ccy, lines):
    return {"seller": seller, "buyer": buyer, "currency": ccy, "issue_date": "2026-03-02", "terms": "NET30", "lines": lines}


def test_domestic_mixed():
    t = invoice_totals(inv("DE", {"country": "DE"}, "EUR",
                           [L("A", 2, "50"), L("B", 1, "20", "reduced"), L("C", 1, "5", "exempt")]))
    assert t == {"currency": "EUR", "treatment": "domestic", "subtotal": D("125.00"),
                 "tax_by_rate": {"19": D("19.00"), "7": D("1.40")}, "tax": D("20.40"), "total": D("145.40")}


def test_per_rate_rounding():
    t = invoice_totals(inv("DE", {"country": "DE"}, "EUR", [L("A", 1, "0.13"), L("B", 1, "0.13"), L("C", 1, "0.13")]))
    assert t["tax_by_rate"] == {"19": D("0.07")} and t["tax"] == D("0.07") and t["total"] == D("0.46")


def test_reverse_charge():
    t = invoice_totals(inv("DE", {"country": "NL", "vat_id": "NL1"}, "EUR", [L("A", 1, "100"), L("B", 1, "10", "reduced")]))
    assert t["treatment"] == "reverse_charge" and t["tax_by_rate"] == {"0": D("0")} and t["total"] == D("110.00")


def test_distance_sale():
    t = invoice_totals(inv("DE", {"country": "FR"}, "EUR", [L("A", 1, "100"), L("B", 10, "3.10", "reduced")]))
    assert t["treatment"] == "distance_sale"
    assert t["tax_by_rate"] == {"20": D("20.00"), "5.5": D("1.71")} and t["total"] == D("152.71")


def test_only_exempt_and_export_kwd():
    assert invoice_totals(inv("FR", {"country": "FR"}, "EUR", [L("A", 1, "9", "exempt")]))["tax_by_rate"] == {}
    t = invoice_totals(inv("GB", {"country": "KW"}, "KWD", [L("A", 3, "1.2345"), L("B", 1, "0.0005")]))
    assert t["treatment"] == "export" and t["subtotal"] == D("3.705") and t["total"] == D("3.705")


@pytest.mark.parametrize("bad", [
    inv("DE", {"country": "DE"}, "EUR", []), inv("DE", {"country": "DE"}, "XYZ", [L("A", 1, "1")]),
    inv("IT", {"country": "IT"}, "EUR", [L("A", 1, "1")]),
])
def test_invalid(bad):
    with pytest.raises(ValueError):
        invoice_totals(bad)


def test_yen_invoice():
    t = invoice_totals(inv("JP", {"country": "JP"}, "JPY", [L("A", 3, "1999", disc="15"), L("B", 1, "333", "reduced")]))
    assert t["subtotal"] == D("5430")
    assert t["tax_by_rate"] == {"10": D("510"), "8": D("27")}
    assert t["total"] == D("5967")


def test_dutch_grocery_invoice():
    t = invoice_totals(inv("NL", {"country": "NL"}, "EUR", [L("A", 1, "50"), L("B", 8, "25", "reduced")]))
    assert t["tax_by_rate"] == {"21": D("10.50"), "9": D("18.00")} and t["total"] == D("278.50")
