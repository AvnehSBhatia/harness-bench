import pytest
from zone import zone


@pytest.mark.parametrize("o,d,z", [("10115", "10117", 1), ("10115", "14467", 2), ("10115", "34117", 3),
                                   ("10115", "50667", 4), ("10115", "80331", 5), ("80331", "97070", 6),
                                   ("01067", "01069", 1), ("96050", "96047", 6), ("90402", "60311", 4)])
def test_zones(o, d, z):
    assert zone(o, d) == z


@pytest.mark.parametrize("o,d", [("1234", "10115"), ("10115", "12a45"), ("10115", "101150")])
def test_invalid(o, d):
    with pytest.raises(ValueError):
        zone(o, d)
