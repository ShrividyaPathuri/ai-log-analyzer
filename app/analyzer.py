from collections import Counter, defaultdict
from typing import List, Dict, Tuple
import re
from .schemas import LogEntry, ErrorCluster

EXC_RE = re.compile(r"(Exception|Error|Traceback|Caused by:)", re.IGNORECASE)

def level_counts(entries: List[LogEntry]) -> Dict[str, int]:
    c = Counter()
    for e in entries:
        if e.level:
            c[e.level] += 1
    return dict(c)

def signature_for(entry: LogEntry) -> str:
    msg = entry.message.strip()
    m = re.search(r"([A-Za-z0-9_]+(?:Exception|Error))", msg)
    if m:
        exc = m.group(1)
        norm = re.sub(r"\b\d+\b", "<n>", msg)
        norm = re.sub(r"\b[0-9a-f]{8,}\b", "<hex>", norm, flags=re.IGNORECASE)
        return f"{exc}: {norm[:160]}"
    norm = re.sub(r"\b\d+\b", "<n>", msg)
    norm = re.sub(r"\b[0-9a-f]{8,}\b", "<hex>", norm, flags=re.IGNORECASE)
    return norm[:180] if norm else "<empty>"

def cluster_errors(entries: List[LogEntry], top_k: int = 8) -> List[ErrorCluster]:
    buckets = defaultdict(list)
    for e in entries:
        is_errorish = (e.level in ("ERROR", "FATAL")) or bool(EXC_RE.search(e.message))
        if is_errorish:
            buckets[signature_for(e)].append(e)

    clusters: List[Tuple[str, List[LogEntry]]] = sorted(buckets.items(), key=lambda kv: len(kv[1]), reverse=True)
    out: List[ErrorCluster] = []
    for sig, items in clusters[:top_k]:
        out.append(ErrorCluster(
            signature=sig,
            count=len(items),
            sample_lines=[it.line_no for it in items[:5]],
            sample_messages=[it.message[:220] for it in items[:3]],
        ))
    return out
