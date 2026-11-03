import re

UNITS = {"d": 86400, "h": 3600, "m": 60, "s": 1, "ms": 0.001}
PART = re.compile(r"(\d+)(ms|d|h|m|s)")


def parse_duration(text):
    """Seconds in a duration string."""
    if not isinstance(text, str) or not re.fullmatch(r"(?:\d+(?:ms|d|h|m|s))+", text.strip()):
        raise ValueError(f"bad duration: {text!r}")
    total = 0
    for n, unit in PART.findall(text.strip()):
        total += int(n) * UNITS[unit]
    return total
