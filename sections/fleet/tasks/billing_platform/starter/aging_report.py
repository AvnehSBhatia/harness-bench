"""aging_report — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import MINOR_UNITS, payment_due, quantum, to_decimal  # noqa: F401


def aging_report(invoices: list, payments: list, as_of: str) -> dict:
    """Receivables aging (SPEC 14).

    Use the platform_common helpers (``payment_due``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
