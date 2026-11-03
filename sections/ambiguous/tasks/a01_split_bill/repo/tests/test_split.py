from decimal import Decimal

from billing.split import split_bill


def test_even_split():
    assert split_bill("90.00", 3) == [Decimal("30.00")] * 3


def test_two_guests():
    assert split_bill("10", 2) == [Decimal("5.00"), Decimal("5.00")]
