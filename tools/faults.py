#!/usr/bin/env python3
"""
Unit 9: the fault-injection harness — produces the bad path on demand.

    python tools/faults.py --fault f1_bad_input
    python tools/faults.py --all
    python tools/faults.py --list

Faults are injected at runtime from here, never by a switch inside production
code, so the code that is graded is the code that is tested. Each fault starts
its own server subprocess (the stubs are patched in-process by `--_serve`),
sends real HTTP with urllib, and prints: name, injection, status + body, and
whether a record appeared in the log.

  f1_bad_input      five malformed bodies               -> 400 bad_input
  f2_no_index       chroma_db moved aside               -> 503 no_index
  f3_invalid_key    bogus GEMINI_API_KEY (needs network)-> 502 upstream
  f4_empty_response model returns no text               -> 502 upstream/empty_response
  f5_hung_upstream  model call sleeps 120 s             -> 504 model_timeout in ~timeout
  f6_no_reranker    sentence_transformers un-importable -> 200, degraded.rerank=degraded

Logs go to config.LOG_FILE unless AI201_LOG_DIR is set in the environment.
"""

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

GOOD_QUESTION = "How expensive is it to stay at Thornby Wells?"


# ─── the in-process patches (run inside the server subprocess) ───────────────


def _stub_client(behaviour):
    class Models:
        def generate_content(self, **kwargs):
            return behaviour()

    return SimpleNamespace(models=Models())


def _serve_patched(fault: str):
    import generate

    if fault == "f4_empty_response":
        generate._client = _stub_client(lambda: SimpleNamespace(text=None, usage_metadata=None))
    elif fault == "f5_hung_upstream":

        def hang():
            time.sleep(120)
            return SimpleNamespace(text="too late", usage_metadata=None)

        generate._client = _stub_client(hang)
    import serve

    serve.main()


# ─── plumbing ────────────────────────────────────────────────────────────────


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _log_file() -> Path:
    import config

    return config.LOG_FILE


def _log_lines() -> int:
    f = _log_file()
    return len(f.read_text().splitlines()) if f.exists() else 0


def _start_server(fault: str, env_extra=None):
    port = _free_port()
    # AI201_CACHE=0: a cached answer would skip the model call a fault is trying
    # to break (the cache is keyed on the prompt, not the API key).
    env = {
        **os.environ,
        "PORT": str(port),
        "AI201_CORPUS": os.getenv("AI201_CORPUS", "city_guides"),
        "AI201_CACHE": "0",
    }
    env.update(env_extra or {})
    proc = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "--_serve", fault],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    for _ in range(120):
        try:
            urllib.request.urlopen(base + "/health", timeout=1)
            return proc, base
        except Exception:
            if proc.poll() is not None:
                raise RuntimeError(f"server exited early: {proc.stderr.read()}")
            time.sleep(0.5)
    proc.kill()
    raise RuntimeError("server did not come up")


def _post(base, body, raw=None, headers=None, timeout=90):
    data = raw if raw is not None else json.dumps(body).encode()
    req = urllib.request.Request(
        base + "/ask", data=data, headers=headers or {"Content-Type": "application/json"}, method="POST"
    )
    t = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, text = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        status, text = e.code, e.read().decode()
    return status, text, time.perf_counter() - t


def _show(name, injection, status, text, secs, before):
    after = _log_lines()
    print(f"--- {name}\n    injection: {injection}\n    status: {status}   client wall-clock: {secs:.1f}s")
    print(f"    body: {text.strip()[:400]}")
    print(f"    new log records: {after - before}\n")
    return status, text


def _kind(text):
    try:
        return json.loads(text).get("error_kind")
    except Exception:
        return None


# ─── the faults ──────────────────────────────────────────────────────────────


def f1_bad_input():
    proc, base = _start_server("none")
    results = []
    try:
        cases = [
            ("{}", {"body": {}}),
            ('{"question": 123}', {"body": {"question": 123}}),
            ('{"question": ""}', {"body": {"question": ""}}),
            ('{"question": "x"*5000}', {"body": {"question": "x" * 5000}}),
            ("not json", {"raw": b"this is not json", "headers": {"Content-Type": "text/plain"}}),
        ]
        for label, kw in cases:
            before = _log_lines()
            status, text, secs = _post(base, kw.get("body"), kw.get("raw"), kw.get("headers"))
            _show("f1_bad_input", label, status, text, secs, before)
            results.append(status == 400 and _kind(text) == "bad_input")
    finally:
        proc.kill()
    return all(results), f"{sum(results)}/{len(results)} bad bodies -> 400 bad_input"


def f2_no_index():
    import config

    moved = config.CHROMA_DIR.with_name(config.CHROMA_DIR.name + ".bak")
    shutil.move(str(config.CHROMA_DIR), str(moved))
    proc = None
    try:
        proc, base = _start_server("none")
        before = _log_lines()
        status, text, secs = _post(base, {"question": GOOD_QUESTION})
        _show("f2_no_index", "chroma_db moved aside", status, text, secs, before)
        ok = status == 503 and _kind(text) == "no_index" and "python app.py index" in text and "Traceback" not in text
    finally:
        if proc:
            proc.kill()
        # The server recreated an empty chroma_db while it was missing: remove it,
        # or the move below nests the real index inside it.
        shutil.rmtree(config.CHROMA_DIR, ignore_errors=True)
        shutil.move(str(moved), str(config.CHROMA_DIR))
    return ok, "503 no_index naming `python app.py index`"


def f3_invalid_key():
    proc, base = _start_server("none", {"GEMINI_API_KEY": "AI201_invalid_key_for_testing"})
    try:
        before = _log_lines()
        status, text, secs = _post(base, {"question": GOOD_QUESTION})
        _show("f3_invalid_key", "GEMINI_API_KEY=AI201_invalid_key_for_testing", status, text, secs, before)
        ok = status == 502 and _kind(text) == "upstream" and "API key" not in text and "INVALID" not in text.upper().replace("BAD_INPUT", "")
    finally:
        proc.kill()
    return ok, "502 upstream, provider text not quoted"


def f4_empty_response():
    proc, base = _start_server("f4_empty_response")
    try:
        before = _log_lines()
        status, text, secs = _post(base, {"question": GOOD_QUESTION})
        _show("f4_empty_response", "generate._get_client stubbed to return text=None", status, text, secs, before)
        ok = status == 502 and _kind(text) == "upstream" and '"answer"' not in text
    finally:
        proc.kill()
    return ok, "502 upstream (empty_response), never a 200 with answer=''"


def f5_hung_upstream():
    import config

    proc, base = _start_server("f5_hung_upstream")
    try:
        before = _log_lines()
        status, text, secs = _post(base, {"question": GOOD_QUESTION}, timeout=config.GENERATION_TIMEOUT_S + 60)
        _show("f5_hung_upstream", "model call sleeps 120 s", status, text, secs, before)
        ok = status == 504 and _kind(text) == "model_timeout" and secs < config.GENERATION_TIMEOUT_S + 10
    finally:
        proc.kill()
    return ok, f"504 model_timeout in {secs:.1f}s (bound {config.GENERATION_TIMEOUT_S:g}s)"


def f6_no_reranker():
    tmp = tempfile.mkdtemp()
    (Path(tmp) / "sentence_transformers.py").write_text('raise ImportError("fault f6: reranker unavailable")\n')
    proc, base = _start_server("none", {"PYTHONPATH": tmp + os.pathsep + os.getenv("PYTHONPATH", "")})
    try:
        before = _log_lines()
        status, text, secs = _post(base, {"question": GOOD_QUESTION})
        _show("f6_no_reranker", "sentence_transformers shadowed by a module that raises ImportError", status, text, secs, before)
        body = json.loads(text) if status == 200 else {}
        ok = status == 200 and body.get("degraded", {}).get("rerank") == "degraded" and bool(body.get("answer"))
    finally:
        proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)
    return ok, "200 with degraded.rerank == 'degraded' and an answer"


FAULTS = {f.__name__: f for f in (f1_bad_input, f2_no_index, f3_invalid_key, f4_empty_response, f5_hung_upstream, f6_no_reranker)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fault", choices=sorted(FAULTS))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--_serve", help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args._serve:
        _serve_patched(args._serve)
        return
    if args.list or not (args.fault or args.all):
        print("\n".join(FAULTS))
        return
    names = sorted(FAULTS) if args.all else [args.fault]
    verdicts = []
    for name in names:
        ok, summary = FAULTS[name]()
        verdicts.append((name, ok, summary))
    print("=" * 60)
    for name, ok, summary in verdicts:
        print(f"{'OK  ' if ok else 'FAIL'} {name}: {summary}")
    sys.exit(0 if all(ok for _, ok, _ in verdicts) else 1)


if __name__ == "__main__":
    main()
