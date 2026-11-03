# Port Bench report

- Sample: 10 libraries × 1 trial(s) per harness.
- Ports that work (every original test passes, no rule broken): codex 10/10, heliod 10/10.
- Cost per passing test: heliod used 3.4× less money per passing test than codex (geometric mean over 10 libraries; per library a01_split_bill 3.7×, a02_parse_duration 3.6×, a03_leaderboard 3.5×, a04_phone 1.9×, a05_report_since 3.0×, a06_unique_slug 3.3×, a07_backoff 4.4×, a08_vat 3.7×, a09_format_size 3.7×, a10_bank_dates 3.7×).
- Tokens per passing test: heliod used 4.7× fewer tokens per passing test than codex (geometric mean over 10 libraries; per library a01_split_bill 4.2×, a02_parse_duration 6.3×, a03_leaderboard 5.6×, a04_phone 3.0×, a05_report_since 4.1×, a06_unique_slug 4.8×, a07_backoff 6.2×, a08_vat 4.3×, a09_format_size 5.0×, a10_bank_dates 4.9×).
- Billed cost: heliod used 3.4× less money than codex (geometric mean over 10 libraries; per library a01_split_bill 3.7×, a02_parse_duration 3.6×, a03_leaderboard 3.5×, a04_phone 1.9×, a05_report_since 3.0×, a06_unique_slug 3.3×, a07_backoff 4.4×, a08_vat 3.7×, a09_format_size 3.7×, a10_bank_dates 3.7×).
- Tokens: heliod used 4.7× fewer tokens than codex (geometric mean over 10 libraries; per library a01_split_bill 4.2×, a02_parse_duration 6.3×, a03_leaderboard 5.6×, a04_phone 3.0×, a05_report_since 4.1×, a06_unique_slug 4.8×, a07_backoff 6.2×, a08_vat 4.3×, a09_format_size 5.0×, a10_bank_dates 4.9×).

Billing audit: OpenRouter confirmed 128 of 128 metered calls ($0.0507 of $0.0507 metered), 0 served by a provider other than the pin.

## Per library (medians over trials)

| Library | Harness | Works | Tests passed | Billed ($, min-max) | Tokens (uncached in / out) | Minutes | $ per 100 passing tests | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a01_split_bill | codex | 1/1 | 100.0% | 0.003 (0.003-0.003) | 0.10M (17k / 1k) | 0.3 | 0.041 | 12050 |
| a01_split_bill | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.3 | 0.011 | 2846 |
| a02_parse_duration | codex | 1/1 | 100.0% | 0.005 (0.005-0.005) | 0.14M (19k / 3k) | 0.6 | 0.042 | 11340 |
| a02_parse_duration | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (5k / 1k) | 0.3 | 0.012 | 1789 |
| a03_leaderboard | codex | 1/1 | 100.0% | 0.004 (0.004-0.004) | 0.10M (17k / 1k) | 0.3 | 0.088 | 24356 |
| a03_leaderboard | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.3 | 0.025 | 4378 |
| a04_phone | codex | 1/1 | 100.0% | 0.005 (0.005-0.005) | 0.12M (20k / 3k) | 0.8 | 0.043 | 10191 |
| a04_phone | heliod | 1/1 | 100.0% | 0.003 (0.003-0.003) | 0.04M (8k / 3k) | 0.7 | 0.023 | 3437 |
| a05_report_since | codex | 1/1 | 100.0% | 0.003 (0.003-0.003) | 0.10M (17k / 1k) | 0.3 | 0.047 | 13708 |
| a05_report_since | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.2 | 0.016 | 3368 |
| a06_unique_slug | codex | 1/1 | 100.0% | 0.003 (0.003-0.003) | 0.10M (17k / 1k) | 0.2 | 0.066 | 19260 |
| a06_unique_slug | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.3 | 0.020 | 4020 |
| a07_backoff | codex | 1/1 | 100.0% | 0.004 (0.004-0.004) | 0.11M (17k / 1k) | 0.3 | 0.050 | 16034 |
| a07_backoff | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.2 | 0.011 | 2606 |
| a08_vat | codex | 1/1 | 100.0% | 0.003 (0.003-0.003) | 0.10M (17k / 1k) | 0.2 | 0.041 | 11971 |
| a08_vat | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.2 | 0.011 | 2808 |
| a09_format_size | codex | 1/1 | 100.0% | 0.004 (0.004-0.004) | 0.10M (18k / 3k) | 0.6 | 0.044 | 10056 |
| a09_format_size | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.3 | 0.012 | 2013 |
| a10_bank_dates | codex | 1/1 | 100.0% | 0.004 (0.004-0.004) | 0.10M (17k / 2k) | 0.4 | 0.041 | 10870 |
| a10_bank_dates | heliod | 1/1 | 100.0% | 0.001 (0.001-0.001) | 0.02M (4k / 1k) | 0.2 | 0.011 | 2235 |

## Ratios to Heliod (other / Heliod; above 1 means Heliod used less)

| Harness | Library | Cost | Tokens | Minutes | Cost per passing test | Tokens per passing test |
| --- | --- | --- | --- | --- | --- | --- |
| codex | a01_split_bill | 3.7× | 4.2× | 1.0× | 3.7× | 4.2× |
| codex | a02_parse_duration | 3.6× | 6.3× | 2.0× | 3.6× | 6.3× |
| codex | a03_leaderboard | 3.5× | 5.6× | 1.0× | 3.5× | 5.6× |
| codex | a04_phone | 1.9× | 3.0× | 1.1× | 1.9× | 3.0× |
| codex | a05_report_since | 3.0× | 4.1× | 1.5× | 3.0× | 4.1× |
| codex | a06_unique_slug | 3.3× | 4.8× | 0.7× | 3.3× | 4.8× |
| codex | a07_backoff | 4.4× | 6.2× | 1.5× | 4.4× | 6.2× |
| codex | a08_vat | 3.7× | 4.3× | 1.0× | 3.7× | 4.3× |
| codex | a09_format_size | 3.7× | 5.0× | 2.0× | 3.7× | 5.0× |
| codex | a10_bank_dates | 3.7× | 4.9× | 2.0× | 3.7× | 4.9× |
| codex | **all (geometric mean)** | 3.4× | 4.7× | 1.3× | 3.4× | 4.7× |

Source: <run>. Definitions at the top of report.mjs.
