from decimal import Decimal as D
from surcharges import surcharges
from helpers_ship import P, S


def test_fuel_only():
    assert surcharges(S(), "SWIFT", "express") == {"fuel": D("3.68")}


def test_terra_residential():
    assert surcharges(S(residential=True), "TERRA", "ground") == {"fuel": D("0.95"), "residential": D("2.10")}


def test_peak_window():
    assert surcharges(S(ship_at="2026-11-27T10:00"), "SWIFT", "express")["peak"] == D("1.52")
    assert "peak" in surcharges(S(ship_at="2026-12-24T10:00"), "SWIFT", "express")
    assert "peak" not in surcharges(S(ship_at="2026-12-28T10:00"), "SWIFT", "express")


def test_oversize():
    assert surcharges(S(parcel=P(121, 10, 10, "1")), "SWIFT", "express")["oversize"] == D("25.00")
    assert surcharges(S(parcel=P(100, 50, 51, "1")), "TERRA", "ground")["oversize"] == D("18.00")
    assert "oversize" not in surcharges(S(parcel=P(100, 50, 50, "1")), "TERRA", "ground")


def test_remote_island_and_coast():
    assert surcharges(S(dest="08056"), "SWIFT", "standard")["remote"] == D("7.50")
    assert surcharges(S(dest="97070"), "TERRA", "ground")["remote"] == D("5.00")


def test_remote_alpine_area():
    assert surcharges(S(dest="59071"), "TERRA", "ground").get("remote") == D("5.00")
    assert surcharges(S(dest="59071"), "SWIFT", "express").get("remote") == D("7.50")
