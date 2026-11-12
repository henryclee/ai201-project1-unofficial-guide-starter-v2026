# Unit 9 Capstone — Execution Plan

**System being extended:** The Unofficial Guide — RAG over the `city_guides` corpus, in this repo (the one submitted for units 1–2). The service serves text only — JSON over the HTTP API unit 2 shipped, exercised with `curl`; the frontend (browser page, `GET /`, gunicorn) is entirely out of scope.
**Shape:** **B — Harden against failure, carried alongside the required A half.** `unit9.txt:40` is explicit: *"all three still deploy and instrument — shape A just makes that the whole job, while B and C carry it alongside. The run path and the log are required in every case."* So this unit ships **A + B**: the hardening layer is the chosen extension, the operational layer (run path, instrumentation, measured numbers) is the part every shape must also deliver.
**Run path:** **Path B — local with logs, one documented start command, committed run record, text only.** `run.sh` starts `python serve.py`, and the service is exercised with `curl` against the two routes unit 2 already shipped (`POST /ask`, `GET /health`) — JSON text, no HTML, no browser surface. The frontend is out of scope entirely: no page, no `GET /`, no gunicorn (out-of-scope item 5). Path A (hosting) is out of scope, not the run path — `unit9.txt:54` directs a system that loads local models to Path B.
**This plan's only artifact is this file.** No other repo changes were made, and the only git commit so far (`Unit 9 - planning docs`) committed the planning docs themselves — no milestone work has started. Every commit below is a checkpoint *you* read the diff for and run by hand.

The assignment text is in this repo as `unit9.txt` (untracked, 416 lines) — every requirement quoted or paraphrased below was read from it, and **where this plan and `unit9.txt` disagree, `unit9.txt` wins.** Code line references (`file.py:NN`) were verified against the current working tree at the time of writing; re-check one before you act on it if you've edited that file since.

---

## Milestones at a glance

| | Half | Doing | Exit condition (the brief's, not mine) |
|---|---|---|---|
| 0 | *prep* | *Preflight — environment, index, clean-install reranker test* | *(not one of the seven)* the system runs and the W6 finding is confirmed or dead |
| 1 | *scope* | Shape, scope, the size cut | README names the system, the shape, and what's out of scope (the brief's words) |
| 2 | **B** | Build the hardening layer, plus the logging seam it depends on | the extension is demonstrable **and** the original system still works |
| — | *M4's work, pulled forward* | *2.9 draft + commit the criteria* | `add unit 9 capstone criteria` lands before any result exists |
| 3 | **A** | The required operational layer — run path, worked curl examples, clean clone, log evidence, measured cost | it starts from `RUNNING.md` and answers a question over `curl`; ≥10 log entries and a cost number are in the README |
| 4 | *test* | Criteria self-check + pair review (writing happened at 2.9) | five numbered criteria with targets and reasons, committed before results |
| 5 | *test* | Run the test | five criteria, three trials each, pasted output underneath |
| 6 | *test* | Diagnose and improve | one fix made; everything re-run; both result sets kept |
| 7 | *test* | Cost, what's broken, write-up, submit | README complete and honest; history proves criteria → results |

**Milestones 2 and 3 are the build half, and they are two halves, not one.** Milestone 2 is the **B half** — the hardening layer you chose. Milestone 3 is the **A half** — the run path, the instrumentation and the numbers, which `unit9.txt:40` requires whichever shape you picked, and which picking shape B does not exempt you from. The build half's second grading question (*"does it run somewhere that isn't your editor, with a record of it running?"*, `unit9.txt:410`) is answered almost entirely by Milestone 3, so it is a deliverable here, not plumbing. The worked `curl` examples added at 3.2 belong to this half too: they are the run path made **reproducible by someone who isn't you**, not a second capability — see ground rule 10 for the line the text-only surface must not cross.

**No time estimates in this plan, on purpose.** Implementation time is not being tracked or monitored, so steps and milestones carry no budgets, no totals and no "saves N minutes" figures. Where a piece of work needs to be traded off, §3's size check decides it by *what it costs the submission* — which evidence would go missing — and by an ordered cut list, never by minutes.

---

## 0. Ground rules for executing this plan

1. **One milestone per sitting.** Each ends with a **Commit checkpoint** block — inspect the diff, then commit yourself. Nothing commits automatically.
2. **Never rewrite history, never delete/recreate the repo.** With both halves landing in one unit, commit order is the *only* evidence that the criteria predate the results.
3. `criteria.md` gets its own commit, with a message that names it (`add unit 9 capstone criteria`), **before** any commit containing results. The first results commit names itself too (`unit 9 results — run log before fix`).
4. ≥ 8 new commits are required this unit; this plan schedules **11** (Appendix D).
5. Everything landing in `README.md` / `RUNNING.md` is pasted **as text** — no screenshots, no video.
6. **Do not delete unit 1 / unit 2 content.** Unit 9 is appended. Revised criteria keep the original line with the revision underneath.
7. `results/` and `logs/` must stay committable. `results/` already is (`.gitignore:26-27` says so out loud); `logs/` is not ignored today — re-verify before Milestone 3.
8. **The A half is not optional because shape B was chosen.** The run path, the structured log, the ten pasted entries and the measured cost number are required in every shape (`unit9.txt:40`, `:89`–`:95`). They are scheduled at Milestone 3 and they are graded on their own (build-half Q2), so nothing in the cut list may remove them.
9. **No time tracking.** This plan carries no estimates for steps or milestones and none should be added; scope is managed through §3's cut list by what evidence would be lost, not by minutes.
10. **The service stays text-only.** The interface is exactly what unit 2 shipped — `POST /ask` and `GET /health`, JSON, exercised with `curl` — plus the `app.py` CLI. No HTML page, no `GET /`, no static assets, no gunicorn, no new endpoint, no new dependency for the surface. The frontend is declared out of scope (out-of-scope item 5), and that declaration is a decision made at Milestone 1, not a trim taken later; the moment anything wants to render in a browser, it is out of this unit by this rule.

---

## 1. Decisions locked in

| Question | Decision | Why |
|---|---|---|
| Which system | The Unofficial Guide, `city_guides` | The one whose weak points you know from memory — which is what unit 9 asks you to write criteria about. Retrieval quality was already tuned in unit 2, so nothing has to be redone. |
| Shape | **B — Harden against failure**, carried alongside the **required A half** | The failure handling genuinely isn't there (nine verified weak points below; Appendix B turns them into ten injectable faults, each with a bad outcome today), and the bad path is where this rubric's points live. Shape A is not a competing option here: `unit9.txt:40` makes the run path and the log mandatory in every shape, so A is *carried*, not chosen. |
| The two halves | **B = the extension** (the hardening layer → Milestone 2). **A = the required operational layer** (run path, structured log, measured cost, observability → Milestone 3). | Naming them separately keeps the scope story honest in both directions: *The Shape* claims one extension, while *Running It*, *Instrumentation* and *What It Costs* deliver the half the brief requires regardless of shape — and build-half grading Q2 (`unit9.txt:410`) is answered there and nowhere else. It also tells you at 2.9 that the operational layer is new code, so criteria about it count toward "at least three about the extension". |
| Run path | **Path B — local with logs** | Retrieval loads **two** local models: Chroma's ONNX `all-MiniLM-L6-v2` (~80 MB) *and* the cross-encoder `ms-marco-MiniLM-L-6-v2` via `sentence-transformers` (`store.py:125-151`), which drags in PyTorch (~2 GB installed). A 512 MB free host cannot hold that. Path B is worth the same and is the honest answer here — and it narrows *where* the system runs, never *what it must show*: the A-half requirement list arrives intact at Milestone 3. |
| Web surface | **None — text only.** The frontend is out of scope: no page, no `GET /`, no `static/`, no gunicorn. The interface is the JSON API unit 2 already shipped (`POST /ask`, `GET /health`), exercised with `curl`, plus the `app.py` CLI | The page was this plan's one optional A-half item, and cutting it whole is a scope decision made here, at Milestone 1, not a trim taken under pressure. What replaces its job is documentation: worked `curl` examples in `RUNNING.md` (the ones `RUNNING.md:201-214` never had) make the service reproducible by someone who isn't you (`unit9.txt:56`), and a classified failure is visible in the JSON body and the log. Cost of the cut: nobody reaches the system from a browser, every record reads `server: "flask-dev"`, and F4/F6 prove themselves as pasted JSON rather than rendered HTML. The gunicorn pin in `requirements.txt` (added "for unit 9") is removed in the Milestone 3 commit, and the README says the frontend is out of scope in one sentence |
| The one extension | **Every request leaves the pipeline with a classified outcome and a log record**: bounded execution time, no traceback to a caller, no silent empty answer, and no hard dependency on the reranker to answer at all. | One sentence, one thing. Everything in Milestone 2 serves that sentence. The operational layer is **not** a second thing this plan is doing — the brief mandates it in every shape (`unit9.txt:40`), so it doesn't count against the one-thing rule; see 1.6 for how to say this in the standup. |
| Instrumentation | Structured JSONL, one record per request including failures (`metrics.py`), **plus a reader that answers questions about the running system without new code** (`metrics.py --summary`) | Two separate requirements sit on this line: the log itself (*"at minimum a timestamp, what came in, what came out, and how long it took"*, `unit9.txt:92`) and *observability* as the brief defines it — *"answer a question about a running system without adding new code first"* (`unit9.txt:25`). The writer satisfies the first; only the reader satisfies the second. Both also make the Milestone 5–6 diagnosis possible. Records carry process provenance (`server`/`pid`/`port`) but no traffic channel — there is no page, so there is no traffic to separate. |
| Stretch | **Declare one, at Milestone 1:** the measured per-stage latency breakdown | It's the only stretch item this design already produces (`stage_ms`), so declaring it costs a sentence and no extra code. A second improvement and a load test stay out — see §3's stretch block for why each is declined. It is also an A-half item, which fits a unit that ships A + B. |

**The shape in one paragraph** (goes in README under *The Shape*):

> Unit 9 adds a hardening layer around the existing five-stage pipeline. A request to `POST /ask` now either returns a grounded answer, a gate refusal, or a *classified* failure — bounded by a wall-clock timeout, mapped to a status code, carrying a machine-readable `error_kind` — and in all three cases it leaves exactly one structured record in `logs/runs.jsonl`. Answer quality is deliberately unchanged: retrieval, chunking, the gate threshold and the prompt are exactly what unit 2 left behind.
>
> Carried alongside it is the operational layer the brief requires of every shape, not just shape A: the system starts from one documented command (`run.sh` → `python serve.py`) instead of from the editor, it answers over the HTTP surface unit 2 already shipped as JSON text — `POST /ask` and `GET /health`, exercised with `curl` — every request, every failure included, appends one structured record that `metrics.py` can summarise without adding new code, and the cost of a run is measured rather than read off a pricing page. The frontend is out of scope, declared as such: no page, no `GET /`, no gunicorn. What makes the service reproducible by someone who isn't you is the documentation instead — worked `curl` examples in `RUNNING.md` that a stranger can run verbatim from a clean clone. So: **shape B, with shape A delivered beside it**, because the run path and the log are required in every case.

---

## 2. What the system does today — verified weak points

Read off the code, not assumed — line numbers verified against the current tree. Confirm each one empirically in step 2.0 **before** changing anything: that is your "before" evidence, and it is what the criteria you draft at 2.9 are written against.

| # | Today's behaviour | Where |
|---|---|---|
| W1 | **No timeout exists anywhere in the repo** (`grep -rn timeout *.py` → no hits). `client.models.generate_content()` blocks for as long as the service likes, inside the HTTP request. | `generate.py:241` |
| W2 | **An empty model response is returned as a success.** `(response.text or "").strip()` yields `""`, which flows through `ask_pipeline` into a `200` with `"refused": false` and a populated `sources` list. A caller cannot tell "the model said nothing" from a good answer — and unit 1's criterion 2 ("every answer names a source") *passes* on an empty answer. | `generate.py:243` → `app.py:268` → `serve.py:95-105` |
| W3 | **Every pipeline exception becomes the same 500**, raw exception text handed to the caller, nothing written down. A missing index is indistinguishable from an API outage. | `serve.py:90-93` |
| W4 | **A missing index is a 500.** `search()` raises a bare `RuntimeError("No index called …")` into W3, while `/health` already knows the index is missing (`index_ready: false`). | `store.py:281-286`, `serve.py:49-51` |
| W5 | **Malformed input can 500 instead of 400.** `question = (payload.get("question") or "").strip()` sits *outside* the `try` (which starts at line 90), so `{"question": 123}` raises `AttributeError` and Flask answers 500 with an HTML traceback page. A missing or non-JSON body is the only handled case (→ 400). | `serve.py:76-88` |
| W6 | **Retrieval hard-fails if the reranker can't load.** `_rerank()` sits on the happy path of `search()` (`store.py:331`) and calls `_cross_encoder()` unconditionally for any non-empty result set (`store.py:168`), which raises if `sentence_transformers` isn't importable or the weights won't download. **`requirements.txt` does not list `sentence-transformers`** — and `requirements.txt:12-24` explains that omission as a *deliberate* choice (PyTorch, ~2 GB), while `RUNNING.md:234-240` mentions the package only as the prerequisite for a *stretch* option (`:17-33`'s install steps never install it). A clean checkout that follows `RUNNING.md` therefore builds an index fine and then fails on *every* `ask` / `retrieve` / `POST /ask`. Verify in Milestone 0 — this is the single biggest finding in the repo. | `store.py:125-151`, `:168`, `:331`, `requirements.txt:12-24` |
| W7 | **Pacing sleeps or explodes inside a request.** `_wait_for_slot()` can `time.sleep()` up to ~60 s while a client waits, and passing `SESSION_REQUEST_BUDGET` raises `QuotaGuard` mid-request → W3. | `generate.py:89-123`, `config.py:95-97` |
| W8 | **Nothing is recorded.** No `logging` import exists anywhere (`grep -rn -e 'import logging' -e 'logger.' *.py tools/*.py` → no hits). `serve.py:23-27` says this is deliberate and that unit 9 supplies it. | repo-wide |
| W9 | `run_eval.py::run_once` has no error handling, so one bad upstream during an eval aborts the whole run instead of scoring it. | `run_eval.py:52-66` |

**Already good, do not change:** the explicit cosine collection (`store.py:234-240`), the gate as a pre-model decision (`gate.py`), token counts read off the response rather than a pricing page (`generate.py:125-150`), and `ask_pipeline` returning a dict instead of printing (`app.py:198-270`) — that dict is the cleanest possible seam to instrument.

---

## 3. Scope: the two halves in, what's out, and the size check

### In scope — two halves, deliberately separated

**The B half — the extension** (what shape B was chosen for):
- An error taxonomy and **one** mapping from exception → status code + `error_kind`.
- A wall-clock bound on the model call; a retry-then-fail policy for empty responses.
- Graceful degradation when the reranker is unavailable (answer anyway, flagged).
- Input validation at the HTTP edge that answers 400 instead of 500.
- A fault-injection harness (`tools/faults.py`) to *produce* the bad path on demand.

**The A half — the required operational layer** (mandatory in every shape per `unit9.txt:40`; **not** optional because shape B was chosen):
- Structured JSONL logging of **successes and failures**, carrying at minimum a timestamp, what came in, what came out and how long it took (`unit9.txt:92`).
- A log **reader**, so a question about the running system is answerable without adding new code — the brief's own definition of observability (`unit9.txt:25`).
- The run path: one documented start command (`run.sh`), `RUNNING.md` verified from a clean clone, and a committed record proving it ran somewhere that isn't the editor (`unit9.txt:49`–`:52`, `:410`).
- **Worked `curl` examples in `RUNNING.md`** for `/health` and `/ask` — the ones it never had — so a stranger reproduces the service from the doc alone (`unit9.txt:56`).
- A cost per run, measured (tokens or seconds of compute), with the method written down (`unit9.txt:95`).
- ≥ 10 log entries and the cost number pasted into the README as text.

Putting the two lists next to each other is the point: the extension is one thing, the operational layer is the thing every shape must also ship, and a reader of the README can see which claims belong to which. Nothing in the **second** list is optional: every item on it is a brief mandate (`unit9.txt:40`, `:89`–`:95`), which is why the cut list below draws only from the B half.

### Out of scope — declare these in the README
1. **Retrieval quality is not part of the extension.** The chunker, `THRESHOLD`, BM25/RRF fusion and the cross-encoder choice are untouched, and no retrieval dial moves at any point before the criteria are measured — the extension is the hardening layer, and answer quality is deliberately unchanged (which is also what keeps the new criteria attributable). The one exception is the Milestone 6 improvement, which the brief requires to follow the diagnosis: if a measured miss (or a MET-but-thin criterion needing the required improvement) points at a retrieval dial — e.g. `TOP_K` — that dial moves **once**, everything is re-run three trials each, what got worse is named in the comparison, and this line is amended in the same commit as the fix. Written into the README in this wording at the Milestone 1 commit, so the exception is declared before it is ever invoked — never improvised at M6.
2. **Hosted deployment (Path A).** No Render/Railway signup, no Dockerfile, no `Procfile`. This is a decision about *which run path*, not about whether to deploy: the system does get deployed, on Path B, because the retriever loads two local models and `unit9.txt:54` directs exactly that case to Path B ("you can stop reading this section"). Path A and Path B are worth the same (`unit9.txt:45`).
3. **Traffic handling.** No auth, API keys, per-client limits, queueing or cache changes; no 10× load test — unless the declared stretch item (§3's stretch block) takes the load observation, in which case this line gets amended in the same commit that declares the stretch, before any of it is run.
4. **The CLI surface.** `app.py` subcommands and the interactive loop behave as before; only the shared `ask_pipeline` gains fields.
5. **The frontend, entirely.** No browser page, no `GET /`, no `static/`, no gunicorn. The service serves text: JSON over the two routes unit 2 already shipped, exercised with `curl`, plus the `app.py` CLI. The brief's own model out-of-scope answer is "I'm not rebuilding the interface" (`unit9.txt:143`) — this plan goes further and ships no interface beyond the API at all. `run.sh` starts Flask's development server, which is the right weight for a single-user local run; the gunicorn pin in `requirements.txt` (added "for unit 9") is removed in the Milestone 3 commit and the removal named in the README, so the pinned file describes exactly what runs.

### Size check — what this build actually contains *(no time tracking anywhere in this plan; see ground rule 9)*

The brief pictures Milestone 2 as the shortest build block in the course, holding *"one capability, one hardening layer, or the operational scaffolding — whatever your shape named"* (`unit9.txt:174`). This unit is unusual: it needs **two of those three**. The hardening layer, because that's the chosen shape; the operational scaffolding, because `unit9.txt:40` requires it in every shape. That is the honest reason the build is larger than the brief pictures — and it is a reason to refuse to grow it further, not a licence. So the trade-offs are decided now, by **what evidence would go missing**, never by minutes.

| Piece | Half | Why it's on the list |
|---|---|---|
| Error taxonomy + `classify()` | B | every status code and `error_kind` in the submission is decided here, in one place |
| Timeout + empty-response policy in `generate.py` | B | kills W1 and W2 — the two weakest points in the repo |
| Reranker degrade + `NoIndexError` in `store.py` | B | kills W4 and W6, and makes the clean-clone story survivable |
| `metrics.py` writer + `--summary` reader | A | the log the brief mandates, and the only thing that makes "observability" more than a claim |
| Worked `curl` examples in `RUNNING.md` | A | makes the run path reproducible by someone who has never opened this repo — the page's old job, done in documentation instead of code |
| `ask_pipeline` timings + `serve.py` mapping/logging | A + B | per-request records, `duration_ms`, `stage_ms`, status codes at the HTTP edge |
| `tools/faults.py` harness | B | without it there is no bad path to summon, and Milestone 5 has nothing to run |
| Regression pass | both | the brief's Milestone 2 exit condition |
| Capturing today's bad behaviour first (2.0) | both | the "before" evidence the criteria and the Milestone 6 fix are written against |

**Ordered cut list — cut from the top, and stop as soon as the build fits.** Each entry names the evidence that disappears if it goes, because that, not minutes, is what decides the order.

The page is **not on this list**: it was cut whole as out-of-scope item 5 before any code — a scope decision declared at Milestone 1, not a trim taken under pressure. What remains:

1. Faults **F9/F10** in the harness. Lost: the body-abuse proof and the blocked-logger proof. Kept: F1–F6 and F8, the faults the extension is actually judged on.
2. The `--tail` / `--kind` filters on the log reader. Lost: convenience. **Kept, non-negotiably: `--summary`.** Don't substitute `jq` — it isn't installed by default on macOS, and a reader that depends on a tool the reader doesn't have isn't observability; `python -m json.tool` and a two-line `python -c` are always present.
3. Per-stage `stage_ms` — **⚠️ do not cut this one.** It is the declared stretch item (*"a latency breakdown — where the time actually goes across the stages of one run, measured"*), it is what lets 6.2 name a *stage* instead of guessing, and once `duration_ms` exists the split is ~6 lines. If you are truly out of room, ship it anyway and drop the stretch sentence instead.
4. The `degraded` flag plumbing — listed only so the choice is visible: **do not cut it**, because without it the reranker story has no evidence.

**Never cut, B half:** the timeout, the empty-response failure, the 400 path, the log record on failures, and `tools/faults.py`. Those five *are* the extension; cut one and the unit becomes "I added a logger", which fails the brief's Milestone 3 condition (the log must contain failures) no matter how good the logger is.

**Never cut, A half:** `run.sh`, `RUNNING.md` with its worked `curl` examples, the log writer, the `metrics.py --summary` reader, ≥ 10 pasted log entries, and the measured cost number. These are not part of the extension, so cutting one doesn't shrink the extension — it deletes a requirement that applies to **every** shape (`unit9.txt:40`, `:89`–`:95`) and leaves build-half Q2 with nothing to point at. Note the word the brief uses when it describes an acceptable *smaller* extension: one that "runs, **is instrumented**, and is tested honestly" (`unit9.txt:184`).

Step 2.9 sits outside this table on purpose: drafting the criteria is Milestone 4's work pulled forward into Milestone 2, not extra build work.

### Stretch, and which of the four options this repo gives you almost free
The brief offers four stretch items and requires you to **declare in the README before you start** — so decide at Milestone 1, not at Milestone 7.
- **Latency breakdown across the stages of one run, measured** → this is `stage_ms` (2.5). Already in scope; declaring it costs a sentence and the log rows are the evidence. **Take this one.**
- **A load observation at ten times your normal rate** → nearly free too: the 10-request cost run (3.8) *is* a 10× burst for a single-user CLI, and two known weak points make the finding interesting — the per-process `LAST_RETRIEVAL` global (2.3) is not thread-safe under Flask's dev server, whose default is threaded, and W7's `_wait_for_slot()` pacing can sleep *inside* a request, so at 10× the pacing rather than the model dominates the wall clock. Only take this if the required loop is already closed, and amend out-of-scope item 3 when you do.
- **A second measured improvement** → only if 6.6's fix lands clean and re-measured without anything left unverified; it must be logged exactly like the first, so it costs a full re-run of all fifteen-plus trials.
- **Both run paths** → no. A 512 MB host can't hold two local models (W6 + `store.py:125-151`), which is already the Path B justification.

---

## Milestone 0 — Preflight: make the system run again *(prep — not one of the unit's seven)*

There is no `.venv` in this directory and `python3` on the shell default is **3.9.6**, which this codebase cannot even parse (`config.py:110` uses `str | None`). Supported range is 3.11–3.13, explicitly **not 3.14** (`requirements.txt:4-5`). `/opt/homebrew/bin/python3.12` and `python3.13` both exist.

- [ ] 0.1 `cd` into the repo; create the env with a supported interpreter:
      `/opt/homebrew/bin/python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- [ ] 0.2 `cp .env.example .env`, paste the key, `python test.py`.
- [ ] 0.3 `python app.py --corpus city_guides index` (note the wall-clock — you need it for RUNNING.md) and one `python app.py --corpus city_guides ask "How expensive is it to stay at Thornby Wells?"`. **Why the flag:** `config.CORPUS` defaults to `campus_life` (`config.py:23`) while `questions.py`'s five test questions are `city_guides` questions — every command must pin the corpus or the system silently answers from the wrong one.
- [ ] 0.4 **Confirm W6.** In a *second* throwaway venv installed from `requirements.txt` alone, run `python app.py retrieve "tram schedule"`. Record verbatim what comes back. This is the single most important finding for `RUNNING.md` and it is the honest justification for the degrade path you build in 2.3.
- [ ] 0.5 Record the local artefacts a stranger needs: embedding model download (~80 MB from Chroma's CDN), the cross-encoder weights, `sentence-transformers`+PyTorch install size, `chroma_db/` rebuild time. These go in `RUNNING.md` in Milestone 3.

**Commit checkpoint (M0):** nothing to commit unless you changed a file. If 0.1–0.3 required a fix, commit it as `unit 9 preflight: environment fixes`.

---

## Milestone 1 — Shape, scope, and the size cut

Deliverable: a `# Unit 9` heading appended to `README.md` with three filled sections. Write-only milestone — no code.

- [ ] 1.1 Append a `# Unit 9` block at the end of `README.md` (769 lines, ends with a complete sentence at `:769` but **no trailing newline** — add one first or your heading glues onto unit 2's last words). Unit 1 (`:8`) and unit 2 (`:309`) headings stay untouched. Scaffold all **nine** of the brief's section names now — *What This Extends · The Shape · Running It · Instrumentation · What It Costs · Run Log and Verdicts · The Improvement · What's Still Broken · How I Used AI* — fill the first three in 1.2–1.4, and leave the other six as `_(filled in Milestone 3/5/6/7)_`. The scaffold guarantees the section names match the brief exactly no matter how late in the unit the filling-in happens.
- [ ] 1.2 **What This Extends** — name the system, the corpus, and the one sentence of what's new (Section 1 of this plan, in your own words). Say plainly that answer quality is unchanged on purpose.
- [ ] 1.3 **The Shape** — "B — Harden against failure", the two paragraphs from Section 1 of this plan (the hardening layer, then the sentence saying shape A is carried alongside because the run path and the log are required in every shape), plus the five out-of-scope items from Section 3 written as sentences ("I am not changing the chunker or the cutoff…"), **item 1 in its amended wording** — the version that declares the Milestone 6 `TOP_K` exception up front, so the fix table at 6.3 and the scope statement agree from day one — the fifth being the frontend itself: no page, no `GET /`, no gunicorn — the service serves text over the routes unit 2 shipped, exercised with `curl`. Say explicitly that out-of-scope item 2 is *hosted* deployment only — the system is deployed, on Path B.
- [ ] 1.4 **Running It** — "Path B — local with logs, one documented start command, committed run record, text only", one sentence on why (two local models won't fit a 512 MB free tier, which is what `unit9.txt:54` tells you to do in that case), pointer to `RUNNING.md`, one line saying the service answers `POST /ask` as JSON text, exercised with the `curl` examples the doc carries — and one line naming the frontend as out of scope. Name it as the A half of the build, not as setup. Fill the rest in Milestone 3.
- [ ] 1.5 Re-read §3's size check and ordered cut list. If a piece has outgrown what §3 gives it, cut in that order and write the cut into *What's Still Broken* later — cutting an **A half** item is not an available option, so cut from the B half instead. The page is **not** an available cut either: it was removed from scope outright (out-of-scope item 5), before any code — the one scope decision this plan makes on the A half, made at Milestone 1 and stated in the README rather than improvised later.
- [ ] 1.6 Scope standup check on yourself: say the extension out loud in one sentence. If the word "and" appears twice, it's three projects. The sentence in Section 1 is the target shape. **The A half does not count against this rule** — say it as a second sentence, attributed to the brief rather than to your ambition: *"the extension is one thing — every request leaves the pipeline with a classified outcome and a log record; the run path and the log ride along because the brief requires them in every shape."* That is the answer when someone asks "is that one thing or three?" — one extension, one mandated layer, plus the harness that proves the first one works.
- [ ] 1.7 **Stretch, yes or no, declared now** (the brief requires the declaration before you start, not after). Recommended: the **latency breakdown** item only, because `stage_ms` is already in the design (§3's stretch block) and it costs a sentence here — write *"Stretch: a measured latency breakdown across the stages of one run, from `stage_ms` in `logs/runs.jsonl`."* Declaring more than one is how the required loop gets sacrificed for the optional one.

> ⚠️ **Optional cleanup:** the file has no trailing newline (`od -c` on the last bytes confirms unit 2 ends `…this small question set.` with no `\n`), so anything appended needs a newline first — and unit 2's last two paragraphs sit there as loose ends it names but never resolves ("It should be tightened to 5/5"). A one-line pointer under them to unit 9's *What's Still Broken* reads far better than silence. Do not otherwise rewrite unit 1/2.

**Commit checkpoint (M1) — do this by hand:**

```bash
git add README.md
git commit -m "unit 9 milestone 1: declare shape B + required A half, Path B, and scope"
```

**Before you move on:** README names the system, the shape (B, with the required A half named), and what's out of scope.

---

## Milestone 2 — Build the B half: the hardening layer *(scope triage in §3; the A half lands at Milestone 3)*

Rule: one path end-to-end before it's good. Commit three times inside this milestone (the brief asks for ≥3 here alone). Keep the unit-2 behaviour of every existing caller working — all new dict keys are **additive**.

### 2.0 Capture "before" — ⚠️ do this first
Start the server (`python serve.py`) and record verbatim responses for the Appendix B faults that need no code to trigger: **F1** (`{"question": 123}` → expect W5), **F2** (rename `chroma_db/` → expect a 500 whose body quotes `python app.py index`), **F3** (invalid API key in `.env` → expect a 500 carrying the provider's text). Paste into a scratch file; this is evidence for the README and the baseline your Milestone 6 fix is measured against. Also write down the two sentences you expect to change: "no timeout" and "empty answer looks like success".

### 2.1 `errors.py` — the taxonomy *(new file ~60 lines)*
One module, six types, one mapper. Nothing else in the repo decides a status code.

```python
class PipelineError(Exception):        # kind, http_status, stage, user_message
class BadInputError(PipelineError):    # kind="bad_input",              400
class NoIndexError(PipelineError):     # kind="no_index",               503   # subclass RuntimeError too, so existing callers keep working
class ModelTimeoutError(PipelineError):# kind="model_timeout",          504
class ModelEmptyResponseError(...):    # kind="model_empty_response",   502
class UpstreamError(PipelineError):    # kind="upstream",               502
class QuotaError(PipelineError):       # kind="quota",                  429   # wraps generate.QuotaGuard (:48)
def classify(exc) -> PipelineError     # known types pass through; everything else → kind="internal", 500
```
`QuotaError` is the one that isn't a crash: `generate.py:108-121` raises `QuotaGuard` mid-request today and it lands in W3's generic 500 (`serve.py:92`), which reads to a caller like an outage when it's actually "slow down". Mapping it to 429 costs two lines and is the cheapest defensible criterion in the set.
Two rules that matter: the caller gets `user_message` **plus the `request_id`**, never the exception text (that goes to the log); and a gate refusal is **not** an error — empty results from a real index stay a `200` with `"refused": true`. Empty *index* is `no_index`; empty *results* is a refusal. Get that line wrong and you'll "fix" the thing that already worked.

### 2.2 `generate.py` — bound the call, refuse to lie *(edit inside `generate()`, lines 202–271 only)*
- **Timeout.** Wrap `client.models.generate_content(**kwargs)` (`:241`) in a wall-clock bound of `config.GENERATION_TIMEOUT_S`. Two ways; pick one and write the other down as the alternative you rejected:
  - *(a) dependency-free, recommended:* `concurrent.futures.ThreadPoolExecutor` + `future.result(timeout=…)`, raising `ModelTimeoutError` on `TimeoutError`. Covers a hang *inside* the SDK, which a transport timeout does not.
  - *(b) transport-level:* `google.genai` `HttpOptions(timeout=…)` at `_get_client()` (`:186-200`). Verify the exact kwarg for the pinned `google-genai>=1.0,<2.0`; note it won't bound work the SDK does after the socket closes.
  - ⚠️ A thread you abandon keeps running. Say so in a comment and in the README — bounded *response*, not cancelled *work*, is an honest limit and a real one to name in *What's Still Broken*.
- **Empty is a failure.** At `:243`, if the stripped text is empty: make **one** second attempt, then raise `ModelEmptyResponseError`. Returning `""` is what lets W2 pass unit 1's criterion 2.
- **Retries stay as they are** (`:246-268`) — only rate-limit-shaped messages retry today; don't broaden that today, or you change latency for a reason unrelated to your criteria.
- **Expose per-call stats** for the log: attempts made, whether it timed out, and the tokens already captured by `_record_tokens` (`:125`).

### 2.3 `store.py` — one error type, one degrade
- `:284` **and `:347`** — both raise sites carry the same bare `RuntimeError("No index called … Run \`python app.py index\` first.")`; swap both for `NoIndexError` (the message keeps the "run `python app.py index`" instruction — that sentence is the fix's user-facing half). Grep `RuntimeError` in `store.py` before you finish: `:87` and `:142` are the embedder/reranker ones and belong to the degrade work below, not here.
- `_rerank()` (`:154-169`) — if `_cross_encoder()` can't load (ImportError **or** weights unavailable), **return the fused RRF order unchanged** and flag it. Retrieval then still works, which is exactly what W6 makes impossible today, and answers the question a grader will ask about a repo whose pinned file doesn't contain a dependency its happy path needs.
- Flag plumbing, simplest option: a module-level `LAST_RETRIEVAL = {"rerank": "ok"|"degraded", "candidates": n, "results": n}` set by `search()` and read by `ask_pipeline`. Cheaper than threading a callback through three call sites. **Write down the caveat** — a module global is per-process but not safe across threads, and Flask's development server threads by default; the documented run is a single-user local session, so say that in the README rather than hide it (and if the load stretch is ever taken, this is where it bites).

**Commit checkpoint (M2a) — by hand:**

```bash
git add errors.py generate.py store.py config.py
git commit -m "unit 9 milestone 2a: error taxonomy, generation timeout, empty-response failure, reranker degrade"
```

### 2.4 `config.py` + `metrics.py` — knobs and the log *(the A half's first lines of code)*
`config.py`, new block near `:91-100`, each overridable by env like the existing ones:
`GENERATION_TIMEOUT_S = 30`, `EMPTY_RESPONSE_RETRIES = 1`, `MAX_QUESTION_CHARS = 1000`, `LOG_DIR = ROOT / "logs"`, `LOG_FILE = LOG_DIR / "runs.jsonl"`, `RERANK_STRICT = False`.
(`RERANK_STRICT` is the honest switch: `True` restores today's hard failure. Add constants as you reach for them — some may already be in the M2a commit.)

`metrics.py`, new file, ~90 lines, two jobs:
- **Write:** `record(**fields)` appends one JSON object per line to `logs/runs.jsonl`, creating the dir, never raising (a broken logger must not break a request — mirror the attitude of `generate.py:145-146`, whose comment reads *"accounting never breaks the thing it is accounting for"*). Schema in **Appendix A**; the four fields the brief mandates are `ts`, input, output and duration, and every record also carries `outcome` and `error_kind` so failures are legible.
- **Read:** `python metrics.py --tail 10`, `--summary`, `--kind model_timeout` — counts, mean/median/p-max `duration_ms`, error kinds, degraded share. This is what makes "observability" true rather than claimed: you can answer a question about the running system without adding code (the brief's own definition, `unit9.txt:25`), which is the only reason Milestone 5 can be done from the log at all. **`--summary` is on the never-cut list** (§3) — if anything must go, it is `--tail` and `--kind`, never the summary. If you find yourself reaching for `jq`, don't: it isn't installed by default on macOS; `python -m json.tool` is. `--summary` groups by outcome and error kind, and splits by stage: *"which stage do the failures actually come from?"* is the first question worth asking, and answering it without writing new code is precisely the brief's definition of observability (`unit9.txt:25`).
- `logs/` must be committed as evidence. `.gitignore` currently does not ignore it — verify with `git status` after the first write, and do **not** add it to `.gitignore`.

### 2.5 `app.py::ask_pipeline` — timings, additive fields *(`:198-270`)*
Wrap each stage in `time.perf_counter()` deltas and add to the returned dict: `request_id` (`uuid4().hex[:8]`), `error_kind` (`None` on the happy path), `degraded` (`{"rerank": "ok"|"degraded"}`), `duration_ms`, `stage_ms` (`retrieve`/`gate`/`generate`), `n_results`, `n_candidates`, `answer_chars`, `attempts`. It still prints nothing — `_ask_one` (`:273`) and `run_eval.py::run_once` (`:52`) keep working untouched because you only added keys.

### 2.6 `serve.py` — the shell becomes a service *(`:66-105`)*
- Mint `request_id` at the top of `/ask`; echo it in every response body and in `X-Request-Id`.
- Move parsing/validation **inside** the protected region (fixes W5): non-string, missing, blank or > `MAX_QUESTION_CHARS` question → `400` JSON `{error_kind: "bad_input", request_id, message}`. Confirm the exact today-behaviour in 2.0 first; W5 is a claim until you see the 500.
- `except PipelineError` → `classify()` → its status; `except Exception` → `500` with `kind: "internal"`, the `request_id`, **and no exception text** (W3's raw leak).
- Write the log record in a `finally` so 400s, 500s and timeouts are all recorded — the brief's "a failure that shows up only as an absence is one you'll never find".
- `/health` (`:39-63`) gains `reranker: "ok"|"degraded"` and `log_path`; keep it cheap — no embedder load, per the note at `store.py:358-361`.
- Record **who is serving** in every log record — `server` (`"flask-dev"` when the record comes from `serve.py`, `"cli"` from `app.py`), `pid`, `port`. It costs three lines and it is what turns the committed log into Path B's proof that the system ran as the documented server process (`unit9.txt:410`, `:49`–`:52`) rather than a bare function call inside an editor. See Appendix A.
- **Add no route.** The frontend is out of scope (out-of-scope item 5): no `GET /`, no `static/`, no template, no gunicorn behind it. `POST /ask` and `GET /health` are the only routes, exactly what unit 2 shipped — confirm nothing else appears in this file's diff. `app.run` stays the only server; the documented start command (`run.sh`, Milestone 3) execs `python serve.py`, and the README says plainly that what's running is Flask's development server and that a production server is declared out of scope — the right weight for a single-user local run, and enough for the brief's question, *"does it run somewhere that isn't your editor, with a record of it running?"* (`unit9.txt:410`).
- `app.run` stays the only server. The documented start command (`run.sh`, Milestone 3) execs `python serve.py`; say in the README that what runs is Flask's development server and that a production server is declared out of scope.

### 2.7 `tools/faults.py` — the harness you test with in Milestone 5 *(new file)*
Model it on `tools/smoke_test.py`, which already proves the pattern of faking an embedder and a key. Each fault is injected **at runtime, never with a switch inside production code** — an `AI201_FAULT=…` branch in `generate.py` would mean the code you graded isn't the code you tested.

Mechanics per fault are in **Appendix B**. Only external dependency note: `requests`/`httpx` are **not** in `requirements.txt`, so drive HTTP with stdlib `urllib.request` or a `curl` loop rather than adding a dependency (adding one costs a README sentence for no gain).

Print, for each fault: the name, how it was injected, the status/body that came back, and whether a log record appeared. That output pastes straight into the README and the run log.

### 2.8 Regression gate — before committing
- [ ] `python test.py`
- [ ] `python tools/smoke_test.py` (the repo's own end-to-end check; it needs no key)
- [ ] `python app.py --corpus city_guides ask "How expensive is it to stay at Thornby Wells?"` — unchanged answer shape
- [ ] `python run_eval.py --corpus city_guides --label unit9-regression` — the five questions still 3/3 pass, gate still refuses 5/5
- [ ] `curl -s localhost:5000/health` then one happy `POST /ask`, then `python metrics.py --tail 3` — the record for that call reads `server: "flask-dev"` with a `pid` and a port

**Confirm the original system still works** — this is the brief's Milestone 2 exit condition, and it's cheaper to prove here than in Milestone 5. If this milestone has outgrown §3's size check, apply §3's ordered cut list rather than borrowing work from Milestones 5–6, and remember the A half is on the never-cut list.

**Commit checkpoints (M2b, M2c) — by hand:**

```bash
git add metrics.py app.py serve.py config.py
git commit -m "unit 9 milestone 2b: structured JSONL log, per-request timings, status mapping at the HTTP edge"

git add tools/faults.py
git commit -m "unit 9 milestone 2c: fault-injection harness for the bad path"
```

### 2.9 Draft the five criteria and commit them — **before any measurement**
The build now exists and 2.8 proved it runs, so you know exactly what the extension does — and you have measured nothing yet. This is the moment the brief's ordering actually permits. Read the criteria guidance in **Milestone 4** (targets, reasons, the four tests each sentence must pass) and write the five there; commit them now so the history proves the order:

```bash
git add criteria.md
git commit -m "add unit 9 capstone criteria"
```

Then go and measure things in Milestone 3. If the class pair-review later shows a sentence is unmeasurable, revise it **underneath** the original with your reason — don't overwrite it.

**Before you move on:** the extension is demonstrable (one fault, one classified failure, one log record), the original system still passes, and the criteria commit exists while no result does.

---

> ### ⚠️ The ordering decision, made deliberately — why the criteria commit sits at 2.9
> The brief puts "write your criteria" at Milestone 4, but it also says *"write these before you run anything"* and *"commit them before you commit any results — your commit history is what shows that order."* Milestone 3 commits measured artifacts (a run log, a cost number). Do the measurement commits before the criteria commit and your history argues against you on the one thing the history is graded for.
>
> **So: draft and commit the five criteria at the end of Milestone 2** — the build is done and verified by 2.8, so you know exactly what the extension does, and nothing has been measured yet. That is the `add unit 9 capstone criteria` commit, and it must precede `milestone 3a`. Milestone 4 then keeps its class slot for the self-check and the pair review; if that review shows a criterion is *unmeasurable* rather than unmet, revise it **underneath** the original line with your reason (the mechanism the brief sanctions) instead of editing the original.

## Milestone 3 — The A half: get it running somewhere that isn't your editor, make it observable, measure the cost

**This milestone is the A half, not setup.** The run path and the log are what shape A would have made the whole job, and `unit9.txt:40` requires them whatever shape you chose: *"the run path and the log are required in every case."* Choosing shape B buys you a different **extension**, not a shorter requirement list — and the build half is graded on *"does it run somewhere that isn't your editor, with a record of it running?"* (`unit9.txt:410`), which is answered here or nowhere. Steps 3.1–3.6 build the layer, including the `curl` examples that make it reproducible by someone who isn't you; 3.7–3.9 **prove it exists** in the repo rather than on your machine.

Order matters: run path → worked `curl` examples → clean-clone test → logging evidence → cost. The examples land *before* the clean-clone test on purpose, so the test exercises the documented HTTP path and not just the terminal you happen to be standing in.

- [ ] 3.1 **One start command.** Add `run.sh` (executable, and `git add --chmod=+x run.sh` so the mode bit lands in the commit) that does exactly what `RUNNING.md` says: activate `.venv`, exit with a readable message if `GEMINI_API_KEY` is missing, **export `AI201_CORPUS="${AI201_CORPUS:-city_guides}"`** — `serve.py` reads `config.CORPUS` with no flag (`serve.py:91`), whose default is `campus_life`, and `questions.py`'s criteria are `city_guides` questions; the pin keeps the service answering from the corpus units 1–2 tuned — build the index if `store.index_exists("city_guides")` is false (the corpus argument matters; the default is the wrong corpus), then `exec python serve.py`. One command, no hidden steps — that is the whole Path B requirement. The server is Flask's development server (`serve.py:132`'s `app.run`), which is the declared choice: **remove the `gunicorn>=23.0,<24.0` pin from `requirements.txt` in the same commit** — it was added "for unit 9"'s production server, and unit 9 no longer runs one (out-of-scope item 5) — and say in the README that the frontend/production serving is out of scope, text only.
- [ ] 3.2 **Rewrite `RUNNING.md:195-222`** ("Running it somewhere else — unit 9", currently a future-tense promise that `serve.py` has no logging). New content: Path B declared; the single command (`./run.sh`); **a worked `curl` for `/health` and for `/ask`** — the two examples `RUNNING.md:201-214` has never contained; what `/health` and `/ask` return including `error_kind` and `request_id`; **the corpus pin** (`AI201_CORPUS=city_guides`, and why: the config default is `campus_life` while the test questions and unit 1–2 tuning are `city_guides`); where the log lives and how to read it (`python metrics.py --tail 10`); the fault harness; one line saying the frontend is out of scope — the service is JSON text only, no page, no browser surface; then the environment section below.
- [ ] 3.3 **Environment section** in `RUNNING.md`: Python 3.12 (supported 3.11–3.13, **not 3.14**), `pip install -r requirements.txt`, **plus the `sentence-transformers>=3.4,<3.5` line the reranker needs** and its size, the two model downloads with sizes and origins (`chroma-onnx-models.s3.amazonaws.com` ~80 MB; Hugging Face `cross-encoder/ms-marco-MiniLM-L-6-v2`), the `chroma_db/` rebuild time measured in 0.3, and the `.env` key.
- [ ] 3.4 **Decide W6 on the record.** `sentence-transformers` is a hard requirement of today's retrieval path but is deliberately **not** in `requirements.txt` — `requirements.txt:12-24` explains why (it drags in ~2 GB of PyTorch, and Chroma's bundled ONNX embedder avoids that), and `RUNNING.md:234-240` mentions it only under *Stretch features*. Two honest endings; **the recommended one is the second**:
  - *Pin it:* add `sentence-transformers>=3.4,<3.5`. Pro: the pinned file describes what the happy path needs. Con: it reverses a documented decision that the starter made on purpose, and it makes every clean install download ~2 GB for a reranker that only reorders 25 candidates down to 7 (`config.py:47`, `:36`).
  - *Recommended — make it genuinely optional:* leave `requirements.txt` alone, ship the degrade path from 2.3 (unreranked RRF order, `degraded.rerank = "degraded"`), and give the model a documented, named line in `RUNNING.md`'s environment section. Then the repo's stated position ("you don't need it") becomes **true**, which is the thing a clean clone currently disproves — and a clean-clone failure becomes a documented, measurable degrade instead of an outage.
  - Whichever you pick, say which in the README under *Running It* and repeat it in `RUNNING.md`'s environment section, and label every Milestone 5 number with the mode that produced it. `RERANK_STRICT = True` restores today's hard failure for anyone who wants the old contract.
- [ ] 3.5 **Prove reachability with text, and nothing else.** The frontend is out of scope (out-of-scope item 5), so this step's job is to prove the text surface works from the doc alone: from a clean terminal, `./run.sh`, then the `curl` commands from `RUNNING.md` verbatim — `/health`, then one real `POST /ask`, then one classified failure (`python tools/faults.py --fault f4_empty_response`) with `error_kind` and `request_id` visible in the JSON body. Paste what came back as text. Confirm the negative space too: `GET /` answers 404 (Flask's default — fine; the interface is out of scope, declared, not forgotten), and `git status` shows no `static/` directory, because a declared absence is a decision and an undeclared one reads as a gap. Hard rules, each one cheap and each load-bearing:
  - **No new route, no new file for the surface.** If a step here starts wanting an `index.html`, that is the signal to stop, not to continue (ground rule 10).
  - **A failure has to look like a failure in the text.** A classified failure is visible in the JSON body and in the log — run **F4** and **F6** and paste both bodies; that is the evidence the page would have rendered, delivered as text instead, sitting next to the log line written for the same request.
  - Smoke it end to end: `./run.sh`, then the doc's `curl` examples, one real question, then `python metrics.py --tail 1` → **exactly one** new record, reading `server: "flask-dev"`.
- [ ] 3.6 **Clean-clone test.** Clone the repo into a fresh folder **outside** the project dir, follow your own `RUNNING.md` top to bottom, paste the real failures. It will fail at least once — likely the reranker, likely a missing `chmod +x run.sh`, likely the venv. Whatever bit you is what a reader hits; fix the *document*, not only your machine. **Finish the test with the documented `curl`, not with a command you memorised:** the last line of the clean clone is copying the `POST /ask` example straight out of `RUNNING.md` and getting a grounded answer, because that is the moment the run path is proven for someone who isn't you (`unit9.txt:56`, `:410`).
- [ ] 3.7 **Produce the log evidence.** Restart via `run.sh`, generate ≥ 12 records in one session: the 5 real `QUESTIONS`, 2 `OUT_OF_SCOPE` refusals, ≥ 3 failures from `tools/faults.py` — driven with the same `curl` commands `RUNNING.md` documents, so "someone else can run this" has lines in the file behind it, not only a sentence in the README. Paste **≥ 10 records verbatim** into README → *Instrumentation*, with at least 3 failures and at least one degrade. Add a sentence on what each record holds and which file/function wrote it (`metrics.py::record`, called from `serve.py::ask`). **Check the provenance field before you paste:** every record from this session must carry `server: "flask-dev"` (plus `pid`/`port`) — those are the fields that make the committed log evidence of a run as the documented server process instead of an editor session, which is the exact thing Path B is graded on. One count that has to be right before you paste: the session's new lines in `logs/runs.jsonl` equal the number of `/ask` calls you made — there is no `GET /` to muddy the count, which is one thing the text-only scope buys.
- [ ] 3.8 **Measure the cost of one run** — measured, not from a pricing page:
  - `AI201_CACHE=0` for the whole measurement, or the cache (`generate.py:60-73`) reports 0 tokens and you silently report fiction. Note in the README that you turned it off, and that a warm rerun legitimately costs nothing — that difference is worth naming.
  - Run **10** distinct real questions over HTTP against a warm server, cache off, with the same `curl` command `RUNNING.md` documents — the measurement then describes the documented run path, not whichever client was handiest. Tokens come from the service, already captured by `_record_tokens` (`generate.py:125-150`), readable per request from the log (`tokens_in`/`tokens_out`) or `generate.token_counts()` (`:169`).
  - Report mean **and max** tokens/run (prompt and output separately), mean/median/max wall-clock, and the `stage_ms` split if you kept it. Expect the prompt to dominate: `TOP_K = 7` (`config.py:36`) chunks plus the grounding instruction is most of the input, and `RERANK_CANDIDATES = 25` (`config.py:47`) means 25 cross-encoder pairs scored per request even though only 7 survive.
  - Seconds of local compute are cost too: report rerank and embed time separately from API wait — a reranker loading on the first request is a local cost with no API line item.
  - Any `$` figure is **arithmetic on measured tokens × a published rate**, labelled as such. The measured number is the token count.
- [ ] 3.9 Paste the cost number and its method into README → *What It Costs*. The 100-people-a-day arithmetic waits for Milestone 7.

**Commit checkpoints (M3a, M3b) — by hand, two of them:**

```bash
git add RUNNING.md run.sh requirements.txt
git commit -m "unit 9 milestone 3a: Path B run path — run.sh, curl examples, gunicorn pin removed, clean-clone fixes"

git add logs/runs.jsonl README.md
git commit -m "unit 9 milestone 3b: committed run log, instrumentation extract, measured cost per run"
```

`git status` after the first one must show `requirements.txt` staged with the gunicorn pin **removed** — a pin whose own comment says it exists "for unit 9" while unit 9 no longer uses it is exactly the drift a reviewer greps for, and `git log --oneline -- requirements.txt` should show the pin arrive (unit 2's history) and leave (this commit), which reads as a decision rather than an accident. `logs/` still gets the same check: nothing in `.gitignore` names it today (verified: it lists only `.env`, Python artifacts, venvs, `chroma_db/`, `.cache/`, OS noise), but this is the class of mistake that silently eats evidence.

**Before you move on:** the system starts from `RUNNING.md` alone and answers a question **with the documented `curl`** on a clean clone; ≥10 log entries carrying server-process provenance and a measured cost number are in the README. That is the A half delivered, and delivered *reproducible by someone who isn't you*: the same bar shape A would have been graded against, met in text.

---

## Milestone 4 — Criteria self-check, unaided *(the drafting happened at 2.9)*

⚠️ **This plan deliberately does not write your five criteria.** The brief is explicit — don't ask a model to author them; a criterion you didn't write is one you can't defend. Below is the *measurement surface* you now have, the discipline each sentence must pass, and a blank template.

Add a `## Unit 9 criteria` block to `criteria.md`. Leave the unit 1/2 criteria exactly as they are.

**What the extension can produce a number for** (choose from these; word them yourself):

| Surface | Field / evidence you'd read |
|---|---|
| Malformed input → 400, not 500 | status + `error_kind` for each bad body (Appendix B, F1, F7) |
| Missing index → 503 with an actionable message, no traceback | F2 response body |
| Model returns nothing → never a `200` with an empty answer | F4: `answer_chars`, `outcome`, `error_kind` |
| Hung upstream → bounded response time | F5: client-side wall-clock vs `GENERATION_TIMEOUT_S` |
| Reranker absent → still answers, and says so | F6: `degraded.rerank`, plus gate/refusal behaviour in that mode |
| Every request incl. failures leaves exactly one record | record count vs request count in `logs/runs.jsonl` |
| **A half** — a clean clone starts from the doc alone | the transcript of 3.6: the fresh clone dir, the commands you typed, the answer that came back **via the doc's `curl` example** |
| **A half** — it ran outside the editor | `server` / `pid` / `port` on the records pasted in 3.7 |
| **A half** — a stranger can reproduce it with the doc alone, not just you with a terminal | the worked `curl` examples in `RUNNING.md` run verbatim from a clean clone, and the F4/F6 failure **pasted as JSON** with `error_kind` and `request_id` visible |
| **A half** — a question about the running system is answerable with no new code | the literal output of `python metrics.py --summary`, plus the question it answered |
| **A half** — cost per run | measured tokens/run from 3.8, with the method named |
| Warm latency | `duration_ms` over N warm runs |

**Both halves are fair game for the "≥ 3 about the extension" rule, but say which one each criterion tests.** The extension is the Milestone 2 hardening layer; the Milestone 3 operational layer is also code that didn't exist when the unit started, so a criterion about the log reader or the run path is a criterion about something you built this unit. If a reviewer could reasonably call it "the mandatory layer rather than the extension", your five still need three that clearly aim at the hardening work — so write the aim into the sentence (*"…about a failure the hardening layer classifies…"*). The curl row above is operational-layer evidence, and a criterion resting on the doc alone is a criterion about reachability, not hardening: let at most one of the five lean on it, and it still has to carry all four parts below. The upside is that pasted JSON makes two hardening criteria *easy* for a stranger to check — F4's classified empty response and F6's degrade are fully legible in the response body and the log line, with nothing to render or open.

**Every criterion must carry all four:**
1. a number, a rate, or a plainly observable thing — if it turns on *works*, *reliable*, *good* or *fast* it isn't a criterion yet;
2. a reason for **that** target and not a stricter or looser one, referencing something about this system or what being wrong would cost;
3. checkable by a person who cannot ask you what you meant;
4. at least one of the five is about the bad path.

≥ **three of five about the extension** — easy here, since the extension *is* the bad path. Spend at most two on retrieval-quality carry-overs from unit 1.

**Settle before you write the sentences:**
- **Warm or any request?** The first request loads the ONNX embedder *and* the cross-encoder, so cold runs are seconds slower. Every latency target must name which it means.
- **What does "10 of 10" mean for a deterministic check?** A malformed-body→400 check doesn't vary; 5 distinct bad bodies × 3 trials is honest, and you should say why determinism doesn't excuse a single run. Anything touching the model must genuinely re-run with cache off — if a model-touching criterion comes out identical three times, you measured the cache (see 3.8).
- **Could a stranger reproduce your failure trigger?** Name `tools/faults.py` in the criterion so two people score it the same way.

```markdown
### 1. <the claim, with a number in it>
**Target:** <n of m / a threshold / an observable thing>
**Why this target:** <something about this system, or what being wrong would cost>
**How it's checked:** <the exact command or artifact — a stranger could run it>
```

**Self-check, each criterion, in order:** how exactly would you test it from the sentence alone; would two people score it the same way; **what would have to happen for it to fail?** The third finds more problems than the other two combined — if you can't picture it, the target is too low. Then the pair review: each of you reads all five of the other's criteria against the same three questions.

**Commit checkpoint (M4) — by hand** (this is the 2.9 commit if you wrote them after Milestone 2):

```bash
git add criteria.md
git commit -m "add unit 9 capstone criteria"
```

**Before you move on:** five numbered criteria with targets, reasons and check-methods, ≥3 about the extension, ≥1 about the bad path, committed while no result exists.

---

## Milestone 5 — Run the test

Three trials each, changing nothing in between. Nobody wrote a test set for you: decide what each criterion must be run against, then run it.

- [ ] 5.1 **Restart clean** via `run.sh` so the log's boundary is unambiguous, and note the timestamp.
- [ ] 5.2 **Produce each criterion's number deliberately.** Failure criteria need *real* failures — `python tools/faults.py --fault <name>` per Appendix B. Latency needs enough runs to be a distribution (≥10 warm), not one number. Cost needs 10 runs cache-off. Read the numbers out of the log with `python metrics.py --summary`; that's the point of building the reader in 2.4.
- [ ] 5.3 **Three separate trials per criterion**, identical inputs, nothing changed in between. Re-read 3.8's cache warning before you trust a triple.
- [ ] 5.4 **Fill the run log** — one row per **criterion** (not per question), five rows minimum:

```markdown
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Malformed input gets 400, not 500 | 5 of 5 | | | | |
| 2. Missing index → 503, actionable, no traceback | 5 of 5 | | | | |
| 3. Empty model response never returns 200 | 5 of 5 | | | | |
| 4. A hung model call answers within 30 s (warm) | 9 of 10 | | | | |
| 5. Every request incl. failures leaves one log record | 10 of 10 | | | | |
```
  Those five rows are a **format example** with placeholder targets — your rows must carry *your* committed criteria and targets, in your committed order.
- [ ] 5.5 **Under the table, paste real output** for each criterion from one run — actual JSON bodies and actual log lines, not descriptions — and name the file and function that produced each (`serve.py::ask`, `metrics.py::record`, `tools/faults.py::f5_timeout`).
- [ ] 5.6 Commit `results/run_<stamp>_unit9-before.md` plus the log with a message that names it as results: `unit 9 results — run log before fix`. This is the commit that must come *after* `add unit 9 capstone criteria`.

**Before you move on:** five criteria, three trials each, pasted output underneath.

---

## Milestone 6 — Diagnose and improve

- [ ] 6.1 **Mark each criterion** in the run log — **MET** or **MISSED**. A criterion that passed is worth as much thought as one that failed: if you can't say *why* it passed, you don't know whether it was the system or a warm cache.
- [ ] 6.2 **One paragraph per miss:** *at which stage did it happen* (`stage_ms` should tell you — bad_input / retrieve / gate / generate), *and what mechanism do you think is responsible* (name the line). If `error_kind` was missing or wrong for a miss, say so — that's an instrumentation failure, not a pipeline failure, and it's still a diagnosis.
- [ ] 6.3 **Pick exactly one fix**, aimed at the *weakest* criterion — the one furthest from its target, usually the one with the least room between the bad path and the target. Candidates this system is likely to hand you:

| If this missed | Where to look | The one fix | What it will cost |
|---|---|---|---|
| Bad path (timeout / empty / malformed / missing index) | `serve.py:66-105`, `generate.py:241-271`, `store.py:284` | the timeout in 2.2, **or** moving validation inside the protected region in 2.6 | low — but check the 400/504 body is *legible*, not just the status code |
| Warm latency | the `stage_ms` split | cut `TOP_K = 7` (`config.py:36`) | ⚠️ **the trap:** it moves a retrieval criterion — permitted only under the exception declared in out-of-scope item 1: re-run everything, name what got worse, and cite the item 1 wording already committed in Milestone 1 (no new scope exception is invented here) |
| Every request incl. failures leaves a record | `serve.py` — is the write in a `finally`? do 400s write? | move/extend the `finally` | low |
| Degraded reranker | `store.py:154-169` | fix the degrade branch and its flag | low |

- [ ] 6.4 **One fix only.** The cap is the point; a second fix in the same commit makes before/after unreadable. Commit separately, naming the criterion.
- [ ] 6.5 **Re-run every criterion, three trials, fresh log**, saved as `results/run_<stamp2>_unit9-after.md` next to the first. Keep **both** sets — one result set is fine; two side by side *is the evidence the loop ran.*
- [ ] 6.6 **Write the comparison:** before → after per criterion; what improved **and what got worse**. Check specifically that your fix didn't move a previously-met criterion (latency↔accuracy is the usual trade); if it did, say so in plain words. A change that fixed one thing and cost another, with the trade named out loud, is full credit — a silent trade is not.
- [ ] 6.7 **If a criterion turns out to be broken rather than unmet, there is only one legitimate repair.** Loosening a target you missed earns nothing ("9 of 10" → "7 of 10" because 9 was hard); replacing a sentence you genuinely could not reach a verdict from ("reliable under load" → "at 10 requests per minute, at least 9 of 10 return a response rather than an error") does. Either way: **never delete the original line** — keep it and put the revision plus the reason underneath it in `criteria.md`, so the history shows what you asked first. Then re-measure the revised one against new runs, not the old ones.

**Commit checkpoints (M6a, M6b) — by hand:**

```bash
git add <the files the fix touched>
git commit -m "unit 9 milestone 6a: <fix> for criterion <n>"

git add results/ criteria.md
git commit -m "unit 9 milestone 6b: run log after fix"   # criteria.md only if you revised one
```

---

## Milestone 7 — Cost, what's broken, the write-up, submit

- [ ] 7.1 **README → *What it costs*:** the cost of one run from 3.8 and its method; a **labelled guess** at 100 people a day; a sentence on how you got from one to the other. Do the arithmetic on your own measured numbers and show the multiplication you did:
  ```
  mean prompt tokens/run ≈ ____   × 100 runs/day = ____ in/day
  mean output tokens/run ≈ ____   × 100 runs/day = ____ out/day
  × published rate for gemini-flash      = $____/day, ≈ $____/30 days
  ```
  Say plainly that the tokens came from the API response, and that the money is **arithmetic on a published rate, not a bill**.
- [ ] 7.2 **README → *What's still broken*, honestly:** the three things to fix next *unit*, named in order. The honest leftovers are already written down in this plan — the abandoned timeout thread (2.2), the per-process `LAST_RETRIEVAL` global that is only safe single-user (2.3), no queue or backpressure so retrieval degrades silently under load, the reranker dependency question (3.4), and the fact that `TOP_K = 7` was tuned to the five test questions rather than derived, so the numbers don't generalise beyond them — unit 2's own *What's Still Broken* says this in its last paragraph (`README.md:752-756`). Fold in where-this-goes-next: a hosted version, a real corpus instead of the fictional `city_guides` guides, and the two fixes unit 2 itself names (`README.md:752-756`): test against a larger question set, and re-derive `TOP_K` instead of inheriting the tuned value — then re-run `run_eval.py`. "No auth yet" is fine here. "It works" is not.
- [ ] 7.3 **README structure — the real situation, checked.** The brief does **not** ask you to reorganise the README; it asks for **nine named sections, "added to what's already there"**: *What This Extends · The Shape · Running It · Instrumentation · What It Costs · Run Log and Verdicts · The Improvement · What's Still Broken · How I Used AI*. Those exact names are what a grader greps for. What the file actually looks like today: `# Unit 1` (`:8`: *What This Does, Chunking Strategy, Sample Answer, How I Used AI*…) then `# Unit 2` (`:309`: *Run Log — Before, Verdicts, Diagnoses, The Improvement, What's Still Broken* at `:745`) — unit 2 already used several of the nine names **inside its own block**, which is exactly why the unit 9 block must repeat them under its own heading rather than lean on them.
  - **The move:** finish the `# Unit 9` block started in 1.1, in place at the end of the file, with the nine sub-headings spelled **exactly** as the brief spells them — three drafted in Milestone 1, the other six filled from Milestones 3, 5, 6 and 7.1/7.2. Where a unit 2 section is now superseded, add a pointer line under it (*"unit 2's list, kept as history — the current one is under `# Unit 9`"*) instead of editing it: overwriting unit 2's verdicts destroys before/after evidence unit 2 earned (ground rule 6).
  - **Everything pasted as text** — the ten log records (3.7), both run-log tables, the cost arithmetic. The brief says it twice: **no screenshots, no video.** What you saw scroll past your terminal is *not* the evidence — paste the JSON the request returned and the log line it wrote instead.
- [ ] 7.4 **Justify Path B under *Running It*, and claim the A half while you're there.** Not required as a confession, but the brief says a path switch deserves a sentence and Path B has to carry "the environment it needs." Write: "The retriever runs two local models — an ONNX embedder and a cross-encoder — so a 512 MB free tier cannot hold both; the honest move was to keep it local, make it observable, and say so." Then say, under the same heading, that shape A's requirements were **carried, not skipped**: one documented start command, a service a stranger can drive from the doc's own `curl` examples, one structured record per request including failures, a log that answers questions without new code, and a measured cost per run — and point at the `server`/`pid`/`port` fields on the pasted records as the proof those runs happened under the documented server process. Close with the two sentences the text-only scope earns: one line naming the frontend as **out of scope** — no page, no `GET /`, no gunicorn; the service serves JSON text over the routes unit 2 shipped — and one line saying why that's the right weight here (a single-user local run; `unit9.txt:143`'s "I'm not rebuilding the interface", taken all the way). Path B is a smaller *deployment*, never a smaller *set of requirements*.
- [ ] 7.5 **Re-read the README as a stranger** who has never seen this repo and cannot ask you anything. That's who it's written for.
## Final self-check — actually perform these, don't assume

- [ ] The system runs: `./run.sh`, then a real question answered (`RUNNING.md:226-233`'s checklist).
- [ ] The extension is demonstrable: `python tools/faults.py --fault f4_empty_response`, and the classified response that comes back.
- [ ] You can show it got better from what you measured: the two run logs side by side, not a claim.
- [ ] Criteria are in `criteria.md`, results are in `results/`.
- [ ] Log entries are real and at least three of the ten pasted ones are failures.
- [ ] You can say what a run costs and how you worked it out.
- [ ] **The A half — run it as its own block, because no other line on this list covers it:**
  - [ ] A clean clone in a fresh folder starts from `RUNNING.md` alone, with no command you actually used missing from the doc (3.6), **and the last thing that test does is ask a question with the doc's own `curl` example against `/ask` — nothing memorised, everything read straight from the doc.**
  - [ ] The committed `logs/runs.jsonl` is in the repo (`git log --oneline -- logs/runs.jsonl` is non-empty), parses with `json.loads` line by line, holds **≥ 10 records with ≥ 3 failures**, **≥ 3 of them under `server: "flask-dev"`**, and ≥ 3 of those failures are pasted in the README.
  - [ ] Those records carry `server` / `pid` / `port` from the documented server process — i.e. the log proves it ran outside the editor, and *Running It* says so.
  - [ ] One question about the running system is answered by pasted `python metrics.py --summary` output, with no new code written between the run and the answer.
  - [ ] **The service is exactly the text it claims to be:** no page ships (`grep -rn "static/" . --include="*.py"` prints nothing, `git check-ignore -v static/` prints nothing), `GET /` returns 404 and the README says that's the point, and *Running It* declares the interface not rebuilt (`unit9.txt:143`).
  - [ ] The cost of one run is a measured number with its method beside it, and the README says the cache was off while measuring.
- [ ] **The four submission files exist by name:** `criteria.md`, `RUNNING.md`, `README.md`, and the commit history. Nothing else substitutes for them.
- [ ] All nine of the brief's README sections are present under `# Unit 9`, spelled as the brief spells them, **everything pasted as text — zero screenshots, zero video links.**
- [ ] `git log --oneline | wc -l` grows by **≥ 8** since `d43f3e0`, and the two named commits sit in the right order.
- [ ] Nothing sensitive: `.env` still untracked (`git check-ignore -v .env` reports a hit), `git log --all --name-only | grep -x .env` prints nothing, and the key appears in **no** README/log/results line — check without echoing it: `grep -rqF "$GEMINI_API_KEY" README.md RUNNING.md logs/ results/ && echo LEAK || echo clean`.
- [ ] Same repository, not a copy: `git remote -v` still points at the repo you submitted for units 1–2, and `d43f3e0` is still an ancestor of `HEAD` (no history rewrite, no re-created repo).

## Submission

- [ ] `git add -A`, then `git status` — are `logs/` **and `results/`** in it, and `serve.py`/`run.sh` changes staged? is `.env` *not*? `.gitignore` already handles `.env`, `.venv/`, `chroma_db/`, `chroma/` and `.cache/`, and deliberately does **not** ignore `results/` (`:26-27`) — `logs/` isn't mentioned either way, so it commits fine (confirm with `git check-ignore -v logs/runs.jsonl`, which must print nothing). `static/` should not exist to be staged — if `git status` lists it, the page was rebuilt instead of cut.
- [ ] ⚠️ **`unit9.txt` is sitting untracked in the repo right now** (it's the brief text, 25 KB). `git add -A` will sweep it in. Decide on purpose: `rm` it or move it out of the repo — leaving the assignment prompt committed next to your README reads as untidiness, and it's the one file a reviewer will ask about.
- [ ] `git commit -m "unit 9 capstone: hardening the RAG system against failure"` (one final commit is fine).
- [ ] **Push it** — your final commit is what gets graded. No history rewriting, no squashing, no force-push from here: the brief's "do not delete or recreate your repository" is literal, and this unit's history is the only proof that the criteria predates the results.
- [ ] `git log --oneline` and read the order: does `add unit 9 capstone criteria` come **before** the first results commit, and are both named in their messages? If the history doesn't prove the order, the milestone reads as unmet however good the code is.
- [ ] Submit the **repository URL of the system you extended** — the same URL you submitted for units 1–2, not a new repo and not a copy. Both halves (build and test) are submitted with it this unit.

---

## Appendix A — `logs/runs.jsonl`, one record per request

One JSON object per line, appended by `metrics.py::record`, called from the `finally` in `serve.py::ask`. Fields marked ★ are the ones the brief mandates (input, output, duration, plus failure kind and degrade flag). Fields marked ◆ aren't named by the brief but carry Path B's evidence: without them the log can't claim it came from somewhere other than your editor. One record per **`/ask` call** — `GET /` doesn't exist, so the count of lines *is* the count of requests, which is what makes "every request leaves exactly one record" countable.

```json
{
  "ts": "2026-11-07T14:22:03.481+08:00",              // ★ ISO-8601, local tz
  "request_id": "9f3c1a02",
  "server": "flask-dev",                                 // ◆ "flask-dev" | "cli" — proof it ran outside the editor
  "pid": 41807, "port": 8000,                           // ◆ which process answered, on which port
  "endpoint": "/ask",
  "question": "How expensive is it to stay at Thornby Wells?",  // ★ input, truncated to 200 chars
  "outcome": "answered",                              // ★ answered|refused|degraded_answered|error
  "error_kind": null,                                 // ★ null | bad_input | no_index | model_timeout
                                                      //   | model_empty_response | upstream | quota | internal
  "stage": null,                                      // where it failed: bad_input|retrieve|gate|generate
  "http_status": 200,
  "degraded": {"rerank": "ok"},                       // ★ ok|degraded, plus any other flag later
  "duration_ms": 1240.5,                              // ★ whole request
  "stage_ms": {"retrieve": 812.4, "gate": 0.1, "generate": 414.9},
  "n_results": 7, "n_candidates": 16, "top_score": 0.62,
  "refused": false, "refusal_reason": null,           // gate decision, kept separate from error_kind
  "answer_chars": 412,                                // ★ output summary, not the whole answer
  "answer_head": "Thornby Wells is the mid-priced guest house…",  // first 120 chars
  "tokens_in": 1893, "tokens_out": 96,                // from generate.token_counts()
  "attempts": 1,
  "cache_hit": false,
  "model": "gemini-3.5-flash-lite"                     // whatever config.MODEL resolves to (config.py:88)
}
```

The `//` notes are for reading only — what `metrics.py` writes is **strict JSON with no comments**, one object per line, so `json.loads` on every line of `logs/runs.jsonl` must succeed. `test.py`'s style of assertion is a fine place to prove it: read the file back and parse every line.

Deliberate choices, all defensible in the README:
- **`answer_head` + `answer_chars`, not the whole answer** — the log is an instrument, not a second database, and the full answer is reconstructible from the cache. If you want the whole thing, that's one more field and one more sentence about size.
- **`outcome` and `error_kind` separate** — a refusal is a *correct* outcome with no error; an error is never a refusal. Conflating them is how W2's empty answer looks like a pass.
- **Timestamp with timezone** (`datetime.now().astimezone()`), because a log without a zone can't be compared to a run log entry.
- **`server` / `pid` / `port`** — Path B's requirement is *a record of it running* somewhere that isn't your editor (`unit9.txt:49`–`:52`, `:410`). A record with no process provenance cannot make that claim: the identical line could have come from `python serve.py` in a terminal or from `app.py ask` inside an editor. Resolve `server` once per process at import (`app.run` vs the CLI paths are distinguishable without guessing), stamp `pid` and the bound port, and keep `model` for *what answered* so the two never blur. Three lines, and the only provenance field a reviewer can check without trusting your prose.
- **`server` is provenance; there is no `channel` field.** Under the documented run path every record is `server: "flask-dev"`; the CLI writes `"cli"`. No client header is recorded — a header the client sends is *claimed* provenance, not evidence, and with a single documented surface there is nothing to distinguish. If a reviewer asks "did browser traffic fail differently from curl traffic?", the answer is that there is no browser traffic: one route, one client, one kind of record.
- **Never raises.** A logging failure must not become a 500. Copy the repo's own attitude at `generate.py:145-146` — `except Exception: pass  # accounting never breaks the thing it is accounting for` — but add the one line to stderr that the rate-limit notice at `generate.py:262-266` already models, so a silent logging failure is still findable (that's fault F10).

## Appendix B — fault-injection recipes for `tools/faults.py`

Every fault is injected from the harness, never by an `if FAULT:` branch inside production code. Each prints: name → injection → status + body → whether a `logs/runs.jsonl` record appeared. **Run F4 and F6 against the server with the harness's `curl` and paste the full JSON response body plus the log line** into your run log: those two are the faults a reviewer can see working without reading a line of code, and "`model_empty_response` came back with a `request_id`, and the log line matches it" is stronger evidence than a status code only you looked at.

| # | Fault | Injection | Expected after M2 |
|---|---|---|---|
| F1 | Missing / non-string question | POST `{}`, `{"question": 123}`, `{"question": ""}`, `{"question": "x"*5000}`, non-JSON body | **400** `bad_input`, logged |
| F2 | Index missing | `mv chroma_db chroma_db.bak` → POST → `mv` back (in a `finally`) | **503** `no_index`, message names `python app.py index` |
| F3 | Invalid API key | set `GEMINI_API_KEY=AI201_invalid_key_for_testing` in the harness's `env` for a subprocess server | **502** `upstream`; body must **not** quote the provider |
| F4 | Empty model response | monkeypatch `generate._get_client` to return an object whose `models.generate_content(**kw)` returns `SimpleNamespace(text=None, usage_metadata=None)`; run the server as a subprocess so the patch is in-process | **502** `model_empty_response`, never a 200 with `answer: ""` |
| F5 | Hung upstream | same stub, but `generate_content` does `time.sleep(120)` before returning text | **504** `model_timeout` in ≲ `GENERATION_TIMEOUT_S`; measure client-side wall-clock, that's the number criterion N needs |
| F6 | Reranker unavailable | run server with `PYTHONPATH` pointed at a temp dir containing a `sentence_transformers.py` that raises `ImportError` on import | **200**, `degraded.rerank == "degraded"`, answer still cites sources |
| F7 | Broken retrieval mid-pipeline | monkeypatch `store.search` to `raise ValueError("boom")` | **500** `internal`, `request_id` present, no traceback in body |
| F8 | Rate limit | two sub-flavours: (i) retry succeeds — stub returns a `"429 Resource has been exhausted"` error then good text; (ii) exhausts — always that error | (i) 200 with `attempts ≥ 2`; (ii) **502** `upstream` with a *clean* message, not today's raw text |
| F9 | Body-level abuse | wrong `Content-Type`, giant body, `[]` instead of `{}` | 400/415, logged, server still up |
| F10 | Log write blocked | run with `AI201_LOG_DIR=/root/nowhere` | request still **200**, one line on stderr, no 500 — proves the logger can't take the system down |

F1/F2/F3/F9 need no code changes and can also produce your Milestone 2.0 "before" evidence. F8's message-matching depends on `generate.py:252-258`'s `rate_limited` pattern list (`"429"`, `"resource"`+`"exhaust"`, `"rate"`+`"limit"`) — that coupling is real and belongs in a comment so unit 10 doesn't "fix" the retry by rewording the pattern list.

---

## Appendix C — file inventory

| File | Status | What changes |
|---|---|---|
| `errors.py` | **new** | exception types + `classify()` — the taxonomy, in one place |
| `metrics.py` | **new** | append a JSONL record; read/summarise the log — `--summary` is never cut (§3), it's what makes the brief's observability requirement true |
| `tools/faults.py` | **new** | the fault harness (Appendix B) |
| `run.sh` | **new** | the single start command — `exec python serve.py` — the A half's "one documented start command", and the thing a clean clone is tested against (3.1, exercised by 3.6) |
| `logs/runs.jsonl` | **new, committed** | the evidence — never git-ignored; carries `server`/`pid`/`port` so it proves a run outside the editor, not just a request |
| `results/run_<stamp>_unit9-{before,after}.md` | **new** | two run logs, both kept |
| `config.py` | edit | `GENERATION_TIMEOUT_S`, `EMPTY_RESPONSE_RETRIES`, `MAX_QUESTION_CHARS`, `LOG_DIR`/`LOG_FILE`, `RERANK_STRICT`, each env-overridable |
| `generate.py` | edit, inside `generate()` only | timeout wrapper; empty → retry once → raise; expose attempts |
| `store.py` | edit, two spots | `NoIndexError` at `:284`; reranker degrade at `:154-169`; `LAST_RETRIEVAL` flag |
| `app.py` | edit, `ask_pipeline` only | `request_id`, `stage_ms`, `duration_ms`, `error_kind`, `degraded` — additive keys |
| `serve.py` | edit | validation + status mapping + `finally` log write; `/health` gains reranker state; **no new routes** — the service stays JSON text over the routes unit 2 shipped (frontend is out of scope) |
| `criteria.md` | append | the `## Unit 9 criteria` block |
| `RUNNING.md` | rewrite `:195-222` + env section | Path B, one command, log reader, model downloads |
| `README.md` | edit | the `# Unit 9` block carrying the brief's nine sections — nine names scaffolded in 1.1, then the measured cost, both run logs, the honest "still broken", Path B justification |
| `unit9.txt` | decide | the assignment text is untracked in the repo today; move it out or delete it before the final `git add -A` (Submission) |
| `requirements.txt` | one-line decision | **leave as-is** per 3.4 (reranker becomes optional via the degrade path) — or add `sentence-transformers>=3.4,<3.5` and say why you reversed the starter's reasoning. **`gunicorn` is removed** in the M3a commit: the documented run path is the Flask dev server, and production serving is out of scope with the frontend (`unit9.txt:143`). |

Untouched on purpose: `app.py` CLI surface, `chunker.py`, `gate.py`, `scorer.py`, `corpus_info.py`, `ingest.py`, `run_eval.py`, `test.py`, `tools/smoke_test.py`, `corpora/`, `criteria.md`'s unit 1/2 blocks, `.gitignore`.

## Appendix D — the commit ledger you should be able to read afterwards

```
unit 9 milestone 1: scope …                                    (before any code)
unit 9 milestone 2a: error taxonomy, timeout, empty-response failure, reranker degrade
unit 9 milestone 2b: structured JSONL log, timings, status mapping
unit 9 milestone 2c: fault-injection harness
add unit 9 capstone criteria            ← BEFORE every results commit
unit 9 milestone 3a: run path rewrite (run.sh → serve.py, RUNNING.md), gunicorn pin removed  ← the A half
unit 9 milestone 3b: committed run log, instrumentation extract, measured cost  ← the A half
unit 9 results — run log before fix     ← the pair the history is graded on
unit 9 milestone 6a: <fix> for criterion <n>                   (exactly one)
unit 9 milestone 6b: run log after fix
unit 9 capstone: hardening the RAG system against failure
```
**The brief's floor is eight new commits from this unit**, with `criteria.md` committed before any results and **both** of those commits named in their messages (`unit9.txt:384`) — the ten above clear it with two to spare, and the ledger should read top to bottom in this order. The "at least three commits in this milestone alone" ask (`unit9.txt:180`) sits on **Milestone 2**, which is why M2 carries 2a/2b/2c; M3 lands as the two named checkpoints above. Roughly 550–710 added lines: `errors.py` ~60, `metrics.py` ~90, `tools/faults.py` ~140, `serve.py` ~75, `generate.py` ~40, `store.py` ~30, `app.py` ~25, `run.sh` ~25, plus docs. Docs count.

## Appendix E — what could still go wrong

| Risk | Consequence | Check | Mitigation |
|---|---|---|---|
| Local Python is 3.14 (supported: 3.11–3.13) and there is no verified `.venv` | the 2 GB torch install stalls or breaks | 0.1 | `brew install python@3.12`; treat the install as the unit's biggest download |
| No index and you forget to rebuild | every criterion fails at once | 0.2 | `run.sh` builds if missing; it's step one of every trial |
| Response cache answers three "trials" identically | a false MET you can't defend | 3.8 | `AI201_CACHE=0` for all measurement; say so in the run log |
| Timeout thread left running | resource leak under load | 2.2 | name it in *What's still broken*; the documented run is single-user local, so nobody's request queues behind the leak |
| `LAST_RETRIEVAL` global misreports under concurrency | an observability lie | 2.3 | the documented run is single-user local; note it before a reviewer finds it — it bites only if the load stretch is taken |
| `logs/runs.jsonl` accidentally ignored | the evidence isn't committed | 3.6, 3.7 | `git status` after the first write; `git check-ignore -v logs/runs.jsonl` prints nothing — the path doesn't appear in `.gitignore` today |
| The A half reads as "setup" and gets trimmed when the build grows | build-half Q2 has no answer and a requirement that applies to every shape goes unmet, however good the hardening is | §3's never-cut list, 3.1–3.9, Final self-check's A-half block | cut from the B half first (§3's ordered list); the A half's five **mandated** artifacts stay: `run.sh`, `RUNNING.md`, the log, ≥10 pasted entries, the cost number. The frontend is already declared out of scope, so trimming the B half is a decision you can state — trimming those five is not |
| The one fix is TOP_K and it moves a retrieval criterion | a worse system wearing a better score | 6.3 | re-run everything; report what got worse — the move is sanctioned by the exception declared in out-of-scope item 1 at Milestone 1, and the fix commit cites it |
| Criteria committed after results | milestone 4 reads as unmet regardless of quality | 2.9, Final self-check | write criteria at end of M2; read `git log --oneline` before pushing |
| A 400 body leaks an exception string | the W3 leak reopens at a new edge | 2.6 | F1/F7 assertions check the body has no traceback |
| README headings drift from the brief's nine names | a grader can't find the sections and marks them absent | 1.1, 7.3 | scaffold the exact names in M1; `grep -n '^#' README.md` before pushing |
| Fault harness leaves the repo dirty (renamed `chroma_db`, stray `.env`) | the next session starts broken | Appendix B | each fault restores its state in a `finally`; `git status` clean at the end of every fault run |
| The JSON surface grows into a second extension (new endpoints, response shaping for hypothetical clients, client-state features) | the one-thing rule (`unit9.txt:42`) is broken and *The Shape*'s claim becomes untrue on the surface a reviewer touches most | ground rule 10, §2.6 | no route is added beyond what unit 2 shipped; the moment a change serves a hypothetical client instead of the five criteria, it's out |
| A request errors but leaves no record (an early return skips the `finally`) | "every request leaves exactly one record" stops being countable and the log understates traffic | 2.6, 3.7's line count | the log write lives only in `ask`'s `finally`; count new lines against `curl` invocations in the F1–F10 run |
| A `print()` debug line sneaks into the JSONL stream | the log stops parsing and the `json.loads` check fails | 2.8, Appendix A | logging goes only through `metrics.py::record`; the parse-every-line check runs after every session |

## Not doing, and why (say this out loud if asked)

Retrieval tuning (chunks, weights, model swap) — those are unit 1's dials and moving them would make the new criteria unattributable, which is why they are out outright; `TOP_K` is the single declared exception (out-of-scope item 1): it may move once, as the Milestone 6 improvement, if and only if the diagnosis points there. A new CLI surface — `app.py ask` already does everything; new verbs are surface, not capability. A frontend — out entirely, no exceptions and no thinnest-possible-page compromise: no browser page, no `GET /`, no gunicorn; the service stays the JSON text API unit 2 shipped, and every interaction is `curl` against the documented examples (ground rule 10). The interface wasn't rebuilt — it was never on the board (`unit9.txt:143`). Redis, a queue, auth, rate limiting — none is a bottleneck in this system, and inventing a fix for a bottleneck you haven't hit is the shape of work this course is asking you to stop doing. A second shape *as a choice* — breadth is explicitly worth less than one loop completed; note that this does **not** mean shape A was skipped, since only shape A *as an alternative* is out, while its run path, log, instrumentation and measured cost are in, because `unit9.txt:40` demands them of B and C too. Hosted deployment — see out-of-scope item 2; the system still runs as a service a stranger can reach, just on the machine in front of you.
