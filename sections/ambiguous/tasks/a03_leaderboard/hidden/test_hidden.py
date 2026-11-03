import json
import os

from leaderboard import rank

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def e(name, score, at):
    return {"name": name, "score": score, "achieved_at": at}


def test_no_ties():
    assert rank([e("a", 10, "2026-01-01T00:00:00Z"), e("b", 30, "2026-01-02T00:00:00Z")]) == ["b", "a"]


def test_season_9():
    entries = json.load(open(os.path.join(HERE, "fixtures", "season-9-entries.json")))
    assert rank(entries) == ["cat", "amy", "bob", "zed", "eve", "dan"]


def test_ties_other_order():
    entries = [e("yan", 5, "2026-06-03T00:00:00Z"), e("abe", 5, "2026-06-09T00:00:00Z"), e("kim", 5, "2026-06-01T00:00:00Z")]
    assert rank(entries) == ["kim", "yan", "abe"]


def test_empty():
    assert rank([]) == []
