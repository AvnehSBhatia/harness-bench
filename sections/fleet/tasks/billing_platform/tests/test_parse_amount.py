from decimal import Decimal as D
from parse_amount import parse_amount
from helpers_billing import raises_msg


def test_plain_and_grouped():
    assert parse_amount("1234.5", "EUR") == D("1234.50")
    assert parse_amount("1,234,567.89", "USD") == D("1234567.89")
    assert parse_amount("  42 ", "GBP") == D("42.00")
    assert str(parse_amount("12.5", "EUR")) == "12.50"


def test_negative_forms():
    assert parse_amount("-12.30", "EUR") == D("-12.30")
    assert parse_amount("(1,234)", "USD") == D("-1234.00")
    assert parse_amount("USD (0.5)", "USD") == D("-0.50")


def test_currency_code_prefix():
    assert parse_amount("EUR 10", "EUR") == D("10.00")
    assert parse_amount("KWD -1,000.5", "KWD") == D("-1000.500")
    raises_msg(lambda: parse_amount("EUR 10", "USD"), "currency mismatch")


def test_minor_units():
    assert parse_amount("KWD 1.234", "KWD") == D("1.234")
    assert str(parse_amount("1.5", "KWD")) == "1.500"
    assert parse_amount("1,500", "JPY") == D("1500")
    assert str(parse_amount("500", "JPY")) == "500"


def test_too_many_decimals():
    raises_msg(lambda: parse_amount("1.234", "EUR"), "too many decimals")
    raises_msg(lambda: parse_amount("5.0", "JPY"), "too many decimals")
    raises_msg(lambda: parse_amount("(1.2345)", "KWD"), "too many decimals")


def test_rejected_formats():
    for bad in ["12,34", "1,2345", "1234,567", ".5", "5.", "+5", "-(5)", "(-5)", "1 000", "5 EUR", "usd 5",
                "EUR  5", "EUR5", "", "1.2.3", "--5", "(5"]:
        raises_msg(lambda: parse_amount(bad, "EUR"), f"bad amount: {bad}")
    raises_msg(lambda: parse_amount(" 12,34", "EUR"), "bad amount:  12,34")


def test_check_order():
    raises_msg(lambda: parse_amount("abc", "CHF"), "unknown currency: CHF")
    raises_msg(lambda: parse_amount("EUR 1.234", "USD"), "currency mismatch")
    raises_msg(lambda: parse_amount("XYZ 5", "EUR"), "currency mismatch")
    raises_msg(lambda: parse_amount("1,23.456", "EUR"), "bad amount: 1,23.456")


def test_zero_values():
    assert parse_amount("0", "USD") == D("0")
    assert parse_amount("-0.00", "USD") == D("0")
    assert parse_amount("(0)", "JPY") == D("0")
    assert parse_amount("000,000", "EUR") == D("0")
