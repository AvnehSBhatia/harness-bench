"""due_date — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from platform_common import payment_due  # noqa: F401


def due_date(issued: str, terms: str) -> str:
    """Due date under payment terms (SPEC 10).

    Use the platform_common helpers (``payment_due``), see TEAM_NOTES.md.
    """
    raise NotImplementedError
