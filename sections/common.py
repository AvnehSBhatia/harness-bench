"""Shared by the section graders: run pytest in a scratch copy, count test cases from JUnit XML, start a git repo."""
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

SKIP = shutil.ignore_patterns("target", "__pycache__", ".pytest_cache", ".git", "node_modules", ".venv", "venv")


def pytest_cases(cwd, targets, timeout=900):
    """Run pytest on targets inside cwd; return passed/failed/errors/total test cases and the failing names."""
    xml = os.path.join(cwd, ".junit.xml")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=cwd)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={xml}", *targets],
                           cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
        tail = (r.stdout + r.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 0, "errors": 1, "total": 0, "failing": [], "tail": "pytest timed out"}
    out = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "total": 0, "failing": [], "tail": tail}
    if not os.path.exists(xml):
        out["errors"] = 1
        return out
    for tc in ET.parse(xml).getroot().iter("testcase"):
        out["total"] += 1
        kids = {c.tag for c in tc}
        name = f'{tc.get("classname", "")}::{tc.get("name", "")}'
        if "failure" in kids:
            out["failed"] += 1
            out["failing"].append(name)
        elif "error" in kids:
            out["errors"] += 1
            out["failing"].append(name)
        elif "skipped" in kids:
            out["skipped"] += 1
        else:
            out["passed"] += 1
    return out


def scratch_copy(ws):
    tmp = tempfile.mkdtemp(prefix="hb-grade-")
    dst = os.path.join(tmp, "ws")
    shutil.copytree(ws, dst, ignore=SKIP, symlinks=True)
    return tmp, dst


def git_init(ws):
    for cmd in (["git", "init", "--quiet"], ["git", "add", "-A"],
                ["git", "-c", "user.email=bench@heliod.dev", "-c", "user.name=bench", "commit", "--quiet", "-m", "start"]):
        subprocess.run(cmd, cwd=ws, check=True, capture_output=True)


def result(cases, expected=None, modified=(), build="ok"):
    expected = expected if expected is not None else cases["total"]
    rules = [f"edited a protected file: {m}" for m in modified]
    return {
        "works": cases["passed"] == expected and expected > 0 and not cases["failed"] and not cases["errors"],
        "passed": cases["passed"],
        "failed": cases["failed"],
        "errors": cases["errors"],
        "total": cases["total"],
        "expected_passed": expected,
        "build": build,
        "rules": rules,
        "detail": {"failing": cases["failing"][:50], "tail": cases.get("tail", "")[-800:], "protected_files_edited": list(modified)},
    }
