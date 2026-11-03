"""coupon_discount — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import coupon_active, merged_lines, money, product, tier_price, to_decimal  # noqa: F401


def coupon_discount(cart: dict, catalog: dict, coupon: dict, today: str) -> Decimal:
    """Discount of one coupon (SPEC 4.1-4.2).

    Line prices via ``promo_common.tier_price``; windows via ``promo_common.coupon_active``.
    """
    raise NotImplementedError
