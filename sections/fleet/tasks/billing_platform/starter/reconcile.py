"""reconcile — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import MINOR_UNITS, quantum, to_decimal  # noqa: F401


def reconcile(invoices: list, payments: list) -> dict:
    """Payment reconciliation (SPEC 13).

    Use the platform_common helpers (``quantum``, ``to_decimal``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
