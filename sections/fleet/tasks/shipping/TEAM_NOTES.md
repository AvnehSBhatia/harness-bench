# shipping — team notes

## Decision log

**2026-09-30 · Billing step and dimensional weight (Marcus O., tech lead, ops platform)** — *Accepted*

Billable weights are computed only through `rates_common.parcel_metric()`, `dim_weight()` and `to_billing_step()`.
Label printing and checkout use the same functions, so a quote can never disagree with the label. Re-implementing
weight rounding in a feature service is a review blocker.

**2026-10-08 · Remote areas** — *Accepted*

The remote-area list is synced from the carrier portal into `rates_common.REMOTE_PREFIXES`; use `is_remote()`.
Do not keep postcode lists in feature code.

**2026-10-21 · Transit calendar (network ops)** — *Accepted*

Delivery dates use `rates_common.next_pickup_day()` + `add_delivery_days()` — the same calendar the tracking page
shows customers.

## Samples
`fixtures/checked_quotes_2026-10.json` holds quotes and delivery dates ops checked against carrier invoices.
