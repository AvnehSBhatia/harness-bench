#!/usr/bin/env python3
"""Human-readable pages for everything in runs/: every model call of every agent, in order.

  python3 tools/transcripts.py      (after tools/export_traces.py and tools/summary.py)

Writes:
  runs/README.md                          the sections, with links
  runs/<section>/README.md                every task in the section: both harnesses side by side
  runs/<section>/<task>/<harness>/README.md      the attempt: numbers, agents, plan, steps, links
  runs/<section>/<task>/<harness>/transcript.md  every model call: what was new in the request, the reply, tokens, cost
"""
import glob
import gzip
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs")
TITLE = {"fleet": "Large fleet jobs", "ambiguous": "Ambiguous specs", "quick": "Quick tasks",
         "fleet-private-checks": "Large fleet jobs, Heliod with every check on the task's model"}
ORDER = ["fleet", "ambiguous", "quick", "fleet-private-checks"]
HARNESS = {"codex": "Codex CLI", "heliod": "Heliod Harness", "heliod-private": "Heliod Harness --private-checks"}
LONG = 40  # lines; longer blocks fold into <details>


def money(x):
    return f"${x:.4f}"


def fence(text):
    """A code block that survives any backticks inside the text."""
    text = text if isinstance(text, str) else json.dumps(text, indent=1)
    ticks = max([len(m) for m in re.findall(r"`+", text)] + [2]) + 1
    f = "`" * ticks
    block = f"{f}\n{text}\n{f}"
    n = text.count("\n") + 1
    return f"<details><summary>{n} lines</summary>\n\n{block}\n\n</details>" if n > LONG else block


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for p in content:
            if isinstance(p, dict):
                out.append(p.get("text") or p.get("output_text") or p.get("input_text") or (json.dumps(p) if p.get("type") not in ("image_url", "input_image") else "[image]"))
            else:
                out.append(str(p))
        return "\n".join(out)
    return json.dumps(content)


def item_md(it):
    """One request item (chat message or Responses API item) as Markdown."""
    if not isinstance(it, dict):
        return fence(str(it))
    t = it.get("type")
    role = it.get("role")
    if role in ("user", "system", "developer") or (t == "message" and role in ("user", "developer")):
        return f"**{role}**\n\n{fence(text_of(it.get('content')))}"
    if role == "assistant" or (t == "message" and role == "assistant"):
        parts = []
        body = text_of(it.get("content")) if it.get("content") else ""
        if body.strip():
            parts.append(f"**assistant**\n\n{fence(body)}")
        for c in it.get("tool_calls") or []:
            fn = c.get("function") or {}
            parts.append(f"**assistant → tool `{fn.get('name')}`**\n\n{fence(pretty(fn.get('arguments')))}")
        return "\n\n".join(parts) or "**assistant** (no text)"
    if role == "tool":
        return f"**tool result** (`{it.get('tool_call_id', '')}`)\n\n{fence(text_of(it.get('content')))}"
    if t in ("function_call", "custom_tool_call"):
        return f"**assistant → tool `{it.get('name')}`**\n\n{fence(pretty(it.get('arguments') or it.get('input')))}"
    if t in ("function_call_output", "custom_tool_call_output"):
        return f"**tool result** (`{it.get('call_id', '')}`)\n\n{fence(text_of(it.get('output')))}"
    if t == "reasoning":
        return "*(the model's reasoning from an earlier turn, encrypted by the provider)*"
    return fence(json.dumps(it, indent=1))


def pretty(args):
    if isinstance(args, str):
        try:
            return json.dumps(json.loads(args), indent=1)
        except ValueError:
            return args
    return json.dumps(args, indent=1)


def reply_md(resp):
    parts = []
    if resp.get("api") == "responses":
        for it in resp.get("output") or []:
            t = it.get("type")
            if t == "reasoning":
                summ = " ".join(s.get("text", "") for s in it.get("summary") or [])
                parts.append(f"*reasoning summary:* {summ}" if summ else "*(reasoning, encrypted by the provider)*")
            elif t == "message":
                parts.append(fence(text_of(it.get("content"))))
            elif t in ("function_call", "custom_tool_call"):
                parts.append(f"→ tool `{it.get('name')}`\n\n{fence(pretty(it.get('arguments') or it.get('input')))}")
            else:
                parts.append(fence(json.dumps(it, indent=1)))
    else:
        if resp.get("reasoning"):
            parts.append(f"*reasoning:* {resp['reasoning']}")
        if resp.get("content"):
            parts.append(fence(resp["content"]))
        for c in resp.get("tool_calls") or []:
            parts.append(f"→ tool `{c.get('name')}`\n\n{fence(pretty(c.get('arguments')))}")
    return "\n\n".join(parts) or "*(empty reply)*"


def thread_label(first_items, harness):
    blob = "\n".join(text_of(i.get("content")) if isinstance(i, dict) and "content" in i else json.dumps(i) for i in first_items)[:4000]
    m = re.search(r"You are (w\d+·g\d+)[^\n]*?Your part is \"([^\"]+)\"", blob, re.S)
    if m:
        return f"worker {m.group(1)} ({m.group(2)})"
    if harness.startswith("heliod") and re.search(r"(?i)\b(answer|reply) with (a|one) (number|probability|json)|question:", blob):
        return "checker"
    return "main agent"


def attempt_pages(adir, section, task, arm):
    rows = [json.loads(l) for l in gzip.open(os.path.join(adir, "calls.jsonl.gz"), "rt")] if os.path.exists(os.path.join(adir, "calls.jsonl.gz")) else []
    s = json.load(open(os.path.join(adir, "summary.json")))
    label = {}
    for r in rows:
        prev = r["request"].get("continues_call")
        label[r["call"]] = label.get(prev) if prev in label else thread_label(r["request"]["new_items"][:3], arm)
    agents = {}
    for r in rows:
        a = agents.setdefault(label[r["call"]], {"calls": 0, "input": 0, "cached": 0, "output": 0, "usd": 0.0})
        a["calls"] += 1
        a["input"] += r.get("input") or 0
        a["cached"] += r.get("cached") or 0
        a["output"] += r.get("output") or 0
        a["usd"] += r.get("cost") or 0
    who = HARNESS.get(arm, arm)
    head = (f"**{'Passed' if s.get('works') else 'Not passed'}** · {s.get('tests') or '-'} test cases · {money(s.get('billed_usd', 0))} billed · "
            f"{s.get('minutes')} min · {s.get('calls')} model calls · input {s.get('input_tokens', 0):,} tokens ({s.get('cached_tokens', 0):,} cached) · "
            f"output {s.get('output_tokens', 0):,} tokens")
    # transcript.md
    t = [f"# {task} · {who} · every model call", "", head, "",
         f"[Attempt summary](README.md) · [diff](diff.patch) · [grade](grade.json) · [raw calls](calls.jsonl.gz)", "",
         "Each call shows only what is new in the request (the rest is the conversation so far) and the full reply."
         + (" Heliod's system prompts and tool definitions are removed; see METHODOLOGY.md." if arm.startswith("heliod") else ""), ""]
    for r in rows:
        when = r.get("started")
        t += [f"## Call {r['call']} · {label[r['call']]}", "",
              f"{r.get('input') or 0:,} in ({r.get('cached') or 0:,} cached) · {r.get('output') or 0:,} out · {money(r.get('cost') or 0)} · {r.get('ms') or 0} ms · OpenRouter id `{r.get('gen')}`", ""]
        prev = r["request"].get("continues_call")
        t.append(f"**New in this request** (continues call {prev}):" if prev else "**Request:**")
        t.append("")
        for it in r["request"]["new_items"]:
            t += [item_md(it), ""]
        t += ["**Reply:**", "", reply_md(r["response"]), ""]
    open(os.path.join(adir, "transcript.md"), "w").write("\n".join(t) + "\n")
    # README.md for the attempt
    a = [f"# {task} · {who}", "", head, "", f"Stopped by: {s.get('stopped_by')}. Section: [{TITLE.get(section, section)}](../../README.md).", "",
         "| File | What it is |", "| --- | --- |",
         "| [transcript.md](transcript.md) | Every model call: what was sent, what came back, tokens, cost |",
         "| [diff.patch](diff.patch) | Everything the agent changed |",
         "| [grade.json](grade.json) | The grader's verdict, with any failing test names |",
         "| [summary.json](summary.json) | The numbers on this page |",
         "| [calls.jsonl.gz](calls.jsonl.gz) | The same calls as JSON, one per line |",
         "| [events.jsonl.gz](events.jsonl.gz) | The harness's own event stream |",
         "| [session/](session/) | The harness's session files |"]
    fleet = os.path.join(adir, "fleet.json")
    if os.path.exists(fleet):
        a.append("| [fleet.json](fleet.json) | The fleet: its plan, agents, steps, messages and cost ledger |")
    a += ["", "## Agents", "", "| Agent | Model calls | Input tokens (cached) | Output tokens | Cost |", "| --- | --- | --- | --- | --- |"]
    def order(name):
        m = re.match(r"worker w(\d+)", name)
        return (name != "main agent", int(m.group(1)) if m else 0, name)

    for name, v in sorted(agents.items(), key=lambda kv: order(kv[0])):
        a.append(f"| {name} | {v['calls']} | {v['input']:,} ({v['cached']:,}) | {v['output']:,} | {money(v['usd'])} |")
    if os.path.exists(fleet):
        f = json.load(open(fleet))
        runs = f.get("fleet_runs", [])
        if runs:
            a += ["", "## How Heliod split the work", ""]
            for fr in runs:
                cfg = fr.get("config") or {}
                a += [f"Fleet run `{fr.get('run_id')}`, {fr.get('status')}: {cfg.get('task', '') if isinstance(cfg, dict) else ''}", ""]
            a += ["| Agent | Part | Steps | Cost |", "| --- | --- | --- | --- |"]
            steps = {}
            for st in f.get("agent_steps", []):
                steps.setdefault((str(st.get("slot")), str(st.get("gen"))), []).append(st)
            for ag in f.get("agents", []):
                n = len(steps.get((str(ag.get("slot")), str(ag.get("gen"))), []))
                a.append(f"| w{int(ag.get('slot', 0)) + 1}·g{ag.get('gen')} | {ag.get('task')} | {n} | {money(float(ag.get('usd') or 0))} |")
            msgs = f.get("relay_messages", [])
            a += ["", "## Messages between agents", ""]
            if msgs:
                for m in msgs:
                    a += [f"**{m.get('sender')} → {m.get('recipient')}**", "", fence(str(m.get("text"))), ""]
            else:
                a.append("None in this run: no agent needed to tell another anything.")
            if any(st.get("summary") for sts in steps.values() for st in sts):
                a += ["", "## Each agent's steps", ""]
                for (slot, gen), sts in sorted(steps.items(), key=lambda kv: (int(kv[0][0]), kv[0][1])):
                    a.append(f"- **w{int(slot) + 1}·g{gen}**: " + " → ".join(str(st.get("summary", "")).strip() for st in sorted(sts, key=lambda x: int(x.get("step", 0)))))
    open(os.path.join(adir, "README.md"), "w").write("\n".join(a) + "\n")
    return s


def main():
    secs = [d for d in ORDER if os.path.isdir(os.path.join(RUNS, d))]
    top = ["# Every attempt", "", "One folder per section, one per task, one per harness. Start with a section, then open any attempt's",
           "`transcript.md` to read every model call.", "", "| Section | Tasks | |", "| --- | --- | --- |"]
    for sec in secs:
        sdir = os.path.join(RUNS, sec)
        attempts = json.load(open(os.path.join(sdir, "attempts.json")))
        tasks = []
        for x in attempts:
            if x["task"] not in tasks:
                tasks.append(x["task"])
        lines = [f"# {TITLE.get(sec, sec)}", "", f"[All sections](../README.md) · numbers for every section: [SUMMARY.md](../../SUMMARY.md) · billing audit: [AUDIT.md](AUDIT.md)", "",
                 "| Task | Harness | Passed | Test cases | Billed | Minutes | Model calls | Input tokens | Output tokens | |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for task in tasks:
            for x in sorted([y for y in attempts if y["task"] == task], key=lambda y: y["arm"]):
                arm = x["arm"] + (f"-t{x['trial']}" if x.get("trial", 1) > 1 else "")
                adir = os.path.join(sdir, task, arm)
                if not os.path.isdir(adir):
                    continue
                attempt_pages(adir, sec, task, x["arm"])
                lines.append(f"| {task} | {HARNESS.get(x['arm'], x['arm'])} | {'yes' if x['works'] else 'no'} | {x.get('tests') or '-'} | {money(x['billed_usd'])} | {x['minutes']} | "
                             f"{x['calls']} | {x['input_tokens']:,} | {x['output_tokens']:,} | [open]({task}/{arm}/README.md) |")
        task_src = {"fleet": "sections/fleet", "fleet-private-checks": "sections/fleet", "ambiguous": "sections/ambiguous", "quick": "sections/quick"}.get(sec)
        if task_src:
            lines += ["", f"The tasks themselves, with their graders: [{task_src}](../../{task_src})."]
        open(os.path.join(sdir, "README.md"), "w").write("\n".join(lines) + "\n")
        top.append(f"| [{TITLE.get(sec, sec)}]({sec}/README.md) | {len(tasks)} | |")
    open(os.path.join(RUNS, "README.md"), "w").write("\n".join(top) + "\n")
    print(f"pages written for {len(secs)} sections")


if __name__ == "__main__":
    main()
