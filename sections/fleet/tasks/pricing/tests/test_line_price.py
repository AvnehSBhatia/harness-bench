from decimal import Decimal as D
import pytest
from line_price import line_price
from helpers_pricing import CATALOG


def test_plain_product():
    assert line_price("PEN", 3, CATALOG) == D("3.60")
    assert line_price("BOOK", 1, CATALOG) == D("12.50")


def test_below_first_tier():
    assert line_price("LAMP", 4, CATALOG) == D("160.00")
    assert line_price("CABLE", 9, CATALOG) == D("44.91")


@pytest.mark.parametrize("sku,qty", [("NOPE", 1), ("PEN", 0), ("PEN", "2"), ("PEN", -1)])
def test_invalid(sku, qty):
    with pytest.raises(ValueError):
        line_price(sku, qty, CATALOG)


def test_quantity_across_tiers():
    assert line_price("LAMP", 7, CATALOG) == D("268.00")
    assert line_price("LAMP", 22, CATALOG) == D("796.00")
    assert line_price("CABLE", 12, CATALOG) == D("58.41")
