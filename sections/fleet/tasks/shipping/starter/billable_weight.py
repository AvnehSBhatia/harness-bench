"""billable_weight — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import parcel_metric, dim_weight, to_billing_step, MAX_KG  # noqa: F401


def billable_weight(parcel: dict, carrier: str) -> Decimal:
    """Billable weight in kg (SPEC 2).

    Use ``rates_common.parcel_metric``, ``dim_weight`` and ``to_billing_step`` (carrier billing step, see TEAM_NOTES.md).
    """
    raise NotImplementedError
