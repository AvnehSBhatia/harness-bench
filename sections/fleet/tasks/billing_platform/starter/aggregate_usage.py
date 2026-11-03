"""aggregate_usage — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import USAGE_METRICS, format_ts, in_period, parse_ts  # noqa: F401


def aggregate_usage(lines: list, start: str, end: str) -> dict:
    """Usage totals in a billing window (SPEC 5).

    Use the platform_common helpers (``in_period``, ``parse_ts``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
