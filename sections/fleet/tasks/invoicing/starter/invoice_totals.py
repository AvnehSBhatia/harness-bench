"""invoice_totals — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import EU_MEMBERS, has_vat_id, round_money, tax_rate, to_decimal, check_currency  # noqa: F401


def invoice_totals(invoice: dict) -> dict:
    """Invoice subtotal / tax_by_rate / tax / total (SPEC 5.2, 8.3).

    Use ``billing_common.tax_rate`` for rates and ``billing_common.round_money`` for every rounding
    (see TEAM_NOTES.md).
    """
    raise NotImplementedError
