"""convert — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import quantum, round_money, to_decimal  # noqa: F401


def convert(amount, src: str, dst: str, rates: dict) -> Decimal:
    """FX conversion (SPEC 7).

    Use the platform_common helpers (``round_money``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
