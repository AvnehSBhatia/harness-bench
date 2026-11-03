# Codex vs Heliod on GPT-6 Luna

Harnesses: codex-cli 0.157.1 and Heliod Harness heliod 0.1.14. Model: openai/gpt-6-luna through OpenRouter, pinned to the OpenAI provider, the same one-line prompt; both main agents at medium reasoning (Heliod's fleet workers ask for low reasoning, a harness choice). Costs are what OpenRouter billed for each call (checked call by call in each run's AUDIT.md).

## All sections

| Section | Harness | Tasks passed | Test cases passed | Billed | $ per passed task | Output tokens (reasoning) | Input tokens (cached) | Time, total (median per task) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Large fleet jobs | codex | 4/5 | 284/290 | $0.106 | $0.0264 | 89,561 (37,609) | 3,396,373 (3,161,215) | 16.1 min (3) |
| Large fleet jobs | heliod | 5/5 | 290/290 | $0.071 | $0.0142 | 52,442 (3,843) | 1,016,715 (713,784) | 6.0 min (1) |
| Ambiguous specs | codex | 10/10 | 82/82 | $0.038 | $0.0039 | 16,138 (8,399) | 1,034,725 (859,408) | 4.0 min (0.3) |
| Ambiguous specs | heliod | 10/10 | 82/82 | $0.012 | $0.0012 | 9,911 (4,268) | 217,684 (174,245) | 3.0 min (0.3) |
| Quick tasks | codex | 6/6 | 92/92 | $0.035 | $0.0059 | 14,731 (6,100) | 1,287,840 (1,157,837) | 3.6 min (0.5) |
| Quick tasks | heliod | 6/6 | 92/92 | $0.017 | $0.0028 | 8,439 (3,575) | 449,349 (376,915) | 2.3 min (0.3) |

## Overall

| Harness | Tasks passed | Test cases passed | Billed | $ per passed task | Output tokens (reasoning) | Input tokens (cached) | Time, total (median per task) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| codex | 20/21 | 458/464 | $0.180 | $0.0090 | 120,430 (52,108) | 5,718,938 (5,178,460) | 23.7 min (0.5) |
| heliod | 21/21 | 464/464 | $0.100 | $0.0048 | 70,792 (11,686) | 1,683,748 (1,264,944) | 11.3 min (0.3) |

Codex / Heliod: billed 1.8x, output tokens 1.7x, input tokens 3.4x, time 2.1x; tasks passed 20 vs 21.

## Head to head, task by task

Counts over the tasks both harnesses attempted. A tie counts for neither.

| Section | Tasks | More cases passed (Codex / Heliod) | Cheaper | Faster | Fewer output tokens |
| --- | --- | --- | --- | --- | --- |
| Large fleet jobs | 5 | 0 / 1 | 0 / 5 | 0 / 5 | 0 / 5 |
| Ambiguous specs | 10 | 0 / 0 | 0 / 10 | 1 / 6 | 0 / 10 |
| Quick tasks | 6 | 0 / 0 | 1 / 5 | 1 / 5 | 1 / 5 |

## Large fleet jobs, with every Heliod check on the task's own model

Heliod normally sends its checks (is this agent's work right?) to Heliod's hosted checker, which is free and so not in the bills above. This run repeats the section with `heliod --private-checks`: every check runs on GPT-6 Luna through the same meter, so the bill is the whole cost.

| Harness | Tasks passed | Test cases passed | Billed | $ per passed task | Output tokens (reasoning) | Input tokens (cached) | Time, total (median per task) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| codex | 4/5 | 284/290 | $0.106 | $0.0264 | 89,561 (37,609) | 3,396,373 (3,161,215) | 16.1 min (3) |
| heliod (hosted checks) | 5/5 | 290/290 | $0.071 | $0.0142 | 52,442 (3,843) | 1,016,715 (713,784) | 6.0 min (1) |
| heliod --private-checks | 5/5 | 290/290 | $0.099 | $0.0197 | 67,930 (8,908) | 1,489,115 (1,055,796) | 6.9 min (1.1) |

## Every attempt

| Section | Task | Harness | Passed | Cases | Billed | Input tokens (cached) | Output tokens (reasoning) | Hosted checks | Minutes | Stopped by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Large fleet jobs | billing_platform | codex | no | 90/96 | $0.0242 | 864,286 (811,603) | 18,906 (7,766) | - | 3.9 | finished |
| Large fleet jobs | billing_platform | heliod | yes | 96/96 | $0.0198 | 233,732 (138,415) | 13,027 (169) | 13 | 1.3 | finished |
| Large fleet jobs | invoicing | heliod | yes | 68/68 | $0.0145 | 201,849 (129,958) | 8,525 (219) | 9 | 0.8 | finished |
| Large fleet jobs | invoicing | codex | yes | 68/68 | $0.0301 | 962,442 (899,737) | 26,566 (12,090) | - | 4.6 | finished |
| Large fleet jobs | pricing | codex | yes | 38/38 | $0.0207 | 659,157 (610,495) | 17,098 (7,057) | - | 3 | finished |
| Large fleet jobs | pricing | heliod | yes | 38/38 | $0.0131 | 186,240 (129,556) | 9,481 (248) | 10 | 1 | finished |
| Large fleet jobs | shipping | heliod | yes | 48/48 | $0.0131 | 172,171 (114,761) | 9,592 (168) | 13 | 0.8 | finished |
| Large fleet jobs | shipping | codex | yes | 48/48 | $0.0162 | 647,611 (613,653) | 11,623 (4,351) | - | 2.2 | finished |
| Large fleet jobs | longrun | codex | yes | 40/40 | $0.0146 | 262,877 (225,727) | 15,368 (6,345) | - | 2.4 | finished |
| Large fleet jobs | longrun | heliod | yes | 40/40 | $0.0106 | 222,723 (201,094) | 11,817 (3,039) | 0 | 2.1 | finished |
| Ambiguous specs | a01_split_bill | codex | yes | 8/8 | $0.0033 | 95,500 (78,698) | 903 (343) | - | 0.3 | finished |
| Ambiguous specs | a01_split_bill | heliod | yes | 8/8 | $0.0009 | 22,243 (18,490) | 526 (157) | 0 | 0.3 | finished |
| Ambiguous specs | a02_parse_duration | heliod | yes | 12/12 | $0.0014 | 20,162 (15,448) | 1,302 (586) | 0 | 0.3 | finished |
| Ambiguous specs | a02_parse_duration | codex | yes | 12/12 | $0.0050 | 133,139 (114,043) | 2,944 (1,664) | - | 0.6 | finished |
| Ambiguous specs | a03_leaderboard | codex | yes | 4/4 | $0.0035 | 96,282 (79,127) | 1,143 (495) | - | 0.3 | finished |
| Ambiguous specs | a03_leaderboard | heliod | yes | 4/4 | $0.0010 | 16,742 (12,676) | 771 (380) | 0 | 0.3 | finished |
| Ambiguous specs | a04_phone | heliod | yes | 12/12 | $0.0028 | 38,251 (30,495) | 2,987 (1,867) | 0 | 0.7 | finished |
| Ambiguous specs | a04_phone | codex | yes | 12/12 | $0.0052 | 118,854 (98,985) | 3,441 (2,154) | - | 0.8 | finished |
| Ambiguous specs | a05_report_since | codex | yes | 7/7 | $0.0033 | 95,162 (78,314) | 797 (85) | - | 0.3 | finished |
| Ambiguous specs | a05_report_since | heliod | yes | 7/7 | $0.0011 | 22,891 (18,589) | 682 (67) | 0 | 0.2 | finished |
| Ambiguous specs | a06_unique_slug | heliod | yes | 5/5 | $0.0010 | 19,354 (15,620) | 746 (192) | 0 | 0.3 | finished |
| Ambiguous specs | a06_unique_slug | codex | yes | 5/5 | $0.0033 | 95,393 (78,614) | 906 (369) | - | 0.2 | finished |
| Ambiguous specs | a07_backoff | codex | yes | 7/7 | $0.0035 | 111,317 (94,584) | 924 (236) | - | 0.3 | finished |
| Ambiguous specs | a07_backoff | heliod | yes | 7/7 | $0.0008 | 17,725 (14,186) | 516 (59) | 0 | 0.2 | finished |
| Ambiguous specs | a08_vat | heliod | yes | 8/8 | $0.0009 | 21,894 (18,132) | 566 (127) | 0 | 0.2 | finished |
| Ambiguous specs | a08_vat | codex | yes | 8/8 | $0.0033 | 94,941 (78,356) | 824 (205) | - | 0.2 | finished |
| Ambiguous specs | a09_format_size | codex | yes | 10/10 | $0.0044 | 97,893 (79,688) | 2,668 (1,908) | - | 0.6 | finished |
| Ambiguous specs | a09_format_size | heliod | yes | 10/10 | $0.0012 | 19,041 (15,083) | 1,085 (665) | 0 | 0.3 | finished |
| Ambiguous specs | a10_bank_dates | heliod | yes | 9/9 | $0.0010 | 19,381 (15,526) | 730 (168) | 0 | 0.2 | finished |
| Ambiguous specs | a10_bank_dates | codex | yes | 9/9 | $0.0037 | 96,244 (78,999) | 1,588 (940) | - | 0.4 | finished |
| Quick tasks | affine-cipher | codex | yes | 16/16 | $0.0048 | 176,584 (157,170) | 1,537 (476) | - | 0.5 | finished |
| Quick tasks | affine-cipher | heliod | yes | 16/16 | $0.0012 | 23,813 (18,372) | 672 (123) | 0 | 0.2 | finished |
| Quick tasks | beer-song | heliod | yes | 8/8 | $0.0021 | 52,642 (41,645) | 598 (61) | 0 | 0.3 | finished |
| Quick tasks | beer-song | codex | yes | 8/8 | $0.0075 | 312,243 (286,369) | 2,725 (1,315) | - | 0.8 | finished |
| Quick tasks | book-store | codex | yes | 20/20 | $0.0049 | 176,106 (156,684) | 1,815 (719) | - | 0.5 | finished |
| Quick tasks | book-store | heliod | yes | 20/20 | $0.0012 | 20,764 (15,326) | 806 (342) | 0 | 0.2 | finished |
| Quick tasks | bottle-song | heliod | yes | 7/7 | $0.0017 | 39,305 (31,703) | 780 (125) | 0 | 0.3 | finished |
| Quick tasks | bottle-song | codex | yes | 7/7 | $0.0063 | 259,670 (237,620) | 2,310 (851) | - | 0.5 | finished |
| Quick tasks | bowling | codex | yes | 31/31 | $0.0074 | 245,612 (220,898) | 4,236 (1,655) | - | 0.8 | finished |
| Quick tasks | bowling | heliod | yes | 31/31 | $0.0094 | 284,235 (246,330) | 4,475 (2,495) | 0 | 1 | finished |
| Quick tasks | connect | heliod | yes | 10/10 | $0.0014 | 28,590 (23,539) | 1,108 (429) | 0 | 0.3 | finished |
| Quick tasks | connect | codex | yes | 10/10 | $0.0044 | 117,625 (99,096) | 2,108 (1,084) | - | 0.5 | finished |
| fleet-private | billing_platform | heliod-private | yes | 96/96 | $0.0246 | 279,067 (149,883) | 13,886 (107) | - | 1 | finished |
| fleet-private | invoicing | heliod-private | yes | 68/68 | $0.0217 | 344,424 (233,846) | 11,175 (329) | - | 1.1 | finished |
| fleet-private | pricing | heliod-private | yes | 38/38 | $0.0255 | 464,833 (364,704) | 18,656 (4,721) | - | 2.2 | finished |
| fleet-private | shipping | heliod-private | yes | 48/48 | $0.0171 | 209,667 (135,014) | 12,807 (481) | - | 0.9 | finished |
| fleet-private | longrun | heliod-private | yes | 40/40 | $0.0098 | 191,124 (172,349) | 11,406 (3,270) | - | 1.7 | finished |
