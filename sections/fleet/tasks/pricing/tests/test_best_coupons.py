from best_coupons import best_coupons
from helpers_pricing import BIG, CATALOG, C, FIVER, TEN, TODAY, cart

CART = cart(LAMP=2, MAT=1, PEN=5)


def test_two_non_exclusive_coupons_stack():
    assert best_coupons(CART, CATALOG, [TEN, FIVER], TODAY) == ["FIVER", "TEN"]


def test_invalid_coupons_ignored():
    assert best_coupons(CART, CATALOG, [C("OLD", "percent", "50", ends="2026-02-28"), FIVER], TODAY) == ["FIVER"]
    assert best_coupons(CART, CATALOG, [], TODAY) == []


def test_tie_prefers_fewer_coupons():
    pens = cart(PEN=5)
    assert best_coupons(pens, CATALOG, [C("F2", "fixed", "6"), C("F1", "fixed", "6")], TODAY) == ["F1"]


def test_two_exclusives_pick_larger():
    other = C("BIGGER", "percent", "25", exclusive=True)
    assert best_coupons(CART, CATALOG, [BIG, other], TODAY) == ["BIGGER"]


def test_at_most_two():
    assert len(best_coupons(CART, CATALOG, [TEN, FIVER, C("SIX", "fixed", "6")], TODAY)) == 2


def test_exclusive_coupon_alone():
    assert best_coupons(CART, CATALOG, [TEN, FIVER, BIG], TODAY) == ["BIG"]
