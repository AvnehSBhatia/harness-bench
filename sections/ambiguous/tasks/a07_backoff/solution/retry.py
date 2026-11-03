def backoff_delays(retries):
    """Seconds to wait before each retry."""
    if retries < 0:
        raise ValueError("retries must be >= 0")
    return [min(2 ** i, 30) for i in range(min(retries, 6))]
