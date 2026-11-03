def rank(entries):
    """entries: dicts with name, score and achieved_at (ISO time). Returns the names in leaderboard order."""
    return [e["name"] for e in sorted(entries, key=lambda e: (-e["score"], e["achieved_at"]))]
