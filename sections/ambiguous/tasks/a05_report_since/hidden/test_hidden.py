import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(*flags):
    return subprocess.run([sys.executable, "report.py", "data/orders.csv", *flags], cwd=HERE, capture_output=True, text=True)


@pytest.mark.parametrize("flags,orders,revenue", [
    ((), 6, "155.50"),
    (("--until", "2026-10-05"), 4, "65.50"),
    (("--since", "2026-10-05"), 4, "125.50"),
    (("--since", "2026-10-06"), 2, "90.00"),
    (("--since", "2026-10-03", "--until", "2026-10-08"), 4, "95.50"),
    (("--since", "2026-10-13"), 0, "0.00"),
])
def test_counts(flags, orders, revenue):
    r = run(*flags)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [f"orders: {orders}", f"revenue: {revenue}"]


def test_bad_since_is_a_usage_error():
    r = run("--since", "05/10/2026")
    assert r.returncode == 2
    assert "--since" in r.stderr
