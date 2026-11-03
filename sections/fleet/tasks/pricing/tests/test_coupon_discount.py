from decimal import Decimal as D
import pytest
from coupon_discount import coupon_discount
from helpers_pricing import CATALOG, C, TODAY, cart

CART = cart(LAMP=2, MAT=1, PEN=5)   # 80 + 20 + 6 = 106.00


def test_percent_on_categories():
    assert coupon_discount(CART, CATALOG, C("HOME10", "percent", "10", categories=["home"]), TODAY) == D("10.00")


def test_percent_rounding():
    assert coupon_discount(CART, CATALOG, C("P75", "percent", "7.5"), TODAY) == D("7.95")


def test_fixed_capped_at_eligible():
    assert coupon_discount(CART, CATALOG, C("OFF15", "fixed", "15", categories=["office"]), TODAY) == D("6.00")
    assert coupon_discount(CART, CATALOG, C("OFF15", "fixed", "15"), TODAY) == D("15.00")


def test_validity():
    assert coupon_discount(CART, CATALOG, C("MIN", "fixed", "5", min_spend="106.01"), TODAY) == D("0")
    assert coupon_discount(CART, CATALOG, C("MIN", "fixed", "5", min_spend="106.00"), TODAY) == D("5")
    assert coupon_discount(CART, CATALOG, C("OLD", "fixed", "5", ends="2026-03-14"), TODAY) == D("0")
    assert coupon_discount(CART, CATALOG, C("LAST", "fixed", "5", ends="2026-03-15"), TODAY) == D("5")


def test_bad_kind():
    with pytest.raises(ValueError):
        coupon_discount(CART, CATALOG, C("X", "bogo", "1"), TODAY)
