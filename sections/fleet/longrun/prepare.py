#!/usr/bin/env python3
"""Build the starting repository for the long-session test.

  python3 prepare.py <task-id> <workspace>

kit/ is a small Python package with one finished ticket (T0) that shows the house rules. TICKETS.md states the four
house rules once, at the top, then 40 tickets that never mention them again.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tickets import MODULES, T  # noqa: E402

HOUSE_RULES = """# Tickets

## House rules (they apply to every ticket)

1. Invalid input raises `KitError` from `kit/errors.py`, never any other exception. Each ticket says what counts as
   invalid input.
2. The first line of each new function's docstring ends with the ticket id in square brackets, for example
   `\"\"\"Count the words in s. [T0]\"\"\"`.
3. Export each new function from `kit/__init__.py`: import it there and add its name to `__all__`.
4. Add one line per ticket to `CHANGELOG.md`: `- T<number> <function name>`, for example `- T0 word_count`.

Ticket T0 (done, in `kit/text.py`) follows all four.
"""

TASK_MD = """# Work through the tickets

`kit/` is a small Python utility package. `TICKETS.md` holds 40 tickets: do all of them, in order.

The house rules at the top of `TICKETS.md` apply to every ticket.

Hidden tests grade every ticket: its examples and more cases like them, the invalid inputs it describes, and the house
rules. `tests/` has an example test for ticket T0; add tests of your own if you like. Use only the Python standard
library.
"""

FILES = {
    "kit/__init__.py": '"""kit: small utilities."""\n\nfrom .errors import KitError\nfrom .text import word_count\n\n__all__ = ["KitError", "word_count"]\n',
    "kit/errors.py": '"""Errors raised by kit."""\n\n\nclass KitError(Exception):\n    """Raised for invalid input to any kit function."""\n',
    "kit/text.py": '"""Text utilities."""\n\nfrom .errors import KitError\n\n\ndef word_count(s):\n    """Count the words in s. [T0]"""\n    if not isinstance(s, str):\n        raise KitError("s must be a str")\n    return len(s.split())\n',
    "kit/nums.py": '"""Number utilities."""\n\nfrom .errors import KitError  # noqa: F401\n',
    "kit/seqs.py": '"""List utilities."""\n\nfrom .errors import KitError  # noqa: F401\n',
    "kit/dates.py": '"""Date and time utilities."""\n\nfrom .errors import KitError  # noqa: F401\n',
    "tests/test_t0.py": 'import pytest\n\nfrom kit import KitError, word_count\n\n\ndef test_word_count():\n    assert word_count("one two  three") == 3\n    assert word_count("") == 0\n\n\ndef test_word_count_invalid():\n    with pytest.raises(KitError):\n        word_count(None)\n',
    "CHANGELOG.md": "# Changelog\n\n- T0 word_count\n",
    "TASK.md": TASK_MD,
}


def call(name, args):
    return f"{name}({', '.join(repr(a) for a in args)})"


def tickets_md():
    out = [HOUSE_RULES]
    for t in T:
        out.append(f"## T{t['id']}: {t['name']} (`kit/{t['module']}.py`)\n")
        out.append(f"`{t['name']}({t['params']})`: {t['spec']}\n")
        out.append(f"Invalid input: {t['invalid']}\n")
        out.append("Examples:\n")
        out.append("```python")
        out += [f"{call(t['name'], a)} == {e!r}" for a, e in t["examples"]]
        out += [f"{call(t['name'], a)}  # invalid" for a in t["bad"]]
        out.append("```\n")
    return "\n".join(out)


def main():
    ws = os.path.abspath(sys.argv[2])
    if os.path.exists(ws):
        sys.exit(f"{ws} already exists")
    for path, text in {**FILES, "TICKETS.md": tickets_md()}.items():
        full = os.path.join(ws, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)
    for cmd in (["git", "init", "--quiet"], ["git", "add", "-A"], ["git", "-c", "user.email=bench@heliod.dev", "-c", "user.name=bench", "commit", "--quiet", "-m", "start"]):
        subprocess.run(cmd, cwd=ws, check=True, stdout=subprocess.DEVNULL)
    print(ws)


if __name__ == "__main__":
    assert MODULES == ["text", "nums", "seqs", "dates"]
    main()
