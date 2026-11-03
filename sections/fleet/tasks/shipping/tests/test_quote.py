from decimal import Decimal as D
from quote import quote
from helpers_ship import P, S


def test_example():
    assert quote(S(), "SWIFT", "express") == {"carrier": "SWIFT", "service": "express", "zone": 3, "billable_kg": D("5.0"),
                                              "base": D("25.40"), "surcharges": {"fuel": D("3.68")}, "total": D("29.08")}


def test_terra_residential_imperial():
    q = quote(S(dest="10117", parcel=P(12, 10, 8, "7.5", "imperial"), residential=True), "TERRA", "ground")
    assert q["billable_kg"] == D("3.5") and q["base"] == D("6.90")
    assert q["total"] == D("9.64")


def test_oversize_peak():
    q = quote(S(parcel=P(130, 20, 20, "4"), ship_at="2026-12-01T08:00"), "SWIFT", "standard")
    assert q["billable_kg"] == D("10.5") and q["base"] == D("27.10")
    assert q["surcharges"] == {"fuel": D("3.93"), "peak": D("1.63"), "oversize": D("25.00")}
    assert q["total"] == D("57.66")


def test_light_parcel_just_over_step():
    q = quote(S(dest="10117", parcel=P(10, 10, 10, "2.1")), "SWIFT", "express")
    assert q["billable_kg"] == D("2.5") and q["total"] == D("14.20")


def test_remote_destination_quote():
    q = quote(S(dest="59071"), "TERRA", "ground")
    assert q["zone"] == 4 and q["surcharges"] == {"fuel": D("1.13"), "remote": D("5.00")} and q["total"] == D("18.38")
