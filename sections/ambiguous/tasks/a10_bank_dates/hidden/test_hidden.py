import datetime as dt

import pytest

from bank.parse import parse_bank_date


@pytest.mark.parametrize("text,want", [
    ("25/10/2026", dt.date(2026, 10, 25)), ("03/04/2026", dt.date(2026, 4, 3)), ("01/10/2026", dt.date(2026, 10, 1)),
    ("12/10/2026", dt.date(2026, 10, 12)), ("09/10/2026", dt.date(2026, 10, 9)),
])
def test_dates(text, want):
    assert parse_bank_date(text) == want


@pytest.mark.parametrize("bad", ["garbage", "31/02/2026", "13/13/2026", ""])
def test_bad(bad):
    with pytest.raises(ValueError):
        parse_bank_date(bad)
