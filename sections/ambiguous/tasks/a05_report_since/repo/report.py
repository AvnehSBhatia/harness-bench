import argparse
import csv
import datetime
from decimal import Decimal


def parse_day(parser, flag, value):
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        parser.error(f"{flag} must be YYYY-MM-DD")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Orders report")
    parser.add_argument("orders")
    parser.add_argument("--until", help="only count orders on or before this day (YYYY-MM-DD)")
    args = parser.parse_args(argv)
    until = parse_day(parser, "--until", args.until) if args.until else None
    n, revenue = 0, Decimal("0")
    with open(args.orders, newline="") as f:
        for row in csv.DictReader(f):
            day = datetime.date.fromisoformat(row["date"])
            if until and day > until:
                continue
            n += 1
            revenue += Decimal(row["amount"])
    print(f"orders: {n}")
    print(f"revenue: {revenue:.2f}")


if __name__ == "__main__":
    main()
