#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5001

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

Unit 9: every /ask — answered, refused or failed — is recorded by
`metrics.py::record` from the `finally` in `ask()`, into logs/runs.jsonl.
Failures are classified by `errors.py::classify`, which is the only thing that
decides a status code; a caller gets `error`, `error_kind` and `request_id`,
never exception text (that goes to the log).
"""

import importlib.util
import os
import time
import uuid

from flask import Flask, jsonify, request

import config
import metrics
from errors import BadInputError, classify

metrics.configure(server="flask-dev")

app = Flask(__name__)


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            # Cheap: checks the package is importable, doesn't load the model.
            "reranker": (
                "ok" if importlib.util.find_spec("sentence_transformers") else "degraded"
            ),
            "log_path": str(config.LOG_FILE),
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.

    Every call — including 400s, 5xx and timeouts — leaves exactly one record,
    because the write lives in the `finally`.
    """
    from app import ask_pipeline

    request_id = uuid.uuid4().hex[:8]
    t0 = time.perf_counter()
    question_text = None
    rec: dict = {"request_id": request_id, "endpoint": "/ask"}

    try:
        payload = request.get_json(silent=True)
        question = payload.get("question") if isinstance(payload, dict) else None
        if not isinstance(question, str) or not question.strip():
            raise BadInputError(stage="bad_input")
        question = question.strip()
        question_text = question
        if len(question) > config.MAX_QUESTION_CHARS:
            raise BadInputError(
                f"Question is too long (max {config.MAX_QUESTION_CHARS} characters).",
                stage="bad_input",
            )

        outcome = ask_pipeline(question, corpus=config.CORPUS, request_id=request_id)
        status = 200
        body = {
            "request_id": request_id,
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
            "degraded": outcome["degraded"],
        }
        degraded = outcome["degraded"]["rerank"] == "degraded"
        rec.update(
            outcome=(
                "refused"
                if outcome["refused"]
                else ("degraded_answered" if degraded else "answered")
            ),
            error_kind=None,
            http_status=200,
            degraded=outcome["degraded"],
            stage_ms=outcome["stage_ms"],
            n_results=outcome["n_results"],
            n_candidates=outcome["n_candidates"],
            refused=outcome["refused"],
            answer_chars=outcome["answer_chars"],
            tokens_in=outcome["tokens_in"],
            tokens_out=outcome["tokens_out"],
            attempts=outcome["attempts"],
            pacing_ms=outcome["pacing_ms"],
        )
    except Exception as exc:  # noqa: BLE001 — classified, never leaked
        err = classify(exc)
        status = err.http_status
        body = {
            "error": err.user_message,
            "message": err.user_message,
            "error_kind": err.kind,
            "request_id": request_id,
        }
        rec.update(
            outcome="error",
            error_kind=err.kind,
            reason=err.reason,
            stage=err.stage,
            http_status=status,
            detail=(err.detail or "")[:300] or None,
            stage_ms=err.stage_ms,
        )
    finally:
        rec.update(
            question=(question_text or "")[:200] or None,
            duration_ms=round((time.perf_counter() - t0) * 1000, 1),
            model=config.MODEL,
        )
        metrics.record(**rec)

    response = jsonify(body)
    response.status_code = status
    response.headers["X-Request-Id"] = request_id
    return response


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    # 5001, not 5000: macOS's AirPlay Receiver listens on 5000.
    port = int(os.getenv("PORT", "5001"))
    metrics.configure(server="flask-dev", port=port)

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    # Load the models now, before listening, so the first request is as fast as
    # the hundredth (unit 9, criterion 5). Costs a few seconds of start-up.
    from store import warm_up

    print("Loading models (a few seconds)...", flush=True)
    print(f"Models ready in {warm_up():.1f}s.\n", flush=True)

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
