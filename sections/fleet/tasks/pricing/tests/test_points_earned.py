from points_earned import points_earned
from helpers_pricing import CATALOG, FIVER, TEN, TODAY, cart

ORDER = cart(LAMP=3, MAT=2, PEN=5)   # total 126.40 with TEN + FIVER


def test_multipliers():
    assert points_earned(ORDER, CATALOG, [TEN, FIVER], {"tier": "basic", "points": 0, "redeem": False}, TODAY) == 126
    assert points_earned(ORDER, CATALOG, [TEN, FIVER], {"tier": "silver", "points": 0, "redeem": False}, TODAY) == 158
    assert points_earned(ORDER, CATALOG, [TEN, FIVER], {"tier": "gold", "points": 0, "redeem": False}, TODAY) == 189


def test_no_coupons():
    assert points_earned(cart(BOOK=3), CATALOG, [], {"tier": "gold", "points": 0, "redeem": False}, TODAY) == 56


def test_after_redeeming_points():
    assert points_earned(cart(MAT=5), CATALOG, [], {"tier": "silver", "points": 1500, "redeem": True}, TODAY) == 116
