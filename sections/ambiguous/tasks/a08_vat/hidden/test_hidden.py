from decimal import Decimal as D

import pytest

from tax.vat import vat


@pytest.mark.parametrize("net,country,want", [
    ("100.00", "DE", D("19.00")), ("10", "FR", D("2.00")),
    ("0.50", "NL", D("0.11")), ("1.50", "IE", D("0.35")), ("12.50", "DE", D("2.38")), ("40.00", "FR", D("8.00")),
    ("2.50", "NL", D("0.53")),
])
def test_vat(net, country, want):
    got = vat(net, country)
    assert got == want and isinstance(got, D)


def test_unknown():
    with pytest.raises(KeyError):
        vat("10", "XX")
