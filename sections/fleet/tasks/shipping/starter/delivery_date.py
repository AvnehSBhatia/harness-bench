"""delivery_date — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import add_delivery_days, is_pickup_day, next_pickup_day  # noqa: F401


def delivery_date(shipment: dict, carrier: str, service: str) -> str:
    """Delivery date (SPEC 6).

    Use ``rates_common.next_pickup_day`` and ``rates_common.add_delivery_days`` (network calendar, see TEAM_NOTES.md).
    """
    raise NotImplementedError
