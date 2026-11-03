| Library | Model | Harness | Trial | Works | Tests passed | Time (min) | Billed ($) | Input / cached / output tokens | Stopped by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| billing_platform | openai/gpt-6-luna | codex | 1 | no | 90/96 | 3.9 | 0.0242 | 0.86M / 0.81M / 19k | finished |
| billing_platform | openai/gpt-6-luna | heliod | 1 | yes | 96/96 | 1.3 | 0.0198 | 0.23M / 0.14M / 13k | finished |
| invoicing | openai/gpt-6-luna | heliod | 1 | yes | 68/68 | 0.8 | 0.0145 | 0.20M / 0.13M / 9k | finished |
| invoicing | openai/gpt-6-luna | codex | 1 | yes | 68/68 | 4.6 | 0.0301 | 0.96M / 0.90M / 27k | finished |
| pricing | openai/gpt-6-luna | codex | 1 | yes | 38/38 | 3 | 0.0207 | 0.66M / 0.61M / 17k | finished |
| pricing | openai/gpt-6-luna | heliod | 1 | yes | 38/38 | 1 | 0.0131 | 0.19M / 0.13M / 9k | finished |
| shipping | openai/gpt-6-luna | heliod | 1 | yes | 48/48 | 0.8 | 0.0131 | 0.17M / 0.11M / 10k | finished |
| shipping | openai/gpt-6-luna | codex | 1 | yes | 48/48 | 2.2 | 0.0162 | 0.65M / 0.61M / 12k | finished |
| longrun | openai/gpt-6-luna | codex | 1 | yes | 40/40 | 2.4 | 0.0146 | 0.26M / 0.23M / 15k | finished |
| longrun | openai/gpt-6-luna | heliod | 1 | yes | 40/40 | 2.1 | 0.0106 | 0.22M / 0.20M / 12k | finished |

| Task | Harness | T1-10 done / rules kept | T11-20 done / rules kept | T21-30 done / rules kept | T31-40 done / rules kept |
| --- | --- | --- | --- | --- | --- |
| longrun | codex | 10/10, 100% | 10/10, 100% | 10/10, 100% | 10/10, 100% |
| longrun | heliod | 10/10, 100% | 10/10, 100% | 10/10, 100% | 10/10, 100% |

codex-cli 0.157.1; Heliod Harness heliod 0.1.14; reasoning medium.
