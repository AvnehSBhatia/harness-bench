from decimal import Decimal
import pytest
from line_net import line_net


def L(qty, price, disc=None, cat="standard"):
    d = {"sku": "A", "qty": qty, "unit_price": price, "category": cat}
    if disc is not None:
        d["discount_pct"] = disc
    return d


def test_discounted_line():
    assert line_net(L(3, "19.99", "10"), "EUR") == Decimal("53.97")


def test_fractional_quantity_and_default_discount():
    assert line_net(L("2.5", "40"), "USD") == Decimal("100.00")


def test_half_away_from_zero():
    assert line_net(L(1, "0.125"), "EUR") == Decimal("0.13")
    assert line_net(L(1, "1.2345"), "KWD") == Decimal("1.235")


def test_full_discount():
    assert line_net(L(4, "9.99", "100"), "GBP") == Decimal("0.00")


@pytest.mark.parametrize("line,ccy", [
    (L(0, "1"), "EUR"), (L(1, "-1"), "EUR"), (L(1, "1", "101"), "EUR"), (L(1, "1", cat="luxury"), "EUR"),
    (L(1, "1"), "eur"), (L(1, "1"), "XYZ"),
])
def test_invalid(line, ccy):
    with pytest.raises(ValueError):
        line_net(line, ccy)


def test_yen_line():
    assert line_net(L(3, "1999", "15"), "JPY") == Decimal("5097")
    assert line_net(L(1, "1234.5"), "JPY") == Decimal("1235")
