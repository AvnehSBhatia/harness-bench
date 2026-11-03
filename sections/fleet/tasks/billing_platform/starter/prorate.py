"""prorate — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import period_days, quantum, remaining_fraction, round_money, to_decimal  # noqa: F401


def prorate(amount, currency: str, period_start: str, period_end: str, change: str) -> Decimal:
    """Proration of a mid-period plan change (SPEC 9).

    Use the platform_common helpers (``remaining_fraction``, ``round_money``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
