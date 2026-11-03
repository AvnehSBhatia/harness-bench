from decimal import Decimal as D
from prorate import prorate
from helpers_billing import raises_msg


def test_half_of_april():
    assert prorate("300.00", "USD", "2026-04-01", "2026-05-01", "2026-04-16") == D("150.00")


def test_change_on_first_day():
    assert prorate("99.99", "EUR", "2026-04-01", "2026-05-01", "2026-04-01") == D("99.99")
    assert str(prorate("10", "EUR", "2026-06-01", "2026-07-01", "2026-06-01")) == "10.00"


def test_last_day():
    assert prorate("300.00", "USD", "2026-04-01", "2026-05-01", "2026-04-30") == D("10.00")
    assert prorate("100.00", "EUR", "2026-11-01", "2026-12-01", "2026-11-30") == D("3.33")


def test_calendar_months():
    assert prorate("280.00", "EUR", "2026-02-01", "2026-03-01", "2026-02-15") == D("140.00")
    assert prorate("100.00", "EUR", "2026-02-01", "2026-03-01", "2026-02-28") == D("3.57")
    assert prorate("310.00", "USD", "2026-05-01", "2026-06-01", "2026-05-21") == D("110.00")
    assert prorate("365.00", "USD", "2026-01-01", "2027-01-01", "2026-12-02") == D("30.00")


def test_validation():
    raises_msg(lambda: prorate("1", "CHF", "2026-04-02", "2026-04-01", "2026-04-01"), "unknown currency: CHF")
    raises_msg(lambda: prorate("1", "EUR", "2026-04-01", "2026-04-01", "2026-04-01"), "empty period")
    raises_msg(lambda: prorate("1", "EUR", "2026-04-02", "2026-04-01", "2026-04-01"), "empty period")
    raises_msg(lambda: prorate("1", "EUR", "2026-04-01", "2026-05-01", "2026-05-01"), "change outside period")
    raises_msg(lambda: prorate("1", "EUR", "2026-04-01", "2026-05-01", "2026-03-31"), "change outside period")


def test_jpy_and_kwd():
    assert str(prorate("1000", "JPY", "2026-06-01", "2026-07-01", "2026-06-11")) == "667"
    assert str(prorate("10.000", "KWD", "2026-09-01", "2026-10-01", "2026-09-21")) == "3.333"


def test_period_not_on_month_start():
    assert prorate("90.00", "EUR", "2026-04-10", "2026-05-10", "2026-05-01") == D("27.00")
    raises_msg(lambda: prorate(90.0, "EUR", "2026-04-10", "2026-05-10", "2026-05-01"), "float not allowed", TypeError)


def test_repeating_fractions():
    assert prorate("100.00", "EUR", "2026-04-01", "2026-05-01", "2026-04-02") == D("96.67")
    assert prorate("-30.00", "EUR", "2026-09-01", "2026-10-01", "2026-09-30") == D("-1.00")
