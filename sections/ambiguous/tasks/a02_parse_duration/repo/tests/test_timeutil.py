import pytest

from timeutil import parse_duration


def test_seconds():
    assert parse_duration("45s") == 45


def test_compound():
    assert parse_duration("1h30m") == 5400


def test_bad():
    with pytest.raises(ValueError):
        parse_duration("abc")
