"""quote — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import is_remote, money, parcel_metric, dim_weight, to_billing_step  # noqa: F401


def quote(shipment: dict, carrier: str, service: str) -> dict:
    """Full quote (SPEC 7.5).

    Billable weight via ``rates_common.to_billing_step``, remote areas via ``rates_common.is_remote``,
    rounding via ``rates_common.money`` (see TEAM_NOTES.md).
    """
    raise NotImplementedError
