from .money import from_cents, to_cents


def split_bill(total, people):
    cents = to_cents(total)
    base, extra = divmod(cents, people)
    return [from_cents(base + (1 if i < extra else 0)) for i in range(people)]
