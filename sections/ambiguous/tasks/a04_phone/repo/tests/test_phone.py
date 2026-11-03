from contacts.phone import normalize_phone


def test_us():
    assert normalize_phone("(415) 555-0100", "US") == "+14155550100"


def test_gb_international():
    assert normalize_phone("+44 20 7946 0958", "GB") == "+442079460958"
