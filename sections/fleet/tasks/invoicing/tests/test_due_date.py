import pytest
from due_date import due_date


def test_net_on_business_day():
    assert due_date("2026-03-02", "NET30", "DE") == "2026-04-01"
    assert due_date("2026-06-10", "DUE", "DE") == "2026-06-10"


def test_weekend_rolls_forward():
    assert due_date("2026-03-02", "NET5", "DE") == "2026-03-09"
    assert due_date("2026-02-10", "EOM+15", "DE") == "2026-03-16"


def test_holiday_rolls_forward():
    assert due_date("2026-04-14", "NET30", "DE") == "2026-05-15"


def test_seller_calendar():
    assert due_date("2026-07-04", "NET10", "FR") == "2026-07-15"
    assert due_date("2026-07-04", "NET10", "DE") == "2026-07-14"


def test_eom_on_business_day():
    assert due_date("2026-03-10", "EOM", "GB") == "2026-03-31"


@pytest.mark.parametrize("terms", ["NET0", "NET030", "net30", "EOM+0", "NET121", "NET 30", "COD"])
def test_bad_terms(terms):
    with pytest.raises(ValueError):
        due_date("2026-03-02", terms, "DE")


def test_unknown_country():
    with pytest.raises(ValueError):
        due_date("2026-03-02", "NET30", "IT")


def test_month_end_on_weekend():
    assert due_date("2026-05-04", "EOM", "DE") == "2026-06-01"
    assert due_date("2026-01-02", "NET29", "DE") == "2026-02-02"
