#!/usr/bin/env python3
"""Grade one quick task: put the original test file back (an edited test never counts), run it, count the cases.

  python3 grade.py <exercise> <workspace> [--oracle]   (--oracle grades the reference solution instead)
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import pytest_cases, result, scratch_copy  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ex, ws = args[0], os.path.abspath(args[1])
    src = os.path.join(HERE, "exercises", ex)
    cfg = json.load(open(os.path.join(src, ".meta", "config.json")))
    tmp, dst = scratch_copy(ws)
    try:
        modified = []
        for t in cfg["files"]["test"]:
            p = os.path.join(dst, t)
            pristine = open(os.path.join(src, t), "rb").read()
            if not os.path.exists(p) or open(p, "rb").read() != pristine:
                modified.append(t)
            open(p, "wb").write(pristine)
        if "--oracle" in sys.argv:
            for sol, ex_file in zip(cfg["files"]["solution"], cfg["files"]["example"]):
                shutil.copy(os.path.join(src, ex_file), os.path.join(dst, sol))
        cases = pytest_cases(dst, cfg["files"]["test"])
        return result(cases, modified=modified)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print(json.dumps(main()))
