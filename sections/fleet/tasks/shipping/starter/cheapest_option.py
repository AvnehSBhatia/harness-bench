"""cheapest_option — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import add_delivery_days, is_pickup_day, is_remote, money, next_pickup_day, parcel_metric, dim_weight, to_billing_step  # noqa: F401


def cheapest_option(shipment: dict, deadline: str) -> dict | None:
    """Cheapest carrier/service that delivers by ``deadline`` (SPEC 7.7).

    Delivery dates via ``rates_common.add_delivery_days`` (network calendar), amounts via ``rates_common.money``.
    """
    raise NotImplementedError
