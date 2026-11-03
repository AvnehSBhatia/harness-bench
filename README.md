# Harness Bench

Codex CLI and Heliod Harness on the same model, with the same one-line prompt, on the same 21 coding tasks, graded
by tests neither agent saw. Every model call either agent made is in this repo, and OpenRouter confirmed every one.

## Result

GPT-6 Luna through OpenRouter, one attempt per task, November 2, 2026.

| | Codex CLI 0.157.1 | Heliod Harness 0.1.14 | |
| --- | --- | --- | --- |
| Tasks passed | 20 of 21 | **21 of 21** | |
| Hidden test cases passed | 458 of 464 | **464 of 464** | |
| Billed by OpenRouter | $0.180 | **$0.100** | 44% less |
| Wall time | 23.7 min | **11.3 min** | 2.1x faster |
| Input tokens | 5.72M | **1.68M** | 3.4x fewer |
| Output tokens (of which reasoning) | 120k (52k) | **71k (12k)** | 1.7x fewer |

Task by task, Heliod cost less on 20 of 21 and finished first on 16 (Codex first on 2, 3 tied). Codex passed more
test cases than Heliod on none.

| Section | Tasks | Passed (Codex / Heliod) | Billed (Codex / Heliod) | Time (Codex / Heliod) |
| --- | --- | --- | --- | --- |
| [Large fleet jobs](runs/fleet/README.md) | 5 | 4 / **5** | $0.106 / **$0.071** | 16.1 / **6.0** min |
| [Ambiguous specs](runs/ambiguous/README.md) | 10 | 10 / 10 | $0.038 / **$0.012** | 4.0 / **3.0** min |
| [Quick tasks](runs/quick/README.md) | 6 | 6 / 6 | $0.035 / **$0.017** | 3.6 / **2.3** min |

## Find your way around

| Where | What you will find |
| --- | --- |
| [SUMMARY.md](SUMMARY.md) | Every number: per section, per task, per harness. Dollars, tokens, reasoning tokens, time, model calls |
| [runs/](runs/README.md) | Every attempt. Pick a section, then a task, then a harness. Each attempt has a page with its numbers, its agents and how the work was split, and a `transcript.md` with every model call: what was sent, what came back, tokens, cost |
| [sections/](sections/) | The tasks themselves, their hidden tests and their graders |
| [METHODOLOGY.md](METHODOLOGY.md) | Settings, caps, grading, metering, what is removed from Heliod's traces, limits |

## The sections

| Section | Tasks | What the agent gets | Graded by |
| --- | --- | --- | --- |
| Large fleet jobs | 5 | A written spec for a multi-module package (a billing platform, invoicing, pricing, shipping), or 40 tickets with four house rules stated once | 96 + 68 + 38 + 48 hidden test cases; 40 tickets checked for behaviour and the house rules |
| Ambiguous specs | 10 | A ticket that leaves a gap or reads two ways, in a repo that settles it: a data file, a caller, a runbook, a design mock, an old receipt. Three ship no tests | Hidden tests that pin the reading the repo supports |
| Quick tasks | 6 of 34 | One [Aider Polyglot](https://github.com/Aider-AI/polyglot-benchmark) Python exercise per run | The exercise's own unit tests, restored before grading |

Before any run, every task's reference solution passed all its graded cases and every untouched starting workspace
failed ([sections/VALIDATION.md](sections/VALIDATION.md)).

## Read these with care

- **Subagent settings differ, on purpose.** Both main agents ran at medium reasoning. Heliod's fleet workers ask the
  model for low reasoning; every Codex call asked for medium. Each harness's choices are part of what is compared,
  and every request in the transcripts shows its setting.
- **Heliod's checks.** Heliod checks its workers' output with a hosted checker that is free to users, so those
  checks are not in the bills above (45 checks, all on the fleet jobs). We ran the fleet jobs again with every check
  on GPT-6 Luna through the same meter ([runs/fleet-private-checks](runs/fleet-private-checks/README.md)): Heliod
  $0.099 in 6.9 minutes, 5 of 5 passed, against Codex's $0.106 in 16.1 minutes, 4 of 5.
- **Who used a team.** Codex had its multi-agent feature on and chose to work alone on all 21 tasks. Heliod sent the
  four multi-module jobs to a team of 7 to 12 agents and worked alone on the other 17.
- **Quick tasks is partial.** We stopped it after 6 of its 34 exercises to publish the same evening. All six finished
  pairs are shown.
- **One model, one attempt per task.** The result rests on 21 matched tasks, not on repeats.

## Re-derive every number

```sh
python3 tools/summary.py      # rebuilds SUMMARY.md and summary.json from runs/
python3 tools/transcripts.py  # rebuilds every README and transcript in runs/
git diff --stat               # nothing changes
```

## Run it yourself

Needs Python 3.11+ with pytest, Node 22+, [Codex CLI](https://github.com/openai/codex),
[Heliod Harness](https://heliod.dev) and an OpenRouter key.

```sh
export OPENROUTER_API_KEY=...
sh run-sections.sh             # Large fleet jobs, Ambiguous specs, Quick tasks
sh run-private-checks.sh       # Large fleet jobs again, Heliod with every check metered
python3 tools/export_traces.py results/<run> ...    # the public trace set in runs/
python3 tools/summary.py && python3 tools/transcripts.py
```

`node run.mjs --suite sections/<name> --all --dry-run` prints a section's schedule and spends nothing.

## Sources and licences

The Quick tasks are Exercism's Python exercises as packaged by Aider's polyglot-benchmark (MIT). The fleet jobs come
from our earlier multi-part benchmark; the ambiguous specs were written for this one. Everything here is MIT
([LICENSE](LICENSE)).
