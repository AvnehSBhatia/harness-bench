# Parcel shipping — SPEC (source of truth)

You are building `shipping`, the quoting core of a parcel-shipping service that sells two carriers' services. It is
seven functions, one per file. Standard library only.

All seven depend on the same domain rules (sections 2–6): units and billable weight, zones, rate tables,
surcharges and the transit calendar. They are written once, here. "Per section N" means exactly the rule in
section N, with no additions.

## 0. Files and conventions

| File | Function |
| --- | --- |
| `billable_weight.py` | `billable_weight(parcel: dict, carrier: str) -> Decimal` |
| `zone.py` | `zone(origin: str, dest: str) -> int` |
| `base_rate.py` | `base_rate(carrier: str, service: str, zone: int, billable_kg: Decimal) -> Decimal` |
| `surcharges.py` | `surcharges(shipment: dict, carrier: str, service: str) -> dict` |
| `quote.py` | `quote(shipment: dict, carrier: str, service: str) -> dict` |
| `delivery_date.py` | `delivery_date(shipment: dict, carrier: str, service: str) -> str` |
| `cheapest_option.py` | `cheapest_option(shipment: dict, deadline: str) -> dict \| None` |

- Do not import one function file from another. Each file must work on its own.
- `rates_common.py` is a shared helper module maintained by the ops-platform team. You may import from it, but do
  not edit it. It is not part of this SPEC: where it and this SPEC differ, this SPEC is right.
- Money and weights are `decimal.Decimal`; never use `float`. Inputs given as int/str are read with
  `Decimal(str(x))`. Money is EUR, rounded to cents half-up (`ROUND_HALF_UP`) where this SPEC says "round".
- Errors: every "raises" means `ValueError`.

## 1. Data model

```python
parcel = {"length": 40, "width": 30, "height": 20, "weight": "3.2", "unit": "metric"}   # unit: "metric" | "imperial"
shipment = {
    "origin": "10115",            # 5-digit postcode (string)
    "dest": "80331",
    "parcel": parcel,
    "residential": False,         # optional, default False
    "ship_at": "2026-05-04T16:30",  # local date and time the parcel is handed over (ISO, minutes precision)
}
```

Carriers and services (the only valid combinations; anything else raises):

| Carrier | Services | Max billable weight |
| --- | --- | --- |
| `SWIFT` | `express`, `standard` | 30 kg |
| `TERRA` | `ground` | 50 kg |

## 2. Units and billable weight

### 2.1 Units
`metric`: dimensions in cm, weight in kg. `imperial`: dimensions in inches, weight in pounds. Convert imperial
exactly: 1 in = 2.54 cm, 1 lb = 0.45359237 kg. Do not round converted values. All dimensions and the weight must be
> 0, and `unit` must be one of the two values; otherwise raises.

### 2.2 Dimensional weight
`dim_kg = length_cm × width_cm × height_cm / divisor`, with divisor **5000 for SWIFT** and **6000 for TERRA**.

### 2.3 Billable weight
`raw = max(actual_kg, dim_kg)`. The billable weight is `raw` **rounded up to the next multiple of 0.5 kg**
(a value that already is a multiple of 0.5 stays as it is). So 2.01 → 2.5, 2.1 → 2.5, 2.5 → 2.5, 2.6 → 3.0,
0.2 → 0.5. A billable weight above the carrier's maximum (section 1) raises.

Example: 40 × 30 × 20 cm, 3.2 kg. SWIFT: dim 4.8 kg → billable **5.0**. TERRA: dim 4.0 kg → billable **4.0**.

## 3. Zones

Postcodes are strings of exactly 5 digits (`"01067"` is valid); anything else raises. For an origin `o` and a
destination `d`, the first matching rule gives the zone:

| # | Rule | Zone |
| --- | --- | --- |
| 1 | `d` starts with `96` or `97` (islands) | 6 |
| 2 | same first two digits | 1 |
| 3 | same first digit | 2 |
| 4 | first digits differ by 1 or 2 | 3 |
| 5 | first digits differ by 3, 4 or 5 | 4 |
| 6 | first digits differ by 6 or more | 5 |

Example: `10115` → `10117` zone 1; `10115` → `14467` zone 2; `10115` → `34117` zone 3; `10115` → `80331` zone 5;
`80331` → `97070` zone 6.

## 4. Base rate

`base = first + (steps − 1) × additional`, where `steps = billable_kg / 0.5` and `first`/`additional` come from
the table for the carrier, service and zone. Base is exact (cents already).

| Carrier / service | | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWIFT express | first 0.5 kg | 8.00 | 9.50 | 11.00 | 13.00 | 15.50 | 22.00 |
| | each additional 0.5 kg | 1.10 | 1.30 | 1.60 | 1.90 | 2.30 | 3.40 |
| SWIFT standard | first 0.5 kg | 5.50 | 6.20 | 7.10 | 8.30 | 9.60 | 14.00 |
| | each additional 0.5 kg | 0.70 | 0.85 | 1.00 | 1.20 | 1.45 | 2.20 |
| TERRA ground | first 0.5 kg | 4.20 | 4.80 | 5.40 | 6.30 | 7.20 | 12.00 |
| | each additional 0.5 kg | 0.45 | 0.55 | 0.70 | 0.85 | 1.00 | 1.80 |

`base_rate` raises for a zone outside 1–6, a billable weight that is not a positive multiple of 0.5, a weight
above the carrier maximum, or an invalid carrier/service.

Example: SWIFT express, zone 3, 5.0 kg: 10 steps → 11.00 + 9 × 1.60 = **25.40**.

## 5. Surcharges

Each surcharge is computed separately and rounded to cents. Only surcharges that apply are listed; names are
exactly the keys below.

| Key | Applies when | SWIFT | TERRA |
| --- | --- | --- | --- |
| `fuel` | always | 14.5 % of base | 9.25 % of base |
| `peak` | the ship date (date part of `ship_at`) is between 2026-11-23 and 2026-12-24, both inclusive | 6 % of base | 6 % of base |
| `oversize` | longest side > 120 cm, or length + 2 × (width + height) > 300 cm (using the parcel's own length/width/height in cm) | 25.00 | 18.00 |
| `remote` | the destination postcode's first two digits are one of **08, 29, 59, 64, 79, 96, 97** | 7.50 | 5.00 |
| `residential` | `shipment["residential"]` is true | 3.20 | 2.10 |

Percent surcharges are percentages of the base rate only (never of other surcharges).

## 6. Transit calendar

### 6.1 Network holidays (both carriers, 2026)
01-01, 04-03, 04-06, 05-01, 05-14, 05-25, 10-03, 12-25, 12-26.

### 6.2 Pickup day
A pickup day is a Monday–Friday that is not a network holiday. The pickup day of a shipment is the date of
`ship_at` if that is a pickup day **and** the time is strictly before the carrier's cutoff (SWIFT 18:00, TERRA 16:00);
otherwise it is the next pickup day after that date.

### 6.3 Delivery days
**SWIFT delivers Monday–Saturday; TERRA delivers Monday–Friday.** Neither delivers on Sundays or network holidays.

### 6.4 Transit days (by service and zone)

| Service | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 |
| --- | --- | --- | --- | --- | --- | --- |
| express | 1 | 1 | 1 | 1 | 2 | 3 |
| standard | 2 | 2 | 3 | 3 | 4 | 5 |
| ground | 2 | 3 | 4 | 5 | 6 | 8 |

The delivery date is reached by starting at the pickup day and advancing one calendar day at a time, counting
only the carrier's delivery days (6.3), until `transit` days have been counted. The pickup day itself is never
counted.

Example: SWIFT express, zone 3, `ship_at` Thursday 2026-03-05 17:59 → pickup Thu 03-05 → delivered **Fri 03-06**.
At 18:00 → pickup Fri 03-06 → delivered **Sat 03-07**. TERRA ground, zone 1, Thursday 2026-03-05 10:00 → pickup
03-05 → **Mon 03-09**.

## 7. Functions

### 7.1 `billable_weight(parcel, carrier) -> Decimal`
Section 2 (raises for an unknown carrier).

### 7.2 `zone(origin, dest) -> int`
Section 3.

### 7.3 `base_rate(carrier, service, zone, billable_kg) -> Decimal`
Section 4.

### 7.4 `surcharges(shipment, carrier, service) -> dict[str, Decimal]`
Section 5 for this shipment, with the base rate from sections 2–4. Keys only for surcharges that apply.

### 7.5 `quote(shipment, carrier, service) -> dict`
```python
{"carrier": "SWIFT", "service": "express", "zone": 3, "billable_kg": Decimal("5.0"),
 "base": Decimal("25.40"), "surcharges": {"fuel": Decimal("3.68")}, "total": Decimal("29.08")}
```
`total = base + sum(surcharges)`.

### 7.6 `delivery_date(shipment, carrier, service) -> str`
Section 6, with the zone from section 3. ISO date string.

### 7.7 `cheapest_option(shipment, deadline) -> dict | None`
Consider the three carrier/service combinations of section 1. Skip a combination whose billable weight exceeds
its carrier maximum. Keep those whose delivery date (7.6) is on or before `deadline` (ISO date). Return the one with
the lowest `total` (7.5); ties go to the earlier delivery date, then to the alphabetically first `(carrier, service)`.

```python
{"carrier": "TERRA", "service": "ground", "total": Decimal("12.34"), "delivery_date": "2026-03-09"}
```
Return `None` when no combination qualifies.

## 8. Done means
`python3 -m pytest -q` passes. Only this SPEC defines behaviour.
