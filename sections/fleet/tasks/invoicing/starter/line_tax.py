"""line_tax — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import EU_MEMBERS, has_vat_id, round_money, tax_rate, to_decimal  # noqa: F401


def line_tax(line: dict, seller: str, buyer: dict, currency: str) -> Decimal:
    """Tax of one line (SPEC 4, 5.1).

    Rates come from ``billing_common.tax_rate`` / ``TAX_RATES`` (tax team's rate service, see TEAM_NOTES.md);
    amounts are rounded with ``billing_common.round_money``.
    """
    raise NotImplementedError
