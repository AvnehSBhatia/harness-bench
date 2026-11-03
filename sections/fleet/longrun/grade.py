#!/usr/bin/env python3
"""Grade the long-session test.

  python3 grade.py <task-id> <workspace>     -> one JSON object on stdout

For each of the 40 tickets, five checks:
  behavior   the function exists in the module the ticket names and returns the right value for every example and
             hidden case (exact types: a float where a float is expected, dict key order where it matters);
  errors     every invalid input raises KitError (house rule 1);
  docstring  the first docstring line ends with [T<id>] (house rule 2);
  exported   the function is imported in kit/__init__.py and listed in __all__ (house rule 3);
  changelog  CHANGELOG.md has the line "- T<id> <name>" (house rule 4).
A ticket is done when all five pass. Results are also split by block of ten tickets, to show whether the work and
the house rules hold up late in a long session.
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = ["behavior", "errors", "docstring", "exported", "changelog"]
RULES = ["errors", "docstring", "exported", "changelog"]

CHECKER = r'''
import copy, importlib, importlib.util, json, os, re, signal, sys
ws, tickets_path = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("_longrun_tickets", tickets_path)
tk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tk)
sys.path.insert(0, ws)
sys.dont_write_bytecode = True

def on_alarm(sig, frame):
    raise TimeoutError("took more than 2 s")
signal.signal(signal.SIGALRM, on_alarm)

def same(got, exp):
    if isinstance(exp, dict):
        return isinstance(got, dict) and list(got.items()) == list(exp.items())
    if isinstance(exp, float):
        return isinstance(got, float) and got == exp
    return type(got) is type(exp) and got == exp

try:
    import kit
    from kit.errors import KitError
except BaseException as e:
    print(json.dumps({"import_error": repr(e)[:300]}))
    sys.exit(0)
log = os.path.join(ws, "CHANGELOG.md")
changelog = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
out = {}
for t in tk.T:
    r = {}
    try:
        fn = getattr(importlib.import_module("kit." + t["module"]), t["name"], None)
    except BaseException:
        fn = None
    ok = callable(fn)
    for args, exp in (t["examples"] + t["hidden"]) if ok else []:
        try:
            signal.alarm(2)
            got = fn(*copy.deepcopy(args))
            signal.alarm(0)
        except BaseException:
            signal.alarm(0)
            ok = False
            break
        if not same(got, exp):
            ok = False
            break
    r["behavior"] = ok
    ok = callable(fn)
    for args in (t["bad"] + t["hidden_bad"]) if ok else []:
        try:
            signal.alarm(2)
            fn(*copy.deepcopy(args))
            signal.alarm(0)
            ok = False
            break
        except KitError:
            signal.alarm(0)
        except BaseException:
            signal.alarm(0)
            ok = False
            break
    r["errors"] = ok
    doc = ((getattr(fn, "__doc__", None) or "").strip().splitlines() or [""])[0].rstrip()
    r["docstring"] = callable(fn) and doc.endswith("[T%d]" % t["id"])
    r["exported"] = callable(fn) and t["name"] in list(getattr(kit, "__all__", [])) and getattr(kit, t["name"], None) is fn
    r["changelog"] = re.search(r"^- T%d %s\s*$" % (t["id"], re.escape(t["name"])), changelog, re.M) is not None
    out[t["id"]] = r
print(json.dumps(out))
'''


def grade(ws):
    with tempfile.TemporaryDirectory() as tmp:
        checker = os.path.join(tmp, "checker.py")
        with open(checker, "w") as f:
            f.write(CHECKER)
        try:
            r = subprocess.run([sys.executable, "-I", checker, ws, os.path.join(HERE, "tickets.py")], capture_output=True, text=True, timeout=300, cwd=tmp)
            raw = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception as e:
            raw = {"import_error": f"checker failed: {e!r}"[:300]}
    if "import_error" in raw:
        per = {i: {c: False for c in CHECKS} for i in range(1, 41)}
    else:
        per = {int(k): v for k, v in raw.items()}
    done = {i: all(per[i].values()) for i in per}
    blocks = {}
    for lo in (1, 11, 21, 31):
        ids = range(lo, lo + 10)
        blocks[f"T{lo}-{lo + 9}"] = {
            "done": sum(done[i] for i in ids),
            "behavior": sum(per[i]["behavior"] for i in ids),
            "rules_kept": round(sum(per[i][c] for i in ids for c in RULES) / (10 * len(RULES)), 3),
        }
    passed = sum(done.values())
    return {
        "works": passed == 40,
        "passed": passed,
        "failed": 40 - passed,
        "errors": 0,
        "total": 40,
        "expected_passed": 40,
        "build": raw.get("import_error", "ok") if "import_error" in raw else "ok",
        "rules": [],
        "detail": {"blocks": blocks, "checks": {c: sum(per[i][c] for i in per) for c in CHECKS}, "per_ticket": per},
    }


if __name__ == "__main__":
    print(json.dumps(grade(os.path.abspath(sys.argv[2]))))
