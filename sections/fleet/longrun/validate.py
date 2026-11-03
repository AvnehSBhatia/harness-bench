#!/usr/bin/env python3
"""Validate the long-session test: the hidden checks are right, solvable, and see late-session slips.

  python3 validate.py

  fresh       the untouched starting repository: no ticket done.
  oracle      the reference solutions in oracle.py, following every house rule: all 40 done.
  forgetful   the same solutions, but from T21 on the house rules are dropped (ValueError instead of KitError, no
              docstring tag, no changelog line): every ticket still behaves, but only T1-T20 count as done and the
              rules-kept score falls to 0.25 (exports only) in the last two blocks.
"""

import ast
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from grade import grade  # noqa: E402
from tickets import MODULES, T  # noqa: E402


def oracle_sources():
    src = open(os.path.join(HERE, "oracle.py")).read()
    return {n.name: ast.get_source_segment(src, n) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}


def install(ws, forget_from=None):
    srcs = oracle_sources()
    names = []
    log = []
    for module in MODULES:
        path = os.path.join(ws, "kit", f"{module}.py")
        text = open(path).read().rstrip() + "\n"
        for t in [t for t in T if t["module"] == module]:
            body = srcs[t["name"]]
            forget = forget_from is not None and t["id"] >= forget_from
            if forget:
                body = body.replace("raise KitError(", "raise ValueError(").replace(f" [T{t['id']}]", "")
            else:
                log.append(f"- T{t['id']} {t['name']}")
            text += "\n\n" + body + "\n"
            names.append((module, t["name"]))
        open(path, "w").write(text)
    init = os.path.join(ws, "kit", "__init__.py")
    text = open(init).read()
    imports = "".join(f"from .{m} import {n}\n" for m, n in names)
    text = text.replace("from .text import word_count\n", "from .text import word_count\n" + imports)
    text = re.sub(r"__all__ = \[(.*)\]", lambda m: "__all__ = [" + m.group(1) + "".join(f', "{n}"' for _, n in names) + "]", text)
    open(init, "w").write(text)
    with open(os.path.join(ws, "CHANGELOG.md"), "a") as f:
        f.write("\n".join(log) + "\n")


def fresh(root, name):
    ws = os.path.join(root, name)
    subprocess.run([sys.executable, os.path.join(HERE, "prepare.py"), "longrun", ws], check=True, capture_output=True)
    return ws


def main():
    root = tempfile.mkdtemp(prefix="longrun-validate-")
    rows = []

    g = grade(fresh(root, "fresh"))
    rows.append(("fresh", "no ticket done", g, g["passed"] == 0))

    ws = fresh(root, "oracle")
    install(ws)
    g = grade(ws)
    rows.append(("oracle", "all 40 done", g, g["passed"] == 40 and g["works"]))
    t0 = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests"], cwd=ws, capture_output=True, text=True)
    rows.append(("visible test", "tests/test_t0.py passes", {"passed": int("1 passed" in t0.stdout or "2 passed" in t0.stdout), "detail": {}}, t0.returncode == 0))

    ws = fresh(root, "forgetful")
    install(ws, forget_from=21)
    g = grade(ws)
    b = g["detail"]["blocks"]
    ok = g["detail"]["checks"]["behavior"] == 40 and g["passed"] == 20 and b["T21-30"]["rules_kept"] == 0.25 and b["T31-40"]["rules_kept"] == 0.25 and b["T1-10"]["rules_kept"] == 1.0
    rows.append(("forgetful", "behaves 40/40, done 20/40, rules kept 1.0 early and 0.25 late", g, ok))

    print("| Check | Must | Result | OK |")
    print("| --- | --- | --- | --- |")
    for name, must, g, ok in rows:
        blocks = g.get("detail", {}).get("blocks")
        res = ("passes" if name == "visible test" else f"done {g.get('passed')}/40") + (f"; blocks {json.dumps({k: (v['done'], v['rules_kept']) for k, v in blocks.items()})}" if blocks else "")
        print(f"| {name} | {must} | {res} | {'yes' if ok else 'NO'} |")
    bad = [r for r in rows if not r[3]]
    print(f"\n{len(rows) - len(bad)} of {len(rows)} checks passed.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
