#!/usr/bin/env python3
"""
Unit 9: the structured log, and the reader that makes it observable.

    python metrics.py --summary              summarise logs/runs.jsonl
    python metrics.py --summary --file PATH  summarise another log

Writer: `record(**fields)` appends ONE JSON object per line to config.LOG_FILE
(logs/runs.jsonl, or $AI201_LOG_DIR/runs.jsonl). It never raises — accounting
never breaks the thing it is accounting for — but a failed write prints one
line to stderr so a silent logging failure is still findable.

Reader: `--summary` answers "what happened?" without adding code first: counts
by outcome and error kind, latency, where failures came from, tokens.
"""

import argparse
import json
import os
import statistics
import sys
from datetime import datetime
from pathlib import Path

import config

# Set once per process by serve.py. Provenance: which process answered.
_provenance = {"server": "cli", "pid": os.getpid(), "port": None}


def configure(server=None, port=None):
    if server is not None:
        _provenance["server"] = server
    if port is not None:
        _provenance["port"] = port


def record(**fields) -> None:
    """Append one record. Never raises."""
    try:
        entry = {
            "ts": datetime.now().astimezone().isoformat(timespec="milliseconds"),
            **_provenance,
            **fields,
        }
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(config.LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [metrics] could not write the log: {exc}", file=sys.stderr, flush=True)


def read(path=None) -> list[dict]:
    path = Path(path or config.LOG_FILE)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _stats(values):
    values = [v for v in values if isinstance(v, (int, float))]
    if not values:
        return "n/a"
    return (
        f"mean {statistics.mean(values):.0f}  median {statistics.median(values):.0f}  "
        f"max {max(values):.0f}  (n={len(values)})"
    )


def summary(rows: list[dict]) -> str:
    if not rows:
        return "No records."
    out = [f"{len(rows)} records"]

    def counts(key, label):
        tally: dict = {}
        for r in rows:
            k = r.get(key)
            tally[str(k)] = tally.get(str(k), 0) + 1
        out.append(f"{label}: " + ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))

    counts("outcome", "outcome")
    counts("error_kind", "error_kind")
    counts("http_status", "http_status")

    out.append("duration_ms (all):      " + _stats([r.get("duration_ms") for r in rows]))
    answered = [r for r in rows if r.get("outcome") in ("answered", "degraded_answered")]
    out.append("duration_ms (answered): " + _stats([r.get("duration_ms") for r in answered]))

    for stage in ("retrieve", "gate", "generate"):
        vals = [(r.get("stage_ms") or {}).get(stage) for r in rows]
        out.append(f"stage_ms.{stage:<9}     " + _stats(vals))

    failures = [r for r in rows if r.get("outcome") == "error"]
    if failures:
        tally: dict = {}
        for r in failures:
            k = f"{r.get('stage')}:{r.get('error_kind')}"
            tally[k] = tally.get(k, 0) + 1
        out.append("failures by stage:error_kind: " + ", ".join(f"{k}={v}" for k, v in sorted(tally.items())))

    degraded = sum(1 for r in rows if (r.get("degraded") or {}).get("rerank") == "degraded")
    out.append(f"degraded rerank: {degraded}/{len(rows)}")
    out.append("tokens_in:  " + _stats([r.get("tokens_in") for r in rows if r.get("tokens_in")]))
    out.append("tokens_out: " + _stats([r.get("tokens_out") for r in rows if r.get("tokens_out")]))
    nonzero = sum(1 for r in rows if (r.get("pacing_ms") or 0) > 0)
    out.append(f"runs with pacing_ms > 0: {nonzero}  (those latencies include the rate limiter)")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--summary", action="store_true", help="summarise the log")
    ap.add_argument("--file", help="log file (default: config.LOG_FILE)")
    args = ap.parse_args()
    if not args.summary:
        ap.print_help()
        return
    print(summary(read(args.file)))


if __name__ == "__main__":
    main()
