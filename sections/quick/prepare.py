#!/usr/bin/env python3
"""Quick tasks: one Aider Polyglot (Exercism) Python exercise per run.

  python3 prepare.py <exercise> <workspace>

The workspace gets the stub, the unit tests and the instructions (.docs), never the reference solution (.meta).
TASK.md carries the same prompt Aider-style runners use, word for word for every exercise.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import git_init  # noqa: E402


def main():
    ex, ws = sys.argv[1], os.path.abspath(sys.argv[2])
    src = os.path.join(HERE, "exercises", ex)
    cfg = json.load(open(os.path.join(src, ".meta", "config.json")))
    shutil.copytree(src, ws, ignore=shutil.ignore_patterns(".meta", "__pycache__"))
    docs = ".docs/instructions.md and .docs/instructions.append.md" if os.path.exists(os.path.join(src, ".docs", "instructions.append.md")) else ".docs/instructions.md"
    task = (
        "Solve the Exercism exercise in this directory.\n\n"
        f"Read the instructions in {docs}. Implement the solution in {', '.join(cfg['files']['solution'])}, keeping the existing "
        f"function and class names, since the unit tests in {', '.join(cfg['files']['test'])} call them. Use only the standard "
        "library. Do not modify the test files.\n\nRun the tests with: python3 -m pytest -q\nStop when all tests pass.\n"
    )
    open(os.path.join(ws, "TASK.md"), "w").write(task)
    git_init(ws)


if __name__ == "__main__":
    main()
