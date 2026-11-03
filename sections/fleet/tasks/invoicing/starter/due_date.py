"""due_date — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import apply_terms, parse_iso, roll_to_business_day  # noqa: F401


def due_date(issue_date: str, terms: str, country: str) -> str:
    """Due date for payment terms in the seller's calendar (SPEC 6).

    Use ``billing_common.apply_terms`` and ``billing_common.roll_to_business_day`` so dunning and the invoice
    PDF agree (TREAS-12, see TEAM_NOTES.md).
    """
    raise NotImplementedError
