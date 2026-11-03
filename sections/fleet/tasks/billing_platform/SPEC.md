# Billing platform — SPEC (source of truth)

You are building `billing_platform`, the core of a usage-based SaaS billing system: ingesting amounts and usage
events, rating usage, FX conversion and tax, invoice assembly with proration and payment terms, credits, payment
reconciliation and an aging report. It is twelve functions, one per file. Standard library only.

The domain rules (sections 2–15) are written once, here. Later sections are defined in terms of earlier ones:
"per section N" means exactly the rule of section N, with no additions or omissions.

## 0. Files and conventions

| Concern | File | Function |
| --- | --- | --- |
| Ingest | `parse_amount.py` | `parse_amount(text: str, currency: str) -> Decimal` |
| Ingest | `parse_usage.py` | `parse_usage(line: str) -> dict` |
| Ingest | `aggregate_usage.py` | `aggregate_usage(lines: list, start: str, end: str) -> dict` |
| Pricing | `rated_usage.py` | `rated_usage(quantity: int, plan: dict) -> Decimal` |
| Pricing | `convert.py` | `convert(amount, src: str, dst: str, rates: dict) -> Decimal` |
| Pricing | `line_tax.py` | `line_tax(net, currency: str, country: str, category: str) -> Decimal` |
| Invoicing | `prorate.py` | `prorate(amount, currency: str, period_start: str, period_end: str, change: str) -> Decimal` |
| Invoicing | `due_date.py` | `due_date(issued: str, terms: str) -> str` |
| Invoicing | `build_invoice.py` | `build_invoice(account: dict, usage_lines: list, period: dict, rates: dict) -> dict` |
| Invoicing | `apply_credits.py` | `apply_credits(total, currency: str, credits: list, today: str) -> dict` |
| Ledger | `reconcile.py` | `reconcile(invoices: list, payments: list) -> dict` |
| Ledger | `aging_report.py` | `aging_report(invoices: list, payments: list, as_of: str) -> dict` |

- Do not import one function file from another. Each file must work on its own (re-implement what you need).
- `platform_common.py` is a shared helper module maintained by the platform team. You may import from it, but do
  not edit it. It is not part of this SPEC: where it and this SPEC differ, this SPEC is right.
- Errors: every "raises X" means `ValueError` with exactly the message X, unless another exception type is named.
- Dates are ISO strings `YYYY-MM-DD`; returned dates use the same format.

## 2. Money

- Currencies and their minor units (decimal places): **USD 2, EUR 2, GBP 2, JPY 0, KWD 3**. Any other currency code
  anywhere raises `unknown currency: <code>` (checked before anything else in a function that takes a currency).
- Amount arguments (`amount`, `net`, `total`, prices and unit prices inside dicts) are `Decimal`, `int` or `str` and
  are read with `Decimal(str(x))`; a `float` raises `TypeError("float not allowed")`.
- **Round** to a currency means: quantize to that currency's minor unit with **`ROUND_HALF_EVEN`** (banker's
  rounding: 0.125 → 0.12, 0.135 → 0.14, JPY 4.5 → 4, 5.5 → 6). Every "round" in this SPEC is this rounding.
- Amounts stored as text inside records (credit `amount`, invoice `total`, payment `amount`) are in the section 3
  format and are read with section 3 using that record's `currency`.

## 3. Amount text — `parse_amount(text, currency)`

After stripping surrounding whitespace, `text` is: an optional currency code (three capital letters) followed by
exactly one space, then a number. The number is either `[-]N` or `(N)` (parentheses = negative; not both).
`N` is an integer part, optionally followed by `.` and one or more fraction digits. The integer part is either
plain digits (`1234`) or digit groups separated by `,` where the first group has 1–3 digits and every later group
exactly 3 (`1,234,567`). Nothing else is allowed (no `+`, no symbols, no inner spaces, no `.5`, no `5.`).

Checks, in this order:
1. unknown currency (section 2);
2. `text` does not match the format above → raises `bad amount: <text>` (`<text>` exactly as passed);
3. a code is present and differs from `currency` → raises `currency mismatch`;
4. more fraction digits than the currency's minor unit → raises `too many decimals` (JPY allows none at all).

Result: the value as a `Decimal` quantized to the currency's minor unit (`"12.5"` EUR → `Decimal("12.50")`,
`"(1,234)"` USD → `Decimal("-1234.00")`).

## 4. Usage events — `parse_usage(line)`

A line is `event_id|account|metric|quantity|timestamp`. Checks, in this order:
1. not exactly 5 `|`-separated fields → raises `bad line: expected 5 fields`; each field is then stripped of
   surrounding whitespace;
2. `event_id` or `account` empty → raises `bad line: empty field`;
3. `metric` not one of `api_calls`, `gb_hours`, `seats` → raises `unknown metric: <metric>`;
4. `quantity` not one or more ASCII digits → raises `bad quantity: <quantity>`;
5. `timestamp` not `YYYY-MM-DDTHH:MM:SS` immediately followed by `Z` or an offset `+HH:MM` / `-HH:MM`, or not a
   real date/time → raises `bad timestamp: <timestamp>`. A timestamp without offset is invalid.

Result: `{"id": str, "account": str, "metric": str, "quantity": int, "ts": str}` where `ts` is the instant
converted to UTC and written `YYYY-MM-DDTHH:MM:SSZ` (`2026-04-30T23:30:00-02:00` → `2026-05-01T01:30:00Z`).

## 5. Usage aggregation — `aggregate_usage(lines, start, end)`

`start` and `end` are timestamps in the section 4 format (any offset); invalid ones raise as in section 4 step 5.
`start >= end` raises `empty period`. The billing window is **half-open: `start <= ts < end`** (an event exactly at
`end` belongs to the next window).

Lines that are empty after stripping, or whose stripped text starts with `#`, are skipped. Every other line is
parsed with section 4 (a bad line raises its section 4 error). **Duplicate `event_id`s: the first occurrence in the
list wins and every later line with that id is ignored**, whether or not the first one is inside the window.

Result: `{account: {metric: total_quantity}}` over the events inside the window. An account or metric appears only
if at least one event of it is inside the window (an event with quantity 0 still creates the entry).

## 6. Rated usage — `rated_usage(quantity, plan)`

```python
plan = {"currency": "USD", "minimum": "5.00",          # "minimum" optional (missing or None = no minimum)
        "tiers": [{"up_to": 1000, "unit": "0"}, {"up_to": 10000, "unit": "0.002"}, {"up_to": None, "unit": "0.0015"}]}
```
`quantity` must be an `int` (not `bool`) ≥ 0, else raises `bad quantity`. Tiers are **graduated**: units
`1 … up_to₁` cost `unit₁` each, units `up_to₁+1 … up_to₂` cost `unit₂` each, and so on; `up_to: None` is
unbounded. If the quantity is larger than the last `up_to` (and no tier is unbounded) → raises
`quantity exceeds tiers`. The charge is the exact sum, rounded once (section 2) to the plan currency. Then, if the
quantity is > 0 and a minimum is set and the charge is below it, the charge is the minimum (rounded).
A quantity of 0 always costs 0.

Example (plan above): 12,000 units = 1000 × 0 + 9000 × 0.002 + 2000 × 0.0015 = 18.00 + 3.00 = **21.00**;
1,500 units = 1.00 → minimum → **5.00**.

## 7. FX conversion — `convert(amount, src, dst, rates)`

`rates` maps a currency code to how many units of it one unit of the base currency buys, as strings
(`{"USD": "1", "EUR": "0.5", "JPY": "150"}`). Checks: both currencies known (section 2, `src` first). If
`src == dst` the result is `amount` rounded to `dst` (no rate needed). Otherwise a missing rate raises
`no rate for <code>` (`src` checked first), and the result is **`amount × rates[dst] / rates[src]`**, computed in
that order with `Decimal` at default context precision, then rounded once (section 2) to `dst`.

## 8. Tax — `line_tax(net, currency, country, category)`

Rates in percent:

| Country | standard | reduced |
| --- | --- | --- |
| DE | 19 | 7 |
| FR | 20 | 5.5 |
| GB | 20 | 0 |
| JP | 10 | 8 |
| US | 0 | 0 |

Categories: `standard` and `digital` use the standard rate; `books` and `food` the reduced rate; `exempt` is 0 %
in every country. Checks, in order: unknown currency; unknown country raises `unknown country: <country>`;
unknown category raises `unknown category: <category>`. Tax = `net × rate / 100` rounded (section 2) to the
currency. `net` may be negative (credit lines); the tax is then negative.

## 9. Proration — `prorate(amount, currency, period_start, period_end, change)`

A billing period is the half-open date range `[period_start, period_end)`: `period_end` is the first day of the next
period. `period_days = period_end − period_start` in **actual calendar days** (February 2026 has 28, May has 31,
a yearly period has 365). Checks: unknown currency; `period_start >= period_end` raises `empty period`; `change`
outside `[period_start, period_end)` raises `change outside period`.

The prorated amount for a plan change on `change` (the change day is included) is
**`amount × (period_end − change) / period_days`**, computed in that order, rounded (section 2) to the currency.
`change == period_start` gives the whole amount.

## 10. Payment terms — `due_date(issued, terms)`

`terms` is `NET<n>` with `n` a whole number 0–120 written without sign or leading `+` (`NET0`, `NET30`), or `EOM`.
Anything else raises `bad terms: <terms>`. The raw due date is `issued + n days` (`NET<n>`), or the last calendar day
of the month of `issued` (`EOM`). **If the raw due date is a Saturday or a Sunday, the due date is the following
Monday.** No holidays.

## 11. Invoice — `build_invoice(account, usage_lines, period, rates)`

```python
account = {"id": "acme", "currency": "EUR", "country": "DE",
           "plan": {"currency": "USD", "price": "300.00"},
           "change": {"date": "2026-04-16", "price": "450.00"},        # optional (missing or None = no change)
           "usage_plans": {"api_calls": {...section 6 plan...}}}      # optional, may be empty
period = {"start": "2026-04-01", "end": "2026-05-01"}                 # section 9 period
```
Lines, in this order (all `net` and `tax` values in `account["currency"]`):
1. Subscription. Without a change: one line `{"kind": "subscription", "net": N}` where N = the plan price converted
   (section 7) from the plan currency. With a change on date `c`: the line `subscription` has
   `net = convert(round(price) − prorate(price, c))` and a second line `{"kind": "subscription_change", "net":
   convert(prorate(new_price, c))}` — both prorations per section 9 in the plan currency, over `period`, then converted.
2. Usage: for each metric of `usage_plans` in alphabetical order, `quantity` = the account's total for that metric in
   section 5 aggregation of `usage_lines` over `start = period["start"] + "T00:00:00Z"`,
   `end = period["end"] + "T00:00:00Z"` (0 when absent). Metrics with quantity 0 get no line. Otherwise the line is
   `{"kind": "usage", "metric": m, "quantity": q, "net": convert(rated_usage(q, plan))}` (section 6 in the usage
   plan's currency, then section 7).
3. Every line also gets `"tax"`: section 8 on that line's `net`, the account currency and country, category
   `digital`. **Tax is computed per line and summed**, never on the invoice net.

Result: `{"account": id, "currency": ccy, "lines": [...], "net": Σ line nets, "tax": Σ line taxes,
"total": net + tax}`.

## 12. Credits — `apply_credits(total, currency, credits, today)`

`credits` is a list of `{"id": str, "currency": str, "amount": text, "expires": "YYYY-MM-DD" or None}`. `total` is
rounded to `currency` first; a negative total raises `negative total`. A credit is **usable** when its currency equals
`currency` and it has not expired (`expires` missing/None = never; a credit is still usable on its `expires` day).
Usable credits are applied in order of `expires` ascending (never-expiring last), ties by `id` ascending; each takes
`min(its balance, what is still due)`.

Result: `{"applied": [{"id": str, "amount": Decimal}, ...]` (application order, only amounts > 0),
`"due": Decimal` (what is left), `"remaining": {id: Decimal}`} where `remaining` holds the leftover balance of every
usable credit (including those not touched or fully used) and nothing for unusable ones.

## 13. Reconciliation — `reconcile(invoices, payments)`

Invoices: `{"id", "currency", "total": text, "issued": date, "terms": str}`. Payments:
`{"id", "currency", "amount": text, "date": date, "reference": str or None}`. Payments are processed in order of
`date`, ties by `id`; open invoices are taken in order of `issued`, ties by `id`. Money never crosses currencies.

1. **By reference** (all payments, first): if a payment's `reference`, stripped and compared case-insensitively,
   equals an invoice `id` of the same currency, the payment pays that invoice up to its open balance.
2. **FIFO** (then): every payment's leftover pays open invoices of its currency, oldest first, each invoice fully
   before the next.

Result: `{"allocations": [{"payment": id, "invoice": id, "amount": Decimal}, ...]` (in the order made, only amounts
> 0), `"open": {invoice_id: balance}` (only balances > 0), `"unapplied": {payment_id: leftover}` (only > 0)}.

## 14. Aging — `aging_report(invoices, payments, as_of)`

Invoices and payments as in section 13. Ignore invoices `issued` after `as_of` and payments dated after `as_of`.
Open balances are section 13 on what remains. For each invoice with an open balance, its due date is section 10 on
`issued` and `terms`, and `days = as_of − due date` in days. Buckets: `current` (days ≤ 0), `1-30`, `31-60`,
`61-90`, `90+` (days > 90).

Result: `{currency: {"current": Decimal, "1-30": Decimal, "31-60": Decimal, "61-90": Decimal, "90+": Decimal}}`
with every bucket present (sum of open balances, 0 when none) for each currency that has at least one open invoice.

## 15. Done means
`python3 -m pytest -q` passes. Only this SPEC defines behaviour.
