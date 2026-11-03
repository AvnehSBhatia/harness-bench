from decimal import Decimal as D
from cheapest_option import cheapest_option
from helpers_ship import P, S

Z1 = dict(dest="10117", ship_at="2026-03-02T09:00")


def test_cheapest_with_slack():
    assert cheapest_option(S(**Z1), "2026-03-10") == {"carrier": "TERRA", "service": "ground", "total": D("8.03"),
                                                      "delivery_date": "2026-03-04"}


def test_deadline_forces_express():
    assert cheapest_option(S(**Z1), "2026-03-03") == {"carrier": "SWIFT", "service": "express", "total": D("20.50"),
                                                      "delivery_date": "2026-03-03"}


def test_nothing_qualifies():
    assert cheapest_option(S(**Z1), "2026-03-02") is None


def test_heavy_parcel_skips_swift():
    r = cheapest_option(S(parcel=P(30, 30, 30, "40"), **Z1), "2026-03-03")
    assert r is None
    assert cheapest_option(S(parcel=P(30, 30, 30, "40"), **Z1), "2026-03-04")["carrier"] == "TERRA"


def test_saturday_delivery_meets_deadline():
    s = S(dest="10117", ship_at="2026-03-05T18:30")
    assert cheapest_option(s, "2026-03-07") == {"carrier": "SWIFT", "service": "express", "total": D("20.50"),
                                                "delivery_date": "2026-03-07"}
    assert cheapest_option(s, "2026-03-09")["service"] == "standard"
