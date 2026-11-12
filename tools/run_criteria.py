#!/usr/bin/env python3
"""
Unit 9: run the five criteria in criteria.md once (one trial) and print real output.

    python tools/run_criteria.py --trial 1 [--phase before] [--only 1 2 3 4 5]

Each trial gets its own log directory, logs/<phase>-t<N>/cK/, so "exactly one
record per request" is countable per criterion. The cache is off for every
server it starts. Nothing here is imported by production code.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import config  # noqa: E402
import faults  # noqa: E402
from questions import OUT_OF_SCOPE, QUESTIONS  # noqa: E402

LEAKS = ["Traceback", "API key", "INVALID_ARGUMENT", "API_KEY_INVALID"]
GOOD = "How expensive is it to stay at Thornby Wells?"
BAD_BODIES = [
    ("{}", {"body": {}}),
    ('{"question": 123}', {"body": {"question": 123}}),
    ('{"question": ""}', {"body": {"question": ""}}),
    ('{"question": "x"*5000}', {"body": {"question": "x" * 5000}}),
    ("not json", {"raw": b"this is not json", "headers": {"Content-Type": "text/plain"}}),
]


def kind_of(text):
    try:
        return json.loads(text).get("error_kind")
    except Exception:
        return None


def clip(text, n=170):
    return text.strip().replace("\n", " ")[:n]


def run_sh_server(logdir: Path):
    """Start ./run.sh (the documented command) on a free port with its own log dir."""
    port = faults._free_port()
    env = {**os.environ, "PORT": str(port), "AI201_CACHE": "0", "AI201_LOG_DIR": str(logdir)}
    proc = subprocess.Popen(["./run.sh"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f"http://127.0.0.1:{port}"
    import urllib.request

    for _ in range(180):
        try:
            urllib.request.urlopen(base + "/health", timeout=1)
            return proc, base
        except Exception:
            if proc.poll() is not None:
                raise RuntimeError("run.sh exited early")
            time.sleep(0.5)
    proc.kill()
    raise RuntimeError("run.sh did not come up")


def logrows(logdir: Path):
    f = logdir / "runs.jsonl"
    return [json.loads(line) for line in f.read_text().splitlines()] if f.exists() else []


# ─── criterion 1 ─────────────────────────────────────────────────────────────


def c1(logdir: Path):
    os.environ["AI201_LOG_DIR"] = str(logdir)
    results = []

    def judge(label, status, text, secs, want_status, want_kind, must_contain=None, forbid_answer=False):
        ok = status == want_status and kind_of(text) == want_kind
        ok = ok and not any(leak in text for leak in LEAKS)
        if must_contain:
            ok = ok and must_contain in text
        if forbid_answer:
            ok = ok and '"answer"' not in text
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {status} {kind_of(text)}  ({secs:.1f}s)  {clip(text)}")
        results.append(ok)

    proc, base = faults._start_server("none")
    try:
        for label, kw in BAD_BODIES:
            s, t, secs = faults._post(base, kw.get("body"), kw.get("raw"), kw.get("headers"))
            judge(f"f1 {label}", s, t, secs, 400, "bad_input")
    finally:
        proc.kill()

    moved = config.CHROMA_DIR.with_name(config.CHROMA_DIR.name + ".bak")
    shutil.move(str(config.CHROMA_DIR), str(moved))
    proc = None
    try:
        proc, base = faults._start_server("none")
        s, t, secs = faults._post(base, {"question": GOOD})
        judge("f2 no_index", s, t, secs, 503, "no_index", must_contain="python app.py index")
    finally:
        if proc:
            proc.kill()
        shutil.rmtree(config.CHROMA_DIR, ignore_errors=True)
        shutil.move(str(moved), str(config.CHROMA_DIR))

    proc, base = faults._start_server("none", {"GEMINI_API_KEY": "AI201_invalid_key_for_testing"})
    try:
        s, t, secs = faults._post(base, {"question": GOOD})
        judge("f3 invalid_key", s, t, secs, 502, "upstream")
    finally:
        proc.kill()

    proc, base = faults._start_server("f4_empty_response")
    try:
        s, t, secs = faults._post(base, {"question": GOOD})
        judge("f4 empty_response", s, t, secs, 502, "upstream", forbid_answer=True)
    finally:
        proc.kill()

    return sum(results), len(results), f"{sum(results)}/{len(results)}"


# ─── criterion 2 ─────────────────────────────────────────────────────────────


def c2(logdir: Path):
    os.environ["AI201_LOG_DIR"] = str(logdir)
    proc, base = faults._start_server("f5_hung_upstream")
    try:
        s, t, secs = faults._post(base, {"question": GOOD}, timeout=120)
    finally:
        proc.kill()
    ok = s == 504 and kind_of(t) == "model_timeout" and secs <= 35
    print(f"  [{'PASS' if ok else 'FAIL'}] f5 hung upstream: {s} {kind_of(t)} in {secs:.1f}s (limit 35 s)  {clip(t)}")
    return int(ok), 1, f"{int(ok)}/1 ({secs:.1f}s)"


# ─── criterion 3 ─────────────────────────────────────────────────────────────


def c3(logdir: Path):
    os.environ["AI201_LOG_DIR"] = str(logdir)
    shadow = tempfile.mkdtemp()
    (Path(shadow) / "sentence_transformers.py").write_text('raise ImportError("c3: reranker unavailable")\n')
    proc, base = faults._start_server("none", {"PYTHONPATH": shadow + os.pathsep + os.getenv("PYTHONPATH", "")})
    passed = 0
    try:
        for q in QUESTIONS:
            s, t, secs = faults._post(base, {"question": q["question"]})
            try:
                body = json.loads(t)
            except Exception:
                body = {}
            answer = body.get("answer") or ""
            sources = body.get("sources") or []
            named = any(src in answer for src in sources)
            ok = (
                s == 200
                and body.get("degraded", {}).get("rerank") == "degraded"
                and bool(answer.strip())
                and bool(sources)
                and named
            )
            passed += ok
            print(
                f"  [{'PASS' if ok else 'FAIL'}] {q['question'][:48]!r}: {s} degraded={body.get('degraded')} "
                f"sources={len(sources)} names_source={named} ({secs:.1f}s)  {clip(answer, 110)}"
            )
    finally:
        proc.kill()
        shutil.rmtree(shadow, ignore_errors=True)
    return passed, len(QUESTIONS), f"{passed}/{len(QUESTIONS)}"


# ─── criterion 4 ─────────────────────────────────────────────────────────────


def c4(logdir: Path):
    proc, base = run_sh_server(logdir)
    sent = 0
    try:
        for label, kw in BAD_BODIES:
            faults._post(base, kw.get("body"), kw.get("raw"), kw.get("headers"))
            sent += 1
        for q in QUESTIONS:
            faults._post(base, {"question": q["question"]})
            sent += 1
        for q in OUT_OF_SCOPE[:2]:
            faults._post(base, {"question": q})
            sent += 1
    finally:
        proc.kill()
    lines = (logdir / "runs.jsonl").read_text().splitlines()
    parsed, bad_lines = [], 0
    for line in lines:
        try:
            parsed.append(json.loads(line))
        except Exception:
            bad_lines += 1
    complete = [
        r
        for r in parsed
        if all(r.get(k) is not None for k in ("ts", "outcome", "duration_ms", "question"))
    ]
    incomplete = [r for r in parsed if r not in complete]
    print(f"  requests sent: {sent}   log lines: {len(lines)}   unparseable: {bad_lines}   complete: {len(complete)}/{len(parsed)}")
    for r in incomplete:
        missing = [k for k in ("ts", "outcome", "duration_ms", "question") if r.get(k) is None]
        print(f"    incomplete: request_id={r.get('request_id')} outcome={r.get('outcome')} missing={missing}")
    ok = len(lines) == sent == 12 and bad_lines == 0 and len(complete) == 12
    return int(ok), 1, f"{len(complete)}/12 complete, {len(lines)} lines for {sent} requests"


# ─── criterion 5 ─────────────────────────────────────────────────────────────


def c5(logdir: Path):
    passed = 0
    for i in range(1, 4):
        d = logdir / f"r{i}"
        proc, base = run_sh_server(d)
        try:
            s, t, secs = faults._post(base, {"question": QUESTIONS[1]["question"]})
        finally:
            proc.kill()
        rows = logrows(d)
        retrieve = (rows[-1].get("stage_ms") or {}).get("retrieve") if rows else None
        ok = retrieve is not None and retrieve <= 500
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] restart {i}: first /ask status {s}, stage_ms.retrieve = {retrieve} ms (limit 500)")
        time.sleep(2)
    return passed, 3, f"{passed}/3 restarts"


CRITERIA = {1: c1, 2: c2, 3: c3, 4: c4, 5: c5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trial", type=int, required=True)
    ap.add_argument("--phase", default="before")
    ap.add_argument("--only", type=int, nargs="*")
    args = ap.parse_args()
    base = ROOT / "logs" / f"{args.phase}-t{args.trial}"
    summary = {}
    print(f"=== {args.phase} trial {args.trial}  ({time.strftime('%Y-%m-%d %H:%M:%S')}) ===")
    for n in args.only or sorted(CRITERIA):
        print(f"\nCriterion {n}")
        t0 = time.time()
        _, _, label = CRITERIA[n](base / f"c{n}")
        summary[n] = label
        print(f"  -> criterion {n}: {label}  [{time.time() - t0:.0f}s]")
    print("\nSUMMARY " + json.dumps(summary))


if __name__ == "__main__":
    main()
