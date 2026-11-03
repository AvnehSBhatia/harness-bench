# shipping · Heliod Harness

**Passed** · 48/48 test cases · $0.0131 billed · 0.8 min · 33 model calls · input 172,171 tokens (114,761 cached) · output 9,592 tokens

Stopped by: finished. Section: [Large fleet jobs](../../README.md).

| File | What it is |
| --- | --- |
| [transcript.md](transcript.md) | Every model call: what was sent, what came back, tokens, cost |
| [diff.patch](diff.patch) | Everything the agent changed |
| [grade.json](grade.json) | The grader's verdict, with any failing test names |
| [summary.json](summary.json) | The numbers on this page |
| [calls.jsonl.gz](calls.jsonl.gz) | The same calls as JSON, one per line |
| [events.jsonl.gz](events.jsonl.gz) | The harness's own event stream |
| [session/](session/) | The harness's session files |
| [fleet.json](fleet.json) | The fleet: its plan, agents, steps, messages and cost ledger |

## Agents

| Agent | Model calls | Input tokens (cached) | Output tokens | Cost |
| --- | --- | --- | --- | --- |
| main agent | 5 | 27,845 (20,273) | 796 | $0.0015 |
| worker w1·g1 (billable_weight) | 4 | 19,644 (13,446) | 813 | $0.0013 |
| worker w2·g1 (zone) | 2 | 9,456 (4,482) | 445 | $0.0009 |
| worker w3·g1 (base_rate) | 2 | 9,736 (4,482) | 736 | $0.0011 |
| worker w4·g1 (surcharges) | 4 | 21,008 (13,446) | 1,331 | $0.0017 |
| worker w5·g1 (quote) | 5 | 26,848 (17,928) | 2,736 | $0.0027 |
| worker w6·g1 (delivery_date) | 5 | 26,220 (17,928) | 1,249 | $0.0018 |
| worker w7·g1 (cheapest_option) | 6 | 31,414 (22,776) | 1,486 | $0.0021 |

## How Heliod split the work

Fleet run `r8xveh784`, done: Implement functions described in SPEC.md; each function in its starter file.

| Agent | Part | Steps | Cost |
| --- | --- | --- | --- |
| w1·g1 | billable_weight | 4 | $0.0013 |
| w2·g1 | zone | 2 | $0.0009 |
| w3·g1 | base_rate | 2 | $0.0011 |
| w4·g1 | surcharges | 4 | $0.0017 |
| w5·g1 | quote | 5 | $0.0027 |
| w6·g1 | delivery_date | 5 | $0.0018 |
| w7·g1 | cheapest_option | 5 | $0.0021 |

## Messages between agents

None in this run: no agent needed to tell another anything.

## Each agent's steps

- **w1·g1**: Read assigned file. Looked up read billable_weight.py (13 lines). → Implemented billable weight calculation. Edited billable_weight.py (1 change). Tests after the edit: 1 failing. → Corrected billable step calculation to ceiling semantics. Edited billable_weight.py (3 changes). → Billable weight implementation complete.
- **w2·g1**: Implemented zone selection. Wrote zone.py. → Zone task complete; 12 assigned tests passed.
- **w3·g1**: Added base_rate implementation. Wrote base_rate.py. → base_rate is complete; assigned tests pass.
- **w4·g1**: Read surcharge stub. Looked up read surcharges.py (14 lines). → Implemented surcharges per SPEC. Wrote surcharges.py. Tests after the write: 1 failing. → Fix remote surcharge detection for postcode prefix 59. Edited surcharges.py (1 change). → Surcharges complete; six assigned tests pass.
- **w5·g1**: Inspect quote.py stub. Looked up read quote.py (14 lines). → Added quote composition and exact Decimal total. Wrote quote.py. Tests after the write: 1 failing. → Corrected quote billable-weight rounding to always round upward to the next 0.5 kg step. Edit refused: no edits given for quote.py. → Fix billable weight rounding in quote. Edited quote.py (1 change). → Quote task complete.
- **w6·g1**: Read delivery_date.py. Looked up read delivery_date.py (13 lines). → Added delivery_date implementation per calendar and transit rules. Wrote delivery_date.py. Tests after the write: 1 failing. → Inspect delivery date logic. Looked up read delivery_date.py (50 lines). → Implement SWIFT Saturday delivery days while excluding Sundays and holidays. Edited delivery_date.py (1 change). → delivery_date implementation complete.
- **w7·g1**: Read cheapest_option.py starter. Looked up read cheapest_option.py (13 lines). → Added cheapest timely option selection. Wrote cheapest_option.py. Tests after the write: 4 failing. → Reading delivery calendar helper. Looked up read delivery_date.py (47 lines). → Adjusted timely-option filtering to count SWIFT Saturdays. Edited cheapest_option.py (2 changes). → cheapest_option complete; assigned tests pass.
