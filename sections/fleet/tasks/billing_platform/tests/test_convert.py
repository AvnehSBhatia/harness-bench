from decimal import Decimal as D
from convert import convert
from helpers_billing import RATES, raises_msg


def test_from_base_currency():
    assert convert("100.00", "USD", "EUR", RATES) == D("50.00")
    assert convert("12.34", "USD", "EUR", RATES) == D("6.17")


def test_to_base_currency():
    assert convert("50.00", "EUR", "USD", RATES) == D("100.00")
    assert convert(D("12.35"), "EUR", "USD", RATES) == D("24.70")


def test_cross_rate():
    assert convert("10.00", "EUR", "GBP", RATES) == D("16.00")
    assert convert("7.77", "EUR", "GBP", RATES) == D("12.43")


def test_into_jpy():
    assert str(convert("12.34", "USD", "JPY", RATES)) == "1851"
    assert convert("1.01", "EUR", "JPY", RATES) == D("303")
    assert convert("0.07", "GBP", "JPY", RATES) == D("13")


def test_into_kwd():
    assert str(convert("10.00", "USD", "KWD", RATES)) == "3.000"
    assert convert("1.00", "EUR", "KWD", RATES) == D("0.600")
    assert convert("1.2345", "USD", "KWD", RATES) == D("0.370")


def test_same_currency():
    assert str(convert("10", "EUR", "EUR", {})) == "10.00"
    assert convert(7, "JPY", "JPY", {}) == D("7")
    raises_msg(lambda: convert(1.5, "USD", "EUR", RATES), "float not allowed", TypeError)


def test_errors():
    raises_msg(lambda: convert("1", "CHF", "EUR", RATES), "unknown currency: CHF")
    raises_msg(lambda: convert("1", "USD", "XXX", RATES), "unknown currency: XXX")
    raises_msg(lambda: convert("1", "CHF", "XXX", RATES), "unknown currency: CHF")
    raises_msg(lambda: convert("1", "USD", "GBP", {"USD": "1"}), "no rate for GBP")
    raises_msg(lambda: convert("1", "GBP", "EUR", {"USD": "1"}), "no rate for GBP")


def test_small_amounts():
    assert convert("10.01", "USD", "EUR", RATES) == D("5.00")
    assert convert("0.03", "USD", "JPY", RATES) == D("4")
    assert convert("0.05", "EUR", "JPY", RATES) == D("15")
