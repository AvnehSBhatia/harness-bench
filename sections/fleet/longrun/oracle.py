"""Reference solutions for the 40 tickets, following every house rule. validate.py installs them to prove the hidden
tests are right and solvable. Each function imports what it needs, so its source can be copied on its own."""

from kit.errors import KitError


def slugify(s):
    """Return a URL slug for s. [T1]"""
    import re
    if not isinstance(s, str):
        raise KitError("s must be a str")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def count_vowels(s):
    """Count the vowels in s. [T2]"""
    if not isinstance(s, str):
        raise KitError("s must be a str")
    return sum(1 for c in s.lower() if c in "aeiou")


def is_palindrome(s):
    """Check whether s is a palindrome. [T3]"""
    if not isinstance(s, str):
        raise KitError("s must be a str")
    t = [c for c in s.lower() if c in "abcdefghijklmnopqrstuvwxyz0123456789"]
    return t == t[::-1]


def reverse_words(s):
    """Reverse the order of the words in s. [T4]"""
    if not isinstance(s, str):
        raise KitError("s must be a str")
    return " ".join(reversed(s.split()))


def caesar(s, shift):
    """Shift the ASCII letters of s. [T5]"""
    if not isinstance(s, str) or not isinstance(shift, int):
        raise KitError("bad arguments")
    out = []
    for c in s:
        if "a" <= c <= "z":
            out.append(chr((ord(c) - 97 + shift) % 26 + 97))
        elif "A" <= c <= "Z":
            out.append(chr((ord(c) - 65 + shift) % 26 + 65))
        else:
            out.append(c)
    return "".join(out)


def wrap(s, width):
    """Greedy word wrap. [T6]"""
    if width < 1:
        raise KitError("width must be at least 1")
    lines = []
    for w in s.split():
        if lines and len(lines[-1]) + 1 + len(w) <= width:
            lines[-1] += " " + w
        else:
            lines.append(w)
    return lines


def initials(name):
    """Return the initials of name. [T7]"""
    if not isinstance(name, str) or not name.strip():
        raise KitError("name must be a non-empty str")
    return "".join(p[0].upper() + "." for p in name.split())


def run_length_encode(s):
    """Run-length encode s. [T8]"""
    import itertools
    if not isinstance(s, str) or any(c.isdigit() for c in s):
        raise KitError("s must be a str without digits")
    return "".join(f"{len(list(g))}{c}" for c, g in itertools.groupby(s))


def run_length_decode(s):
    """Decode run-length encoded s. [T9]"""
    import re
    if not isinstance(s, str):
        raise KitError("s must be a str")
    pairs = re.findall(r"(\d+)(\D)", s)
    if "".join(n + c for n, c in pairs) != s or any(int(n) == 0 for n, _ in pairs):
        raise KitError("malformed")
    return "".join(c * int(n) for n, c in pairs)


def camel_to_snake(s):
    """Convert camelCase to snake_case. [T10]"""
    import re
    if not isinstance(s, str):
        raise KitError("s must be a str")
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", s).lower()


def clamp(x, lo, hi):
    """Limit x to lo..hi. [T11]"""
    if lo > hi:
        raise KitError("lo > hi")
    return max(lo, min(hi, x))


def gcd_list(nums):
    """Greatest common divisor of nums. [T12]"""
    import math
    if not nums or not all(isinstance(n, int) for n in nums):
        raise KitError("nums must be a non-empty list of ints")
    return math.gcd(*nums)


def is_prime(n):
    """Check whether n is prime. [T13]"""
    if not isinstance(n, int):
        raise KitError("n must be an int")
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def digit_sum(n):
    """Sum of the decimal digits of n. [T14]"""
    if not isinstance(n, int):
        raise KitError("n must be an int")
    return sum(int(c) for c in str(abs(n)))


def to_roman(n):
    """Roman numeral for n. [T15]"""
    if not isinstance(n, int) or not 1 <= n <= 3999:
        raise KitError("n must be 1..3999")
    out = ""
    for v, r in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out += r
            n -= v
    return out


def from_roman(s):
    """Value of a Roman numeral. [T16]"""
    if not isinstance(s, str):
        raise KitError("s must be a str")
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not s or any(c not in vals for c in s):
        raise KitError("not a Roman numeral")
    total = sum(-vals[a] if vals[a] < vals[b] else vals[a] for a, b in zip(s, s[1:])) + vals[s[-1]]
    if not 1 <= total <= 3999 or to_roman(total) != s:
        raise KitError("not in standard form")
    return total


def mean(xs):
    """Arithmetic mean of xs. [T17]"""
    if not isinstance(xs, list) or not xs:
        raise KitError("xs must be a non-empty list")
    return sum(xs) / len(xs)


def median(xs):
    """Median of xs. [T18]"""
    if not isinstance(xs, list) or not xs:
        raise KitError("xs must be a non-empty list")
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def percent(part, whole, places=1):
    """part as a percentage of whole. [T19]"""
    if whole == 0:
        raise KitError("whole is 0")
    return round(100 * part / whole, places)


def fizzbuzz(n):
    """FizzBuzz from 1 to n. [T20]"""
    if not isinstance(n, int) or n < 0:
        raise KitError("n must be a non-negative int")
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i) for i in range(1, n + 1)]


def chunk(xs, n):
    """Split xs into lists of n items. [T21]"""
    if n < 1:
        raise KitError("n must be at least 1")
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def flatten(xs):
    """Flatten nested lists. [T22]"""
    if not isinstance(xs, list):
        raise KitError("xs must be a list")
    out = []
    for x in xs:
        if isinstance(x, list):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out


def dedupe(xs):
    """Remove duplicates from xs, keeping order. [T23]"""
    if not isinstance(xs, list):
        raise KitError("xs must be a list")
    return list(dict.fromkeys(xs))


def rotate(xs, k):
    """Rotate xs right by k. [T24]"""
    if not isinstance(k, int):
        raise KitError("k must be an int")
    if not xs:
        return []
    k %= len(xs)
    return xs[-k:] + xs[:-k] if k else list(xs)


def window(xs, n):
    """Sliding windows of n items. [T25]"""
    if n < 1:
        raise KitError("n must be at least 1")
    return [tuple(xs[i:i + n]) for i in range(len(xs) - n + 1)]


def interleave(a, b):
    """Alternate items of a and b. [T26]"""
    if not isinstance(a, list) or not isinstance(b, list):
        raise KitError("a and b must be lists")
    out = []
    for i in range(max(len(a), len(b))):
        if i < len(a):
            out.append(a[i])
        if i < len(b):
            out.append(b[i])
    return out


def frequencies(xs):
    """Count the items of xs. [T27]"""
    if not isinstance(xs, list):
        raise KitError("xs must be a list")
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


def pairwise_diff(xs):
    """Differences between neighbours. [T28]"""
    if not isinstance(xs, list):
        raise KitError("xs must be a list")
    return [b - a for a, b in zip(xs, xs[1:])]


def transpose(rows):
    """Transpose a list of lists. [T29]"""
    if len({len(r) for r in rows}) > 1:
        raise KitError("rows differ in length")
    return [list(c) for c in zip(*rows)]


def group_by_len(words):
    """Group words by length. [T30]"""
    if not isinstance(words, list) or not all(isinstance(w, str) for w in words):
        raise KitError("words must be a list of str")
    out = {}
    for w in words:
        out.setdefault(len(w), []).append(w)
    return dict(sorted(out.items()))


def is_leap(year):
    """Gregorian leap year. [T31]"""
    if not isinstance(year, int) or year < 1:
        raise KitError("bad year")
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year, month):
    """Days in a month. [T32]"""
    import calendar
    if not isinstance(month, int) or not 1 <= month <= 12 or year < 1:
        raise KitError("bad month or year")
    return calendar.monthrange(year, month)[1]


def day_of_year(year, month, day):
    """Day number within the year. [T33]"""
    import datetime
    try:
        d = datetime.date(year, month, day)
    except (ValueError, TypeError):
        raise KitError("no such date")
    return d.timetuple().tm_yday


def parse_duration(s):
    """Parse a duration like 1h30m. [T34]"""
    import re
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", s) if isinstance(s, str) else None
    if not s or not m:
        raise KitError("bad duration")
    h, mi, se = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + se


def format_duration(seconds):
    """Format seconds like 1h30m. [T35]"""
    if not isinstance(seconds, int) or seconds < 0:
        raise KitError("seconds must be a non-negative int")
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    out = (f"{h}h" if h else "") + (f"{m}m" if m else "") + (f"{s}s" if s else "")
    return out or "0s"


def hhmm_to_minutes(s):
    """Minutes after midnight for HH:MM. [T36]"""
    import re
    m = re.fullmatch(r"(\d\d):(\d\d)", s) if isinstance(s, str) else None
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        raise KitError("bad time")
    return int(m.group(1)) * 60 + int(m.group(2))


def minutes_to_hhmm(m):
    """HH:MM for minutes after midnight. [T37]"""
    if not isinstance(m, int):
        raise KitError("m must be an int")
    m %= 1440
    return f"{m // 60:02d}:{m % 60:02d}"


def weekday(year, month, day):
    """Day of the week, 0 for Monday. [T38]"""
    import datetime
    try:
        return datetime.date(year, month, day).weekday()
    except (ValueError, TypeError):
        raise KitError("no such date")


def add_days(year, month, day, n):
    """The date n days later. [T39]"""
    import datetime
    try:
        d = datetime.date(year, month, day) + datetime.timedelta(days=n)
    except (ValueError, TypeError):
        raise KitError("no such date")
    return (d.year, d.month, d.day)


def quarter(month):
    """Quarter of the year for month. [T40]"""
    if not isinstance(month, int) or not 1 <= month <= 12:
        raise KitError("month must be 1..12")
    return (month - 1) // 3 + 1
