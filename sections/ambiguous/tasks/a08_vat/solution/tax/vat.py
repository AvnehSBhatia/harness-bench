import json
import os
from decimal import ROUND_HALF_UP, Decimal

RATES = json.load(open(os.path.join(os.path.dirname(__file__), "rates.json")))


def vat(net, country):
    """VAT due on a net amount in EUR, as a Decimal."""
    rate = Decimal(RATES[country])
    return (Decimal(str(net)) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
