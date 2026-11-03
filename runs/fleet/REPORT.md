# Port Bench report

- Sample: 5 libraries × 1 trial(s) per harness.
- Ports that work (every original test passes, no rule broken): codex 4/5, heliod 5/5.
- Cost per passing test: heliod used 1.5× less money per passing test than codex (geometric mean over 5 libraries; per library billing_platform 1.3×, invoicing 2.1×, pricing 1.6×, shipping 1.2×, longrun 1.4×).
- Tokens per passing test: heliod used 3.1× fewer tokens per passing test than codex (geometric mean over 5 libraries; per library billing_platform 3.8×, invoicing 4.7×, pricing 3.5×, shipping 3.6×, longrun 1.2×).
- Billed cost: heliod used 1.5× less money than codex (geometric mean over 5 libraries; per library billing_platform 1.2×, invoicing 2.1×, pricing 1.6×, shipping 1.2×, longrun 1.4×).
- Tokens: heliod used 3.0× fewer tokens than codex (geometric mean over 5 libraries; per library billing_platform 3.6×, invoicing 4.7×, pricing 3.5×, shipping 3.6×, longrun 1.2×).

Billing audit: OpenRouter confirmed 240 of 255 metered calls ($0.1624 of $0.1770 metered), 0 served by a provider other than the pin.

## Per library (medians over trials)

| Library | Harness | Works | Tests passed | Billed ($, min-max) | Tokens (uncached in / out) | Minutes | $ per 100 passing tests | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| billing_platform | codex | 0/1 | 93.8% | 0.024 (0.024-0.024) | 0.88M (53k / 19k) | 3.9 | 0.027 | 9813 |
| billing_platform | heliod | 1/1 | 100.0% | 0.020 (0.020-0.020) | 0.25M (95k / 13k) | 1.3 | 0.021 | 2570 |
| invoicing | codex | 1/1 | 100.0% | 0.030 (0.030-0.030) | 0.99M (63k / 27k) | 4.6 | 0.044 | 14544 |
| invoicing | heliod | 1/1 | 100.0% | 0.015 (0.015-0.015) | 0.21M (72k / 9k) | 0.8 | 0.021 | 3094 |
| longrun | codex | 1/1 | 100.0% | 0.015 (0.015-0.015) | 0.28M (37k / 15k) | 2.4 | 0.036 | 6956 |
| longrun | heliod | 1/1 | 100.0% | 0.011 (0.011-0.011) | 0.23M (22k / 12k) | 2.1 | 0.026 | 5864 |
| pricing | codex | 1/1 | 100.0% | 0.021 (0.021-0.021) | 0.68M (49k / 17k) | 3.0 | 0.054 | 17796 |
| pricing | heliod | 1/1 | 100.0% | 0.013 (0.013-0.013) | 0.20M (57k / 9k) | 1.0 | 0.034 | 5151 |
| shipping | codex | 1/1 | 100.0% | 0.016 (0.016-0.016) | 0.66M (34k / 12k) | 2.2 | 0.034 | 13734 |
| shipping | heliod | 1/1 | 100.0% | 0.013 (0.013-0.013) | 0.18M (57k / 10k) | 0.8 | 0.027 | 3787 |

## Ratios to Heliod (other / Heliod; above 1 means Heliod used less)

| Harness | Library | Cost | Tokens | Minutes | Cost per passing test | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- |
| codex | billing_platform | 1.2× | 3.6× | 3.0× | 1.3× | 3.8× |
| codex | invoicing | 2.1× | 4.7× | 5.7× | 2.1× | 4.7× |
| codex | pricing | 1.6× | 3.5× | 3.0× | 1.6× | 3.5× |
| codex | shipping | 1.2× | 3.6× | 2.8× | 1.2× | 3.6× |
| codex | longrun | 1.4× | 1.2× | 1.1× | 1.4× | 1.2× |
| codex | **all (geometric mean)** | 1.5× | 3.0× | 2.8× | 1.5× | 3.1× |

Source: <run>. Definitions at the top of report.mjs.
