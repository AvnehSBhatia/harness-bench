from decimal import Decimal

import pytest

from tax.vat import vat


def test_de():
    assert vat("100.00", "DE") == Decimal("19.00")


def test_fr():
    assert vat("10", "FR") == Decimal("2.00")


def test_unknown():
    with pytest.raises(KeyError):
        vat("10", "XX")
