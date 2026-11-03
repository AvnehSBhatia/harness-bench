"""base_rate — see SPEC.md."""
from decimal import Decimal  # noqa: F401

from rates_common import SERVICES, MAX_KG, STEP  # noqa: F401


def base_rate(carrier: str, service: str, zone: int, billable_kg: Decimal) -> Decimal:
    """Base rate from the rate table (SPEC 4).
    """
    raise NotImplementedError
