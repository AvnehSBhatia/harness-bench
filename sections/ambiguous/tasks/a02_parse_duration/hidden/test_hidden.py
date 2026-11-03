import pytest

from timeutil import parse_duration


@pytest.mark.parametrize("text,want", [
    ("45s", 45), ("1h30m", 5400), ("500ms", 0.5), ("2d", 172800), ("15m", 900),
    ("1d2h3m4s", 93784), ("1m500ms", 60.5),
])
def test_values(text, want):
    assert parse_duration(text) == pytest.approx(want)


@pytest.mark.parametrize("bad", ["", "abc", "10x", "h1", "5 parsecs"])
def test_bad(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)
