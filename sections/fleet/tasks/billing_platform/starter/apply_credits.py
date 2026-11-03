"""apply_credits — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import MINOR_UNITS, quantum, round_money, to_decimal  # noqa: F401


def apply_credits(total, currency: str, credits: list, today: str) -> dict:
    """Customer credits against an invoice total (SPEC 12).

    Use the platform_common helpers (``round_money``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
