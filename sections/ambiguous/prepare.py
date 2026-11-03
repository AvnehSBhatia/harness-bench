#!/usr/bin/env python3
"""Ambiguous specs: small repositories whose TASK.md leaves a gap or can be read two ways. The repository itself
settles it (a data file, a caller, a runbook, a design mock, an old receipt), the way a real codebase does.
Seven tasks ship a few visible tests for the parts that are not in doubt; three ship no tests at all.

  python3 prepare.py <task> <workspace>
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import git_init  # noqa: E402


def main():
    task, ws = sys.argv[1], os.path.abspath(sys.argv[2])
    shutil.copytree(os.path.join(HERE, "tasks", task, "repo"), ws, ignore=shutil.ignore_patterns("__pycache__"))
    git_init(ws)


if __name__ == "__main__":
    main()
