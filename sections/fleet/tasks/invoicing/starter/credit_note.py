"""credit_note — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import EU_MEMBERS, has_vat_id, round_money, tax_rate, to_decimal, check_currency  # noqa: F401


def credit_note(invoice: dict, returns: list) -> dict:
    """Credit note for returned quantities (SPEC 8.6).

    Same rates and rounding as invoices: ``billing_common.tax_rate`` and ``billing_common.round_money``.
    """
    raise NotImplementedError
