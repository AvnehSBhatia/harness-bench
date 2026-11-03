#!/usr/bin/env python3
"""Turn raw run folders (results/<run>/) into the public trace set (runs/<run>/).

  python3 tools/export_traces.py results/<run> [results/<run> ...]      -> runs/<run>/..., runs/LEAKCHECK.md

What a reader gets for every attempt (runs/<run>/<task>/<harness>/):
  grade.json      the grader's verdict          timing.json   start, end, why it stopped, its caps
  diff.patch      every change the harness made  summary.json  cost, tokens, calls, agent threads, tools used
  calls.jsonl.gz  every model call, in order: what was new in the request since the call it continues, and the full
                  response (text, tool calls, the reasoning summary when the API returns one), with OpenRouter's
                  generation id, tokens and billed cost
  events.jsonl.gz the harness's own event stream (Codex `exec --json`, Heliod `--mode json`), streaming deltas dropped
  session/        Codex rollout files (main thread and every subagent) or the Heliod session file
  fleet.json      Heliod only: the fleet's plan, agents, steps, messages and per-agent tokens and cost

Heliod is closed source. Its system prompts and tool definitions are removed from every request (the tool names stay),
and a leak check scans everything published from a Heliod attempt for any 40-character run of text from the installed
Heliod package or from the removed prompts; matches are replaced with [heliod text removed] and counted in
runs/LEAKCHECK.md. Codex is open source, so its traces are published as they are. Every file is scanned for API keys
and tokens; one found stops the export.
"""
import glob
import gzip
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
HELIOD_PKG = os.environ.get("HELIOD_PKG", os.path.join(HOME, ".heliod/lib/node_modules/heliod-harness"))
W = 32  # window indexed from secret text; any shared run of >= W + STEP characters (40) is caught
STEP = 8
SECRET_RE = re.compile(r"sk-or-v1-[0-9a-f]{20,}|sk-or-[A-Za-z0-9_-]{24,}|sk-[A-Za-z0-9]{32,}|gh[opsu]_[A-Za-z0-9]{30,}|Bearer\s+[A-Za-z0-9._-]{24,}")
DELTA_EVENTS = {"message_update", "tool_execution_update"}


# ----------------------------------------------------------------------------------------------- leak guard
class Guard:
    """Windows of Heliod's own text. Anything published from a Heliod attempt passes through clean()."""

    def __init__(self):
        self.windows = set()
        self.public = set()
        self.sources = 0
        self.hits = 0
        self.hit_files = {}

    def add(self, text):
        text = text if isinstance(text, str) else json.dumps(text)
        if len(text) < W:
            return
        self.sources += 1
        for i in range(len(text) - W + 1):
            self.windows.add(hash(text[i:i + W]))

    def add_public(self, text):
        """Text anyone can already read (task files, the agents' own code): never treated as Heliod's."""
        if isinstance(text, str) and len(text) >= W:
            for i in range(len(text) - W + 1):
                self.public.add(hash(text[i:i + W]))

    def secret(self, h):
        return h in self.windows and h not in self.public

    def add_package(self):
        for f in glob.glob(os.path.join(HELIOD_PKG, "dist", "**", "*"), recursive=True):
            if os.path.isfile(f) and f.endswith((".js", ".json", ".md", ".txt", ".mjs", ".cjs")):
                self.add(open(f, encoding="utf8", errors="replace").read())

    def clean(self, text, where):
        """Replace every run of Heliod text (>= W + STEP chars) in text."""
        if not isinstance(text, str) or len(text) < W:
            return text
        marks = []
        for i in range(0, len(text) - W + 1, STEP):
            if self.secret(hash(text[i:i + W])):
                # grow the match both ways one character at a time while windows still match
                lo, hi = i, i + W
                while lo > 0 and self.secret(hash(text[lo - 1:lo - 1 + W])):
                    lo -= 1
                while hi < len(text) and self.secret(hash(text[hi - W + 1:hi + 1])):
                    hi += 1
                marks.append((lo, hi))
        if not marks:
            return text
        marks.sort()
        merged = [list(marks[0])]
        for lo, hi in marks[1:]:
            if lo <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        self.hits += len(merged)
        self.hit_files[where] = self.hit_files.get(where, 0) + len(merged)
        out, last = [], 0
        for lo, hi in merged:
            out.append(text[last:lo])
            out.append("[heliod text removed]")
            last = hi
        out.append(text[last:])
        return "".join(out)

    def deep(self, obj, where):
        if isinstance(obj, str):
            return self.clean(obj, where)
        if isinstance(obj, list):
            return [self.deep(x, where) for x in obj]
        if isinstance(obj, dict):
            return {k: self.deep(v, where) for k, v in obj.items()}
        return obj


ENCRYPTED = "[encrypted by the provider; not readable]"


ENCRYPTED_KEYS = ("encrypted_content", "encrypted", "thinkingSignature", "signature")


def drop_encrypted(obj):
    """Encrypted reasoning blobs are unreadable random text: replace them. Codex carries them as encrypted_content
    (Responses API); Heliod as reasoning_details entries of type reasoning.encrypted and as thinkingSignature."""
    if isinstance(obj, list):
        return [drop_encrypted(x) for x in obj]
    if isinstance(obj, dict):
        blob = obj.get("type") == "reasoning.encrypted"
        return {k: (ENCRYPTED if isinstance(v, str) and (k in ENCRYPTED_KEYS or (blob and k == "data")) else drop_encrypted(v)) for k, v in obj.items()}
    return obj


def scrub_paths(text, run_dir):
    return text.replace(run_dir, "<run>").replace(HOME, "~")


# ----------------------------------------------------------------------------------------------- model calls
def assemble(response_text):
    """The response as the harness received it: one object, whether it streamed or not."""
    text = response_text or ""
    datas = [l[5:].strip() for l in text.split("\n") if l.startswith("data:")]
    if not datas:
        try:
            j = json.loads(text)
        except Exception:
            return {"raw": text[:2000]}
        if isinstance(j, dict) and j.get("object") == "response":
            return responses_out(j)
        msg = (j.get("choices") or [{}])[0].get("message", {}) if isinstance(j, dict) else {}
        return {"api": "chat", "content": msg.get("content"), "reasoning": msg.get("reasoning"), "tool_calls": msg.get("tool_calls"),
                "finish_reason": (j.get("choices") or [{}])[0].get("finish_reason") if isinstance(j, dict) else None, "usage": j.get("usage") if isinstance(j, dict) else None}
    events = []
    for d in datas:
        if d == "[DONE]":
            continue
        try:
            events.append(json.loads(d))
        except Exception:
            pass
    for e in events:
        if e.get("type") in ("response.completed", "response.incomplete", "response.failed") and isinstance(e.get("response"), dict):
            return responses_out(e["response"])
    content, reasoning, calls, finish, usage, details = [], [], {}, None, None, []
    for e in events:
        if e.get("usage"):
            usage = e["usage"]
        for ch in e.get("choices") or []:
            d = ch.get("delta") or {}
            if d.get("content"):
                content.append(d["content"])
            if d.get("reasoning"):
                reasoning.append(d["reasoning"])
            for rd in d.get("reasoning_details") or []:
                if rd.get("type") != "reasoning.encrypted":
                    details.append(rd)
            for tc in d.get("tool_calls") or []:
                c = calls.setdefault(tc.get("index", 0), {"id": None, "name": "", "arguments": ""})
                c["id"] = tc.get("id") or c["id"]
                fn = tc.get("function") or {}
                c["name"] += fn.get("name") or ""
                c["arguments"] += fn.get("arguments") or ""
            finish = ch.get("finish_reason") or finish
    return {"api": "chat", "content": "".join(content) or None, "reasoning": "".join(reasoning) or None,
            "reasoning_details": drop_encrypted([d for d in details if d.get("type") != "reasoning.text" or not reasoning]) or None,
            "tool_calls": [calls[k] for k in sorted(calls)] or None, "finish_reason": finish, "usage": usage}


def responses_out(r):
    out = []
    for it in r.get("output") or []:
        it = dict(it)
        out.append(drop_encrypted(it))
    return {"api": "responses", "status": r.get("status"), "output": out, "usage": r.get("usage")}


def request_items(req):
    """(list of conversation items, everything else) for a chat or Responses request."""
    if not isinstance(req, dict):
        return [], {"raw": str(req)[:2000]}
    if isinstance(req.get("messages"), list):
        return req["messages"], {k: v for k, v in req.items() if k != "messages"}
    if isinstance(req.get("input"), list):
        return req["input"], {k: v for k, v in req.items() if k != "input"}
    return [], dict(req)


def export_calls(run_dir, key, heliod, guard, dst):
    files = sorted(glob.glob(os.path.join(run_dir, "calls", key, "*.json.gz")), key=lambda p: (json.loads(gzip.open(p).read()).get("started", 0), p))
    seen = []  # filtered item lists of earlier calls, as JSON strings
    instructions_seen = {}
    threads = set()
    rows = []
    for n, p in enumerate(files, 1):
        rec = json.loads(gzip.open(p).read())
        req = rec.pop("request", None)
        resp = assemble(rec.pop("response", ""))
        items, rest = request_items(drop_encrypted(req))
        removed = []
        if heliod:
            kept = []
            for m in items:
                if isinstance(m, dict) and m.get("role") in ("system", "developer"):
                    removed.append(m)
                else:
                    kept.append(m)
            items = kept
            if rest.get("instructions"):
                removed.append(rest.pop("instructions"))
            if rest.get("tools"):
                removed.extend(rest["tools"])
                rest["tools"] = [((t.get("function") or {}).get("name") or t.get("name")) for t in rest["tools"] if isinstance(t, dict)]
            for r in removed:
                guard.add(r)
        elif rest.get("instructions"):
            h = hashlib.sha256(str(rest["instructions"]).encode()).hexdigest()[:12]
            if h in instructions_seen:
                rest["instructions"] = f"[same as call {instructions_seen[h]}]"
            else:
                instructions_seen[h] = n
        enc = [json.dumps(m, sort_keys=True) for m in items]
        best, best_len = None, 0
        for i, prev in enumerate(seen):
            k = 0
            while k < len(prev) and k < len(enc) and prev[k] == enc[k]:
                k += 1
            if k > best_len and k == len(prev):
                best, best_len = i + 1, k
        seen.append(enc)
        if rest.get("prompt_cache_key"):
            threads.add(rest["prompt_cache_key"])
        row = {"call": n, **{k: rec.get(k) for k in ("started", "ms", "status", "model", "gen", "input", "cached", "cacheWrite", "output", "cost", "costSource")},
               "request": {"continues_call": best, "items_from_it": best_len, "new_items": items[best_len:], "params": rest,
                           "removed_heliod_prompt_parts": len(removed) if heliod else None},
               "response": resp}
        rows.append(row)
    # the guard has every removed prompt now; clean and write
    with gzip.open(os.path.join(dst, "calls.jsonl.gz"), "wt") as f:
        for row in rows:
            if heliod:
                row = guard.deep(row, f"{dst}/calls")
            f.write(scrub_paths(json.dumps(row), run_dir) + "\n")
    return {"traced_calls": len(rows), "agent_threads": len(threads) or None}


# ----------------------------------------------------------------------------------------------- harness files
def export_events(src, dst, heliod, guard, run_dir):
    p = os.path.join(src, "stdout.jsonl")
    if not os.path.exists(p):
        return {}
    tools = {}
    with gzip.open(os.path.join(dst, "events.jsonl.gz"), "wt") as out:
        for line in open(p, encoding="utf8", errors="replace"):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("type") in DELTA_EVENTS:
                continue
            name = e.get("toolName") or ((e.get("item") or {}).get("type") if isinstance(e.get("item"), dict) else None)
            if e.get("type") in ("tool_execution_start", "item.started") and name:
                tools[name] = tools.get(name, 0) + 1
            e = drop_encrypted(e)
            if heliod:
                e = guard.deep(e, f"{dst}/events")
            out.write(scrub_paths(json.dumps(e), run_dir) + "\n")
    return {"tool_uses": tools}


def export_sessions(src, dst, heliod, guard, run_dir):
    pattern = os.path.join(src, "heliodhome/agent/sessions/**/*.jsonl") if heliod else os.path.join(src, "codexhome/sessions/**/*.jsonl")
    files = sorted(glob.glob(pattern, recursive=True))
    if not files:
        return {"session_files": 0}
    os.makedirs(os.path.join(dst, "session"), exist_ok=True)
    for f in files:
        name = os.path.basename(f) + ".gz"
        with gzip.open(os.path.join(dst, "session", name), "wt") as out:
            for line in open(f, encoding="utf8", errors="replace"):
                try:
                    e = json.loads(line)
                except Exception:
                    continue
                e = drop_encrypted(e)
                if heliod:
                    e = guard.deep(e, f"{dst}/session")
                out.write(scrub_paths(json.dumps(e), run_dir) + "\n")
    return {"session_files": len(files)}


FLEET_TABLES = ["fleet_runs", "fleet_slots", "fleet_slot_history", "fleet_reassignments", "agents", "agent_steps",
                "relay_messages", "ledger_entries", "cases", "agent_checkpoints"]


def export_fleet(src, dst, guard, run_dir):
    db = os.path.join(src, "heliodhome/harness/state.db")
    if not os.path.exists(db):
        return {"fleet_agents": 0}
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    have = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    out = {}
    for t in FLEET_TABLES:
        if t not in have:
            continue
        rows = []
        for r in con.execute(f"select * from {t}"):
            d = {k: r[k] for k in r.keys() if k != "embedding"}
            for k, v in list(d.items()):
                if isinstance(v, bytes):
                    d[k] = f"[{len(v)} bytes]"
                elif isinstance(v, str) and v[:1] in "[{":
                    try:
                        d[k] = json.loads(v)
                    except Exception:
                        pass
            rows.append(d)
        out[t] = rows
    con.close()
    out = guard.deep(out, f"{dst}/fleet")
    open(os.path.join(dst, "fleet.json"), "w").write(scrub_paths(json.dumps(out, indent=1), run_dir))
    agents = out.get("agents", [])
    return {"fleet_runs": len(out.get("fleet_runs", [])), "fleet_agents": len(agents),
            "fleet_usd": round(sum(a.get("usd") or 0 for a in agents), 6)}


# ----------------------------------------------------------------------------------------------- main
def export_run(run_dir, guard):
    run_dir = os.path.abspath(run_dir)
    res = json.load(open(os.path.join(run_dir, "results.json")))
    # runs/<section>: named for people, not timestamps. A Heliod-only --private-checks run is <section>-private-checks.
    m = res.get("manifest", {})
    name = m.get("section") or os.path.basename(run_dir).rsplit("-", 1)[-1]
    if m.get("arms") == ["heliod-private"]:
        name += "-private-checks"
    dst_root = os.path.join(ROOT, "runs", name)
    if os.path.exists(dst_root):
        shutil.rmtree(dst_root)
    os.makedirs(dst_root)
    open(os.path.join(dst_root, "run.json"), "w").write(json.dumps({"run": os.path.basename(run_dir), "manifest": m, "versions": res.get("versions")}, indent=1))
    TRIALS["n"] = res.get("manifest", {}).get("trials", 1)
    # first pass: register every removed Heliod prompt before cleaning anything, and everything a model wrote as
    # public (the plan, the agents' code and messages are model output, even where Heliod copies them into a prompt)
    for row in res["rows"]:
        tag = f"-t{row['trial']}" if TRIALS["n"] > 1 else ""
        guard.add_public(os.path.join(run_dir, row["task"], row["arm"] + tag, "ws"))
        for p in glob.glob(os.path.join(run_dir, "calls", glob.escape(key_of(row)), "*.json.gz")):
            rec = json.loads(gzip.open(p).read())
            out = assemble(rec.get("response", ""))
            for piece in (out.get("content"), out.get("reasoning")):
                guard.add_public(piece)
            for c in out.get("tool_calls") or []:
                guard.add_public(c.get("arguments"))
                try:
                    for v in json.loads(c.get("arguments") or "{}").values():
                        guard.add_public(v if isinstance(v, str) else json.dumps(v))
                except (ValueError, AttributeError):
                    pass
            for it in out.get("output") or []:
                guard.add_public(json.dumps(it))
                for k in ("arguments", "input", "text"):
                    guard.add_public(it.get(k))
            if not row["arm"].startswith("heliod"):
                continue
            items, rest = request_items(rec.get("request"))
            for m in items:
                if isinstance(m, dict) and m.get("role") in ("system", "developer"):
                    guard.add(m)
            if rest.get("instructions"):
                guard.add(rest["instructions"])
            for t in rest.get("tools") or []:
                guard.add(t)
    summaries = []
    for row in res["rows"]:
        heliod = row["arm"].startswith("heliod")
        tag = f"-t{row['trial']}" if res.get("manifest", {}).get("trials", 1) > 1 else ""
        src = os.path.join(run_dir, row["task"], row["arm"] + tag)
        dst = os.path.join(dst_root, row["task"], row["arm"] + tag)
        os.makedirs(dst, exist_ok=True)
        for f in ("grade.json", "timing.json", "diff.patch", "diffstat.txt"):
            if os.path.exists(os.path.join(src, f)):
                text = open(os.path.join(src, f), encoding="utf8", errors="replace").read()
                if heliod:
                    text = guard.clean(text, f"{dst}/{f}")
                open(os.path.join(dst, f), "w").write(scrub_paths(text, run_dir))
        s = dict(row)
        s.update(export_calls(run_dir, key_of(row), heliod, guard, dst))
        s.update(export_events(src, dst, heliod, guard, run_dir))
        s.update(export_sessions(src, dst, heliod, guard, run_dir))
        if heliod:
            s.update(export_fleet(src, dst, guard, run_dir))
        else:
            s["subagent_threads"] = max(0, s.get("session_files", 0) - 1)
        open(os.path.join(dst, "summary.json"), "w").write(json.dumps(s, indent=1))
        summaries.append(s)
    for f in ("results.json", "SCORECARD.md", "REPORT.md", "AUDIT.md", "proxy.jsonl"):
        p = os.path.join(run_dir, f)
        if os.path.exists(p):
            open(os.path.join(dst_root, f), "w").write(scrub_paths(open(p, encoding="utf8").read(), run_dir))
    open(os.path.join(dst_root, "attempts.json"), "w").write(json.dumps(summaries, indent=1))
    return dst_root


TRIALS = {"n": 1}


def key_of(row):
    # run.mjs: key = `${name}-${t.id}${tag}`, tag = -t<trial> only when the run had more than one trial
    return f"{row['arm']}-{row['task']}" + (f"-t{row['trial']}" if TRIALS["n"] > 1 else "")


def secret_scan(root):
    bad = []
    for base, _, files in os.walk(root):
        for f in files:
            p = os.path.join(base, f)
            data = gzip.open(p).read().decode("utf8", "replace") if p.endswith(".gz") else open(p, encoding="utf8", errors="replace").read()
            for m in SECRET_RE.finditer(data):
                bad.append(f"{os.path.relpath(p, ROOT)}: {m.group(0)[:10]}...")
    return bad


PUBLIC_SKIP = {"target", "node_modules", ".git", "__pycache__", ".pytest_cache", ".venv", "venv", "codexhome", "heliodhome", "calls"}


def add_public_tree(guard, root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in PUBLIC_SKIP]
        for f in files:
            p = os.path.join(base, f)
            try:
                if os.path.getsize(p) <= 1_000_000:
                    guard.add_public(open(p, encoding="utf8", errors="strict").read())
            except (OSError, UnicodeDecodeError):
                pass


def main():
    guard = Guard()
    guard.add_package()
    # Public: every task file in this repo, and every workspace the agents left (their own code and the task's files).
    add_public_tree(guard, os.path.join(ROOT, "sections"))
    for r in sys.argv[1:]:
        for ws in glob.glob(os.path.join(os.path.abspath(r), "*", "*", "ws")):
            add_public_tree(guard, ws)
    pkg_sources = guard.sources
    outs = [export_run(r, guard) for r in sys.argv[1:]]
    bad = []
    for o in outs:
        bad += secret_scan(o)
    lines = [
        "# Leak check", "",
        f"Heliod text indexed: {pkg_sources} files from the installed Heliod package plus {guard.sources - pkg_sources} removed prompt parts "
        f"(system prompts and tool definitions), as {len(guard.windows):,} windows of {W} characters.",
        f"Runs of Heliod text found in published Heliod traces and replaced with [heliod text removed]: {guard.hits}.", "",
    ]
    if guard.hit_files:
        lines += ["| Where | Replaced |", "| --- | --- |"] + [f"| {scrub_paths(k, ROOT)} | {v} |" for k, v in sorted(guard.hit_files.items())]
    lines += ["", f"API keys or tokens found: {len(bad)}"]
    open(os.path.join(ROOT, "runs", "LEAKCHECK.md"), "a" if os.path.exists(os.path.join(ROOT, "runs", "LEAKCHECK.md")) else "w").write("\n".join(lines) + "\n\n")
    print("\n".join(lines))
    if bad:
        print("SECRETS FOUND, do not publish:\n" + "\n".join(bad))
        sys.exit(2)


if __name__ == "__main__":
    main()
