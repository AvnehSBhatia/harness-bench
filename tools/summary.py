#!/usr/bin/env python3
"""One table for the whole bench: every section, both harnesses, from the graded results and the billed costs.

  python3 tools/summary.py                    the newest published run of each section in runs/  -> SUMMARY.md, summary.json
  python3 tools/summary.py runs/<run> ...     chosen runs (raw results/<run> folders work too)

Per section and harness: tasks fully passed, test cases passed, dollars billed (OpenRouter's own figure per call),
dollars per passed task, output and input tokens, wall time (total and median per task), and head-to-head counts over
the tasks both harnesses attempted: who passed more cases, who was cheaper, faster, wrote fewer output tokens.
"""
import glob
import gzip
import json
import os
import sqlite3
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ["fleet", "ambiguous", "quick"]
TITLE = {"fleet": "Large fleet jobs", "ambiguous": "Ambiguous specs", "quick": "Quick tasks"}
ARMS = ["codex", "heliod"]


def newest_runs(folder="runs"):
    runs = {}
    for d in sorted(glob.glob(os.path.join(ROOT, folder, "*"))):
        if not os.path.exists(os.path.join(d, "results.json")):
            continue
        runs[load(d)[0]] = d
    return runs


def usage_of(text):
    """The usage block of one saved response (streamed or not, chat completions or Responses API)."""
    found = None
    for line in (text or "").split("\n"):
        if not line.startswith("data:"):
            continue
        try:
            j = json.loads(line[5:])
        except ValueError:
            continue
        if j.get("type") == "response.completed":
            found = (j.get("response") or {}).get("usage") or found
        elif j.get("usage"):
            found = j["usage"]
    if found is None:
        try:
            found = json.loads(text).get("usage")
        except (ValueError, AttributeError):
            pass
    return found or {}


def attempt_dir(run_dir, row):
    return os.path.join(run_dir, row["task"], row["arm"] + (f"-t{row['trial']}" if row.get("trial", 1) > 1 else ""))


def reasoning_tokens(run_dir, row):
    """Reasoning tokens (part of output tokens), summed over the attempt's responses: from the published
    calls.jsonl.gz in runs/, or from the raw per-call files in results/."""
    published = os.path.join(attempt_dir(run_dir, row), "calls.jsonl.gz")
    if os.path.exists(published):
        total = 0
        for line in gzip.open(published, "rt"):
            u = (json.loads(line).get("response") or {}).get("usage") or {}
            d = u.get("output_tokens_details") or u.get("completion_tokens_details") or {}
            total += d.get("reasoning_tokens") or 0
        return total
    key = f"{row['arm']}-{row['task']}" + (f"-t{row['trial']}" if row.get("trial", 1) > 1 else "")
    total = 0
    for f in glob.glob(os.path.join(run_dir, "calls", key, "*.json.gz")):
        u = usage_of(json.loads(gzip.open(f).read()).get("response", ""))
        d = u.get("output_tokens_details") or u.get("completion_tokens_details") or {}
        total += d.get("reasoning_tokens") or 0
    return total


def hosted_checks(run_dir, row):
    """Checks a Heliod attempt sent to Heliod's hosted checker (free to users, so not in the OpenRouter bill)."""
    if not row["arm"].startswith("heliod"):
        return 0
    fleet = os.path.join(attempt_dir(run_dir, row), "fleet.json")
    if os.path.exists(fleet):
        return sum(1 for e in json.load(open(fleet)).get("ledger_entries", []) if e.get("category") == "jev")
    db = os.path.join(attempt_dir(run_dir, row), "heliodhome", "harness", "state.db")
    if not os.path.exists(db):
        return 0
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        return con.execute("SELECT COUNT(*) FROM ledger_entries WHERE category = 'jev'").fetchone()[0]
    except sqlite3.Error:
        return 0
    finally:
        con.close()


def load(d):
    """(section key, results). A Heliod-only --private-checks run is its own key: <section>-private."""
    r = json.load(open(os.path.join(d, "results.json")))
    m = r.get("manifest", {})
    sec = m.get("section") or os.path.basename(d).rsplit("-", 1)[-1]
    return (f"{sec}-private" if m.get("arms") == ["heliod-private"] else sec), r


def stats(rows):
    ran = [x for x in rows if x["stopped_by"] != "section-budget"]
    passed = [x for x in rows if x["works"]]
    usd = sum(x["billed_usd"] for x in rows)
    mins = [x["minutes"] for x in ran]
    return {
        "tasks": len(rows), "attempted": len(ran), "passed": len(passed),
        "cases_passed": sum(x["tests_passed"] or 0 for x in rows),
        "cases_expected": sum(x["tests_expected"] or 0 for x in rows),
        "usd": round(usd, 4), "usd_per_pass": round(usd / len(passed), 4) if passed else None,
        "output_tokens": sum(x["output_tokens"] for x in rows), "reasoning_tokens": sum(x.get("reasoning_tokens", 0) for x in rows),
        "input_tokens": sum(x["input_tokens"] for x in rows),
        "cached_tokens": sum(x["cached_tokens"] for x in rows), "calls": sum(x["calls"] for x in rows),
        "hosted_checks": sum(x.get("hosted_checks", 0) for x in rows),
        "minutes": round(sum(mins), 1), "median_minutes": round(statistics.median(mins), 2) if mins else None,
        "stopped": {k: sum(1 for x in rows if x["stopped_by"] == k) for k in sorted({x["stopped_by"] for x in rows})},
    }


def paired(rows):
    by = {}
    for x in rows:
        by.setdefault(x["task"], {})[x["arm"]] = x
    both = [v for v in by.values() if all(a in v and v[a]["stopped_by"] != "section-budget" for a in ARMS)]
    w = {a: {"more_cases": 0, "cheaper": 0, "faster": 0, "fewer_output_tokens": 0} for a in ARMS}
    for v in both:
        c, h = v["codex"], v["heliod"]
        for a, me, other in (("codex", c, h), ("heliod", h, c)):
            w[a]["more_cases"] += (me["tests_passed"] or 0) > (other["tests_passed"] or 0)
            w[a]["cheaper"] += me["billed_usd"] < other["billed_usd"]
            w[a]["faster"] += me["minutes"] < other["minutes"]
            w[a]["fewer_output_tokens"] += me["output_tokens"] < other["output_tokens"]
    return len(both), w


def ratio(a, b):
    return f"{a / b:.1f}x" if a and b else "-"


def main():
    dirs = sys.argv[1:] or list(newest_runs().values())
    data = {}
    for d in dirs:
        sec, r = load(d)
        for row in r["rows"]:
            row["reasoning_tokens"] = reasoning_tokens(d, row)
            row["hosted_checks"] = hosted_checks(d, row)
        data[sec] = {"dir": os.path.relpath(d, ROOT), "versions": r.get("versions"), "rows": r["rows"]}
    out = {"sections": {}, "overall": {}}
    md = ["# Codex vs Heliod on GPT-6 Luna", ""]
    first = next(iter(data.values()), None)
    if first:
        md += [f"Harnesses: {first['versions'].get('codex')} and Heliod Harness {first['versions'].get('heliod')}. Model: openai/gpt-6-luna "
               "through OpenRouter, pinned to the OpenAI provider, the same one-line prompt; both main agents at medium reasoning "
               "(Heliod's fleet workers ask for low reasoning, a harness choice). Costs are what "
               "OpenRouter billed for each call (checked call by call in each run's AUDIT.md).", ""]
    head = ["| Section | Harness | Tasks passed | Test cases passed | Billed | $ per passed task | Output tokens (reasoning) | Input tokens (cached) | Time, total (median per task) |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    md += ["## All sections", ""] + head
    tot = {a: [] for a in ARMS}
    for sec in [s for s in ORDER if s in data] + [s for s in data if s not in ORDER and not s.endswith("-private")]:
        rows = data[sec]["rows"]
        out["sections"][sec] = {"run": data[sec]["dir"]}
        for a in ARMS:
            ra = [x for x in rows if x["arm"] == a]
            tot[a] += ra
            s = stats(ra)
            out["sections"][sec][a] = s
            md.append(f"| {TITLE.get(sec, sec)} | {a} | {s['passed']}/{s['tasks']} | {s['cases_passed']}/{s['cases_expected']} | ${s['usd']:.3f} | "
                      f"{'$%.4f' % s['usd_per_pass'] if s['usd_per_pass'] else '-'} | {s['output_tokens']:,} ({s['reasoning_tokens']:,}) | {s['input_tokens']:,} ({s['cached_tokens']:,}) | "
                      f"{s['minutes']} min ({s['median_minutes']}) |")
        n, w = paired(rows)
        out["sections"][sec]["head_to_head"] = {"tasks": n, **w}
    for a in ARMS:
        out["overall"][a] = stats(tot[a])
    md += ["", "## Overall", "", head[0].replace("| Section | Harness |", "| Harness |"), head[1][6:]]
    for a in ARMS:
        s = out["overall"][a]
        md.append(f"| {a} | {s['passed']}/{s['tasks']} | {s['cases_passed']}/{s['cases_expected']} | ${s['usd']:.3f} | "
                  f"{'$%.4f' % s['usd_per_pass'] if s['usd_per_pass'] else '-'} | {s['output_tokens']:,} ({s['reasoning_tokens']:,}) | {s['input_tokens']:,} ({s['cached_tokens']:,}) | "
                  f"{s['minutes']} min ({s['median_minutes']}) |")
    c, h = out["overall"]["codex"], out["overall"]["heliod"]
    md += ["", f"Codex / Heliod: billed {ratio(c['usd'], h['usd'])}, output tokens {ratio(c['output_tokens'], h['output_tokens'])}, "
               f"input tokens {ratio(c['input_tokens'], h['input_tokens'])}, time {ratio(c['minutes'], h['minutes'])}; "
               f"tasks passed {c['passed']} vs {h['passed']}.", ""]
    md += ["## Head to head, task by task", "", "Counts over the tasks both harnesses attempted. A tie counts for neither.", "",
           "| Section | Tasks | More cases passed (Codex / Heliod) | Cheaper | Faster | Fewer output tokens |", "| --- | --- | --- | --- | --- | --- |"]
    for sec, v in out["sections"].items():
        if "head_to_head" not in v:
            continue
        hh = v["head_to_head"]
        md.append(f"| {TITLE.get(sec, sec)} | {hh['tasks']} | {hh['codex']['more_cases']} / {hh['heliod']['more_cases']} | {hh['codex']['cheaper']} / {hh['heliod']['cheaper']} | "
                  f"{hh['codex']['faster']} / {hh['heliod']['faster']} | {hh['codex']['fewer_output_tokens']} / {hh['heliod']['fewer_output_tokens']} |")
    for sec in [s for s in data if s.endswith("-private")]:
        base = sec[: -len("-private")]
        rows = data[sec]["rows"]
        p = stats(rows)
        out["sections"][sec] = {"run": data[sec]["dir"], "heliod-private": p}
        md += ["", f"## {TITLE.get(base, base)}, with every Heliod check on the task's own model", "",
               "Heliod normally sends its checks (is this agent's work right?) to Heliod's hosted checker, which is free and so "
               "not in the bills above. This run repeats the section with `heliod --private-checks`: every check runs on GPT-6 "
               "Luna through the same meter, so the bill is the whole cost.", "", head[0].replace("| Section | Harness |", "| Harness |"), head[1][6:]]
        for a, st in (("codex", out["sections"].get(base, {}).get("codex")), ("heliod (hosted checks)", out["sections"].get(base, {}).get("heliod")), ("heliod --private-checks", p)):
            if st:
                md.append(f"| {a} | {st['passed']}/{st['tasks']} | {st['cases_passed']}/{st['cases_expected']} | ${st['usd']:.3f} | "
                          f"{'$%.4f' % st['usd_per_pass'] if st['usd_per_pass'] else '-'} | {st['output_tokens']:,} ({st['reasoning_tokens']:,}) | {st['input_tokens']:,} ({st['cached_tokens']:,}) | "
                          f"{st['minutes']} min ({st['median_minutes']}) |")
    md += ["", "## Every attempt", "", "| Section | Task | Harness | Passed | Cases | Billed | Input tokens (cached) | Output tokens (reasoning) | Hosted checks | Minutes | Stopped by |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for sec in out["sections"]:
        for x in data[sec]["rows"]:
            hosted = x.get("hosted_checks", 0) if x["arm"] == "heliod" else "-"
            md.append(f"| {TITLE.get(sec, sec)} | {x['task']} | {x['arm']} | {'yes' if x['works'] else 'no'} | {x['tests'] or '-'} | ${x['billed_usd']:.4f} | "
                      f"{x['input_tokens']:,} ({x['cached_tokens']:,}) | {x['output_tokens']:,} ({x['reasoning_tokens']:,}) | {hosted} | {x['minutes']} | {x['stopped_by']} |")
    keep = ("task", "arm", "works", "tests", "tests_passed", "tests_expected", "billed_usd", "minutes", "calls", "input_tokens",
            "cached_tokens", "output_tokens", "reasoning_tokens", "hosted_checks", "stopped_by")
    out["attempts"] = [{"section": sec, **{k: x.get(k) for k in keep}} for sec in out["sections"] for x in data[sec]["rows"]]
    out["versions"] = first["versions"] if first else {}
    open(os.path.join(ROOT, "SUMMARY.md"), "w").write("\n".join(md) + "\n")
    open(os.path.join(ROOT, "summary.json"), "w").write(json.dumps(out, indent=1))
    print("\n".join(md[: 12 + 2 * len(out["sections"]) + 8]))
    hosted = out["overall"]["heliod"]["hosted_checks"]
    print(f"\nHeliod hosted checks (free to users, not in the OpenRouter bill): {hosted}")


if __name__ == "__main__":
    main()
