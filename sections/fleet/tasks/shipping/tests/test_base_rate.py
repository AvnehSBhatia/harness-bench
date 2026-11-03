from decimal import Decimal as D
import pytest
from base_rate import base_rate


def test_rates():
    assert base_rate("SWIFT", "express", 3, D("5.0")) == D("25.40")
    assert base_rate("TERRA", "ground", 1, D("0.5")) == D("4.20")
    assert base_rate("SWIFT", "standard", 6, D("3.0")) == D("25.00")
    assert base_rate("TERRA", "ground", 5, D("50")) == D("106.20")


@pytest.mark.parametrize("args", [("SWIFT", "express", 7, D("1")), ("SWIFT", "express", 1, D("2.3")),
                                  ("SWIFT", "express", 1, D("0")), ("SWIFT", "standard", 1, D("30.5")),
                                  ("TERRA", "express", 1, D("1"))])
def test_invalid(args):
    with pytest.raises(ValueError):
        base_rate(*args)
