import csv

from .phone import normalize_phone

SUPPORTED = ("US", "GB")  # other countries are not supported yet: normalize_phone returns None for them


def import_rows(rows):
    kept, skipped = [], 0
    for row in rows:
        phone = normalize_phone(row["phone"], row["country"])
        if phone is None:  # unparseable or unsupported: keep the customer, drop the phone
            skipped += 1
        kept.append({**row, "phone": phone or ""})
    return kept, skipped


def import_file(path):
    with open(path, newline="") as f:
        return import_rows(list(csv.DictReader(f)))
