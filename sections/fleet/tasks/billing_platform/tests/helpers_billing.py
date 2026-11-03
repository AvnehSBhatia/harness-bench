from decimal import Decimal as D
import pytest


def raises_msg(fn, msg, exc=ValueError):
    """fn() raises exc with exactly the message msg."""
    with pytest.raises(exc) as e:
        fn()
    assert str(e.value) == msg


RATES = {"USD": "1", "EUR": "0.5", "GBP": "0.8", "JPY": "150", "KWD": "0.3"}

API_PLAN = {"currency": "USD", "minimum": "5.00",
            "tiers": [{"up_to": 1000, "unit": "0"}, {"up_to": 10000, "unit": "0.002"}, {"up_to": None, "unit": "0.0015"}]}
GB_PLAN = {"currency": "EUR", "tiers": [{"up_to": None, "unit": "0.10"}]}

ACME = {"id": "acme", "currency": "EUR", "country": "DE", "plan": {"currency": "USD", "price": "300.00"},
        "usage_plans": {"api_calls": API_PLAN, "gb_hours": GB_PLAN}}
APRIL = {"start": "2026-04-01", "end": "2026-05-01"}

INVOICES = [
    {"id": "INV-1", "currency": "EUR", "total": "100.00", "issued": "2026-03-02", "terms": "NET30"},
    {"id": "INV-2", "currency": "EUR", "total": "1,200.00", "issued": "2026-03-16", "terms": "NET30"},
    {"id": "INV-3", "currency": "EUR", "total": "50.00", "issued": "2026-03-16", "terms": "NET14"},
    {"id": "INV-4", "currency": "USD", "total": "USD 75.00", "issued": "2026-02-18", "terms": "NET30"},
]


def pay(pid, amount, date, reference=None, currency="EUR"):
    return {"id": pid, "currency": currency, "amount": amount, "date": date, "reference": reference}
