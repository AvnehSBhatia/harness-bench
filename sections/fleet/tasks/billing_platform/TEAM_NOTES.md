# billing_platform — team notes

## Decision log

**2026-08-11 · One rounding function (Priya N., tech lead, platform)** — *Accepted*

Every money rounding goes through `platform_common.round_money()`. The invoice PDF, the customer portal and the
finance export all call it, so a customer never sees two different cents for the same line. Hand-rolled
`quantize()` calls in feature services are a review blocker (INC-2214: invoice and portal disagreed by 0.01).

**2026-09-02 · Proration (FIN-7, finance + platform)** — *Accepted*

Mid-period plan changes are prorated with `platform_common.remaining_fraction()`; do not re-derive day counts in
feature code. Finance reconciles proration against the same helper.

**2026-09-17 · Usage windows (usage pipeline)** — *Accepted*

Whether a usage event belongs to a billing window is decided by `platform_common.in_period()`, shared with the
usage dashboards so the numbers on the dashboard match the invoice.

**2026-10-05 · Payment terms (AR team)** — *Accepted*

Due dates come from `platform_common.payment_due()` (also used by dunning e-mails and the aging export). Do not
compute due dates by hand.
