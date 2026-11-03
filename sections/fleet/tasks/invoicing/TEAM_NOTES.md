# invoicing — team notes

## Decision log

**2026-09-14 · One rounding function (Lena K., tech lead, billing-platform)** — *Accepted*

After the 1-cent mismatches between invoice PDFs and the ledger export (INC-2291), every money amount is rounded
through `billing_common.round_money()`. It knows each currency's minor unit and finance's rounding policy (FIN-2).
Ad-hoc `quantize()` calls in feature services are a review blocker.

**2026-10-02 · Tax rates come from the rate service (tax team)** — *Accepted*

`billing_common.TAX_RATES` / `tax_rate()` are synced nightly from the tax team's rate service. Do not hard-code VAT
rates in feature code: when a country changes a rate, we change it in one place.

**2026-10-19 · Due dates (treasury, TREAS-12)** — *Accepted*

Use `billing_common.apply_terms()` + `billing_common.roll_to_business_day()` so dunning, the customer portal and the
invoice PDF all show the same due date.

## Samples
`fixtures/finance_reconciled_2026-10.json` holds invoices from last month's close with the totals and due dates
finance reconciled against the ledger.
