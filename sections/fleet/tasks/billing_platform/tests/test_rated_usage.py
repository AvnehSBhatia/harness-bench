from decimal import Decimal as D
from rated_usage import rated_usage
from helpers_billing import API_PLAN, raises_msg

STEP = {"currency": "USD", "tiers": [{"up_to": 100, "unit": "1.00"}, {"up_to": 200, "unit": "0.50"},
                                     {"up_to": None, "unit": "0.25"}]}


def test_graduated_tiers():
    assert rated_usage(12000, API_PLAN) == D("21.00")
    assert rated_usage(10000, API_PLAN) == D("18.00")
    assert rated_usage(10001, API_PLAN) == D("18.00")


def test_tier_edges():
    assert rated_usage(100, STEP) == D("100.00")
    assert rated_usage(101, STEP) == D("100.50")
    assert rated_usage(200, STEP) == D("150.00")
    assert rated_usage(201, STEP) == D("150.25")


def test_minimum_charge():
    assert rated_usage(1500, API_PLAN) == D("5.00")
    assert rated_usage(1000, API_PLAN) == D("5.00")
    assert rated_usage(0, API_PLAN) == D("0")


def test_no_minimum():
    plan = dict(API_PLAN, minimum=None)
    assert rated_usage(1500, plan) == D("1.00")
    plan = {k: v for k, v in API_PLAN.items() if k != "minimum"}
    assert rated_usage(1001, plan) == D("0.00")


def test_bounded_last_tier():
    plan = {"currency": "EUR", "tiers": [{"up_to": 10, "unit": "2.50"}, {"up_to": 20, "unit": "2.00"}]}
    assert rated_usage(20, plan) == D("45.00")
    assert rated_usage(15, plan) == D("35.00")
    raises_msg(lambda: rated_usage(21, plan), "quantity exceeds tiers")


def test_bad_quantity():
    for q in (-1, 1.5, True, "10", None):
        raises_msg(lambda: rated_usage(q, STEP), "bad quantity")


def test_sub_unit_prices():
    plan = {"currency": "JPY", "tiers": [{"up_to": None, "unit": "0.3"}]}
    assert rated_usage(7, plan) == D("2")
    assert rated_usage(15, plan) == D("4")
    assert rated_usage(25, plan) == D("8")


def test_currency_checked():
    raises_msg(lambda: rated_usage(5, {"currency": "CHF", "tiers": [{"up_to": None, "unit": "1"}]}),
               "unknown currency: CHF")
    assert str(rated_usage(3, {"currency": "KWD", "tiers": [{"up_to": None, "unit": "0.1234"}]})) == "0.370"
