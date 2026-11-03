"""line_tax — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import TAX_RATES, quantum, round_money, to_decimal  # noqa: F401


def line_tax(net, currency: str, country: str, category: str) -> Decimal:
    """Tax of one line (SPEC 8).

    Use the platform_common helpers (``round_money``, ``TAX_RATES``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
