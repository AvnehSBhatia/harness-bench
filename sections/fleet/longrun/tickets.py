"""The 40 tickets of the long-session test. One source for TICKETS.md (spec, examples) and the hidden grader.

Each ticket: id, module, name, params, spec, invalid (what counts as invalid input, in words), examples (shown),
bad (invalid examples, shown), hidden (graded only), hidden_bad (graded only). Cases are (args, expected).
"""

T = []


def ticket(id, module, name, params, spec, invalid, examples, bad, hidden, hidden_bad):
    T.append(dict(id=id, module=module, name=name, params=params, spec=spec, invalid=invalid, examples=examples, bad=bad, hidden=hidden, hidden_bad=hidden_bad))


# kit/text.py
ticket(1, "text", "slugify", "s", "Return a URL slug: lowercase s, turn every run of characters other than a-z and 0-9 into a single hyphen, and strip hyphens from both ends.", "s is not a str.",
       [(("Hello, World!",), "hello-world"), (("  Rust & Python 3 ",), "rust-python-3")], [(42,)],
       [(("",), ""), (("---",), ""), (("Café au lait",), "caf-au-lait"), (("ABC",), "abc"), (("a__b..c",), "a-b-c")], [(None,), (["a"],)])
ticket(2, "text", "count_vowels", "s", "Count the vowels a, e, i, o, u in s, ignoring case (y is not a vowel).", "s is not a str.",
       [(("Hello World",), 3), (("",), 0)], [(3.5,)],
       [(("AEIOUaeiou",), 10), (("rhythm",), 0), (("Programming",), 3)], [(None,)])
ticket(3, "text", "is_palindrome", "s", "True if s reads the same backwards, looking only at the characters a-z and 0-9 after lowercasing (everything else is ignored). A string with no such characters is a palindrome.", "s is not a str.",
       [(("A man, a plan, a canal: Panama",), True), (("hello",), False)], [(121,)],
       [(("",), True), (("!!",), True), (("No 'x' in Nixon",), True), (("ab",), False), (("12321",), True), (("1231",), False)], [(None,)])
ticket(4, "text", "reverse_words", "s", "Return the words of s (split on any whitespace) in reverse order, joined by single spaces.", "s is not a str.",
       [(("the quick  brown fox",), "fox brown quick the")], [(["a", "b"],)],
       [(("",), ""), (("  one  ",), "one"), (("a\tb\nc",), "c b a")], [(None,)])
ticket(5, "text", "caesar", "s, shift", "Shift every ASCII letter in s by shift places through the alphabet, wrapping around and keeping its case; leave every other character unchanged. shift can be any integer, including negative.", "s is not a str, or shift is not an int.",
       [(("abc", 1), "bcd"), (("Hello, World!", 3), "Khoor, Zruog!")], [(123, 1), ("abc", "1")],
       [(("xyz", 3), "abc"), (("ABC", -1), "ZAB"), (("abc", 27), "bcd"), (("abc", -27), "zab"), (("é1 ", 5), "é1 ")], [("abc", 1.5), (None, 1)])
ticket(6, "text", "wrap", "s, width", "Greedy word wrap: split s on whitespace and fill lines left to right, adding a word to the current line if the line stays at most width characters long (words separated by one space), otherwise starting a new line. A word longer than width gets a line of its own, unbroken. Return the list of lines; an empty or all-whitespace s gives [].", "width is less than 1.",
       [(("the quick brown fox", 10), ["the quick", "brown fox"])], [("abc", 0)],
       [(("", 5), []), (("a b c d", 3), ["a b", "c d"]), (("supercalifragilistic is long", 10), ["supercalifragilistic", "is long"]), (("one two", 7), ["one two"]), (("one two", 6), ["one", "two"])], [("abc", -3)])
ticket(7, "text", "initials", "name", "Return the first letter of each whitespace-separated part of name, uppercased, each followed by a dot.", "name is not a str, or is empty or only whitespace.",
       [(("ada lovelace",), "A.L."), (("Grace Brewster Murray Hopper",), "G.B.M.H.")], [("",), ("   ",)],
       [(("x",), "X."), (("  alan   turing ",), "A.T.")], [(None,)])
ticket(8, "text", "run_length_encode", "s", "Write each run of the same character as its length followed by the character: 'aaabcc' becomes '3a1b2c'. Runs longer than 9 keep their full count ('12x').", "s is not a str, or contains a digit.",
       [(("aaabcc",), "3a1b2c"), (("",), "")], [("a1",)],
       [(("x" * 12,), "12x"), (("abc",), "1a1b1c"), (("  ",), "2 "), (("aAa",), "1a1A1a")], [("123",), (None,)])
ticket(9, "text", "run_length_decode", "s", "Decode the format run_length_encode writes: each run is a positive decimal count followed by one non-digit character.", "s is not a str, or is not made of count-character pairs: a character with no count before it, a count with no character after it, or a count of 0.",
       [(("3a1b2c",), "aaabcc"), (("12x",), "x" * 12)], [("a",), ("3",)],
       [(("",), ""), (("2 1!",), "  !"), (("10z",), "z" * 10)], [("0a",), ("3a2",), ("ab",), (None,)])
ticket(10, "text", "camel_to_snake", "s", "Insert an underscore before every uppercase ASCII letter that directly follows a lowercase ASCII letter or a digit, then lowercase the whole string.", "s is not a str.",
       [(("parseHttpResponse",), "parse_http_response"), (("HTTPServer",), "httpserver")], [(None,)],
       [(("",), ""), (("already_snake",), "already_snake"), (("version2Update",), "version2_update"), (("aB",), "a_b"), (("ABc",), "abc")], [(5,)])

# kit/nums.py
ticket(11, "nums", "clamp", "x, lo, hi", "Return x limited to the range lo..hi, inclusive.", "lo is greater than hi.",
       [((5, 0, 10), 5), ((-3, 0, 10), 0), ((12, 0, 10), 10)], [(1, 5, 0)],
       [((2.5, 0, 1), 1), ((0, 0, 0), 0), ((-1.5, -2, 2), -1.5)], [(0, 1, -1)])
ticket(12, "nums", "gcd_list", "nums", "Return the greatest common divisor of a non-empty list of integers. The result is never negative; the gcd of all zeros is 0.", "nums is empty, or contains something that is not an int.",
       [(([12, 18, 24],), 6), (([7],), 7)], [([],)],
       [(([0, 0],), 0), (([-4, 6],), 2), (([0, 5],), 5), (([-7],), 7), (([17, 34, 51, 5],), 1)], [([1, 2.5],)])
ticket(13, "nums", "is_prime", "n", "True if n is a prime number. Numbers below 2 are not prime.", "n is not an int.",
       [((7,), True), ((1,), False)], [(7.0,)],
       [((2,), True), ((0,), False), ((-7,), False), ((97,), True), ((91,), False), ((7919,), True), ((1_000_000,), False)], [("7",)])
ticket(14, "nums", "digit_sum", "n", "Return the sum of the decimal digits of n, ignoring its sign.", "n is not an int.",
       [((1234,), 10), ((-56,), 11)], [(3.0,)],
       [((0,), 0), ((9_999_999_999,), 90)], [("12",)])
ticket(15, "nums", "to_roman", "n", "Return n in standard Roman numerals (I V X L C D M, with the subtractive pairs IV IX XL XC CD CM).", "n is not an int from 1 to 3999.",
       [((1994,), "MCMXCIV"), ((4,), "IV")], [(0,), (4000,)],
       [((1,), "I"), ((3999,), "MMMCMXCIX"), ((58,), "LVIII"), ((444,), "CDXLIV")], [(-1,), (2.0,)])
ticket(16, "nums", "from_roman", "s", "Parse a Roman numeral written exactly the way to_roman writes it and return its value.", "s is not exactly what to_roman returns for some number from 1 to 3999 (for example 'IIII', 'IC', 'iv' or '').",
       [(("MCMXCIV",), 1994), (("IV",), 4)], [("IIII",), ("",)],
       [(("MMMCMXCIX",), 3999), (("LVIII",), 58), (("I",), 1)], [("IC",), ("iv",), ("VV",), ("MMMM",), (None,)])
ticket(17, "nums", "mean", "xs", "Return the arithmetic mean of a non-empty list of numbers, as a float.", "xs is not a list, or is empty.",
       [(([1, 2, 3, 4],), 2.5)], [([],)],
       [(([5],), 5.0), (([-1, 1],), 0.0), (([0.5, 0.25],), 0.375)], [(None,)])
ticket(18, "nums", "median", "xs", "Return the median of a non-empty list of numbers: the middle value of the sorted list, or, when the length is even, the mean of the two middle values as a float. Do not change xs.", "xs is not a list, or is empty.",
       [(([3, 1, 2],), 2), (([4, 1, 3, 2],), 2.5)], [([],)],
       [(([7],), 7), (([1, 2],), 1.5), (([5, 5, 1, 9],), 5.0)], [(None,)])
ticket(19, "nums", "percent", "part, whole, places=1", "Return part as a percentage of whole, rounded with Python's round() to places decimal places.", "whole is 0.",
       [((1, 3), 33.3), ((1, 3, 2), 33.33), ((5, 5), 100.0)], [(1, 0)],
       [((0, 7), 0.0), ((2, 8, 0), 25.0), ((-1, 4), -25.0)], [(3, 0, 2)])
ticket(20, "nums", "fizzbuzz", "n", "Return the list of strings for 1 to n: 'FizzBuzz' for multiples of 15, 'Fizz' for multiples of 3, 'Buzz' for multiples of 5, otherwise the number itself as a string. n = 0 gives [].", "n is not an int, or is negative.",
       [((5,), ["1", "2", "Fizz", "4", "Buzz"])], [(-1,)],
       [((0,), []), ((15,), ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"])], [(2.5,)])

# kit/seqs.py
ticket(21, "seqs", "chunk", "xs, n", "Split the list xs into consecutive lists of n items; the last one may be shorter. An empty xs gives [].", "n is less than 1.",
       [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])], [([1], 0)],
       [(([], 3), []), (([1, 2, 3], 3), [[1, 2, 3]]), (([1, 2], 5), [[1, 2]])], [([1], -2)])
ticket(22, "seqs", "flatten", "xs", "Flatten nested lists to any depth into one flat list, keeping order. Only lists are flattened; tuples, strings and everything else stay as items.", "xs is not a list.",
       [(([1, [2, [3, [4]]], 5],), [1, 2, 3, 4, 5])], [((1, 2),)],
       [(([],), []), (([[], [[]]],), []), (([(1, 2), "ab", [3]],), [(1, 2), "ab", 3])], [("abc",)])
ticket(23, "seqs", "dedupe", "xs", "Return a new list without duplicates, keeping the first occurrence of each item, in order. Items are hashable.", "xs is not a list.",
       [(([3, 1, 3, 2, 1],), [3, 1, 2])], [("aab",)],
       [(([],), []), ((["a", "A", "a"],), ["a", "A"]), (([None, None, 0],), [None, 0])], [((1, 1),)])
ticket(24, "seqs", "rotate", "xs, k", "Return a new list with xs rotated right by k places. k can be negative (rotate left) or larger than len(xs). An empty xs gives [].", "k is not an int.",
       [(([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]), (([1, 2, 3], -1), [2, 3, 1])], [([1, 2], 1.5)],
       [(([], 3), []), (([1, 2, 3], 3), [1, 2, 3]), (([1, 2, 3], 7), [3, 1, 2]), (([1, 2, 3], -4), [2, 3, 1])], [([1], "1")])
ticket(25, "seqs", "window", "xs, n", "Return the list of tuples of every n consecutive items of xs, in order; [] when n is larger than len(xs).", "n is less than 1.",
       [(([1, 2, 3, 4], 2), [(1, 2), (2, 3), (3, 4)])], [([1, 2], 0)],
       [(([1, 2], 3), []), (([1, 2, 3], 3), [(1, 2, 3)]), (([1, 2, 3], 1), [(1,), (2,), (3,)])], [([1], -1)])
ticket(26, "seqs", "interleave", "a, b", "Alternate items from the lists a and b, starting with a, then append whatever is left of the longer one.", "a or b is not a list.",
       [(([1, 2, 3], ["a", "b"]), [1, "a", 2, "b", 3])], [([1], "ab")],
       [(([], [1, 2]), [1, 2]), (([1], []), [1]), (([], []), [])], [((1,), [2])])
ticket(27, "seqs", "frequencies", "xs", "Return a dict from each item of xs to the number of times it occurs, with keys in the order the items first appear.", "xs is not a list.",
       [((["b", "a", "b"],), {"b": 2, "a": 1})], [("bab",)],
       [(([],), {}), (([1, 2, 1, 3, 1],), {1: 3, 2: 1, 3: 1})], [(None,)])
ticket(28, "seqs", "pairwise_diff", "xs", "Return [xs[1] - xs[0], xs[2] - xs[1], ...]; a list with fewer than 2 items gives [].", "xs is not a list.",
       [(([1, 4, 9, 16],), [3, 5, 7])], [("123",)],
       [(([],), []), (([5],), []), (([3, 1],), [-2]), (([0.5, 1],), [0.5])], [((1, 2),)])
ticket(29, "seqs", "transpose", "rows", "Transpose a list of equal-length lists, so the columns become rows. [] gives [].", "the rows do not all have the same length.",
       [(([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]])], [([[1, 2], [3]],)],
       [(([],), []), (([[1]],), [[1]]), (([[1, 2]],), [[1], [2]])], [([[1], [2, 3], [4]],)])
ticket(30, "seqs", "group_by_len", "words", "Group words by length: return a dict from each length to the list of words of that length, in their original order, with the keys in ascending order.", "words is not a list, or an item is not a str.",
       [((["bb", "a", "cc", "ddd"],), {1: ["a"], 2: ["bb", "cc"], 3: ["ddd"]})], [(["a", 1],)],
       [(([],), {}), ((["xyz", "ab", "q"],), {1: ["q"], 2: ["ab"], 3: ["xyz"]})], [("abc",)])

# kit/dates.py
ticket(31, "dates", "is_leap", "year", "True if year is a leap year in the Gregorian calendar.", "year is not an int, or is less than 1.",
       [((2024,), True), ((1900,), False), ((2000,), True)], [(0,)],
       [((2023,), False), ((2400,), True), ((2100,), False), ((4,), True)], [(-4,), (2024.0,)])
ticket(32, "dates", "days_in_month", "year, month", "Return the number of days in that month of that year.", "month is not 1 to 12, or year is less than 1.",
       [((2024, 2), 29), ((2023, 2), 28), ((2023, 4), 30)], [(2023, 13)],
       [((2023, 1), 31), ((1900, 2), 28), ((2000, 2), 29), ((2023, 12), 31)], [(2023, 0), (0, 5)])
ticket(33, "dates", "day_of_year", "year, month, day", "Return the number of the day within its year, 1 for January 1.", "the date does not exist.",
       [((2023, 1, 1), 1), ((2024, 3, 1), 61)], [(2023, 2, 29)],
       [((2023, 12, 31), 365), ((2024, 12, 31), 366), ((2023, 3, 1), 60)], [(2023, 4, 31), (2023, 0, 1), (2023, 1, 0)])
ticket(34, "dates", "parse_duration", "s", "Parse a duration such as '1h30m', '45s' or '2h5m10s' into seconds. Each part is a non-negative whole number followed by h, m or s; the parts come in the order h, m, s, each at most once, with no spaces, and at least one part is present.", "s is not a str in that format.",
       [(("1h30m",), 5400), (("45s",), 45), (("2h5m10s",), 7510)], [("",), ("90",), ("1m1h",)],
       [(("0s",), 0), (("100m",), 6000), (("1h1s",), 3601)], [("1h 30m",), ("1x",), ("h",), ("1h1h",), ("-5s",)])
ticket(35, "dates", "format_duration", "seconds", "Write a number of seconds the way parse_duration reads it, leaving out zero parts: 5410 is '1h30m10s', 3600 is '1h', 61 is '1m1s', and 0 is '0s'. Hours do not roll over into days.", "seconds is not an int, or is negative.",
       [((5410,), "1h30m10s"), ((0,), "0s")], [(-1,)],
       [((3600,), "1h"), ((61,), "1m1s"), ((86400,), "24h"), ((59,), "59s"), ((3601,), "1h1s")], [(1.5,)])
ticket(36, "dates", "hhmm_to_minutes", "s", "Convert a 24-hour time 'HH:MM' (exactly two digits each, from 00:00 to 23:59) to minutes after midnight.", "s is not a str holding a valid time in that format.",
       [(("07:05",), 425), (("23:59",), 1439)], [("24:00",), ("7:05",)],
       [(("00:00",), 0), (("12:30",), 750)], [("12:60",), ("1230",), ("ab:cd",), (None,)])
ticket(37, "dates", "minutes_to_hhmm", "m", "Convert minutes after midnight to 'HH:MM', wrapping around the day: 1440 is '00:00' and -1 is '23:59'.", "m is not an int.",
       [((425,), "07:05"), ((1440,), "00:00"), ((-1,), "23:59")], [(1.5,)],
       [((0,), "00:00"), ((1439,), "23:59"), ((3000,), "02:00"), ((-1440,), "00:00")], [("10",)])
ticket(38, "dates", "weekday", "year, month, day", "Return the day of the week: 0 for Monday through 6 for Sunday.", "the date does not exist.",
       [((2024, 1, 1), 0), ((2000, 1, 1), 5)], [(2023, 2, 30)],
       [((1970, 1, 1), 3), ((2024, 2, 29), 3), ((2026, 11, 2), 0)], [(2023, 13, 1)])
ticket(39, "dates", "add_days", "year, month, day, n", "Return the date n days after the given date (n can be negative) as a (year, month, day) tuple.", "the starting date does not exist.",
       [((2023, 12, 31, 1), (2024, 1, 1)), ((2024, 3, 1, -1), (2024, 2, 29))], [(2023, 2, 29, 1)],
       [((2024, 1, 1, 0), (2024, 1, 1)), ((2023, 1, 31, 30), (2023, 3, 2)), ((2000, 1, 1, 366), (2001, 1, 1))], [(2023, 4, 31, 1)])
ticket(40, "dates", "quarter", "month", "Return the quarter of the year, 1 to 4, that month falls in.", "month is not an int from 1 to 12.",
       [((1,), 1), ((6,), 2), ((12,), 4)], [(0,), (13,)],
       [((3,), 1), ((4,), 2), ((9,), 3), ((10,), 4)], [(2.0,)])

assert [t["id"] for t in T] == list(range(1, 41))
MODULES = ["text", "nums", "seqs", "dates"]
