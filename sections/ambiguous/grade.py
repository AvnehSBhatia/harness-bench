#!/usr/bin/env python3
"""Grade one ambiguous-spec task with its hidden tests (tasks/<task>/hidden), which pin the reading the repository
supports. Visible tests and data files are put back as shipped first.

  python3 grade.py <task> <workspace> [--oracle]
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import pytest_cases, result, scratch_copy  # noqa: E402

PROTECTED_DIRS = ("tests", "data", "fixtures", "docs", "invoices", "config", "content")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    task, ws = args[0], os.path.abspath(args[1])
    src = os.path.join(HERE, "tasks", task)
    tmp, dst = scratch_copy(ws)
    try:
        modified = []
        repo = os.path.join(src, "repo")
        for base, _, files in os.walk(repo):
            rel_base = os.path.relpath(base, repo)
            if rel_base.split(os.sep)[0] not in PROTECTED_DIRS:
                continue
            for f in files:
                orig = os.path.join(base, f)
                there = os.path.join(dst, rel_base, f)
                pristine = open(orig, "rb").read()
                if not os.path.exists(there) or open(there, "rb").read() != pristine:
                    modified.append(os.path.join(rel_base, f))
                os.makedirs(os.path.dirname(there), exist_ok=True)
                open(there, "wb").write(pristine)
        if "--oracle" in sys.argv:
            shutil.copytree(os.path.join(src, "solution"), dst, dirs_exist_ok=True)
        shutil.copytree(os.path.join(src, "hidden"), os.path.join(dst, "_hidden"))
        cases = pytest_cases(dst, ["_hidden"])
        return result(cases, modified=modified)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    print(json.dumps(main()))
