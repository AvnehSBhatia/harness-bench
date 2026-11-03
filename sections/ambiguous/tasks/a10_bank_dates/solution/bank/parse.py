import datetime


def parse_bank_date(text):
    """The date of a transaction in the bank's CSV export."""
    return datetime.datetime.strptime(text.strip(), "%d/%m/%Y").date()
