"""build_invoice — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import TAX_RATES, USAGE_METRICS, in_period, parse_ts, period_days, quantum, remaining_fraction, round_money, to_decimal  # noqa: F401


def build_invoice(account: dict, usage_lines: list, period: dict, rates: dict) -> dict:
    """One invoice (SPEC 11).

    Use the platform_common helpers (``round_money``, ``remaining_fraction``, ``in_period``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
