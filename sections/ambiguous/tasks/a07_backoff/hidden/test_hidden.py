import pytest

from retry import backoff_delays


@pytest.mark.parametrize("n,want", [(0, []), (1, [1]), (4, [1, 2, 4, 8]), (5, [1, 2, 4, 8, 16]),
                                    (6, [1, 2, 4, 8, 16, 30]), (10, [1, 2, 4, 8, 16, 30])])
def test_delays(n, want):
    assert backoff_delays(n) == want


def test_negative():
    with pytest.raises(ValueError):
        backoff_delays(-1)
