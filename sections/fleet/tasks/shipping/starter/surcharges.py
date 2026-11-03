"""surcharges — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import is_remote, money, parcel_metric, dim_weight, to_billing_step  # noqa: F401


def surcharges(shipment: dict, carrier: str, service: str) -> dict:
    """Applicable surcharges (SPEC 5).

    Remote areas: ``rates_common.is_remote`` (carrier list, see TEAM_NOTES.md); weights via
    ``rates_common.to_billing_step``; amounts via ``rates_common.money``.
    """
    raise NotImplementedError
