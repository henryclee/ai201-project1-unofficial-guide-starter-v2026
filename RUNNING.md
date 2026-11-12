# Running this project

Everything about how the starter works and how to use it.

---

## Before your first class

Setup happens **before class**, not during it. The
[environment setup page](../pages/ide_setup) has the per-operating-system
commands, the exact versions, and where to get your API key.

The short version, from inside this repo after you've forked and cloned it:

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then paste your key into .env
python test.py
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then paste your key into .env
python test.py
```

**You're ready when `python test.py` passes.** The first run is slow — it
downloads the embedding model, about 80 MB. That's exactly why this happens
before class rather than during it.

The model comes down from Chroma's own servers, not from Hugging Face, and
embedding runs entirely on your machine. If your network blocks one of those
and not the other, this is the one that has to get through:
`chroma-onnx-models.s3.amazonaws.com`.

If it doesn't pass and you've made one honest attempt at the error, post the
**whole** output in the help channel. Setup problems are normal and nobody has
ever been judged for having one.

> **Activate the virtual environment every time you open a new terminal.** You
> should see `(.venv)` at the start of your prompt. Installing into your system
> Python instead is the single most common cause of "it worked yesterday."

---

## Your first five minutes

```bash
python app.py corpora                     # see what's available
python app.py index                       # build the search index
python app.py ask "is the housing lottery random?"
```

That's the whole pipeline running end to end. The answer won't be great yet —
you're checking that it runs at all and that your key works.

To use a different corpus:

```bash
python app.py --corpus city_guides index
python app.py --corpus city_guides ask "how do I get to Kestrelford?"
```

Or set `CORPUS` in `config.py` once and stop typing it. **Re-run `index` after
switching corpora.**

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment. Run it whenever something feels off |
| `python app.py corpora` | Lists the provided corpora with a one-line description |
| `python app.py index` | Loads, chunks, embeds and stores your corpus. Run after any change to chunking |
| `python app.py ask "question"` | Asks one question, end to end |
| `python app.py ask` | Keeps asking until you press Enter on an empty line |
| `python app.py chunks` | Prints sample chunks — **Milestone 3** |
| `python app.py retrieve "question"` | Shows distances without spending a model call — **Milestone 4** |
| `python run_eval.py --label before` | Runs every test question three times, puts every `OUT_OF_SCOPE` question through the gate, and writes a run log — **unit 2** |

Useful flags:

| Flag | Works on | What it does |
|---|---|---|
| `--corpus NAME` | all | Use a different corpus without editing `config.py` |
| `--variant NAME` | `index`, `ask`, `retrieve` | Keep two different indexes of the same corpus side by side |
| `-n 5` | `chunks` | How many chunks to print |
| `--top-k 8` | `ask`, `retrieve` | Retrieve more or fewer chunks |
| `--threshold 0.7` | `ask` | Try a different relevance cutoff without editing `config.py` |
| `--label before` | `run_eval.py` | Names the output file, so before and after are distinguishable |

---

## Which command goes with which milestone

| Milestone | What you're doing | Command |
|---|---|---|
| 1 | Pick a corpus and see it work | `app.py corpora`, `app.py index`, `app.py ask "..."` |
| 2 | Write your acceptance criteria | Edit `criteria.md` and `questions.py` |
| 3 | Swap in your own chunker | Edit `chunker.py`, then `app.py index` and `app.py chunks` |
| 4 | Tune retrieval, set your cutoff | `app.py retrieve "..."`, then edit `THRESHOLD` in `config.py` |
| 5 | Write it up | Fill in `README.md` |
| Unit 2 | Run the test, fix one thing, re-run | `run_eval.py --label before` … `run_eval.py --label after` |

`app.py chunks` prints each chunk with its **source file and the function that
produced it** — both of which your README has to name. Copy them straight
across.

`run_eval.py` also runs the five questions in `OUT_OF_SCOPE` at the bottom of
`questions.py` through retrieval and the relevance gate, and puts what happened
in the run log under its own heading. That's the evidence for criterion 3, and
it costs you nothing: a question the gate refuses never reaches the model, so
there is no API call. It runs them once rather than three times, because
retrieval is deterministic and the gate is a comparison against a fixed
number — three passes would produce the same three answers.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting worth changing: chunk size, overlap, top-k, the relevance cutoff |
| `ingest.py` | Loads documents off disk and cleans them — **stage 1** |
| `chunker.py` | Splits documents into chunks — **stage 2, and the file you replace in Milestone 3** |
| `store.py` | Embeds chunks, stores them, retrieves them with distances — **stages 3 and 4** |
| `gate.py` | The relevance gate. Refuses questions nothing came back close enough for |
| `generate.py` | Writes the answer — **stage 5**. The only thing that calls out to a service |
| `app.py` | The command line |
| `serve.py` | The same pipeline behind HTTP, for when it has to run as a service — **unit 9** |
| `run.sh` | The one start command: index if needed, then `serve.py` — **unit 9** |
| `errors.py`, `metrics.py`, `tools/faults.py` | The error taxonomy, the structured log and its reader, the fault harness — **unit 9** |
| `run_eval.py` | Runs your questions repeatedly and writes the run log |
| `questions.py` | Your five test questions, and the five out-of-corpus ones the gate should refuse. **You fill in the first five** |
| `criteria.md` | Your five acceptance criteria. **You fill this in** |
| `README.md` | Your submission |
| `corpora/` | The provided documents, and `corpora/README.md` describing each |
| `results/` | Run logs, written by `run_eval.py`. **Commit these** — they're your evidence |

The five stages matter more than they look. In unit 2 you diagnose each failure
by naming which stage caused it, so it's worth knowing now which file is which.

---

## About rate limits

The free tier allows a small number of calls per minute. `generate.py` handles
this for you:

- **It paces its own requests** and prints a message when it's waiting. **A
  pause is the starter doing its job, not a bug.**
- **It caches repeated prompts** while you're building, so re-running the same
  question twenty times while debugging costs one call.
- **Caching turns itself off during evaluation runs.** Three runs of the same
  question have to be three real answers, not one answer repeated.
- **It stops if a session makes an unreasonable number of calls**, rather than
  silently draining your whole day's allowance. If you hit that, you almost
  certainly have a loop running away — look for it before raising the limit in
  `config.py`.
- **It prints how many calls and tokens you've used** when you exit. The
  token counts come off the responses themselves, so they're a measurement of
  what a run cost rather than an estimate.

If you see a `429` or "resource exhausted" error, that's a rate limit and not a
broken key. Wait a minute and re-run.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `No index called '...'. Run python app.py index first.` | You haven't indexed, or you switched corpus without re-indexing |
| `No GEMINI_API_KEY found` | No `.env` file, or the key wasn't pasted in. On Windows check it didn't save as `.env.txt` |
| `No corpus at ...` | The corpus name is wrong. `python app.py corpora` lists the real ones |
| The system refuses everything | Your cutoff is too low for this corpus. Try `--threshold 0.75` to confirm, then set it properly in Milestone 4 |
| The system never refuses anything | Your cutoff is too high. Same process in reverse |
| `[rate limit] ... Waiting 34s` | Working as intended. Leave it |
| `QuotaGuard: This session has made 300 requests` | A loop is running away. Find it before raising the budget |
| Indexing is very slow | Expected on the first run — it's downloading the embedding model. Later runs are much faster |

Still stuck after one honest attempt? Post in the help channel with the full
error, what you ran, and what you expected. You are not expected to debug your
own machine alone.

---

## Running it somewhere else — **unit 9** (Path B: local, with logs)

The service runs on your own machine, started by one command, and every request
it answers leaves a structured record. It is **not** hosted: the retriever loads
two local models, which will not fit a 512 MB free tier, so this project takes
the brief's Path B. It is text only — JSON over two routes, driven with `curl`.
There is no page, no `GET /`, and no production server.

### Start it

```bash
./run.sh
```

That activates `.venv`, checks that `GEMINI_API_KEY` is set, pins the corpus to
`city_guides`, builds the index if there isn't one, and runs `python serve.py`
(Flask's development server) on **http://localhost:5001**. There is one way to
start it, on purpose.

**The first run looks like a hang and isn't.** With no index, `run.sh` prints
`no index for city_guides — building it now` and then downloads the ~80 MB
embedder before it embeds 115 chunks (about 5 s once the model is on disk). It
prints `index built.` when it is done. Every start-up then
prints `Loading models…` and takes about 3.5 s more, because it loads both models
(and runs one throwaway pass) before it begins listening — so the first
question is as fast as the hundredth (about 75 ms of retrieval, not ~3 s).

Port 5001 rather than 5000 because macOS's AirPlay Receiver already listens on
5000.

### Ask it — worked examples

In a second terminal:

```bash
curl -s localhost:5001/health
```
```json
{"corpus":"city_guides","detail":"ready","index_ready":true,"log_path":"…/logs/runs.jsonl","reranker":"ok","status":"ok"}
```

```bash
curl -s -X POST localhost:5001/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "How expensive is it to stay at Thornby Wells?"}'
```
```json
{"answer":"Prices are moderate and stable year-round (guide_thornby_wells.md).","best_distance":0.3158,"corpus":"city_guides","degraded":{"rerank":"ok"},"question":"How expensive is it to stay at Thornby Wells?","refused":false,"request_id":"4ed6ef91","sources":["guide_accessibility.md","guide_thornby_wells.md"],"threshold":0.65}
```

Every response carries a `request_id` (also in the `X-Request-Id` header) that
matches one line in the log. A question the corpus doesn't cover is a **200**
with `"refused": true` — the gate working, not an error.

### What a failure looks like

A failure is classified: a status code, an `error_kind`, and the `request_id`.
Never a traceback, never the provider's own text (that goes to the log).

```json
{"error":"The model did not answer in time. Try again.","error_kind":"model_timeout","message":"The model did not answer in time. Try again.","request_id":"266ae023"}
```

| Status | `error_kind` | When |
|---|---|---|
| 400 | `bad_input` | body isn't JSON, no `question`, `question` isn't a string, blank, or over 1000 characters |
| 503 | `no_index` | no index for the corpus — the message says to run `python app.py index` |
| 504 | `model_timeout` | one model call took longer than `GENERATION_TIMEOUT_S` (30 s) |
| 502 | `upstream` | the provider failed, rate limits were exhausted, the session budget was hit, or the model returned nothing (the log's `reason` says which) |
| 500 | `internal` | anything unanticipated — `request_id` only, no exception text |

The timeout bounds **one model call**, not the whole request: a pacing sleep
(`REQUESTS_PER_MINUTE`) or a retry happens outside it, so the worst case is
roughly `GENERATION_TIMEOUT_S × attempts + backoff + pacing`. A call that times
out keeps running on a background thread — the response is bounded, the work is
not cancelled.

If the cross-encoder can't load (see Environment), retrieval still answers from
the fused ranking and says so: `"degraded": {"rerank": "degraded"}`.

### The log

Every `/ask` — answered, refused or failed — appends one JSON line to
`logs/runs.jsonl`. Read it without writing code:

```bash
python metrics.py --summary          # counts, error kinds, latency, per-stage times
tail -n 5 logs/runs.jsonl            # the raw records
```

Fields: `ts`, `request_id`, `server`/`pid`/`port` (which process answered),
`question`, `outcome` (`answered | refused | degraded_answered | error`),
`error_kind`, `reason`, `stage`, `http_status`, `degraded`, `duration_ms`,
`stage_ms` (`retrieve`/`gate`/`generate`), token counts, `attempts`,
`pacing_ms` (time spent waiting on the rate limiter — if nonzero, that run's
latency is the limiter's), `detail` (the raw exception text, log only).

### Fault harness

`tools/faults.py` produces the bad path on demand, with real HTTP against a
throwaway server (cache off):

```bash
python tools/faults.py --list
python tools/faults.py --fault f4_empty_response
python tools/faults.py --all             # f1…f6; f3 and f6 call the real model
```

Set `AI201_LOG_DIR=somewhere` first if you don't want these in `logs/runs.jsonl`.

### Environment

| Setting | Value |
|---|---|
| Python | **3.12** (3.11–3.13 work; **not 3.14**) |
| Install | `python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` |
| Key | `cp .env.example .env`, paste `GEMINI_API_KEY` |
| Pinned dependencies | `requirements.txt` — Flask, chromadb 0.6, google-genai, rank-bm25, python-dotenv, posthog |
| Embedder (always) | Chroma's bundled ONNX `all-MiniLM-L6-v2`, **~80 MB**, from `chroma-onnx-models.s3.amazonaws.com`, cached in `~/.cache/chroma` |
| Reranker (optional) | cross-encoder `cross-encoder/ms-marco-MiniLM-L-6-v2`, **~88 MB** from Hugging Face; needs `pip install 'sentence-transformers>=3.4,<3.5'` (pulls in PyTorch: **~626 MB** of torch, the whole venv ≈ 1.4 GB) |
| Index | `chroma_db/`, 25 MB, rebuilt automatically by `run.sh` (~5 s) |

**The reranker is optional on purpose.** `requirements.txt` leaves out
`sentence-transformers` (PyTorch is the heavy part), so a clean install runs
**degraded**: answers come from the fused BM25 + embedding ranking, flagged
`degraded.rerank = "degraded"` in the response and the log. Before unit 9 that
install failed every question outright. To get reranked answers, install the
line in the table above. Every number in the README is labelled with which mode
produced it.

Optional environment variables: `AI201_CORPUS` (default `city_guides` under
`run.sh`, `campus_life` otherwise), `AI201_CACHE=0` (turn the response cache
off — do this when measuring), `AI201_MODEL`, `PORT` (default 5001),
`AI201_LOG_DIR` (where `runs.jsonl` goes, default `logs/`),
`AI201_GENERATION_TIMEOUT_S` (default 30), `AI201_MAX_QUESTION_CHARS`
(default 1000), `AI201_DEBUG=1` (Flask debugger — local only).

### Measuring what a run costs

Turn the cache off, or a repeated question reports zero tokens. With `./run.sh`
up in another terminal (restart it with `AI201_CACHE=0 ./run.sh`), run ten
different questions, spaced so you stay under 30 model calls a minute:

```bash
Q=(
  "Where can I go to eat at Givens Mill?"
  "How expensive is it to stay at Thornby Wells?"
  "What is the tram schedule in Marchwood on the weekend?"
  "What are good places to visit with limited mobility?"
  "Where can I go for bird watching?"
  "How often do buses run from Brightwater to Kestrelford on Saturdays?"
  "How long does the train take from Brightwater to the regional hub?"
  "Why is parking a problem in Halden Bay on summer weekends?"
  "Which walking route follows the old railway line that closed in 1963?"
  "Do the different bus operators in the region accept each other's tickets?"
)
for q in "${Q[@]}"; do
  curl -s -X POST localhost:5001/ask -H 'Content-Type: application/json' \
    -d "{\"question\": \"$q\"}" > /dev/null
done
python metrics.py --summary          # tokens_in / tokens_out / duration_ms
```

Tokens come off the model's own responses (`generate.py::_record_tokens`), one
pair per record in the log. The last five are measurement inputs, kept here and
not in `questions.py`, which stays units 1–2's test set.

---

## Stretch features

Optional, for extra credit. **Say what you're adding in your README before you
start** — a feature the README never claims earns nothing.

- **Metadata filtering** — let people narrow results by source or date. Chroma
  supports a `where` clause on `collection.query`; `store.py::search` is where
  it would go.
- **Conversational memory** — let the next question build on the last.
- **A second embedding model** — swap `EMBEDDING_MODEL` in `config.py`, index
  into a different `--variant`, and write down what moved. This is the one
  option that needs a package the default install doesn't have:
  `pip install 'sentence-transformers>=3.4,<3.5'` first. It's a large install
  (it brings PyTorch), so do it before class, not during. Expect your
  threshold to move too — a different model means different distances, and
  the 0.6 you measured in Milestone 4 was measured against this one.

`rank-bm25` is already installed for unit 2's hybrid-search option. The
dependency ships; the implementation is yours.

---

## A note on committing

Commit as you go — at least four new commits in unit 1, at least four more in
unit 2. Your commit history is what shows your criteria existed before your
results did.

**Do not delete and recreate this repository.** You submit the same URL both
units.

`results/` is deliberately **not** in `.gitignore`. Your run logs are evidence
that the test actually happened, and they're part of what gets graded.
