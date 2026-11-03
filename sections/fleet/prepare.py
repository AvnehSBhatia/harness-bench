#!/usr/bin/env python3
"""Large fleet jobs: multi-module builds from one written spec.

  python3 prepare.py <task> <workspace>

billing_platform, invoicing, pricing, shipping: a SPEC.md, team notes, a shared helper module, one starter file per
function and a test file per function. The workspace is the task folder without the reference solution, with the
starter files at the top level (the layout Neo's Codex baseline used). Some notes, comments and helpers disagree with
the SPEC on purpose; TASK.md says the SPEC wins, and the tests follow the SPEC.
longrun: 40 tickets in one package with four house rules stated once (see longrun/).
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import git_init  # noqa: E402

HIDDEN = {"_solution", "_trap_variant", "task.json", "__pycache__", ".pytest_cache"}


def main():
    task, ws = sys.argv[1], os.path.abspath(sys.argv[2])
    if task == "longrun":
        subprocess.run([sys.executable, os.path.join(HERE, "longrun", "prepare.py"), "longrun-luna", ws], check=True)
        return
    src = os.path.join(HERE, "tasks", task)
    meta = json.load(open(os.path.join(src, "task.json")))
    os.makedirs(ws)
    for name in sorted(os.listdir(src)):
        if name in HIDDEN:
            continue
        p = os.path.join(src, name)
        if name == "starter":
            for f in sorted(os.listdir(p)):
                if f.endswith(".py"):
                    shutil.copy(os.path.join(p, f), ws)
        elif os.path.isdir(p):
            shutil.copytree(p, os.path.join(ws, name), ignore=shutil.ignore_patterns(*HIDDEN))
        else:
            shutil.copy(p, ws)
    fns = [f["name"] for f in meta["functions"]]
    open(os.path.join(ws, "TASK.md"), "w").write(
        "Implement the functions described in SPEC.md. Each function has its own starter file <function>.py in this "
        f"folder. Functions: {', '.join(fns)}. SPEC.md is the source of truth; if any note, comment or file disagrees "
        "with it, follow SPEC.md.\n")
    git_init(ws)


if __name__ == "__main__":
    main()
