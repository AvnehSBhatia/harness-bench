from decimal import Decimal as D
import pytest
from bundle_discount import bundle_discount
from helpers_pricing import CATALOG, cart


def test_bundle_applied_twice():
    assert bundle_discount(cart(LAMP=3, MAT=2), CATALOG) == D("18.00")


def test_duplicate_lines_merged_and_rounded_per_application():
    c = {"lines": [{"sku": "CABLE", "qty": 2}, {"sku": "CABLE", "qty": 5}]}
    assert bundle_discount(c, CATALOG) == D("3.00")


def test_bundles_use_base_price_even_with_tiers():
    assert bundle_discount(cart(LAMP=6, MAT=6), CATALOG) == D("54.00")


def test_no_bundle():
    assert bundle_discount(cart(LAMP=1, PEN=4), CATALOG) == D("0")
    assert bundle_discount(cart(LAMP=1, MAT=1), {"products": CATALOG["products"]}) == D("0")


def test_unknown_sku():
    with pytest.raises(ValueError):
        bundle_discount(cart(NOPE=1), CATALOG)
