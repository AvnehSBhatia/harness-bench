# Port Bench report

- Sample: 6 libraries × 1 trial(s) per harness.
- Ports that work (every original test passes, no rule broken): codex 6/6, heliod 6/6.
- Cost per passing test: heliod used 2.8× less money per passing test than codex (geometric mean over 6 libraries; per library affine-cipher 4.0×, beer-song 3.6×, book-store 4.1×, bottle-song 3.7×, bowling 0.8×, connect 3.1×).
- Tokens per passing test: heliod used 4.5× fewer tokens per passing test than codex (geometric mean over 6 libraries; per library affine-cipher 7.3×, beer-song 5.9×, book-store 8.2×, bottle-song 6.5×, bowling 0.9×, connect 4.0×).
- Billed cost: heliod used 2.8× less money than codex (geometric mean over 6 libraries; per library affine-cipher 4.0×, beer-song 3.6×, book-store 4.1×, bottle-song 3.7×, bowling 0.8×, connect 3.1×).
- Tokens: heliod used 4.5× fewer tokens than codex (geometric mean over 6 libraries; per library affine-cipher 7.3×, beer-song 5.9×, book-store 8.2×, bottle-song 6.5×, bowling 0.9×, connect 4.0×).

Billing audit: OpenRouter confirmed 115 of 115 metered calls ($0.0542 of $0.0542 metered), 0 served by a provider other than the pin.

## Per library (medians over trials)

| Library | Harness | Works | Tests passed | Billed ($, min-max) | Tokens (uncached in / out) | Minutes | $ per 100 passing tests | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| affine-cipher | codex | 1/1 | 100.0% | 0.005 (0.005-0.005) | 0.18M (19k / 2k) | 0.5 | 0.030 | 11133 |
| affine-cipher | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (5k / 1k) | 0.2 | 0.007 | 1530 |
| beer-song | codex | 1/1 | 100.0% | 0.007 (0.007-0.007) | 0.31M (26k / 3k) | 0.8 | 0.094 | 39371 |
| beer-song | heliod | 1/1 | 100.0% | 0.002 (0.002-0.002) | 0.05M (11k / 1k) | 0.3 | 0.026 | 6655 |
| book-store | codex | 1/1 | 100.0% | 0.005 (0.005-0.005) | 0.18M (19k / 2k) | 0.5 | 0.025 | 8896 |
| book-store | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (5k / 1k) | 0.2 | 0.006 | 1079 |
| bottle-song | codex | 1/1 | 100.0% | 0.006 (0.006-0.006) | 0.26M (22k / 2k) | 0.5 | 0.090 | 37426 |
| bottle-song | heliod | 1/1 | 100.0% | 0.002 (0.002-0.002) | 0.04M (8k / 1k) | 0.3 | 0.024 | 5726 |
| bowling | codex | 1/1 | 100.0% | 0.007 (0.007-0.007) | 0.25M (25k / 4k) | 0.8 | 0.024 | 8060 |
| bowling | heliod | 1/1 | 100.0% | 0.009 (0.009-0.009) | 0.29M (38k / 4k) | 1.0 | 0.030 | 9313 |
| connect | codex | 1/1 | 100.0% | 0.004 (0.004-0.004) | 0.12M (19k / 2k) | 0.5 | 0.044 | 11973 |
| connect | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.03M (5k / 1k) | 0.3 | 0.014 | 2970 |

## Ratios to Heliod (other / Heliod; above 1 means Heliod used less)

| Harness | Library | Cost | Tokens | Minutes | Cost per passing test | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- |
| codex | affine-cipher | 4.0× | 7.3× | 2.5× | 4.0× | 7.3× |
| codex | beer-song | 3.6× | 5.9× | 2.7× | 3.6× | 5.9× |
| codex | book-store | 4.1× | 8.2× | 2.5× | 4.1× | 8.2× |
| codex | bottle-song | 3.7× | 6.5× | 1.7× | 3.7× | 6.5× |
| codex | bowling | 0.8× | 0.9× | 0.8× | 0.8× | 0.9× |
| codex | connect | 3.1× | 4.0× | 1.7× | 3.1× | 4.0× |
| codex | **all (geometric mean)** | 2.8× | 4.5× | 1.8× | 2.8× | 4.5× |

Source: results/2026-11-03T02-12-28-514Z-quick. Definitions at the top of report.mjs.
