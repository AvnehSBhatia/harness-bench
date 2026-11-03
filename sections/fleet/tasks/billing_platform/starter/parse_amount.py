"""parse_amount — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import MINOR_UNITS, quantum, to_decimal  # noqa: F401


def parse_amount(text: str, currency: str) -> Decimal:
    """Amount text (SPEC 3).

    Use the platform_common helpers (``quantum``, ``MINOR_UNITS``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
