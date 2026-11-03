"""line_price — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import money, product, tier_price, to_decimal  # noqa: F401


def line_price(sku: str, qty: int, catalog: dict) -> Decimal:
    """Price of one cart line (SPEC 2).

    Volume tiers: ``promo_common.tier_price`` (same pricing the storefront shows, see TEAM_NOTES.md).
    """
    raise NotImplementedError
