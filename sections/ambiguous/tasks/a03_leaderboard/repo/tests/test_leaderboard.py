from leaderboard import rank


def test_highest_first():
    entries = [
        {"name": "a", "score": 10, "achieved_at": "2026-01-01T00:00:00Z"},
        {"name": "b", "score": 30, "achieved_at": "2026-01-02T00:00:00Z"},
        {"name": "c", "score": 20, "achieved_at": "2026-01-03T00:00:00Z"},
    ]
    assert rank(entries) == ["b", "c", "a"]
