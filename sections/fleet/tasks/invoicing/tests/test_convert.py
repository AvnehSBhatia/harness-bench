from decimal import Decimal as D
import pytest
from convert import convert

R = {"USD": "1.0850", "GBP": "0.8550", "CHF": "0.9400", "JPY": "162.37", "KWD": "0.3321"}


def test_from_eur():
    assert convert(D("100"), "EUR", "USD", R) == D("108.50")


def test_cross_rate():
    assert convert(D("100"), "USD", "GBP", R) == D("78.80")


def test_no_intermediate_rounding():
    assert convert(D("1"), "USD", "CHF", R) == D("0.87")


def test_same_currency_rounds():
    assert convert(D("2.345"), "EUR", "EUR", {}) == D("2.35")


def test_into_kwd():
    assert convert(D("10.005"), "EUR", "KWD", R) == D("3.323")


@pytest.mark.parametrize("args", [
    (D("1"), "EUR", "USD", {}), (D("1"), "EUR", "USD", {"USD": "0"}), (D("1"), "EUR", "XYZ", R), (D("1"), "SEK", "EUR", R),
])
def test_invalid(args):
    with pytest.raises(ValueError):
        convert(*args)


def test_into_yen():
    assert convert(D("12.34"), "EUR", "JPY", R) == D("2004")
    assert convert(D("1234.5"), "JPY", "JPY", {}) == D("1235")
