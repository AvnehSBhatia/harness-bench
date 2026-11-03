"""bundle_discount — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from promo_common import merged_lines, money, product, to_decimal  # noqa: F401


def bundle_discount(cart: dict, catalog: dict) -> Decimal:
    """Bundle discount of a cart (SPEC 3).
    """
    raise NotImplementedError
