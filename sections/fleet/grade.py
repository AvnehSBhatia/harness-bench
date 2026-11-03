#!/usr/bin/env python3
"""Grade one fleet job.

  python3 grade.py <task> <workspace> [--oracle]

billing_platform, invoicing, pricing, shipping: the tests, fixtures and shared helper module are put back as shipped
(an edited one never counts and is reported), then every test case runs. Expected = every case the reference passes.
longrun: its own grader (hidden cases per ticket plus the four house rules).
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import pytest_cases, result, scratch_copy  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    task, ws = args[0], os.path.abspath(args[1])
    if task == "longrun":
        if "--oracle" in sys.argv:
            r = subprocess.run([sys.executable, os.path.join(HERE, "longrun", "validate.py")], capture_output=True, text=True)
            return {"works": r.returncode == 0, "passed": 40 if r.returncode == 0 else 0, "total": 40, "expected_passed": 40, "build": r.stdout[-300:]}
        r = subprocess.run([sys.executable, os.path.join(HERE, "longrun", "grade.py"), "longrun-luna", ws], capture_output=True, text=True)
        return json.loads(r.stdout.strip().splitlines()[-1])
    src = os.path.join(HERE, "tasks", task)
    meta = json.load(open(os.path.join(src, "task.json")))
    function_files = {f["file"] for f in meta["functions"]}
    tmp, dst = scratch_copy(ws)
    try:
        modified = []
        protected = []
        for d in ("tests", "fixtures"):
            root = os.path.join(src, d)
            if os.path.isdir(root):
                for base, _, files in os.walk(root):
                    for f in files:
                        if "__pycache__" not in base:
                            full = os.path.join(base, f)
                            protected.append((full, os.path.join(dst, os.path.relpath(full, src))))
        for f in os.listdir(os.path.join(src, "starter")):
            if f.endswith(".py") and f not in function_files:
                protected.append((os.path.join(src, "starter", f), os.path.join(dst, f)))
        for orig, there in protected:
            pristine = open(orig, "rb").read()
            if not os.path.exists(there) or open(there, "rb").read() != pristine:
                modified.append(os.path.relpath(there, dst))
            os.makedirs(os.path.dirname(there), exist_ok=True)
            open(there, "wb").write(pristine)
        if "--oracle" in sys.argv:
            for f in os.listdir(os.path.join(src, "_solution")):
                if f.endswith(".py"):
                    shutil.copy(os.path.join(src, "_solution", f), dst)
        cases = pytest_cases(dst, ["tests"])
        return result(cases, modified=modified)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print(json.dumps(main()))
