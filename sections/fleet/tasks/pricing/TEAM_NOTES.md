# pricing — team notes

## Decision log

**2026-09-22 · One price function (Sofia R., tech lead, commerce-platform)** — *Accepted*

Line prices with volume tiers come only from `promo_common.tier_price()`. The storefront, the cart service and the
POS all call it, so the price a customer sees is the price they pay. Re-implementing tier logic in a feature service
is a review blocker (INC-1840: three different prices for the same basket).

**2026-10-06 · Coupon stacking (PROMO-4, marketing ops)** — *Accepted*

Whether two coupons can be used together is decided by `promo_common.can_combine()`; do not hard-code stacking rules.

**2026-10-13 · Loyalty points (loyalty team)** — *Accepted*

Point values live in `promo_common` (`REDEEM_BLOCK`, `POINT_VALUE`, `points_value()`), shared with the app and the
customer statements.

## Samples
`fixtures/priced_baskets_2026-10.json` holds baskets priced by the production checkout last month.
