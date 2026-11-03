# Harness Bench report

- Sample: 5 libraries × 1 trial(s) per harness.
- Ports that work (every original test passes, no rule broken): heliod-private 5/5.

Billing audit: OpenRouter confirmed 212 of 212 metered calls ($0.0987 of $0.0987 metered), 0 served by a provider other than the pin.

## Per library (medians over trials)

| Library | Harness | Works | Tests passed | Billed ($, min-max) | Tokens (uncached in / out) | Minutes | $ per 100 passing tests | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| billing_platform | heliod-private | 1/1 | 100.0% | 0.025 (0.025-0.025) | 0.29M (129k / 14k) | 1.0 | 0.026 | 3052 |
| invoicing | heliod-private | 1/1 | 100.0% | 0.022 (0.022-0.022) | 0.36M (111k / 11k) | 1.1 | 0.032 | 5229 |
| longrun | heliod-private | 1/1 | 100.0% | 0.010 (0.010-0.010) | 0.20M (19k / 11k) | 1.7 | 0.025 | 5063 |
| pricing | heliod-private | 1/1 | 100.0% | 0.025 (0.025-0.025) | 0.48M (100k / 19k) | 2.2 | 0.067 | 12723 |
| shipping | heliod-private | 1/1 | 100.0% | 0.017 (0.017-0.017) | 0.22M (75k / 13k) | 0.9 | 0.036 | 4635 |

## Ratios to Heliod (other / Heliod; above 1 means Heliod used less)

| Harness | Library | Cost | Tokens | Minutes | Cost per passing test | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- |
| heliod-private | **all (geometric mean)** | - | - | - | - | - |

Source: <run>. Definitions at the top of report.mjs.
