# billing_platform · Heliod Harness

**Passed** · 96/96 test cases · $0.0198 billed · 1.3 min · 37 model calls · input 233,732 tokens (138,415 cached) · output 13,027 tokens

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
| main agent | 4 | 28,183 (19,217) | 1,117 | $0.0019 |
| worker w1·g1 (parse_amount) | 2 | 12,101 (5,660) | 737 | $0.0012 |
| worker w2·g1 (parse_usage) | 2 | 11,981 (5,660) | 617 | $0.0012 |
| worker w3·g1 (aggregate_usage) | 2 | 12,088 (5,660) | 737 | $0.0012 |
| worker w4·g1 (rated_usage) | 4 | 24,458 (16,980) | 973 | $0.0016 |
| worker w5·g1 (convert) | 2 | 11,838 (5,660) | 511 | $0.0011 |
| worker w6·g1 (line_tax) | 2 | 11,873 (5,660) | 504 | $0.0011 |
| worker w7·g1 (prorate) | 2 | 11,868 (5,660) | 467 | $0.0011 |
| worker w8·g1 (due_date) | 2 | 11,873 (5,660) | 428 | $0.0010 |
| worker w9·g1 (build_invoice) | 3 | 19,326 (11,320) | 2,174 | $0.0022 |
| worker w10·g1 (apply_credits) | 2 | 12,237 (5,660) | 849 | $0.0013 |
| worker w11·g1 (reconcile) | 4 | 24,825 (16,980) | 1,344 | $0.0018 |
| worker w12·g1 (aging_report) | 6 | 41,081 (28,638) | 2,569 | $0.0031 |

## How Heliod split the work

Fleet run `rooo58y0f`, done: Implement the functions described in SPEC.md. Functions: parse_amount, parse_usage, aggregate_usage, rated_usage, convert, line_tax, prorate, due_date, build_invoice, apply_credits, reconcile, aging_report.

| Agent | Part | Steps | Cost |
| --- | --- | --- | --- |
| w1·g1 | parse_amount | 2 | $0.0012 |
| w2·g1 | parse_usage | 2 | $0.0012 |
| w3·g1 | aggregate_usage | 2 | $0.0012 |
| w4·g1 | rated_usage | 4 | $0.0016 |
| w5·g1 | convert | 2 | $0.0011 |
| w6·g1 | line_tax | 2 | $0.0011 |
| w7·g1 | prorate | 2 | $0.0011 |
| w8·g1 | due_date | 2 | $0.0010 |
| w9·g1 | build_invoice | 3 | $0.0022 |
| w10·g1 | apply_credits | 2 | $0.0013 |
| w11·g1 | reconcile | 4 | $0.0018 |
| w12·g1 | aging_report | 5 | $0.0031 |

## Messages between agents

None in this run: no agent needed to tell another anything.

## Each agent's steps

- **w1·g1**: Added section 3 amount parser. Wrote parse_amount.py. → parse_amount complete.
- **w2·g1**: Added section 4 usage-line parsing. Wrote parse_usage.py. → parse_usage complete; 8 assigned tests passed.
- **w3·g1**: Added aggregate_usage implementation. Wrote aggregate_usage.py. → aggregate_usage is implemented and assigned tests pass.
- **w4·g1**: Reading assigned file. Looked up read rated_usage.py (13 lines). → Implement rated_usage per section 6. Edited rated_usage.py (1 change). Tests after the edit: 1 failing. → Align rated usage rounding with half-even spec. Edited rated_usage.py (3 changes). → rated_usage complete; assigned tests pass.
- **w5·g1**: Implemented convert.py per section 7. Wrote convert.py. → convert.py is complete; all 8 assigned tests pass.
- **w6·g1**: Implemented section 8 tax calculation. Wrote line_tax.py. → line_tax completed; assigned tests pass.
- **w7·g1**: Added section 9 proration implementation. Wrote prorate.py. → Proration subtask complete.
- **w8·g1**: Implemented due-date calculation with weekend adjustment. Wrote due_date.py. → Due-date implementation complete.
- **w9·g1**: Reading build_invoice.py. Looked up read build_invoice.py (13 lines). → Invoice builder implemented per section 11. Wrote build_invoice.py. → Completed build_invoice per section 11.
- **w10·g1**: Added section 12 credit application behavior. Wrote apply_credits.py. → apply_credits complete.
- **w11·g1**: Checking available local helper APIs before writing reconcile. Wrote reconcile.py. Tests after the write: 1 failing. → Read reconcile implementation. Looked up read reconcile.py (4 lines). → Implement reconciliation and parse stored amount text locally. Edited reconcile.py (1 change). → Reconcile complete; assigned tests pass.
- **w12·g1**: Read assigned file. Looked up read aging_report.py (13 lines). → Aging report implemented; tests not yet run. Wrote aging_report.py. Tests after the write: 1 failing. → Read aging report implementation. Looked up read aging_report.py (74 lines). → Apply weekend adjustment to invoice due dates per SPEC. Edited aging_report.py (1 change). → Aging report implementation passes its assigned test suite.
