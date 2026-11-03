import pytest

from files.format import format_size


@pytest.mark.parametrize("n,want", [
    (0, "0 B"), (512, "512 B"), (999, "999 B"), (1000, "1000 B"), (1023, "1023 B"), (1024, "1.0 KB"),
    (1536, "1.5 KB"), (1048576, "1.0 MB"), (2469606195, "2.3 GB"), (10 * 1024 ** 2, "10.0 MB"),
])
def test_sizes(n, want):
    assert format_size(n) == want
