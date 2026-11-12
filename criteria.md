# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
One of my questions asks about places that are good to visit with limited mobility, 
and there are 3 listed under good, so the retriever may miss the expected chunk.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
Every RAG response should either be rejected as being out of scope, or have a relevant hit,
so every answer should be able to return at least one source document.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

My in-corpus questions had best distances from 0.196 to 0.601. My out-of-scope questions 
had best distances from 0.808 to 0.982. The gap between the two groups is 0.207 wide.
With a larger set of test and out of scope questions, the gap might narrow or there might 
be some overlap.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->
For all of the 5 test questions, every retrieved chunk includes context from 
the document, specifically the source document's heading and all subheadings 
prepended to the chunk text.

**Why this target:**

Without context, a chunk from an “Eat and drink” section doesn’t say which 
town it belongs to. The chunker will add context to chunks algorithmically, 
so every chunk should follow this format.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

Original: For question 4 ("What are good places to visit with limited mobility?"), the answer 
names all 3 towns the corpus lists under Straightforward: Thornby Wells, Marchwood, 
and Brightwater.

Revised: For question 4 ("What are good places to visit with limited mobility?"), the answer 
names 3 of the 3 towns the corpus lists under Straightforward: Thornby Wells, Marchwood, 
and Brightwater.
Why: 3 of 3 is more clearly a metric that I can measure

**Why this target:**

The guide_accessibility.md document sorts towns into Straightforward, Mixed, and 
Difficult sections, with three towns listed under Straightforward. Question 4 is 
phrased "what are good places…", which maps to the Straightforward section. An answer 
that names only one, or that stops at Thornby Wells, is incomplete.

I chose 3 of 3 as the criterion because the question asks for places, plural, and 
the corpus enumerates exactly 3 without qualification. The towns are named explicitly 
so the check is against these three specifically, not any three.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 9 criteria — the capstone extension

Unit 1's and unit 2's criteria above are untouched. These five are for unit 9's
work: a hardening layer around the pipeline (classified failures, a timeout,
a reranker fallback), the structured log, and the documented run path.

Written in Milestone 4, **after** the extension was built and **before** any of
these were tested. In fairness to the targets: I had already seen the Milestone 3
cost runs (warm `/ask`: 88 ms retrieve, ~9 s model call) and one cold first
request (~3.1 s). Criteria 3 and 5 are set at what a correct system should do,
not at what I'd already measured.

Every criterion is run **three times** with nothing changed in between, with
`AI201_CACHE=0` so a model call is a real call, and a fresh `AI201_LOG_DIR` per
trial. "Warm" means the server has already answered one request.

---

### 1. Injected failures come back classified, with nothing leaked  *(extension, bad path)*

**Target:** 8 of 8 injected failures return the expected status and `error_kind`
**and** a body that contains no `Traceback`, no provider text (`API key`,
`INVALID_ARGUMENT`) and, for the model failures, no 200:

| # | Injection (`tools/faults.py`) | Expected |
|---|---|---|
| 1–5 | `f1_bad_input`: `{}`, `{"question": 123}`, `{"question": ""}`, a 5,000-character question, a non-JSON body | 400 `bad_input` |
| 6 | `f2_no_index`: `chroma_db/` moved aside | 503 `no_index`, message contains `python app.py index` |
| 7 | `f3_invalid_key`: a bogus `GEMINI_API_KEY` | 502 `upstream` |
| 8 | `f4_empty_response`: model returns no text | 502 `upstream`, never a 200 with `"answer": ""` |

**Why this target:** all 8, not 7. Each of these was a 500 with a raw exception
string (or an HTML traceback page for the `123` body, or a 200 with an empty
answer for F4) before this unit, and the whole point of the extension is that no
caller sees them. A deterministic check still gets three trials because the
server is a fresh process each time and F3 depends on a live call to the
provider. The cost of being wrong is a caller who can't tell an outage from their
own bad input, or who is shown a provider's key error.

**How it's checked:** `python tools/faults.py --fault f1_bad_input` (and f2, f3,
f4); read status and `error_kind` from the printed body.

**Fails if:** any case returns 500, 200, a missing `error_kind`, or a body that
quotes the provider or a traceback.

---

### 2. A hung model call is abandoned within 35 seconds  *(extension, bad path)*

**Target:** with the model call stubbed to sleep 120 s (`f5_hung_upstream`), the
client gets a `504` with `error_kind: "model_timeout"` in **35 seconds or less**
of client-side wall-clock, in every trial (3 of 3).

**Why this target:** the bound is `GENERATION_TIMEOUT_S = 30` on **one model
call**, and the request also pays a cold first retrieval of about 3 s, so 35 s is
the timeout plus the cold overhead plus a little slack. Looser (say 60 s) would
let a retry or a pacing sleep slip through unnoticed; tighter than 33 s would
measure retrieval rather than the timeout. Without the bound, this request holds
a connection for the stub's full 120 s.

**How it's checked:** `python tools/faults.py --fault f5_hung_upstream`; the
harness prints the client wall-clock and the status.

**Fails if:** the status is anything but 504, the kind is anything but
`model_timeout`, or the wall-clock is over 35 s (for example if the timeout
thread is joined instead of abandoned).

---

### 3. Without the reranker, the system still answers  *(extension)*

**Target:** with `sentence_transformers` unimportable (`f6_no_reranker`'s
method), all 5 of `questions.py`'s test questions return a `200` whose body has
`"degraded": {"rerank": "degraded"}`, a non-empty answer, a non-empty `sources`
list, **and** an answer that names at least one of its source files. 5 of 5, in
every trial.

**Why this target:** 5 of 5 because the point of the fallback is that a clean
install (which doesn't include `sentence-transformers`) stops failing every
question; "most questions" would be the old failure at a lower rate. I'm not
asking for answers as *good* as the reranked ones (the fused ranking surfaces
different chunks, so I expect some to be worse) only that the flag is honest and
every answer is grounded and attributed.

**How it's checked:** start the server the way `f6_no_reranker` does (a stub
`sentence_transformers.py` on `PYTHONPATH` that raises `ImportError`), `curl` each
question from `questions.py::QUESTIONS`, read `degraded`, `answer` and `sources`.

**Fails if:** any response is non-200, is not flagged degraded, is empty, has no
sources, or never names a source file in the answer text. This last condition
is the most likely way for it to fail, since it depends on the model.

---

### 4. Every `/ask` leaves exactly one complete log record  *(instrumentation)*

**Target:** in one session of 12 requests (5 malformed bodies, 5 test questions,
2 out-of-scope questions), the log gains **exactly 12 lines**, every line parses
as JSON, and **12 of 12** records have non-null `ts`, `outcome`, `duration_ms`
**and** `question` (the field that records what came in).

**Why this target:** 12 of 12, not 11, because the log is the only way to
diagnose a failure after the fact, and a failure that leaves a record with no
input is a failure you can count but not reproduce. This is stricter than "a
record exists" on purpose: the brief's minimum is *what came in, what came out,
how long it took*, and malformed requests are exactly the ones whose input is
least obvious.

**How it's checked:** `AI201_LOG_DIR=logs/c4-tN ./run.sh`, send the 12 requests
with `curl`, then `wc -l logs/c4-tN/runs.jsonl` and a one-line `python` loop 
that `json.loads` every line and tests the four fields for `None`.

**Fails if:** the line count differs from 12 (a request that skipped the
`finally`), a line doesn't parse, or any of the four fields is `null`.

---

### 5. The first request after start-up is not slow to retrieve  *(run path)*

**Target:** after `./run.sh` prints `Serving…`, the **first** `POST /ask` has
`stage_ms.retrieve` of **500 ms or less**, in 3 of 3 restarts, per trial (so 9
restarts across the three trials). Measured with the reranker installed.

**Why this target:** a warm retrieve is about 90 ms; 500 ms is five times that,
so it leaves room for noise but rules out loading a model inside someone's first
request. The cost of being wrong is the first impression of a freshly started
service: the first user (and any health-check-then-ask automation) waits on a
model load that nobody can see. I saw about 3.1 s on a cold first request during
Milestone 2, so I expect this to be the criterion at most risk.

**How it's checked:** restart `AI201_CACHE=0 ./run.sh`, wait for `Serving`, send
one question from `questions.py` with `curl`, then read `stage_ms.retrieve` from
the last line of the log (`tail -n 1 logs/runs.jsonl`).

**Fails if:** any first request reports `retrieve` over 500 ms.
