"""convert — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import round_money, to_decimal, check_currency  # noqa: F401


def convert(amount: Decimal, from_ccy: str, to_ccy: str, rates: dict) -> Decimal:
    """Convert between currencies via EUR rates (SPEC 2.3); round with ``billing_common.round_money``.
    """
    raise NotImplementedError
