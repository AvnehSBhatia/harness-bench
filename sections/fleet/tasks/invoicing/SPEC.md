# Multi-currency invoicing — SPEC (source of truth)

You are building `invoicing`, the money core of a B2B/B2C billing service that issues invoices in six currencies
for sellers in six countries. It is seven functions, one per file. Standard library only.

Every function below depends on the same domain rules (sections 2–7): currencies and rounding, tax treatment and
tax rates, payment terms and business-day calendars. They are written once, here. Where a function's behaviour
says "per section N", it means exactly the rule in section N, with no additions.

## 0. Files and conventions

| File | Function |
| --- | --- |
| `line_net.py` | `line_net(line: dict, currency: str) -> Decimal` |
| `line_tax.py` | `line_tax(line: dict, seller: str, buyer: dict, currency: str) -> Decimal` |
| `invoice_totals.py` | `invoice_totals(invoice: dict) -> dict` |
| `convert.py` | `convert(amount: Decimal, from_ccy: str, to_ccy: str, rates: dict) -> Decimal` |
| `due_date.py` | `due_date(issue_date: str, terms: str, country: str) -> str` |
| `credit_note.py` | `credit_note(invoice: dict, returns: list[dict]) -> dict` |
| `late_fee.py` | `late_fee(invoice: dict, paid_date: str) -> Decimal` |

- Do not import one function file from another. Each file must work on its own.
- `billing_common.py` is a shared helper module maintained by the billing-platform team. You may import from it,
  but do not edit it. It is not part of this SPEC: where it and this SPEC differ, this SPEC is right.
- All money values are `decimal.Decimal`. Never use `float` for money: inputs given as strings or ints are
  converted with `Decimal(str(x))`.
- Dates are ISO strings `YYYY-MM-DD` in and out.
- Errors: every "raises" below means `ValueError` (a subclass is fine).

## 1. Data model

### 1.1 Invoice line

```python
{
    "sku": "WIDGET-01",        # str, unique within one invoice
    "qty": 3,                  # int or decimal string ("2.5" hours); must be > 0
    "unit_price": "19.99",     # decimal string or int, in the invoice currency; must be >= 0
    "discount_pct": "10",      # optional, decimal string, 0 <= d <= 100, default "0"
    "category": "standard",    # "standard" | "reduced" | "zero" | "exempt"
}
```

A line that breaks any constraint above (qty <= 0, negative price, discount outside 0–100, unknown category)
raises.

### 1.2 Buyer

```python
{"country": "FR", "vat_id": "FR40303265045"}   # vat_id may be missing or None
```

A buyer **has a VAT id** when `vat_id` is present and is a non-empty string after stripping whitespace.
A buyer with a VAT id is a business (B2B); a buyer without one is a consumer (B2C).

### 1.3 Invoice

```python
{
    "seller": "DE",                     # seller country, one of section 4.1
    "buyer": {"country": "FR", "vat_id": None},
    "currency": "EUR",                  # one of section 2.1
    "issue_date": "2026-05-04",
    "terms": "NET30",                   # section 6.1
    "lines": [ ...lines... ],           # at least one line
}
```

An invoice with no lines, an unknown seller country or an unknown currency raises.

## 2. Currencies and rounding

### 2.1 Supported currencies and minor units

The minor unit is the number of decimal places an amount in that currency is stated in (ISO 4217 exponent).

| Currency | Minor unit | Smallest amount |
| --- | --- | --- |
| EUR | 2 | 0.01 |
| USD | 2 | 0.01 |
| GBP | 2 | 0.01 |
| CHF | 2 | 0.01 |
| JPY | 0 | 1 |
| KWD | 3 | 0.001 |

Any other currency code raises. Codes are upper case; do not normalise case (`"eur"` raises).

### 2.2 Rounding rule

"Round" in this SPEC always means: quantize to the currency's minor unit (2.1) with **round half away from zero**
(`decimal.ROUND_HALF_UP`). Examples: EUR `2.345` → `2.35`, EUR `-2.345` → `-2.35`, JPY `5097.45` → `5097`,
JPY `1234.5` → `1235`, KWD `1.2345` → `1.235`.

Round only where this SPEC says "round". Intermediate values keep full `Decimal` precision. In particular:
a line's net is rounded once (3.1), a line's tax is rounded once (5.1), invoice tax is rounded once per rate (5.2),
and a converted amount is rounded once (2.3).

Every money value a function returns is rounded to the minor unit of its currency, including zero
(EUR zero is `Decimal("0.00")`, JPY zero is `Decimal("0")`). Tests compare values, so `Decimal("5")` and
`Decimal("5.00")` are equal, but `Decimal("5097.45")` is not `Decimal("5097")`.

### 2.3 Currency conversion

`rates` maps a currency code to **units of that currency per 1 EUR**, as decimal strings, e.g.
`{"USD": "1.0850", "JPY": "162.37", "GBP": "0.8550"}`. EUR is always 1 and may be missing from `rates`
(if present it is ignored).

`converted = amount / rate[from_ccy] * rate[to_ccy]`, computed with full precision, then rounded once to the
minor unit of `to_ccy`. Converting a currency to itself returns the amount rounded to its own minor unit (no
rates needed). A needed rate that is missing, zero or negative raises; an unsupported currency on either side
raises.

Example: 12.34 EUR → JPY at 162.37 = 2003.6458 → **2004** JPY. 100 USD → GBP with USD 1.0850 and GBP 0.8550 =
78.80184… → **78.80** GBP.

## 3. Line amounts

### 3.1 Line net

`net = qty × unit_price × (100 − discount_pct) / 100`, rounded once (2.2) to the invoice currency.

Example: 3 × 19.99 EUR at 10 % discount = 53.973 → **53.97** EUR. 3 × 1999 JPY at 15 % = 5097.45 → **5097** JPY.

### 3.2 Line category

| Category | Meaning |
| --- | --- |
| `standard` | taxed at the standard rate of the applicable country |
| `reduced` | taxed at the reduced rate of the applicable country (food, books, …) |
| `zero` | taxable at a rate of 0 (it appears in `tax_by_rate` under key `"0"`) |
| `exempt` | outside the scope of tax: no tax, and it never appears in `tax_by_rate` |

## 4. Tax rates and tax treatment

### 4.1 Rate table (valid for every date in 2026)

Rates are percentages. The "key" column is the exact string used as a key in `tax_by_rate` (5.2).

| Country | EU member | Standard | Reduced |
| --- | --- | --- | --- |
| DE (Germany) | yes | 19 | 7 |
| FR (France) | yes | 20 | 5.5 |
| NL (Netherlands) | yes | 21 | 9 |
| GB (United Kingdom) | no | 20 | 5 |
| CH (Switzerland) | no | 8.1 | 2.6 |
| JP (Japan) | no | 10 | 8 |

The rate key is the percentage written exactly as in the table: `"19"`, `"7"`, `"20"`, `"5.5"`, `"21"`, `"9"`,
`"5"`, `"8.1"`, `"2.6"`, `"10"`, `"8"`, plus `"0"` for every zero-rated amount.

Buyers may be in any country (any two-letter code); only sellers are limited to the six above. A buyer is "in the
EU" when its country is DE, FR or NL.

### 4.2 Tax treatment

The treatment of an invoice depends only on the seller and the buyer. Evaluate the rules in order; the first that
matches applies.

| # | Condition | Treatment | Rate country / rate |
| --- | --- | --- | --- |
| 1 | buyer country == seller country | `domestic` | seller country's rates |
| 2 | seller in EU, buyer in EU (other country), buyer has a VAT id | `reverse_charge` | 0 for every taxable line |
| 3 | seller in EU, buyer in EU (other country), buyer has no VAT id | `distance_sale` | **buyer** country's rates |
| 4 | anything else (non-EU seller selling abroad, EU seller selling outside the EU) | `export` | 0 for every taxable line |

Under `domestic` and `distance_sale`, a `standard` line uses the standard rate of the rate country, a `reduced`
line its reduced rate, a `zero` line 0, and an `exempt` line is untaxed. Under `reverse_charge` and `export`,
`standard`, `reduced` and `zero` lines are all taxed at 0 (key `"0"`), and `exempt` lines stay untaxed.

Examples: DE seller → DE consumer: `domestic`, German rates. DE seller → FR business with VAT id:
`reverse_charge`. DE seller → FR consumer: `distance_sale`, French rates (20 / 5.5). DE seller → US anyone:
`export`. GB seller → FR anyone: `export`. CH seller → CH buyer: `domestic`, 8.1 / 2.6.

## 5. Tax amounts

### 5.1 Tax of one line

`line_tax = net × rate / 100`, rounded once (2.2), where `net` is the rounded line net (3.1) and `rate` comes from
section 4. An exempt line's tax is zero.

### 5.2 Tax of an invoice (per-rate rule)

Invoice tax is **not** the sum of line taxes. Group the lines by rate key (exempt lines are in no group). For each
group: `tax = (sum of the group's rounded line nets) × rate / 100`, rounded once. The invoice tax is the sum of the
group taxes. This can differ from the sum of `line_tax` values by a minor unit; invoices always use the per-rate
rule.

Example (DE domestic, EUR): three standard lines with nets 0.10, 0.10, 0.10. Line taxes 0.019 → 0.02 each (0.06
in total); invoice tax = 0.30 × 19 % = 0.057 → **0.06**. With nets 0.05, 0.05, 0.05: line taxes 0.0095 → 0.01
each (0.03), invoice tax 0.15 × 19 % = 0.0285 → **0.03**. With nets 1.05 and 1.05: line taxes 0.1995 → 0.20 each
(0.40), invoice tax 2.10 × 19 % = 0.399 → **0.40**. With nets 0.13, 0.13 and 0.13: line taxes 0.0247 → 0.02 each
(0.06), invoice tax 0.39 × 19 % = 0.0741 → **0.07**.

## 6. Payment terms and business days

### 6.1 Terms

| Terms | Raw due date |
| --- | --- |
| `DUE` | the issue date |
| `NET<n>` (n = 1…120, no leading zeros, e.g. `NET30`) | issue date + n calendar days |
| `EOM` | the last calendar day of the issue month |
| `EOM+<n>` (n = 1…120, e.g. `EOM+15`) | the last calendar day of the issue month + n calendar days |

Anything else (`NET0`, `NET030`, `net30`, `EOM+0`, `NET 30`, `NET121`, ...) raises.

### 6.2 Business days

A business day in a country is a Monday–Friday that is not a public holiday of that country in the table below.
Saturdays and Sundays are never business days. The table is complete for 2026; dates outside 2026 only skip
weekends.

| Country | Public holidays 2026 |
| --- | --- |
| DE | 01-01, 04-03, 04-06, 05-01, 05-14, 05-25, 10-03, 12-25, 12-26 |
| FR | 01-01, 04-06, 05-01, 05-08, 05-14, 05-25, 07-14, 08-15, 11-01, 11-11, 12-25 |
| NL | 01-01, 04-03, 04-06, 04-27, 05-14, 05-25, 12-25, 12-26 |
| GB | 01-01, 04-03, 04-06, 05-04, 05-25, 08-31, 12-25, 12-28 |
| CH | 01-01, 01-02, 04-03, 04-06, 05-14, 05-25, 08-01, 12-25, 12-26 |
| JP | 01-01, 01-12, 02-11, 02-23, 03-20, 04-29, 05-04, 05-05, 05-06, 07-20, 08-11, 09-21, 09-22, 09-23, 10-12, 11-03, 11-23 |

### 6.3 Due date

The due date is the raw due date (6.1) if that is a business day in the **seller's** country (6.2). Otherwise it
is the first business day after the raw due date, **even if that business day is in the next month or the next
year**. It is never moved backwards.

Examples (DE seller): issued 2026-05-04 with `EOM` → raw 2026-05-31 (Sunday) → due **2026-06-01**. Issued
2026-04-14 with `NET30` → raw 2026-05-14 (Ascension, a DE holiday) → due **2026-05-15**. Issued 2026-03-02 with
`NET5` → raw 2026-03-07 (Saturday) → due **2026-03-09**.

## 7. Late payment

A payment is late when `paid_date` is after the due date (6.3). `days_late = paid_date − due_date` in calendar
days; if that is 0 or negative the late fee is zero.

### 7.1 Statutory interest rate (annual, simple interest, by seller country)

| Seller | DE | FR | NL | GB | CH | JP |
| --- | --- | --- | --- | --- | --- | --- |
| Annual rate % | 9 | 11 | 8 | 8 | 5 | 3 |

### 7.2 Fee

`interest = gross_total × annual_rate / 100 × days_late / 365`, where `gross_total` is the invoice's `total` per
section 8.3 (tax included). In addition, a **flat compensation of 40** (in the invoice currency) is added when all
of these hold: the seller is in the EU, the buyer has a VAT id, and the invoice currency is EUR. The late fee is
`interest + flat`, rounded once (2.2) to the invoice currency. When not late, the fee is zero (no flat amount).

Example: DE seller, DE business buyer, EUR, total 1190.00, 10 days late: 1190 × 9 % × 10 / 365 = 2.934246… plus
40 = 42.934… → **42.93** EUR.

## 8. Functions

### 8.1 `line_net(line, currency) -> Decimal`
Section 3.1, after validating the line (1.1) and the currency (2.1).

### 8.2 `line_tax(line, seller, buyer, currency) -> Decimal`
The tax of one line (5.1) under the treatment of `seller`/`buyer` (4.2), in `currency`. Validates like `line_net`;
an unknown seller country raises.

### 8.3 `invoice_totals(invoice) -> dict`
Returns

```python
{
    "currency": "EUR",
    "treatment": "domestic",                  # 4.2
    "subtotal": Decimal,                      # sum of rounded line nets, all categories
    "tax_by_rate": {"19": Decimal, "7": Decimal},   # 5.2: one entry per rate key used by a non-exempt line
    "tax": Decimal,                           # sum of tax_by_rate values
    "total": Decimal,                         # subtotal + tax
}
```

`tax_by_rate` has exactly the keys used (a `zero` line or a `reverse_charge`/`export` invoice gives key `"0"` with
value zero; an invoice with only exempt lines has `{}`).

### 8.4 `convert(amount, from_ccy, to_ccy, rates) -> Decimal`
Section 2.3.

### 8.5 `due_date(issue_date, terms, country) -> str`
Section 6.3, with `country` the seller country (one of 4.1, else raises). Returns an ISO date string.

### 8.6 `credit_note(invoice, returns) -> dict`
A credit note reverses part of an invoice. `returns` is a non-empty list of `{"sku": str, "qty": int|str}`.

- Each returned `sku` must be on the invoice; each `qty` must be > 0; the total returned qty per sku (summed over
  `returns`) must not exceed the invoiced qty. Otherwise raises.
- Each return becomes a credit line priced like the original line (same unit price, discount and category):
  credit line net = **minus** the line net (3.1) of the returned qty, rounded once.
- Tax uses the original invoice's treatment (4.2) and the per-rate rule (5.2) over the credit lines; amounts are
  negative (rounding half away from zero, 2.2).

Returns

```python
{
    "currency": "EUR",
    "treatment": "domestic",
    "lines": [{"sku": "WIDGET-01", "qty": Decimal("1"), "net": Decimal("-17.99")}],   # in the order of `returns`
    "subtotal": Decimal,          # <= 0
    "tax_by_rate": {"19": Decimal},
    "tax": Decimal,               # <= 0
    "total": Decimal,             # <= 0
}
```

`qty` in a credit line is `Decimal(str(qty))`.

### 8.7 `late_fee(invoice, paid_date) -> Decimal`
Section 7, with the due date from section 6.3 (seller country calendar) and the gross total from 8.3.

## 9. Done means
`python3 -m pytest -q` passes. Only this SPEC defines behaviour.
