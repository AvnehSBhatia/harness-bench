"""rated_usage — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import quantum, round_money, to_decimal  # noqa: F401


def rated_usage(quantity: int, plan: dict) -> Decimal:
    """Graduated usage charge (SPEC 6).

    Use the platform_common helpers (``round_money``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
