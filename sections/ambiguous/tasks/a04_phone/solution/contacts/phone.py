import re


def normalize_phone(raw, country):
    """Return the number in E.164 form."""
    if not isinstance(raw, str):
        return None
    digits = re.sub(r"\D", "", raw)
    if country == "US":
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
        return "+1" + digits if len(digits) == 10 else None
    if country == "GB":
        if digits.startswith("44"):
            digits = digits[2:]
        elif digits.startswith("0"):
            digits = digits[1:]
        else:
            return None
        return "+44" + digits if len(digits) == 10 else None
    return None
