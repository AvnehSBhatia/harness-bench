from decimal import Decimal as D
import pytest
from billable_weight import billable_weight
from helpers_ship import P


def test_dimensional_weight_per_carrier():
    assert billable_weight(P(40, 30, 20, "3.2"), "SWIFT") == D("5.0")
    assert billable_weight(P(40, 30, 20, "3.2"), "TERRA") == D("4.0")


def test_exact_step_and_minimum():
    assert billable_weight(P(10, 10, 10, "2.5"), "SWIFT") == D("2.5")
    assert billable_weight(P(10, 10, 10, "0.2"), "TERRA") == D("0.5")


def test_imperial():
    assert billable_weight(P(10, 10, 10, "4", "imperial"), "SWIFT") == D("3.5")


def test_carrier_maximum():
    with pytest.raises(ValueError):
        billable_weight(P(10, 10, 10, "31"), "SWIFT")
    assert billable_weight(P(10, 10, 10, "31"), "TERRA") == D("31.0")


@pytest.mark.parametrize("p,c", [(P(10, 10, 10, "1", "si"), "SWIFT"), (P(0, 10, 10, "1"), "SWIFT"), (P(10, 10, 10, "1"), "ACME")])
def test_invalid(p, c):
    with pytest.raises(ValueError):
        billable_weight(p, c)


def test_just_over_a_step():
    assert billable_weight(P(10, 10, 10, "2.1"), "SWIFT") == D("2.5")
    assert billable_weight(P(10, 10, 10, "2.01"), "TERRA") == D("2.5")
