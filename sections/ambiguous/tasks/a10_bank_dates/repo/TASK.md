# Bank export dates

Implement `parse_bank_date(text)` in `bank/parse.py`. It reads the transaction dates in our bank's CSV export
(`data/` has last month's) and returns a `datetime.date`. Anything that isn't a valid date raises `ValueError`.
