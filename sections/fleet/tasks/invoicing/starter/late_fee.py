"""late_fee — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from billing_common import EU_MEMBERS, apply_terms, has_vat_id, parse_iso, roll_to_business_day, round_money, tax_rate, to_decimal  # noqa: F401


def late_fee(invoice: dict, paid_date: str) -> Decimal:
    """Late payment fee (SPEC 7).

    Due dates via ``billing_common.apply_terms`` + ``roll_to_business_day`` (TREAS-12); amounts via
    ``billing_common.round_money`` (FIN-2). See TEAM_NOTES.md.
    """
    raise NotImplementedError
