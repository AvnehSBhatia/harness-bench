"""Money helpers shared by the billing code. Amounts are Decimal euros with two places."""
from decimal import Decimal


def to_cents(value):
    """Decimal-safe conversion of an amount (str, int or Decimal) to whole cents."""
    d = Decimal(str(value))
    if d < 0 or d != d.quantize(Decimal("0.01")):
        raise ValueError(f"not a money amount: {value!r}")
    return int(d * 100)


def from_cents(cents):
    return (Decimal(cents) / 100).quantize(Decimal("0.01"))
