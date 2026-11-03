"""price_cart — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import can_combine, coupon_active, merged_lines, money, points_value, product, tier_price, to_decimal, EARN_MULTIPLIER, POINT_VALUE, REDEEM_BLOCK, TIER_CAP  # noqa: F401


def price_cart(cart: dict, catalog: dict, coupons: list, customer: dict, today: str) -> dict:
    """Full cart pricing (SPEC 6).

    Use the promo_common helpers (``tier_price``, ``can_combine``, ``points_value``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
