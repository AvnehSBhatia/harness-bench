# Pricing and promotions engine — SPEC (source of truth)

You are building `pricing`, the checkout pricing core of an online shop: volume tiers, bundles, coupons with
stacking and exclusivity rules, and a loyalty programme. It is seven functions, one per file. Standard library only.

All seven depend on the same domain rules (sections 2–6). They are written once, here. "Per section N" means
exactly the rule in section N, with no additions.

## 0. Files and conventions

| File | Function |
| --- | --- |
| `line_price.py` | `line_price(sku: str, qty: int, catalog: dict) -> Decimal` |
| `bundle_discount.py` | `bundle_discount(cart: dict, catalog: dict) -> Decimal` |
| `coupon_discount.py` | `coupon_discount(cart: dict, catalog: dict, coupon: dict, today: str) -> Decimal` |
| `best_coupons.py` | `best_coupons(cart: dict, catalog: dict, coupons: list, today: str) -> list[str]` |
| `loyalty_redemption.py` | `loyalty_redemption(amount: Decimal, points: int, tier: str) -> dict` |
| `price_cart.py` | `price_cart(cart: dict, catalog: dict, coupons: list, customer: dict, today: str) -> dict` |
| `points_earned.py` | `points_earned(cart: dict, catalog: dict, coupons: list, customer: dict, today: str) -> int` |

- Do not import one function file from another. Each file must work on its own.
- `promo_common.py` is a shared helper module maintained by the commerce-platform team. You may import from it,
  but do not edit it. It is not part of this SPEC: where it and this SPEC differ, this SPEC is right.
- Money is `decimal.Decimal` (EUR); never use `float`. Inputs given as str/int are read with `Decimal(str(x))`.
  "Round" means quantize to cents with `ROUND_HALF_UP`.
- Dates are ISO strings `YYYY-MM-DD`. Errors: every "raises" means `ValueError`.

## 1. Data model

```python
catalog = {
    "products": {
        "PEN":  {"price": "1.20", "category": "office"},
        "LAMP": {"price": "40.00", "category": "home", "tiers": [[5, "36.00"], [20, "32.00"]]},
        "MAT":  {"price": "20.00", "category": "home"},
    },
    "bundles": [ {"id": "DESK", "items": {"LAMP": 1, "MAT": 1}, "pct": "15"} ],   # may be missing or empty
}
cart = {"lines": [{"sku": "LAMP", "qty": 2}, {"sku": "MAT", "qty": 1}]}
coupon = {"code": "SPRING10", "kind": "percent", "value": "10", "min_spend": "50", "starts": "2026-03-01",
          "ends": "2026-03-31", "exclusive": False, "categories": ["home"]}   # "categories" optional
customer = {"tier": "silver", "points": 1500, "redeem": True}
```

- `qty` is an int ≥ 1. An unknown sku or a bad qty raises. The same sku may appear on several cart lines; it is
  then priced as one line with the summed qty.
- Categories: any string.

## 2. Line prices (graduated volume tiers)

A product without `tiers` costs `qty × price`. A product with tiers has a list of `[min_qty, unit_price]` sorted by
`min_qty` ascending (every `min_qty` ≥ 2). Pricing is **graduated**: each unit is priced by the tier its own position
falls in. Units `1 … (first min_qty − 1)` cost the base `price`; units from a tier's `min_qty` up to the next tier's
`min_qty − 1` cost that tier's price; units from the last tier's `min_qty` on cost the last tier's price.
A larger order never makes earlier units cheaper.

Example (LAMP above): 4 units = 4 × 40.00 = 160.00. 7 units = 4 × 40.00 + 3 × 36.00 = **268.00**.
22 units = 4 × 40.00 + 15 × 36.00 + 3 × 32.00 = **796.00**.

`subtotal` of a cart = sum of its line prices (after merging duplicate skus).

## 3. Bundles

Bundles are applied in the order listed in `catalog["bundles"]`. Each bundle is applied as many times as the
cart's **not yet bundled** units allow (an application needs `items[sku]` units of every sku in the bundle).
One application's discount is `pct %` of the sum of `base price × count` of its items (base `price`, never tier
prices), rounded. The bundle discount of the cart is the sum over all applications.

Example: catalog above, cart LAMP × 3 + MAT × 2: DESK applies twice, each 15 % × (40.00 + 20.00) = 9.00 →
**18.00**.

## 4. Coupons

### 4.1 Validity
A coupon is valid on `today` when `starts ≤ today ≤ ends` (both inclusive) and the cart subtotal (section 2,
before any discount) is ≥ `min_spend` (missing `min_spend` = 0). An invalid coupon gives a discount of 0.

### 4.2 Discount of one coupon
`eligible` = sum of the line prices of lines whose category is in `categories` (all lines when `categories` is
missing). Kind `percent`: `eligible × value / 100`, rounded. Kind `fixed`: `min(value, eligible)`. Any other kind
raises.

### 4.3 Combining coupons
A cart uses at most **two** coupons. **An exclusive coupon (`"exclusive": true`) cannot be combined with any
other coupon, exclusive or not.** Two non-exclusive coupons can be combined. Each coupon's discount is computed on
its own (4.2) against the same cart; a combination's discount is the sum, capped at `subtotal − bundle discount`.
Two coupons with the same code count as one coupon.

### 4.4 Best combination
Among all allowed combinations of valid coupons (including the empty one), the best has the largest combined
discount (4.3); ties go to fewer coupons, then to the alphabetically smallest sorted list of codes.
It is returned as a sorted list of codes.

## 5. Loyalty programme

### 5.1 Redemption
**Points are redeemed in blocks of 200 points; each block is worth 1.00 EUR** (one point = 0.005 EUR).
The redemption on an amount uses the largest number of whole blocks such that both: the blocks do not exceed the
customer's points, and their value does not exceed the tier's cap: **basic 20 %, silver 30 %, gold 50 %** of the
amount. Result: `{"points_used": int, "discount": Decimal}` (discount rounded; it is whole euros anyway).

Example: amount 100.00, 1500 points, silver: cap 30.00, points allow 7 blocks → 7 blocks, **1400 points, 7.00**.
Amount 10.00, 5000 points, basic: cap 2.00 → 2 blocks, **400 points, 2.00**.

Unknown tier, negative points or a negative amount raises.

### 5.2 Earning
Points earned on an order = `floor(total × multiplier)` with multiplier **basic 1, silver 1.25, gold 1.5**, where
`total` is the order total of section 6 (after bundles, coupons and redeemed points).

## 6. Order of calculation (price_cart)

1. `subtotal` — section 2.
2. `bundle_discount` — section 3.
3. `coupons`, `coupon_discount` — the best combination (4.4) of the offered coupons and its discount (4.3).
4. `points_used`, `points_discount` — if `customer["redeem"]` is true, redemption (5.1) on
   `subtotal − bundle_discount − coupon_discount`; otherwise 0 and 0.
5. `total = subtotal − bundle_discount − coupon_discount − points_discount`.

## 7. Functions

### 7.1 `line_price(sku, qty, catalog) -> Decimal`
Section 2 for one sku.

### 7.2 `bundle_discount(cart, catalog) -> Decimal`
Section 3.

### 7.3 `coupon_discount(cart, catalog, coupon, today) -> Decimal`
Sections 4.1–4.2 for one coupon (0 when invalid).

### 7.4 `best_coupons(cart, catalog, coupons, today) -> list[str]`
Section 4.4.

### 7.5 `loyalty_redemption(amount, points, tier) -> dict`
Section 5.1.

### 7.6 `price_cart(cart, catalog, coupons, customer, today) -> dict`
```python
{"subtotal": Decimal, "bundle_discount": Decimal, "coupons": ["SPRING10"], "coupon_discount": Decimal,
 "points_used": 1400, "points_discount": Decimal, "total": Decimal}
```
Section 6.

### 7.7 `points_earned(cart, catalog, coupons, customer, today) -> int`
Section 5.2, with the total from 7.6.

## 8. Done means
`python3 -m pytest -q` passes. Only this SPEC defines behaviour.
