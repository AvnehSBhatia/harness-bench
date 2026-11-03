from files.format import format_size


def test_zero():
    assert format_size(0) == "0 B"


def test_bytes():
    assert format_size(512) == "512 B"
