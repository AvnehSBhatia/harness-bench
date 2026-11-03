from decimal import Decimal
import pytest
from line_tax import line_tax


def L(qty, price, cat="standard"):
    return {"sku": "A", "qty": qty, "unit_price": price, "category": cat}


def test_domestic_standard():
    assert line_tax(L(1, "100"), "DE", {"country": "DE"}, "EUR") == Decimal("19.00")


def test_distance_sale_uses_buyer_rates():
    assert line_tax(L(10, "3.10", "reduced"), "DE", {"country": "FR", "vat_id": None}, "EUR") == Decimal("1.71")
    assert line_tax(L(1, "100"), "DE", {"country": "FR", "vat_id": "   "}, "EUR") == Decimal("20.00")


def test_reverse_charge_and_export():
    assert line_tax(L(1, "100"), "DE", {"country": "FR", "vat_id": "FR40303265045"}, "EUR") == Decimal("0")
    assert line_tax(L(1, "100"), "GB", {"country": "US"}, "USD") == Decimal("0")
    assert line_tax(L(1, "100"), "DE", {"country": "CH", "vat_id": "CHE-1"}, "EUR") == Decimal("0")


def test_exempt_and_zero():
    assert line_tax(L(1, "100", "exempt"), "DE", {"country": "DE"}, "EUR") == Decimal("0")
    assert line_tax(L(1, "100", "zero"), "FR", {"country": "FR"}, "EUR") == Decimal("0")


def test_swiss_rate():
    assert line_tax(L(1, "100"), "CH", {"country": "CH"}, "CHF") == Decimal("8.10")
    assert line_tax(L(1, "100", "reduced"), "CH", {"country": "CH"}, "CHF") == Decimal("2.60")


def test_unknown_seller():
    with pytest.raises(ValueError):
        line_tax(L(1, "100"), "IT", {"country": "IT"}, "EUR")


def test_dutch_reduced_rate():
    assert line_tax(L(1, "100", "reduced"), "NL", {"country": "NL"}, "EUR") == Decimal("9.00")
    assert line_tax(L(1, "12.50", "reduced"), "NL", {"country": "NL"}, "EUR") == Decimal("1.13")
