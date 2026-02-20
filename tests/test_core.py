from app.parser import parse_lines
from app.analyzer import cluster_errors

def test_parse_and_cluster():
    text = "2026-02-20 12:00:00,001 INFO api - hello\n2026-02-20 12:00:01,000 ERROR api - NullPointerException at X\n"
    entries, stats = parse_lines(text)
    assert stats["parsed"] == 2
    clusters = cluster_errors(entries)
    assert len(clusters) == 1
    assert clusters[0].count == 1
