#!/usr/bin/env python3
"""Checks every section task before a run: the reference solution passes all hidden cases and the starting workspace
passes none (or only cases it passes by doing nothing). Writes sections/VALIDATION.md. Exit 1 on any problem."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
rows, bad = [], 0
for section in ("fleet", "ambiguous", "quick"):
    sdir = os.path.join(HERE, section)
    for t in json.load(open(os.path.join(sdir, "tasks.json"))):
        tmp = tempfile.mkdtemp()
        ws = os.path.join(tmp, "ws")
        try:
            subprocess.run([sys.executable, os.path.join(sdir, "prepare.py"), t["id"], ws], check=True, capture_output=True)
            g = lambda *extra: json.loads(subprocess.run([sys.executable, os.path.join(sdir, "grade.py"), t["id"], ws, *extra], capture_output=True, text=True).stdout.strip().splitlines()[-1])
            o, s = g("--oracle"), g()
            ok = o["works"] and not s["works"]
            bad += not ok
            rows.append(f"| {section} | {t['id']} | {o['passed']}/{o.get('total')} | {s['passed']}/{s.get('total')} | {'ok' if ok else 'PROBLEM'} |")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
md = "| Section | Task | Reference passes | Starting workspace passes | Check |\n| --- | --- | --- | --- | --- |\n" + "\n".join(rows) + "\n"
open(os.path.join(HERE, "VALIDATION.md"), "w").write(md)
print(md)
print("all good" if not bad else f"{bad} problem(s)")
sys.exit(1 if bad else 0)
