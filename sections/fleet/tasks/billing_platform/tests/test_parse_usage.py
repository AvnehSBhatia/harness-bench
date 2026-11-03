from parse_usage import parse_usage
from helpers_billing import raises_msg

T = "2026-04-01T00:00:00Z"


def test_basic_line():
    assert parse_usage("e1|acme|api_calls|120|2026-04-03T10:00:00Z") == {
        "id": "e1", "account": "acme", "metric": "api_calls", "quantity": 120, "ts": "2026-04-03T10:00:00Z"}


def test_offsets_normalised_to_utc():
    r = parse_usage(" e2 | acme | gb_hours | 5 | 2026-04-30T23:30:00-02:00 ")
    assert r == {"id": "e2", "account": "acme", "metric": "gb_hours", "quantity": 5, "ts": "2026-05-01T01:30:00Z"}
    assert parse_usage("e3|acme|seats|1|2026-05-01T03:00:00+05:30")["ts"] == "2026-04-30T21:30:00Z"


def test_field_count():
    raises_msg(lambda: parse_usage("a|b|api_calls|1"), "bad line: expected 5 fields")
    raises_msg(lambda: parse_usage(f"a|b|api_calls|1|{T}|x"), "bad line: expected 5 fields")
    raises_msg(lambda: parse_usage(""), "bad line: expected 5 fields")


def test_empty_fields():
    raises_msg(lambda: parse_usage(f" |acme|api_calls|1|{T}"), "bad line: empty field")
    raises_msg(lambda: parse_usage(f"e|   |bogus|x|nope"), "bad line: empty field")


def test_metric_checked_before_quantity():
    raises_msg(lambda: parse_usage(f"e|a|API_CALLS|1|{T}"), "unknown metric: API_CALLS")
    raises_msg(lambda: parse_usage("e|a|bogus|x|nope"), "unknown metric: bogus")


def test_quantity_rules():
    raises_msg(lambda: parse_usage(f"e|a|seats|-1|{T}"), "bad quantity: -1")
    raises_msg(lambda: parse_usage(f"e|a|seats|1.5|{T}"), "bad quantity: 1.5")
    raises_msg(lambda: parse_usage(f"e|a|seats| |{T}"), "bad quantity: ")
    raises_msg(lambda: parse_usage("e|a|seats|x|nope"), "bad quantity: x")
    assert parse_usage(f"e|a|seats|007|{T}")["quantity"] == 7


def test_timestamp_rules():
    for ts in ["2026-04-01T00:00:00", "2026-02-30T00:00:00Z", "2026-04-01 00:00:00Z", "2026-04-01T00:00:00.5Z",
               "2026-04-01T24:00:00Z", "2026-04-01T00:00:00+0200", "2026-04-01"]:
        raises_msg(lambda: parse_usage(f"e|a|seats|1|{ts}"), f"bad timestamp: {ts}")


def test_zero_quantity_and_year_rollover():
    r = parse_usage("e9|a|seats|0|2026-12-31T22:00:00-03:00")
    assert r["quantity"] == 0 and r["ts"] == "2027-01-01T01:00:00Z"
