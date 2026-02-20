import re
from typing import List, Tuple, Dict
from .schemas import LogEntry

TS = r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d{3})?(?:Z)?)"
LEVEL = r"(?P<level>TRACE|DEBUG|INFO|WARN|ERROR|FATAL)"
SERVICE = r"(?P<service>[\w\-\.]+)"
SEP = r"(?:\s+|\s*\|\s*)"

PATTERNS = [
    re.compile(rf"^{TS}{SEP}{LEVEL}{SEP}{SERVICE}\s*-\s*(?P<msg>.*)$"),
    re.compile(rf"^{TS}{SEP}{LEVEL}{SEP}(?P<msg>.*)$"),
    re.compile(rf"^{LEVEL}{SEP}{SERVICE}\s*-\s*(?P<msg>.*)$"),
]

def parse_lines(text: str) -> Tuple[List[LogEntry], Dict[str, int]]:
    entries: List[LogEntry] = []
    stats = {"parsed": 0, "unparsed": 0}

    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip("\n")
        if not line.strip():
            stats["unparsed"] += 1
            continue

        matched = None
        for p in PATTERNS:
            m = p.match(line)
            if m:
                matched = m
                break

        if matched:
            d = matched.groupdict()
            entries.append(LogEntry(
                line_no=i,
                timestamp=d.get("ts"),
                level=(d.get("level") or "").upper() or None,
                service=d.get("service"),
                message=d.get("msg") or "",
                raw=line,
            ))
            stats["parsed"] += 1
        else:
            entries.append(LogEntry(
                line_no=i, timestamp=None, level=None, service=None,
                message=line, raw=line
            ))
            stats["unparsed"] += 1

    return entries, stats
