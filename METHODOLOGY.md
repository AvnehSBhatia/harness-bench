# Methodology

## The question

Two coding-agent harnesses get the same model, the same prompt and the same tasks. What does each harness add?
Measured as tasks passed, dollars billed, tokens, and wall time.

## Harnesses and settings

| | Codex CLI | Heliod Harness |
| --- | --- | --- |
| Version | 0.157.1 | 0.1.14, the build heliod.dev served on November 2, 2026 |
| How it was started | `codex exec --json` | `heliod -p --mode json` |
| Main agent reasoning | `model_reasoning_effort="medium"` | `--thinking medium` |
| Subagents | Multi-agent feature on (its strongest stock setting). Codex chose to work alone on all 21 tasks: no subagent threads | Sent the four multi-module jobs to its fleet (12, 7, 7 and 7 agents) and worked alone on the other 17. Fleet workers ask for low reasoning and at most 4,000 output tokens; Heliod checks their work |
| Permissions | `--sandbox workspace-write`, network on, `approval_policy="never"` | `HELIOD_PERMISSION_MODE=full` |
| Config | `--ignore-user-config`, a fresh `CODEX_HOME` per attempt | A fresh `HELIOD_HOME` per attempt |

Both use `openai/gpt-6-luna` through OpenRouter. `proxy.mjs` pins every request to the OpenAI provider with
fallbacks off, so both harnesses hit the same provider, the same prompt cache and the same prices.

Both get the same one-line prompt, `Do the task described in TASK.md in this repository.`, and the same TASK.md.
Neither gets hints written for it.

## Tasks

| Section | Source | Validation |
| --- | --- | --- |
| Large fleet jobs | Four multi-module specs from our earlier benchmark (billing platform, invoicing, pricing, shipping), each with a shared helper module, team notes and starter files that disagree with the spec on purpose; TASK.md says the spec wins. Plus a 40-ticket session with four house rules stated once (`sections/fleet/longrun`) | The reference solution passes all 96, 68, 38, 48 and 40 graded items; every starter passes none |
| Ambiguous specs | Ten small repos written for this bench. Each TASK.md leaves a gap or reads two ways, and the repo settles it: rounding shown on an old invoice, a date format shown by the bank's export, a slug convention shown by existing posts, a retry policy in a runbook. Seven ship a few visible tests for the parts not in doubt; three ship none | The reference solution passes every hidden case; every starter fails; the obvious wrong reading fails too (for example `500ms` read as minutes, or banker's rounding for VAT) |
| Quick tasks | The 34 Python exercises of Aider's polyglot-benchmark, one per attempt | The reference solution passes every case; every stub fails |

`sections/VALIDATION.md` holds the checks; `python3 sections/validate.py` repeats them.

## Procedure

- One attempt per task. Inside a section the two harnesses take turns, never at the same time, and who goes first
  alternates from task to task.
- Caps per attempt: Large fleet jobs $0.20 to $0.25 and 12 to 15 minutes; Ambiguous specs $0.10 and 8 minutes;
  Quick tasks $0.05 and 5 minutes. On top, each harness had at most $1 per section. No attempt reached a cap; all
  42 stopped by themselves.
- Grading runs on a copy of the final workspace. Test files and data files are put back as shipped, then the hidden
  tests run. An edited test never counts, and the edit is reported.

## Measurement

- **Cost** is what OpenRouter billed for each call (`usage.cost`), summed by `proxy.mjs`. After each run,
  `audit.mjs` looked up every call by its generation id at OpenRouter: all calls were found, every billed cost
  equalled the metered cost, and every call was served by the pinned provider (`AUDIT.md` in each run folder).
- **Tokens** come from the same responses: input, cached input, cache writes, output, and the reasoning share of
  output (`output_tokens_details.reasoning_tokens`).
- **Time** is wall clock from starting the harness until it exited, including everything the harness does.
- **Hosted checks.** Heliod sends some checks of its workers' output to Heliod's hosted checker, which is free to
  users. They are not model calls on the user's account, so they are not in the bill. Each Heliod attempt's count is
  in SUMMARY.md (45 across the five fleet jobs, none elsewhere). `heliod --private-checks` runs the same checks on
  the user's own model. `run-private-checks.sh` repeated the fleet section that way: $0.099 billed, 6.9 minutes,
  5 of 5 passed (Codex: $0.106, 16.1 minutes, 4 of 5). OpenRouter confirmed all 212 of its calls.

## What was stopped

Quick tasks was stopped by us during its seventh exercise (dominoes) to publish the same evening. The six finished
pairs are scored and shown. The seventh is not scored; its calls are in that run's `proxy.jsonl` and `AUDIT.md`.

## Traces and what is removed

`tools/export_traces.py` builds `runs/` from the raw results, and `tools/transcripts.py` writes the readable pages:

- Every model call is kept: the new part of each request (what it adds to the call it continues), the full reply,
  OpenRouter's generation id, tokens and cost.
- Heliod is closed source. From its requests the export removes the system prompts and the tool definitions; tool
  names stay. It then removes any run of 40 or more characters that appears in the installed Heliod package or in
  those prompts, unless the same text is public anyway: in the task files, in the agents' own code, or in anything a
  model wrote. What remains removed is Heliod's fixed prompt text, such as the header of each worker's brief.
  `runs/LEAKCHECK.md` counts every removal. An independent rescan of every published Heliod string, at every
  offset, finds no run of Heliod-only text longer than 38 characters.
- The model's reasoning arrives encrypted for both harnesses; the blobs are replaced with a placeholder. Reasoning
  token counts are kept.
- Every published file is scanned for API keys and tokens; one found stops the export.
- Local paths are shortened to `~`.

## Re-deriving the numbers

`python3 tools/summary.py` rebuilds `SUMMARY.md` and `summary.json` from `runs/` alone; the same script run on the
raw results gives identical output.

## Limits

- One model, one attempt per task. The claims rest on matched tasks within each section, not on repeats.
- Ambiguous specs are our tasks, written for this bench. Large fleet jobs come from our earlier benchmark, which
  Heliod's fleet was developed against. Quick tasks are public and standard.
- Wall times come from one laptop, which was also running another benchmark for part of the evening, so some times
  include shared CPU. Costs and tokens are unaffected.
