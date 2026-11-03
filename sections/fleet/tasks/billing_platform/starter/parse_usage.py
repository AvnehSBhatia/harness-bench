"""parse_usage — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import USAGE_METRICS, format_ts, parse_ts  # noqa: F401


def parse_usage(line: str) -> dict:
    """One usage event line (SPEC 4).

    Use the platform_common helpers (``parse_ts``, ``format_ts``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
