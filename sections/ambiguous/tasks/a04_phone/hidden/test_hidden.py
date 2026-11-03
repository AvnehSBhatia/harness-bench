import csv
import os

import pytest

from contacts.import_customers import import_file
from contacts.phone import normalize_phone

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize("raw,country,want", [
    ("(415) 555-0100", "US", "+14155550100"),
    ("415.555.0101", "US", "+14155550101"),
    ("+1 415 555 0102", "US", "+14155550102"),
    ("1-415-555-0103", "US", "+14155550103"),
    ("020 7946 0958", "GB", "+442079460958"),
    ("+44 20 7946 0959", "GB", "+442079460959"),
    ("07700 900123", "GB", "+447700900123"),
])
def test_valid(raw, country, want):
    assert normalize_phone(raw, country) == want


@pytest.mark.parametrize("raw,country", [("555-0100", "US"), ("01 23 45 67 89", "FR"), ("", "US"), ("not a phone", "GB")])
def test_none(raw, country):
    assert normalize_phone(raw, country) is None


def test_import_matches_sample():
    kept, skipped = import_file(os.path.join(HERE, "data", "customers-sample.csv"))
    with open(os.path.join(HERE, "data", "customers-sample.imported.csv"), newline="") as f:
        want = [r["phone"] for r in csv.DictReader(f)]
    assert [r["phone"] for r in kept] == want
    assert skipped == 2
