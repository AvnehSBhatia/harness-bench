from decimal import Decimal as D
from line_tax import line_tax
from helpers_billing import raises_msg


def test_standard_rates():
    assert line_tax("100.00", "EUR", "DE", "standard") == D("19.00")
    assert line_tax("59.99", "EUR", "FR", "digital") == D("12.00")
    assert line_tax("10.00", "GBP", "GB", "standard") == D("2.00")
    assert line_tax("100", "USD", "US", "digital") == D("0")
    assert line_tax("1000", "JPY", "JP", "standard") == D("100")


def test_reduced_rates():
    assert line_tax("20.00", "EUR", "DE", "books") == D("1.40")
    assert line_tax("10.00", "EUR", "FR", "food") == D("0.55")
    assert line_tax("15.00", "GBP", "GB", "books") == D("0")
    assert line_tax("1234", "JPY", "JP", "food") == D("99")


def test_exempt():
    assert line_tax("100.00", "EUR", "DE", "exempt") == D("0")
    assert line_tax("999", "JPY", "JP", "exempt") == D("0")


def test_negative_net():
    assert line_tax("-10.00", "EUR", "DE", "standard") == D("-1.90")
    assert line_tax(D("-3.33"), "EUR", "FR", "books") == D("-0.18")


def test_error_order():
    raises_msg(lambda: line_tax("1", "CHF", "XX", "nope"), "unknown currency: CHF")
    raises_msg(lambda: line_tax("1", "EUR", "XX", "nope"), "unknown country: XX")
    raises_msg(lambda: line_tax("1", "EUR", "DE", "luxury"), "unknown category: luxury")
    raises_msg(lambda: line_tax("1", "EUR", "de", "standard"), "unknown country: de")


def test_float_rejected():
    raises_msg(lambda: line_tax(1.0, "EUR", "DE", "standard"), "float not allowed", TypeError)


def test_three_decimal_currency():
    assert str(line_tax("12.345", "KWD", "DE", "standard")) == "2.346"
    assert str(line_tax("12.34", "EUR", "DE", "standard")) == "2.34"


def test_low_value_lines():
    assert line_tax("1.50", "EUR", "DE", "standard") == D("0.28")
    assert line_tax("3.00", "EUR", "FR", "books") == D("0.16")
    assert line_tax("125", "JPY", "JP", "standard") == D("12")
