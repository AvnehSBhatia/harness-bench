from due_date import due_date
from helpers_billing import raises_msg


def test_net_terms():
    assert due_date("2026-04-01", "NET30") == "2026-05-01"
    assert due_date("2026-03-02", "NET14") == "2026-03-16"
    assert due_date("2026-02-03", "NET45") == "2026-03-20"


def test_net_zero():
    assert due_date("2026-04-01", "NET0") == "2026-04-01"
    assert due_date("2026-05-01", "NET0") == "2026-05-01"


def test_end_of_month():
    assert due_date("2026-04-15", "EOM") == "2026-04-30"
    assert due_date("2026-12-03", "EOM") == "2026-12-31"
    assert due_date("2026-03-31", "EOM") == "2026-03-31"


def test_spring_invoices():
    assert due_date("2026-04-02", "NET30") == "2026-05-04"
    assert due_date("2026-05-01", "EOM") == "2026-06-01"
    assert due_date("2026-01-31", "NET0") == "2026-02-02"


def test_bad_terms():
    for t in ["NET", "net30", "NET-5", "NET+5", "NET121", "NET 30", "EOM+5", "", "NET30 ", "30"]:
        raises_msg(lambda: due_date("2026-04-01", t), f"bad terms: {t}")


def test_crossing_year_end():
    assert due_date("2026-12-15", "NET30") == "2027-01-14"
    assert due_date("2026-06-10", "NET21") == "2026-07-01"


def test_leap_year():
    assert due_date("2028-02-15", "NET14") == "2028-02-29"
    assert due_date("2028-02-01", "EOM") == "2028-02-29"


def test_upper_limit():
    assert due_date("2026-01-05", "NET120") == "2026-05-05"
    assert due_date("2026-04-17", "NET14") == "2026-05-01"
