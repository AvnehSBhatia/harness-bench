import datetime

import pytest

from bank.parse import parse_bank_date


def test_unambiguous_day():
    assert parse_bank_date("25/10/2026") == datetime.date(2026, 10, 25)


def test_garbage():
    with pytest.raises(ValueError):
        parse_bank_date("garbage")
