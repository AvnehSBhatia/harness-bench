from decimal import Decimal as D
from price_cart import price_cart
from helpers_pricing import BIG, CATALOG, FIVER, TEN, TODAY, cart

NO = {"tier": "basic", "points": 0, "redeem": False}


def test_full_order():
    r = price_cart(cart(LAMP=3, MAT=2, PEN=5), CATALOG, [TEN, FIVER], NO, TODAY)
    assert r == {"subtotal": D("166.00"), "bundle_discount": D("18.00"), "coupons": ["FIVER", "TEN"],
                 "coupon_discount": D("21.60"), "points_used": 0, "points_discount": D("0"), "total": D("126.40")}


def test_redeem_with_too_few_points():
    r = price_cart(cart(MAT=5), CATALOG, [], {"tier": "gold", "points": 99, "redeem": True}, TODAY)
    assert r["points_used"] == 0 and r["total"] == D("100.00")


def test_coupon_cap_after_bundles():
    r = price_cart(cart(LAMP=1, MAT=1), CATALOG, [C1 := {"code": "BIGFIX", "kind": "fixed", "value": "60", "starts": "2026-01-01",
                                                         "ends": "2026-12-31", "exclusive": False}], NO, TODAY)
    assert r["bundle_discount"] == D("9.00") and r["coupon_discount"] == D("51.00") and r["total"] == D("0")


def test_bulk_order():
    r = price_cart(cart(LAMP=7), CATALOG, [], NO, TODAY)
    assert r["subtotal"] == D("268.00") and r["total"] == D("268.00")


def test_points_redemption():
    r = price_cart(cart(MAT=5), CATALOG, [], {"tier": "silver", "points": 1500, "redeem": True}, TODAY)
    assert r["points_used"] == 1400 and r["points_discount"] == D("7.00") and r["total"] == D("93.00")


def test_exclusive_with_other_coupon():
    r = price_cart(cart(LAMP=3, MAT=2, PEN=5), CATALOG, [TEN, FIVER, BIG], NO, TODAY)
    assert r["coupons"] == ["BIG"] and r["coupon_discount"] == D("33.20") and r["total"] == D("114.80")
