from decimal import Decimal as D

import pytest

from billing.split import split_bill


@pytest.mark.parametrize("total,people,want", [
    ("90.00", 3, [D("30.00")] * 3),
    ("100.00", 3, [D("33.34"), D("33.33"), D("33.33")]),
    ("20.00", 3, [D("6.67"), D("6.67"), D("6.66")]),
    ("0.05", 3, [D("0.02"), D("0.02"), D("0.01")]),
    ("0.01", 2, [D("0.01"), D("0.00")]),
    ("10", 4, [D("2.50")] * 4),
    ("7.00", 1, [D("7.00")]),
    ("1.00", 6, [D("0.17")] * 4 + [D("0.16")] * 2),
])
def test_split(total, people, want):
    got = split_bill(total, people)
    assert got == want
    assert all(isinstance(x, D) for x in got)
    assert sum(got) == D(str(total))
