"""loyalty_redemption — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import money, points_value, to_decimal, POINT_VALUE, REDEEM_BLOCK, TIER_CAP  # noqa: F401


def loyalty_redemption(amount: Decimal, points: int, tier: str) -> dict:
    """Redeem loyalty points on an amount (SPEC 5.1).

    Point values: ``promo_common.REDEEM_BLOCK`` / ``points_value`` (loyalty team, see TEAM_NOTES.md).
    """
    raise NotImplementedError
