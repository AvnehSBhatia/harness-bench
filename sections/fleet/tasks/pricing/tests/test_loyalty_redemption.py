from decimal import Decimal as D
import pytest
from loyalty_redemption import loyalty_redemption


def test_too_few_points():
    assert loyalty_redemption(D("100"), 99, "gold") == {"points_used": 0, "discount": D("0")}


def test_zero_amount():
    assert loyalty_redemption(D("0"), 1000, "gold") == {"points_used": 0, "discount": D("0")}


@pytest.mark.parametrize("args", [(D("10"), 100, "platinum"), (D("10"), -1, "basic"), (D("-1"), 100, "basic")])
def test_invalid(args):
    with pytest.raises(ValueError):
        loyalty_redemption(*args)


def test_redeem_blocks():
    assert loyalty_redemption(D("100.00"), 1500, "silver") == {"points_used": 1400, "discount": D("7.00")}
    assert loyalty_redemption(D("10.00"), 5000, "basic") == {"points_used": 400, "discount": D("2.00")}
