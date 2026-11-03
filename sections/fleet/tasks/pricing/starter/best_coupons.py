"""best_coupons — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import can_combine, coupon_active, merged_lines, money, product, tier_price, to_decimal  # noqa: F401


def best_coupons(cart: dict, catalog: dict, coupons: list, today: str) -> list:
    """Best allowed coupon combination (SPEC 4.3-4.4).

    Stacking rules: ``promo_common.can_combine`` (promo policy PROMO-4, see TEAM_NOTES.md).
    """
    raise NotImplementedError
