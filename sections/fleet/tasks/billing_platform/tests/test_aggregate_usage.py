from aggregate_usage import aggregate_usage
from helpers_billing import raises_msg

S, E = "2026-04-01T00:00:00Z", "2026-05-01T00:00:00Z"
LINES = [
    "# usage export 2026-04",
    "u1|acme|api_calls|1000|2026-04-01T00:00:00Z",
    "u2|acme|api_calls|500|2026-04-15T12:00:00Z",
    "u3|acme|gb_hours|30|2026-04-20T08:00:00+02:00",
    "u4|beta|seats|3|2026-04-10T00:00:00Z",
    "",
    "u5|acme|api_calls|700|2026-03-31T23:59:59Z",
    "u6|beta|api_calls|0|2026-04-11T00:00:00Z",
]


def test_totals_per_account_and_metric():
    assert aggregate_usage(LINES, S, E) == {"acme": {"api_calls": 1500, "gb_hours": 30},
                                            "beta": {"seats": 3, "api_calls": 0}}


def test_offsets_near_the_edges():
    lines = ["v1|acme|seats|1|2026-05-01T01:00:00+02:00", "v2|acme|seats|2|2026-03-31T23:00:00-02:00",
             "v3|acme|seats|4|2026-04-01T01:00:00+02:00"]
    assert aggregate_usage(lines, S, E) == {"acme": {"seats": 3}}


def test_closing_instant():
    lines = ["w1|acme|api_calls|10|2026-05-01T00:00:00Z", "w2|acme|api_calls|5|2026-04-30T23:59:59Z",
             "w3|acme|api_calls|7|2026-05-01T02:00:00+02:00", "w4|beta|seats|1|2026-05-01T00:00:00Z"]
    assert aggregate_usage(lines, S, E) == {"acme": {"api_calls": 5}}


def test_duplicate_ids_first_wins():
    lines = ["d1|acme|api_calls|10|2026-04-02T00:00:00Z", "d1|acme|api_calls|99|2026-04-03T00:00:00Z",
             "d2|acme|api_calls|5|2026-03-15T00:00:00Z", "d2|acme|api_calls|50|2026-04-05T00:00:00Z"]
    assert aggregate_usage(lines, S, E) == {"acme": {"api_calls": 10}}


def test_comments_and_blank_lines():
    lines = ["   ", "  # comment|x", "\t", "c1|a|seats|1|2026-04-02T00:00:00Z"]
    assert aggregate_usage(lines, S, E) == {"a": {"seats": 1}}
    assert aggregate_usage([], S, E) == {}


def test_bad_line_raises():
    lines = ["c1|a|seats|1|2026-04-02T00:00:00Z", "x|acme|api_calls|1.5|2026-04-02T00:00:00Z"]
    raises_msg(lambda: aggregate_usage(lines, S, E), "bad quantity: 1.5")


def test_window_validation():
    raises_msg(lambda: aggregate_usage([], E, S), "empty period")
    raises_msg(lambda: aggregate_usage([], S, S), "empty period")
    raises_msg(lambda: aggregate_usage([], "2026-04-01", E), "bad timestamp: 2026-04-01")


def test_window_given_with_offsets():
    lines = ["o1|a|gb_hours|2|2026-03-31T22:30:00Z", "o2|a|gb_hours|3|2026-04-01T21:59:59Z",
             "o3|a|gb_hours|4|2026-03-31T21:59:59Z"]
    assert aggregate_usage(lines, "2026-04-01T00:00:00+02:00", "2026-04-02T00:00:00+02:00") == {"a": {"gb_hours": 5}}
