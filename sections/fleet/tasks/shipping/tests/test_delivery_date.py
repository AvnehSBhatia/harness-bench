from delivery_date import delivery_date
from helpers_ship import S


def test_ground_over_weekend():
    assert delivery_date(S(dest="10117", ship_at="2026-03-05T10:00"), "TERRA", "ground") == "2026-03-09"


def test_cutoffs():
    assert delivery_date(S(dest="10117", ship_at="2026-03-05T16:00"), "TERRA", "ground") == "2026-03-10"
    assert delivery_date(S(dest="10117", ship_at="2026-03-03T17:59"), "SWIFT", "standard") == "2026-03-05"


def test_express_weekday():
    assert delivery_date(S(ship_at="2026-03-02T09:00"), "SWIFT", "express") == "2026-03-03"
    assert delivery_date(S(dest="80331", ship_at="2026-03-02T09:00"), "SWIFT", "express") == "2026-03-04"


def test_handover_on_weekend():
    assert delivery_date(S(dest="10117", ship_at="2026-03-07T09:00"), "TERRA", "ground") == "2026-03-11"


def test_holiday_skipped():
    assert delivery_date(S(dest="10117", ship_at="2026-05-13T10:00"), "TERRA", "ground") == "2026-05-18"
    assert delivery_date(S(dest="10117", ship_at="2026-05-13T10:00"), "SWIFT", "express") == "2026-05-15"


def test_express_friday_pickup():
    assert delivery_date(S(ship_at="2026-03-05T18:00"), "SWIFT", "express") == "2026-03-07"
    assert delivery_date(S(dest="10117", ship_at="2026-05-08T10:00"), "SWIFT", "standard") == "2026-05-11"
