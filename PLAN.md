# Unit 9 Capstone — Execution Plan

**System being extended:** The Unofficial Guide — RAG over the `city_guides` corpus, in this repo (the one submitted for units 1–2). The service serves text only: JSON over the two HTTP routes unit 2 shipped (`POST /ask`, `GET /health`), exercised with `curl`. There is no browser surface in this repo and none is added — an interface is declared out of scope at Milestone 1 (out-of-scope item 5), which is the brief's own model answer, "I'm not rebuilding the interface" (`unit9.txt:143`).
**Shape:** **B — Harden against failure, carried alongside the required A half.** `unit9.txt:40` is explicit: *"all three still deploy and instrument — shape A just makes that the whole job, while B and C carry it alongside. The run path and the log are required in every case."* So this unit ships **A + B**: the hardening layer is the chosen extension, the operational layer (run path, instrumentation, measured numbers) is the part every shape must also deliver.
**Run path:** **Path B — local with logs, one documented start command, committed run record, text only.** `run.sh` starts `python serve.py`, and the service is exercised with `curl` against the two routes unit 2 already shipped (`POST /ask`, `GET /health`) — JSON text, no HTML, no browser surface. No interface is built or claimed (out-of-scope item 5), and the starter's `gunicorn` pin is already gone — pulled before Milestone 0, together with both places that advertised it, because the documented path runs Flask's dev server. Path A (hosting) is out of scope, not the run path — `unit9.txt:54` directs a system that loads local models to Path B.
**This plan's only artifact is this file.** No source file has been created or edited — the repo now sits **two commits ahead of `d43f3e0`** (`ef11850 Unit 9 - planning docs`, `b851c4e refactor plan to change scope -- no frontend`), with this file's review edits uncommitted. Both planning commits already count toward the ≥8-commit floor, so Milestones 0–7 need six more (Appendix D schedules eleven). No milestone work has started. Every commit below is a checkpoint *you* read the diff for and run by hand.

The assignment text is in this repo as `unit9.txt` (**tracked** — it was committed in `ef11850`, 416 lines) — every requirement quoted or paraphrased below was read from it, and **where this plan and `unit9.txt` disagree, `unit9.txt` wins.** The grading rubric is in `unit9_rubric.txt` (67 lines, **untracked**, the file `git add -A` would sweep in at Submission — see the corrected note there). Code line references (`file.py:NN`) were verified against the current working tree at the time of writing; re-check one before you act on it if you've edited that file since.

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
4. ≥ 8 new commits are required this unit. **Two are already banked** (`ef11850`, `b851c4e` — the planning commits on top of `d43f3e0`), and this plan schedules **eleven** more (Appendix D), so the floor is met with margin even if a couple get combined.
5. Everything landing in `README.md` / `RUNNING.md` is pasted **as text** — no screenshots, no video.
6. **Do not delete unit 1 / unit 2 content.** Unit 9 is appended. Revised criteria keep the original line with the revision underneath.
7. `results/` and `logs/` must stay committable. `results/` already is (`.gitignore:26-27` says so out loud); `logs/` is not ignored today — re-verify before Milestone 3.
8. **The A half is not optional because shape B was chosen.** The run path, the structured log, the ten pasted entries and the measured cost number are required in every shape (`unit9.txt:40`, `:89`–`:95`). They are scheduled at Milestone 3 and they are graded on their own (build-half Q2), so nothing in the cut list may remove them.
9. **No time tracking.** This plan carries no estimates for steps or milestones and none should be added; scope is managed through §3's cut list by what evidence would be lost, not by minutes. The one exception is the brief's own ~90-minute ceiling on Milestone 2 (§3's size check), which is a stopping rule, not an estimate.
10. **The service stays text-only.** The interface is exactly what unit 2 shipped — `POST /ask` and `GET /health`, JSON, exercised with `curl` — plus the `app.py` CLI. No HTML page, no `GET /`, no static assets, no gunicorn, no new endpoint, no new dependency for the surface. The frontend is declared out of scope (out-of-scope item 5), and that declaration is a decision made at Milestone 1, not a trim taken later; the moment anything wants to render in a browser, it is out of this unit by this rule.

---

## 1. Decisions locked in

| Question | Decision | Why |
|---|---|---|
| Which system | The Unofficial Guide, `city_guides` | The one whose weak points you know from memory — which is what unit 9 asks you to write criteria about. Retrieval quality was already tuned in unit 2, so nothing has to be redone. |
| Shape | **B — Harden against failure**, carried alongside the **required A half** | The failure handling genuinely isn't there (nine verified weak points below; Appendix B turns them into six injectable faults, each with a bad outcome today), and the bad path is where this rubric's points live. Shape A is not a competing option here: `unit9.txt:40` makes the run path and the log mandatory in every shape, so A is *carried*, not chosen. |
| The two halves | **B = the extension** (the hardening layer → Milestone 2). **A = the required operational layer** (run path, structured log, measured cost, observability → Milestone 3). | Naming them separately keeps the scope story honest in both directions: *The Shape* claims one extension, while *Running It*, *Instrumentation* and *What It Costs* deliver the half the brief requires regardless of shape — and build-half grading Q2 (`unit9.txt:410`) is answered there and nowhere else. It also tells you at 2.9 that the operational layer is new code, so criteria about it count toward "at least three about the extension". |
| Run path | **Path B — local with logs** | Retrieval loads **two** local models: Chroma's ONNX `all-MiniLM-L6-v2` (~80 MB) *and* the cross-encoder `ms-marco-MiniLM-L-6-v2` via `sentence-transformers` (`store.py:125-151`), which drags in PyTorch (~2 GB installed). A 512 MB free host cannot hold that. Path B is worth the same and is the honest answer here — and it narrows *where* the system runs, never *what it must show*: the A-half requirement list arrives intact at Milestone 3. |
| Web surface | **None — text only, nothing to remove.** The interface is the two routes unit 2 shipped (`POST /ask`, `GET /health`) plus the `app.py` CLI, driven with `curl` | A declaration, not a removal (`unit9.txt:143`: "I'm not rebuilding the interface"). Worked `curl` examples in `RUNNING.md` give a stranger reproducibility; a classified failure shows in the JSON body and the log. The `gunicorn` pin and both places advertising it were removed before Milestone 0; `grep -rn gunicorn requirements.txt serve.py RUNNING.md` is a regression guard. |
| The one extension | **Every request leaves the pipeline with a classified outcome and a log record**: bounded execution time, no traceback to a caller, no silent empty answer, and no hard dependency on the reranker to answer at all. | One sentence, one thing. Everything in Milestone 2 serves that sentence. The operational layer is **not** a second thing this plan is doing — the brief mandates it in every shape (`unit9.txt:40`), so it doesn't count against the one-thing rule; see 1.6 for how to say this in the standup. |
| Instrumentation | Structured JSONL, one record per request including failures (`metrics.py`), **plus a reader that answers questions about the running system without new code** (`metrics.py --summary`) | Two separate requirements sit on this line: the log itself (*"at minimum a timestamp, what came in, what came out, and how long it took"*, `unit9.txt:92`) and *observability* as the brief defines it — *"answer a question about a running system without adding new code first"* (`unit9.txt:25`). The writer satisfies the first; only the reader satisfies the second. Both also make the Milestone 5–6 diagnosis possible. Records carry process provenance (`server`/`pid`/`port`) but no traffic channel — there is no page, so there is no traffic to separate. |
| Stretch | **One: a latency breakdown** (declared in the README at Milestone 1). The other three are declined | `stage_ms` is built anyway as diagnosis; declaring it before it is built and pasting the measured per-stage table over the 3.8 cost runs is what turns it into the +1 (`unit9_rubric.txt:62`). A second improvement would make the Milestone 6 before/after ambiguous, a 10× load run would measure the dev server and a single-user global, and both run paths means hosted deployment, which Path B rules out. §3's stretch block has the detail |

**The shape in one paragraph** (goes in README under *The Shape*):

> Unit 9 adds a hardening layer around the existing five-stage pipeline. A request to `POST /ask` now either returns a grounded answer, a gate refusal, or a *classified* failure — bounded by a wall-clock timeout, mapped to a status code, carrying a machine-readable `error_kind` — and in all three cases it leaves exactly one structured record in `logs/runs.jsonl`. Answer quality is deliberately unchanged: retrieval, chunking, the gate threshold and the prompt are exactly what unit 2 left behind.
>
> Carried alongside it is the operational layer the brief requires of every shape, not just shape A: the system starts from one documented command (`run.sh` → `python serve.py`) instead of from the editor, it answers over the HTTP surface unit 2 already shipped as JSON text — `POST /ask` and `GET /health`, exercised with `curl` — every request, every failure included, appends one structured record that `metrics.py` can summarise without adding new code, and the cost of a run is measured rather than read off a pricing page. There is no browser surface and none is added, declared as such: no page, no `GET /`, no production server. What makes the service reproducible by someone who isn't you is the documentation instead — worked `curl` examples in `RUNNING.md` that a stranger can run verbatim from a clean clone. So: **shape B, with shape A delivered beside it**, because the run path and the log are required in every case.

---

## 2. What the system does today — verified weak points

Read off the code, not assumed — line numbers verified against the current tree. Confirm each one empirically in step 2.0 **before** changing anything: that is your "before" evidence, and it is what the criteria you draft at 2.9 are written against.

| # | Today's behaviour | Where |
|---|---|---|
| W1 | **No timeout exists anywhere in the repo** (`grep -rn timeout *.py` → no hits). `client.models.generate_content()` blocks for as long as the service likes, inside the HTTP request. | `generate.py:241` |
| W2 | **An empty model response is returned as a success.** `(response.text or "").strip()` yields `""`, which flows through `ask_pipeline` into a `200` with `"refused": false` and a populated `sources` list. A caller cannot tell "the model said nothing" from a good answer — and unit 1's criterion 2 ("every answer names a source") *passes* on an empty answer. | `generate.py:243` → `app.py:268` → `serve.py:94-104` |
| W3 | **Every pipeline exception becomes the same 500**, raw exception text handed to the caller, nothing written down. A missing index is indistinguishable from an API outage. | `serve.py:89-92` |
| W4 | **A missing index is a 500.** `search()` raises a bare `RuntimeError("No index called …")` into W3, while `/health` already knows the index is missing (`index_ready: false`). | `store.py:281-286`, `serve.py:48-50` |
| W5 | **Malformed input can 500 instead of 400.** `question = (payload.get("question") or "").strip()` sits *outside* the `try` (which starts at line 89), so `{"question": 123}` raises `AttributeError` and Flask answers 500 with an HTML traceback page. A missing or non-JSON body is the only handled case (→ 400). | `serve.py:75-87` |
| W6 | **Retrieval hard-fails if the reranker can't load.** `_rerank()` sits on the happy path of `search()` (`store.py:331`) and calls `_cross_encoder()` unconditionally for any non-empty result set (`store.py:168`), which raises if `sentence_transformers` isn't importable or the weights won't download. **`requirements.txt` does not list `sentence-transformers`** — and `requirements.txt:12-24` explains that omission as a *deliberate* choice (PyTorch, ~2 GB), while `RUNNING.md:240-246` mentions the package only as the prerequisite for a *stretch* option (`:17-33`'s install steps never install it). A clean checkout that follows `RUNNING.md` therefore builds an index fine and then fails on *every* `ask` / `retrieve` / `POST /ask`. Verify in Milestone 0 — this is the single biggest finding in the repo. | `store.py:125-151`, `:168`, `:331`, `requirements.txt:12-24` |
| W7 | **Pacing sleeps or explodes inside a request.** `_wait_for_slot()` can `time.sleep()` up to ~60 s while a client waits, and passing `SESSION_REQUEST_BUDGET` raises `QuotaGuard` mid-request → W3. ⚠️ Note *where* the sleep sits: `_wait_for_slot()` runs before the SDK call inside the retry loop, so the wall-clock bound added at 2.2 wraps the **model call**, not the pacing — a slept request can outlast `GENERATION_TIMEOUT_S` with no timeout firing. Handled in 2.2. | `generate.py:89-123`, `:241`, `config.py:95-97` |
| W8 | **Nothing is recorded.** No `logging` import exists anywhere (`grep -rn -e 'import logging' -e 'logger.' *.py tools/*.py` → no hits). `serve.py:22-26` says this is deliberate and that unit 9 supplies it. | repo-wide |
| W9 | `run_eval.py::run_once` has no error handling, so one bad upstream during an eval aborts the whole run instead of scoring it. **Deliberately not fixed this unit** (out-of-scope item 4: the CLI and its harnesses stay as shipped) — named here, and named again in *What's Still Broken*, so it reads as a decision rather than an oversight. | `run_eval.py:54-68` |

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
3. **Traffic handling.** No auth, API keys, per-client limits, queueing or cache changes, and no 10× load test (declined in §3's stretch block), so the repo's own pacing (`REQUESTS_PER_MINUTE = 30`, `config.py:95`) stays a guard rail rather than a dial anyone tunes. The concurrency caveat that *would* matter if this were stressed is named under 2.3 and in *What's Still Broken*.
4. **The CLI surface and the local harnesses.** `app.py` subcommands and the interactive loop behave as before; only the shared `ask_pipeline` gains fields. `run_eval.py` is **not** hardened this unit — W9 is named and left, because touching it would change how unit 1/2's numbers are produced while those numbers are still being cited as the baseline. `questions.py` also stays exactly as shipped: its `QUESTIONS` and `OUT_OF_SCOPE` are units 1–2's test set and the baseline's inputs, so nothing this unit measures is added to them (the cost probes at 3.8 are kept out of this file on purpose).
5. **The frontend, declared out of scope.** No browser page, no `GET /`, no `static/`, no production server — a declaration about a surface this repo never had, so nothing is deleted. The service serves JSON over `POST /ask` and `GET /health`, exercised with `curl`, plus the `app.py` CLI (`unit9.txt:143`: "I'm not rebuilding the interface"). `run.sh` starts Flask's development server, the right weight for a single-user local run.

### Stretch — **one declared: a latency breakdown (+1)** *(said in the README at Milestone 1)*

`unit9.txt:115`–`:118` offers four optional items, each all-or-nothing and each worth points only if declared in the README before it was built (`unit9_rubric.txt:58`). **Declared: the latency breakdown.** `stage_ms` is built anyway for diagnosis; the stretch is the measured table — mean and median per stage (retrieve incl. rerank, gate, generate) over the 3.8 cost runs, pasted under *Instrumentation*, plus one sentence naming the dominant stage. If `stage_ms` is ever cut (§3), withdraw this declaration in the same commit. The other three are declined, and *The Shape* says so:

| Declined stretch | Why |
|---|---|
| A second measured improvement (`:115`) | The brief's Milestone 6 loop is one diagnosis → one fix → re-run; a second fix makes the before/after ambiguous about which change moved which number (`unit9.txt:42`). |
| A load observation at 10× (`:117`) | It would measure Flask's dev server and a module-level `LAST_RETRIEVAL` flag (2.3) that is honest only single-user — not evidence about this system as scoped. |
| Both run paths (`:118`) | Means hosted deployment, ruled out by the two-local-models arithmetic (`unit9.txt:54`). |


### Pruned at review, and the ordered cut list

**Pruned now — decided up front, so none of these is an emergency cut later:** faults F7–F10 (harness is F1–F6); the `RERANK_STRICT` and `EMPTY_RESPONSE_RETRIES` knobs; the pacing-sleep cap; the dedicated `quota` and `model_empty_response` kinds (both folded into `upstream` with a `reason`); `metrics.py --tail` and `--kind`; the `answer_head`, `cache_hit` and `top_score` log fields.

Referenced by ground rules 8 and 9, 1.5, 2.8 and Appendix E. **Nothing in the A half is ever on the list**: `run.sh`, `RUNNING.md` with its `curl` examples, the structured log, the ≥10 pasted records and the measured cost number are mandated in every shape (`unit9.txt:40`, `:89`–`:95`). If M2 isn't demonstrable inside the brief's ~90-minute ceiling, cut from the top, one at a time, and write each cut into *What's Still Broken* in the commit that makes it:

1. **The `/health` additions** (`reranker`, `log_path`). *Lost:* the pre-flight peek. *Kept:* the log, which is the real evidence.
2. **The `stage_ms` split** — keep `duration_ms`. *Lost:* per-stage diagnosis and the declared latency-breakdown stretch (withdraw that declaration in the same commit).

**Stop there.** Never cut: the four-type taxonomy and `classify()`, the timeout, the empty-response failure, the reranker degrade, the log writer and `--summary`, faults F1–F6, the `curl` examples, or anything in the A half. If it still doesn't fit, the shape claim is wrong — say so in *What's Still Broken* and shorten the extension's sentence, not the operational layer.

### Size check — what this build actually contains *(no time tracking anywhere in this plan; see ground rule 9)*

The brief pictures Milestone 2 as the shortest build block in the course, holding *"one capability, one hardening layer, or the operational scaffolding — whatever your shape named"* (`unit9.txt:174`). This unit is unusual: it needs **two of those three**. The hardening layer, because that's the chosen shape; the operational scaffolding, because `unit9.txt:40` requires it in every shape. That is the honest reason the build is larger than the brief pictures — and it is a reason to refuse to grow it further, not a licence. So the trade-offs are decided now, by **what evidence would go missing**, never by minutes. The brief's own ceiling still applies as a stopping rule (`unit9.txt:146`): if Milestone 2 isn't demonstrable after about ninety minutes of building, apply the cut list rather than pushing on.

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


Step 2.9 sits outside this table on purpose: drafting the criteria is Milestone 4's work pulled forward into Milestone 2, not extra build work.

---

## Milestone 0 — Preflight: make the system run again *(prep — not one of the unit's seven)*

There is no `.venv` in this directory and `python3` on the shell default is **3.9.6**, which this codebase cannot even parse (`config.py:110` uses `str | None`). Supported range is 3.11–3.13, explicitly **not 3.14** (`requirements.txt:4-5`). `/opt/homebrew/bin/python3.12` and `python3.13` both exist.

- [ ] 0.1 `cd` into the repo; create the env with a supported interpreter:
      `/opt/homebrew/bin/python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
      Then **decide the reranker mode for this working venv, now, before the first query** (the decision 3.4 makes for the repo; this one is for your measurements). `requirements.txt` deliberately omits `sentence-transformers` (`:12-24`: PyTorch, ~2 GB), so a venv built from it alone answers **nothing** today (W6). Recommended: install it here — `pip install 'sentence-transformers>=3.4,<3.5'` — so Milestone 2's regression pass and every Milestone 5 number are comparable to unit 2's reranked numbers. Record the choice and the installed version in the run log, and label every number you later publish with the mode that produced it (3.4's rule applies to the 2.8 baseline too). The clean-clone test at 3.6 deliberately uses a venv from `requirements.txt` **without** it, to exercise the degrade path — that is the one place the difference is the point.
- [ ] 0.2 `cp .env.example .env`, paste the key, `python test.py`.
- [ ] 0.3 `python app.py --corpus city_guides index` (note the wall-clock — you need it for RUNNING.md) and one `python app.py --corpus city_guides ask "How expensive is it to stay at Thornby Wells?"`. **Why the flag:** `config.CORPUS` defaults to `campus_life` (`config.py:23`) while `questions.py`'s five test questions are `city_guides` questions — every command must pin the corpus or the system silently answers from the wrong one.
- [ ] 0.4 **Confirm W6.** In a *second* throwaway venv installed from `requirements.txt` alone, run `python app.py retrieve "tram schedule"`. Record verbatim what comes back. This is the single most important finding for `RUNNING.md` and it is the honest justification for the degrade path you build in 2.3.
- [ ] 0.5 Record the local artefacts a stranger needs: embedding model download (~80 MB from Chroma's CDN), the cross-encoder weights, `sentence-transformers`+PyTorch install size, `chroma_db/` rebuild time. These go in `RUNNING.md` in Milestone 3.

**Commit checkpoint (M0):** nothing to commit unless you changed a file. If 0.1–0.3 required a fix, commit it as `unit 9 preflight: environment fixes`. **Before Milestone 1, commit the pending pre-M0 changes** (gunicorn removal across `RUNNING.md`, `requirements.txt`, `serve.py`, plus `PLAN.md`) as their own commit, and decide on `unit9_rubric.txt` on purpose (see Submission).

---

## Milestone 1 — Shape, scope, and the size cut

Deliverable: a `# Unit 9` heading appended to `README.md` with three filled sections. Write-only milestone — no code.

- [ ] 1.1 Append a `# Unit 9` block at the end of `README.md`. The file is **770 lines whose last line is unterminated** — `wc -l` reports 769 because it counts newlines, and the final words are `5/5 gate refusals for this small question set.` with **no trailing newline** (`od -c` on the last bytes shows `.` as the final byte). Add a newline first or your heading glues onto unit 2's last words. Unit 1 (`:8`) and unit 2 (`:309`) headings stay untouched. Scaffold all **nine** of the brief's section names now — *What This Extends · The Shape · Running It · Instrumentation · What It Costs · Run Log and Verdicts · The Improvement · What's Still Broken · How I Used AI* — fill the first three in 1.2–1.4, and leave the other six as `_(filled in Milestone 3/5/6/7)_`. The scaffold guarantees the section names match the brief exactly no matter how late in the unit the filling-in happens.
- [ ] 1.2 **What This Extends** — name the system, the corpus, and the one sentence of what's new (Section 1 of this plan, in your own words). Say plainly that answer quality is unchanged on purpose.
- [ ] 1.3 **The Shape** — "B — Harden against failure", the two paragraphs from Section 1 of this plan (the hardening layer, then the sentence saying shape A is carried alongside because the run path and the log are required in every shape), plus the five out-of-scope items from Section 3 written as sentences ("I am not changing the chunker or the cutoff…"), **item 1 in its amended wording** — the version that declares the Milestone 6 `TOP_K` exception up front, so the fix table at 6.3 and the scope statement agree from day one — the fifth being the interface, **declared** out of scope in the brief's own words ("I'm not rebuilding the interface", `unit9.txt:143`): the service serves text over the two routes it has shipped since unit 2, exercised with `curl`, and no page is being built or unbuilt. Declare the stretch: **one — a latency breakdown** (the measured per-stage table from 3.8, pasted under *Instrumentation*) — and state that the other three (second improvement, load observation, both run paths) are declined, with §3's reasons. A stretch earns points only if declared before it is built. Say explicitly that out-of-scope item 2 is *hosted* deployment only — the system is deployed, on Path B.
- [ ] 1.4 **Running It** — "Path B — local with logs, one documented start command, committed run record, text only", one sentence on why (two local models won't fit a 512 MB free tier, which is what `unit9.txt:54` tells you to do in that case), pointer to `RUNNING.md`, one line saying the service answers `POST /ask` as JSON text, exercised with the `curl` examples the doc carries — and one line saying the interface is out of scope by declaration, not by omission. Name it as the A half of the build, not as setup. Fill the rest in Milestone 3.
- [ ] 1.5 Re-read §3's size check and its ordered cut list. If a piece has outgrown what §3 gives it, cut in that order and write the cut into *What's Still Broken* later — cutting an **A half** item is not an available option, so cut from the B half. There is no page on the list to cut: the interface was never part of the build, which is why out-of-scope item 5 is a declaration made at Milestone 1 and stated in the README rather than a trim improvised under pressure.
- [ ] 1.6 Scope standup check on yourself: say the extension out loud in one sentence. If the word "and" appears twice, it's three projects. The sentence in Section 1 is the target shape. **The A half does not count against this rule** — say it as a second sentence, attributed to the brief rather than to your ambition: *"the extension is one thing — every request leaves the pipeline with a classified outcome and a log record; the run path and the log ride along because the brief requires them in every shape."* That is the answer when someone asks "is that one thing or three?" — one extension, one mandated layer, plus the harness that proves the first one works.
- [ ] 1.7 **Stretch, declared now: the latency breakdown only.** One sentence under *The Shape*, in the past tense the rubric can check — *"one stretch feature is added this unit: a latency breakdown, the measured per-stage `stage_ms` table; the other three optional items are declined for the reasons in §3."* `unit9_rubric.txt:58` awards stretch points only for items declared before they were built. Nothing else may quietly grow into a stretch item.

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
One module, four types, one mapper. Nothing else in the repo decides a status code.

```python
class PipelineError(Exception):        # kind, http_status, stage, user_message
class BadInputError(PipelineError):    # kind="bad_input",              400
class NoIndexError(PipelineError):     # kind="no_index",               503   # subclass RuntimeError too, so existing callers keep working
class ModelTimeoutError(PipelineError):# kind="model_timeout",          504
class UpstreamError(PipelineError):    # kind="upstream",               502
def classify(exc) -> PipelineError     # known types pass through; everything else → kind="internal", 500
```
Rate-limit exhaustion and an empty model response are folded into `upstream` (502) with a `reason`, rather than getting their own kinds: a dedicated 429 and a dedicated empty-response kind were each one more thing to build, test and document, and `reason` keeps the distinction in the log. `generate.py:108-121` raises `QuotaGuard` mid-request today and it lands in W3's generic 500 — wrapping it fixes that.
Two rules that matter: the caller gets `user_message` **plus the `request_id`**, never the exception text (that goes to the log); and a gate refusal is **not** an error — empty results from a real index stay a `200` with `"refused": true`. Empty *index* is `no_index`; empty *results* is a refusal. Get that line wrong and you'll "fix" the thing that already worked.

⚠️ **`UpstreamError` needs a producer, or the taxonomy is a lie.** `classify()` passes known types through and maps everything else to `internal`/500 — and today nothing in the repo ever raises `UpstreamError`. An invalid key, a provider 5xx or an exhausted retry loop (`generate.py:270`'s terminal `RuntimeError`) would therefore still arrive as a 500, and Appendix B's F3 would fail their own expectations while looking like the taxonomy works. 2.2 closes this: the provider/SDK exceptions raised around `:241` and the retry-exhaustion path get **wrapped** in `UpstreamError` (with `reason="rate_limited"` or `"quota"`), with the provider's own text copied onto the exception for the log and **never** into the response body — which is W3's leak, closed at the same time.

### 2.2 `generate.py` — bound the call, refuse to lie *(edit inside `generate()`, lines 202–271 only)*
- **Timeout.** Wrap `client.models.generate_content(**kwargs)` (`:241`) in a wall-clock bound of `config.GENERATION_TIMEOUT_S`. Two ways; pick one and write the other down as the alternative you rejected:
  - *(a) dependency-free, recommended:* `concurrent.futures.ThreadPoolExecutor` + `future.result(timeout=…)`, raising `ModelTimeoutError` on `TimeoutError`. ⚠️ **Do not use `with ThreadPoolExecutor() as ex:`** — its exit calls `shutdown(wait=True)` and blocks on the hung call, silently defeating the timeout. Create the executor without `with` and call `ex.shutdown(wait=False)` after `TimeoutError` (or use a daemon `threading.Thread`). F5 must prove it at the end of M2: a 120 s stub answers 504 in ≈ `GENERATION_TIMEOUT_S`. Covers a hang *inside* the SDK, which a transport timeout does not.
  - *(b) transport-level:* `google.genai` `HttpOptions(timeout=…)` at `_get_client()` (`:186-200`). Verify the exact kwarg for the pinned `google-genai>=1.0,<2.0`; note it won't bound work the SDK does after the socket closes.
  - ⚠️ A thread you abandon keeps running. Say so in a comment and in the README — bounded *response*, not cancelled *work*, is an honest limit and a real one to name in *What's Still Broken*.
- **Wrap what the provider throws** (2.1's `UpstreamError` producer). The retry loop's `except` at `:249` sorts failures two ways and both need wrapping: a non-rate-limit error is re-raised **bare** at `:259-260` (invalid key, a 400, a provider 5xx — a raw 500 today) → `UpstreamError(reason="api_error")`; the terminal `RuntimeError` at `:270` ("still rate limited after `MAX_RETRIES` attempts") and `QuotaGuard` → `UpstreamError(reason="rate_limited"|"quota")`, still 502 (a dedicated 429 kind was pruned at review: one more kind to build, test and document). Put `type(exc).__name__` and the provider's message on the exception **for the log only**; `user_message` stays bland. Without this bullet the 502 `upstream` row for F3 is a promise nothing keeps.
- **Pacing is outside the bound — say so, don't build around it.** `_wait_for_slot()` runs before the call, so a slept request can exceed `GENERATION_TIMEOUT_S` with no timeout firing (W7). Record `pacing_ms` (a `perf_counter` pair around `_wait_for_slot`, three lines) so a slow request is diagnosable as pacing rather than model, and document the worst case: **wall-clock ≤ `GENERATION_TIMEOUT_S` × attempts + backoff + pacing**. Capping the sleep with a dedicated error was pruned at review; measurement stays under the limiter instead (3.8, 5.2) and the uncapped sleep goes in *What's Still Broken*.
- **Empty is a failure.** At `:243`, if the stripped text is empty: make **one** second attempt (hard-coded), then raise `UpstreamError(reason="empty_response")`. Returning `""` is what lets W2 pass unit 1's criterion 2.
- **Retries stay as they are** (`:246-268`) — only rate-limit-shaped messages retry today; don't broaden that today, or you change latency for a reason unrelated to your criteria.
- **Expose per-call stats** for the log: attempts made, whether it timed out, `pacing_ms`, and the tokens already captured by `_record_tokens` (`:125`).

### 2.3 `store.py` — one error type, one degrade
- `:284` **and `:347`** — both raise sites carry the same bare `RuntimeError("No index called … Run \`python app.py index\` first.")`; swap both for `NoIndexError` (the message keeps the "run `python app.py index`" instruction — that sentence is the fix's user-facing half). Grep `RuntimeError` in `store.py` before you finish: `:87` and `:142` are the embedder/reranker ones and belong to the degrade work below, not here.
- `_rerank()` (`:154-169`) — if `_cross_encoder()` can't load (ImportError **or** weights unavailable), **return the fused RRF order unchanged** and flag it. Retrieval then still works, which is exactly what W6 makes impossible today, and answers the question a grader will ask about a repo whose pinned file doesn't contain a dependency its happy path needs.
- Flag plumbing, simplest option: a module-level `LAST_RETRIEVAL = {"rerank": "ok"|"degraded", "candidates": n, "results": n}` set by `search()` and read by `ask_pipeline`. Cheaper than threading a callback through three call sites. **Write down the caveat** — a module global is per-process but not safe across threads, and Flask's development server threads by default; the documented run is a single-user local session, so say that in the README rather than hide it. No load test is run this unit (§3's stretch block declines it), so the caveat is documented rather than exercised — which is exactly why it has to be in writing.

**Commit checkpoint (M2a) — by hand:**

```bash
git add errors.py generate.py store.py config.py
git commit -m "unit 9 milestone 2a: error taxonomy, generation timeout, empty-response failure, reranker degrade"
```

### 2.4 `config.py` + `metrics.py` — knobs and the log *(the A half's first lines of code)*
`config.py`, new block near `:91-100`, each overridable by env **using the file's own convention** — the existing knobs read `os.getenv("AI201_…")` (`CORPUS` at `:23`, `MODEL` at `:88`, `CACHE_ENABLED` at `:99`), so every name below keeps that prefix:
`GENERATION_TIMEOUT_S = 30` (`AI201_GENERATION_TIMEOUT_S`), `MAX_QUESTION_CHARS = 1000` (`AI201_MAX_QUESTION_CHARS`), `LOG_DIR = Path(os.getenv("AI201_LOG_DIR", ROOT / "logs"))`, `LOG_FILE = LOG_DIR / "runs.jsonl"`. The empty-response retry count (1) is hard-coded, and there is no `RERANK_STRICT`: both were pruned at review.
`AI201_LOG_DIR` earns its place twice: it keeps each measurement phase's log separate (5.2 — one directory per trial), and it lets the logger's never-raises claim be checked once by hand at 2.8 (`AI201_LOG_DIR=/root/nowhere` → request still 200, one stderr line). Write it into `RUNNING.md`'s environment section at 3.3 alongside `AI201_CORPUS`, `AI201_CACHE` and `AI201_MODEL`.
(The reranker degrade is always on: if the cross-encoder can't load, retrieval returns the fused order flagged `degraded`. The old hard-failure contract is gone — say so in the README.)

`metrics.py`, new file, ~90 lines, two jobs:
- **Write:** `record(**fields)` appends one JSON object per line to `logs/runs.jsonl`, creating the dir, never raising (a broken logger must not break a request — mirror the attitude of `generate.py:145-146`, whose comment reads *"accounting never breaks the thing it is accounting for"*). Schema in **Appendix A**; the four fields the brief mandates are `ts`, input, output and duration, and every record also carries `outcome` and `error_kind` so failures are legible.
- **Read:** `python metrics.py --summary` — counts by outcome and error kind, mean/median/max `duration_ms`, the `stage_ms` split, degraded share. This is what makes "observability" true rather than claimed: a question about the running system is answerable without adding code (`unit9.txt:25`), and it is the only reason Milestone 5 can be done from the log. `--tail` and `--kind` were pruned at review — use `tail -n 10 logs/runs.jsonl` — so `--summary` is the one reader. `jq` isn't installed by default on macOS. `--summary` groups by outcome and error kind and splits by stage: *"which stage do the failures actually come from?"* is the first question worth asking.
- `logs/` must be committed as evidence. `.gitignore` currently does not ignore it — verify with `git status` after the first write, and do **not** add it to `.gitignore`.

### 2.5 `app.py::ask_pipeline` — timings, additive fields *(`:198-270`)*
Wrap each stage in `time.perf_counter()` deltas and add to the returned dict: `request_id` (`uuid4().hex[:8]`), `error_kind` (`None` on the happy path), `degraded` (`{"rerank": "ok"|"degraded"}`), `duration_ms`, `stage_ms` (`retrieve`/`gate`/`generate`), `n_results`, `n_candidates`, `answer_chars`, `attempts`, `pacing_ms` (what 2.2 measures — the seconds the limiter made us wait). It still prints nothing — `_ask_one` (`:273`) and `run_eval.py::run_once` (`:54`) keep working untouched because you only added keys.

### 2.6 `serve.py` — the shell becomes a service *(`:65-104`)*
- Mint `request_id` at the top of `/ask`; echo it in every response body and in `X-Request-Id`.
- Move parsing/validation **inside** the protected region (fixes W5): non-string, missing, blank or > `MAX_QUESTION_CHARS` question → `400` carrying `error_kind: "bad_input"`, the `request_id` and a human `message`. **Keep the existing `error` key as the human-readable field** — `{"error": message, "error_kind": "bad_input", "request_id": "…"}` — rather than renaming it to `message`: today's 400 body is `{"error": …}` (`serve.py:79-87`), Milestone 2's own rule is that new keys are additive and existing callers keep working, and a rename is a silent contract break on the one response a client is most likely to parse. `message` may be added as an alias; `error` must not disappear. Confirm the exact today-behaviour in 2.0 first; W5 is a claim until you see the 500.
- `except PipelineError` → `classify()` → its status; `except Exception` → `500` with `kind: "internal"`, the `request_id`, **and no exception text** (W3's raw leak).
- Write the log record in a `finally` so 400s, 500s and timeouts are all recorded — the brief's "a failure that shows up only as an absence is one you'll never find".
- `/health` (`:38-62`) gains `reranker: "ok"|"degraded"` and `log_path`; keep it cheap — no embedder load, per the note at `store.py:358-361`.
- Record **who is serving** in every log record — `server` (`"flask-dev"` when the record comes from `serve.py`, `"cli"` from `app.py`), `pid`, `port`. It costs three lines and it is what turns the committed log into Path B's proof that the system ran as the documented server process (`unit9.txt:410`, `:49`–`:52`) rather than a bare function call inside an editor. See Appendix A.
- **Move the default port off 5000.** macOS's AirPlay Receiver listens there, so `python serve.py` fails to bind or the first `curl` reaches the wrong process. Change the default at `serve.py:114` (and the docstring at `:5`) to **5001**; `run.sh` exports `PORT` explicitly.
- **Update this file's own docstring, which three of these changes make false.** Its command block used to advertise `gunicorn serve:app` as the way a host runs it; that line is already gone, pulled with the pin before Milestone 0, so the docstring runs `:2-27` and offers exactly one command. What still needs fixing here is `:22-26`, which currently reads *"There is deliberately no logging, no timing and no metrics in this file… Add yours in unit 9"* — after this milestone that is simply untrue, so replace it with two lines naming `metrics.py::record`, the `finally` that calls it, and `logs/runs.jsonl`. A docstring that contradicts the code two lines below it is exactly the drift the gunicorn removal was for, and it arrives from inside the same commit if you leave it.
- **Add no route.** The interface is out of scope by declaration (out-of-scope item 5): no `GET /`, no `static/`, no template, no production server behind it. `POST /ask` and `GET /health` stay the only routes — exactly what unit 2 shipped, so confirm this file's diff adds no `@app.route`. `app.run` (`:131`) stays the only server; the documented start command (`run.sh`, Milestone 3) execs `python serve.py`, and the README says plainly that what runs is Flask's development server and that a production server is declared out of scope — the right weight for a single-user local run, and enough for the brief's question, *"does it run somewhere that isn't your editor, with a record of it running?"* (`unit9.txt:410`).

### 2.7 `tools/faults.py` — the harness you test with in Milestone 5 *(new file)*
Model it on `tools/smoke_test.py`, which already proves the pattern of faking an embedder and a key. Each fault is injected **at runtime, never with a switch inside production code** — an `AI201_FAULT=…` branch in `generate.py` would mean the code you graded isn't the code you tested.

Mechanics per fault are in **Appendix B**. Only external dependency note: `requests`/`httpx` are **not** in `requirements.txt`, so drive HTTP with stdlib `urllib.request` or a `curl` loop rather than adding a dependency (adding one costs a README sentence for no gain).

Print, for each fault: the name, how it was injected, the status/body that came back, and whether a log record appeared. That output pastes straight into the README and the run log.

### 2.8 Regression gate — before committing
- [ ] `python test.py`
- [ ] `python tools/smoke_test.py` (the repo's own end-to-end check; it needs no key)
- [ ] `python app.py --corpus city_guides ask "How expensive is it to stay at Thornby Wells?"` — unchanged answer shape
- [ ] `python run_eval.py --corpus city_guides --label unit9-regression` — the five questions still 3/3 pass, gate still refuses 5/5. **Record the reranker mode this ran in** (0.1's decision): unit 2's committed 3/3 and 5/5 were produced *with* the cross-encoder, so a degraded-mode run here is a different measurement, and a difference in degraded mode is a finding about the degrade path, not a regression. This is a regression check on the pipeline, not a criterion: `run_eval.py` itself is untouched and unhardened (W9, out-of-scope item 4).
- [ ] `curl -s localhost:5001/health` then one happy `POST /ask`, then `tail -n 3 logs/runs.jsonl` — the record for that call reads `server: "flask-dev"` with a `pid` and a port

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

- [ ] 3.1 **One start command.** Add `run.sh` (executable, and `git add --chmod=+x run.sh` so the mode bit lands in the commit) that does exactly what `RUNNING.md` says: activate `.venv`, exit with a readable message if `GEMINI_API_KEY` is missing, **export `AI201_CORPUS="${AI201_CORPUS:-city_guides}"`** — `serve.py` reads `config.CORPUS` with no flag (`serve.py:90`), whose default is `campus_life`, and `questions.py`'s criteria are `city_guides` questions; the pin keeps the service answering from the corpus units 1–2 tuned — build the index if `store.index_exists("city_guides")` is false (the corpus argument matters; the default is the wrong corpus) — **printing a heads-up before you do it**, `no index for city_guides — building it now (first run only: downloads the ~80 MB embedder, then takes the wall-clock you measured in 0.3)`, and one confirming line when it finishes, because 3.6's clean-clone test otherwise reads as a hang to whoever is following the doc, and that sentence belongs in `RUNNING.md` as well — then `exec python serve.py`. One command, no hidden steps — that is the whole Path B requirement. The server is Flask's development server (`serve.py:131`'s `app.run`), and that choice is already consistent across the repo: the `gunicorn` pin and both places advertising it came out together before Milestone 0, so 3.1 has no dependency edit to make — only to keep `grep -rn gunicorn requirements.txt serve.py RUNNING.md` printing nothing, and to leave `RUNNING.md:208-213`'s "one way to start it, on purpose" paragraph standing. Say in the README that the interface and production serving are out of scope, text only.
- [ ] 3.2 **Rewrite `RUNNING.md:195-228`** ("Running it somewhere else — unit 9", currently a future-tense promise that `serve.py` has no logging). New content: Path B declared; the single command (`./run.sh`), including the first-run index-build sentence from 3.1 so a several-minute pause reads as progress and not as a hang; **a worked `curl` for `/health` and for `/ask`** — the two examples `RUNNING.md:201-220` has never contained; what `/health` and `/ask` return, **including the error body's actual shape** (`{"error", "error_kind", "request_id"}`, and `X-Request-Id`) so a reader can tell a `400` from a `503` from a `504` without opening `serve.py`; **the corpus pin** (`AI201_CORPUS=city_guides`, and why: the config default is `campus_life` while the test questions and unit 1–2 tuning are `city_guides`); where the log lives and how to read it (`tail -n 10 logs/runs.jsonl`), with `AI201_LOG_DIR` listed among the env vars; the fault harness; one line saying the interface is out of scope by declaration — the service is JSON text only, no page, no browser surface; Then the environment section below. The gunicorn half is already settled (pre-M0): `:204-213` names one command and explains why there is no second — keep that reasoning standing, and don't reintroduce a production-server path nothing installs.
- [ ] 3.3 **Environment section** in `RUNNING.md`: Python 3.12 (supported 3.11–3.13, **not 3.14**), `pip install -r requirements.txt`, **plus the `sentence-transformers>=3.4,<3.5` line the reranker needs** and its size, the two model downloads with sizes and origins (`chroma-onnx-models.s3.amazonaws.com` ~80 MB; Hugging Face `cross-encoder/ms-marco-MiniLM-L-6-v2`), the `chroma_db/` rebuild time measured in 0.3, and the `.env` key. Document `PORT` too (default 5001, because macOS AirPlay Receiver holds 5000).
- [ ] 3.4 **Decide W6 on the record.** `sentence-transformers` is a hard requirement of today's retrieval path but is deliberately **not** in `requirements.txt` — `requirements.txt:12-24` explains why (it drags in ~2 GB of PyTorch, and Chroma's bundled ONNX embedder avoids that), and `RUNNING.md:240-246` mentions it only under *Stretch features*. Two honest endings; **the recommended one is the second**:
  - *Pin it:* add `sentence-transformers>=3.4,<3.5`. Pro: the pinned file describes what the happy path needs. Con: it reverses a documented decision that the starter made on purpose, and it makes every clean install download ~2 GB for a reranker that only reorders 25 candidates down to 7 (`config.py:47`, `:36`).
  - *Recommended — make it genuinely optional:* leave `requirements.txt` alone, ship the degrade path from 2.3 (unreranked RRF order, `degraded.rerank = "degraded"`), and give the model a documented, named line in `RUNNING.md`'s environment section. Then the repo's stated position ("you don't need it") becomes **true**, which is the thing a clean clone currently disproves — and a clean-clone failure becomes a documented, measurable degrade instead of an outage.
  - Whichever you pick, say which in the README under *Running It* and repeat it in `RUNNING.md`'s environment section, and **label every number in the submission with the reranker mode that produced it** — the unit 2 baseline, the 2.8 regression pass and every Milestone 5 figure come from the 0.1 venv (recommended: reranked), while 3.6's clean clone deliberately runs degraded, and a table that mixes the two silently compares two different systems.
- [ ] 3.5 **Prove reachability with text, and nothing else.** The frontend is out of scope (out-of-scope item 5), so this step's job is to prove the text surface works from the doc alone: from a clean terminal, `./run.sh`, then the `curl` commands from `RUNNING.md` verbatim — `/health`, then one real `POST /ask`, then one classified failure (`python tools/faults.py --fault f4_empty_response`) with `error_kind` and `request_id` visible in the JSON body. Paste what came back as text. Confirm the negative space too: `GET /` answers 404 (Flask's default — fine; the interface is out of scope, declared, not forgotten), and `git status` shows no `static/` directory, because a declared absence is a decision and an undeclared one reads as a gap. Hard rules, each one cheap and each load-bearing:
  - **No new route, no new file for the surface.** If a step here starts wanting an `index.html`, that is the signal to stop, not to continue (ground rule 10).
  - **A failure has to look like a failure in the text.** A classified failure is visible in the JSON body and in the log — run **F4** and **F6** and paste both bodies; that is the evidence the page would have rendered, delivered as text instead, sitting next to the log line written for the same request.
  - Smoke it end to end: `./run.sh`, then the doc's `curl` examples, one real question, then `tail -n 1 logs/runs.jsonl` → **exactly one** new record, reading `server: "flask-dev"`.
- [ ] 3.6 **Clean-clone test.** Clone the repo into a fresh folder **outside** the project dir, follow your own `RUNNING.md` top to bottom, paste the real failures. It will fail at least once — likely the reranker, likely a missing `chmod +x run.sh`, likely the venv. Whatever bit you is what a reader hits; fix the *document*, not only your machine. **Finish the test with the documented `curl`, not with a command you memorised:** the last line of the clean clone is copying the `POST /ask` example straight out of `RUNNING.md` and getting a grounded answer, because that is the moment the run path is proven for someone who isn't you (`unit9.txt:56`, `:410`).
- [ ] 3.7 **Produce the log evidence.** Restart via `run.sh`, generate **≥ 12 records** in one session — the 5 real `QUESTIONS`, 2 `OUT_OF_SCOPE` refusals, ≥ 3 failures from `tools/faults.py`, and two more runs (a repeat question, or one of `RUNNING.md`'s ten cost probes) so the count clears 12 with room to drop a contaminated one — driven with the same `curl` commands `RUNNING.md` documents, so "someone else can run this" has lines in the file behind it, not only a sentence in the README. Paste **≥ 10 records verbatim** into README → *Instrumentation*, with at least 3 failures and at least one degrade. Add a sentence on what each record holds and which file/function wrote it (`metrics.py::record`, called from `serve.py::ask`). **Check the provenance field before you paste:** every record from this session must carry `server: "flask-dev"` (plus `pid`/`port`) — those are the fields that make the committed log evidence of a run as the documented server process instead of an editor session, which is the exact thing Path B is graded on. One count that has to be right before you paste: the session's new lines in `logs/runs.jsonl` equal the number of `/ask` calls you made — there is no `GET /` to muddy the count, which is one thing the text-only scope buys.
- [ ] 3.8 **Measure the cost of one run** — measured, not from a pricing page:
  - `AI201_CACHE=0` for the whole measurement, or the cache (`generate.py:60-73`) reports 0 tokens and you silently report fiction. Note in the README that you turned it off, and that a warm rerun legitimately costs nothing — that difference is worth naming.
  - Run **10** distinct real questions over HTTP against a warm server, cache off, with the same `curl` command `RUNNING.md` documents — the measurement then describes the documented run path, not whichever client was handiest. Tokens come from the service, already captured by `_record_tokens` (`generate.py:125-150`), readable per request from the log (`tokens_in`/`tokens_out`) or `generate.token_counts()` (`:169`).
  - **Where the ten come from.** `questions.py` has only **five** questions that reach the model (`QUESTIONS`); its other five (`OUT_OF_SCOPE`) are gate refusals, which never call the model and would report zero tokens and quietly halve your mean. Write **five new `city_guides` questions** and keep them as a documented list in `RUNNING.md`'s cost section — ten `curl` commands a stranger can paste — **not** in `questions.py`, which is units 1–2's frozen test set (out-of-scope item 4) and the baseline's input. Say in the README that these are measurement inputs, not criteria. Before spending any API budget, screen them for free: `python app.py --corpus city_guides retrieve "<question>"` for each (no model call, no cost) and confirm the gate passes it; a probe that gets refused is not a cost sample, so replace it rather than average it in.
  - **Keep the rate limiter out of the numbers.** `_wait_for_slot()` allows `REQUESTS_PER_MINUTE = 30` (`config.py:95`) and `time.sleep()`s past that **inside the request**, so a tripped limiter inflates `duration_ms` with a wait that has nothing to do with the pipeline — and it counts every model call in the process, including empty-response retries and any fault runs sharing that server. So: hold model-touching runs to roughly 20 per rolling minute against one server process, watch stderr for the two notices this produces — `generate.py:99-104`'s `[rate limit] 30 requests used this minute. Waiting Ns` (the pacing sleep) and `generate.py:262-267`'s `[rate limit] service pushed back. Retrying in Ns` (a provider rejection) — and read `pacing_ms` on every run you keep: a nonzero one means the number is contaminated and must be labelled or dropped. Restart the server between measurement blocks: `_call_times` (`:39`) and `_session_calls` (`:40`) are module-level, so a restart clears both the pacing window and the `SESSION_REQUEST_BUDGET = 300` counter — worth watching, since M3.7's evidence session, M5's three trials per criterion and M6.5's full re-run all draw on the same 300, and a trial that ends in `quota` is a trial you didn't mean to run.
  - Report mean **and max** tokens/run (prompt and output separately), mean/median/max wall-clock, and the per-stage `stage_ms` mean/median — this table is the declared latency-breakdown stretch: paste it under *Instrumentation* with one sentence on which stage dominates. Expect the prompt to dominate: `TOP_K = 7` (`config.py:36`) chunks plus the grounding instruction is most of the input, and `RERANK_CANDIDATES = 25` (`config.py:47`) means 25 cross-encoder pairs scored per request even though only 7 survive.
  - Seconds of local compute are cost too: report rerank and embed time separately from API wait — a reranker loading on the first request is a local cost with no API line item.
  - Any `$` figure is **arithmetic on measured tokens × a published rate**, labelled as such. The measured number is the token count.
- [ ] 3.9 Paste the cost number and its method into README → *What It Costs*. The 100-people-a-day arithmetic waits for Milestone 7.

**Commit checkpoints (M3a, M3b) — by hand, two of them:**

```bash
git add RUNNING.md run.sh      # requirements.txt joins this commit only if 3.4 decides to pin the reranker
git commit -m "unit 9 milestone 3a: Path B run path — run.sh, curl examples, clean-clone fixes"

git add logs/runs.jsonl README.md
git commit -m "unit 9 milestone 3b: committed run log, instrumentation extract, measured cost per run"
```

`git status` after the first one shows `requirements.txt` only if 3.4 pinned the reranker; the gunicorn drift check is already discharged, the pin having left in its own pre-Milestone-0 commit — `git log --oneline -- requirements.txt` shows it arrive (unit 2's history) and leave (that commit), which is what makes it read as a decision rather than an accident. What every later checkpoint does owe: `grep -rn gunicorn requirements.txt serve.py RUNNING.md` prints nothing, because a mention creeping back would advertise a command nothing installs. `logs/` still gets the same check: nothing in `.gitignore` names it today (verified: it lists only `.env`, Python artifacts, venvs, `chroma_db/`, `.cache/`, OS noise), but this is the class of mistake that silently eats evidence.

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
| Hung upstream → bounded response time | F5: client-side wall-clock vs `GENERATION_TIMEOUT_S` — **and name what was bounded**: the bound wraps the model call, so an honest target reads "the call is abandoned within `GENERATION_TIMEOUT_S`" or states the request-level worst case (`× attempts + backoff`) and measures that. Say whether the run was paced (`pacing_ms`) too |
| Reranker absent → still answers, and says so | F6: `degraded.rerank`, plus gate/refusal behaviour in that mode |
| Every `/ask` request incl. failures leaves exactly one record | record count vs request count in `logs/runs.jsonl` |
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

**At least one of the five must be able to miss for a reason you don't control.** The bad-path criteria (400s, 503, no empty 200) are deterministic and will probably pass 3/3, and Milestone 6 needs a diagnosis to aim its one improvement at. So include one criterion with real variance: warm `/ask` latency (`duration_ms` over ≥ 10 warm, cache-off runs with `pacing_ms == 0`), or degraded-reranker behaviour (F6: does the answer still pass the gate and cite sources? `THRESHOLD` was set against cross-encoder scores and the fused RRF order is on a different scale, so read `gate.py` at M2 before choosing the target). Write the target before measuring; don't pick one you already know you'll pass.

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

**Commit checkpoint (M4) — by hand:** the criteria were committed at 2.9, so if the self-check and pair review change nothing there is **nothing to commit** — don't make an empty commit and don't amend. If a criterion proves unmeasurable, revise it **underneath** the original with the reason and commit it as `revise unit 9 criterion <n> — unmeasurable as written` (never touch the original line).

**Before you move on:** five numbered criteria with targets, reasons and check-methods, ≥3 about the extension, ≥1 about the bad path, committed while no result exists.

---

## Milestone 5 — Run the test

Three trials each, changing nothing in between. Nobody wrote a test set for you: decide what each criterion must be run against, then run it.

- [ ] 5.1 **Restart clean** via `run.sh` so the log's boundary is unambiguous, and note the timestamp.
- [ ] 5.2 **Produce each criterion's number deliberately.** Failure criteria need *real* failures — `python tools/faults.py --fault <name>` per Appendix B. Latency needs enough runs to be a distribution (≥10 warm), not one number. Cost needs 10 runs cache-off. Read the numbers out of the log with `python metrics.py --summary`; that's the point of building the reader in 2.4. **Two filters before a number is allowed into the run log:** drop or label any run whose `pacing_ms` is nonzero (3.8's rule — that is the limiter, not the pipeline), and restart the server between criteria so the pacing window and the session budget are reset rather than accumulating across a whole trial. A latency criterion whose runs were paced measures `REQUESTS_PER_MINUTE`, and it is not a criterion you can defend. **Log hygiene:** give every trial its own log directory (`AI201_LOG_DIR=logs/before-t1`, `before-t2`, …) so "exactly one record per `/ask` request" is countable per trial, fault runs don't pollute a latency trial, and the before and after logs never mix. Commit these directories with the results.
- [ ] 5.3 **Three separate trials per criterion**, identical inputs, nothing changed in between. Re-read 3.8's cache warning before you trust a triple.
- [ ] 5.4 **Fill the run log** — one row per **criterion** (not per question), five rows minimum:

```markdown
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Malformed input gets 400, not 500 | 5 of 5 | | | | |
| 2. Missing index → 503, actionable, no traceback | 5 of 5 | | | | |
| 3. Empty model response never returns 200 | 5 of 5 | | | | |
| 4. A hung model call answers within 30 s (warm) | 9 of 10 | | | | |
| 5. Every `/ask` request incl. failures leaves one log record | 10 of 10 | | | | |
```
  Those five rows are a **format example** with placeholder targets — your rows must carry *your* committed criteria and targets, in your committed order.
- [ ] 5.5 **Under the table, paste real output** for each criterion from one run — actual JSON bodies and actual log lines, not descriptions — and name the file and function that produced each (`serve.py::ask`, `metrics.py::record`, `tools/faults.py::f5_timeout`).
- [ ] 5.6 Commit `results/run_<stamp>_unit9-before.md` plus the log with a message that names it as results: `unit 9 results — run log before fix`. This is the commit that must come *after* `add unit 9 capstone criteria`.

**Before you move on:** five criteria, three trials each, pasted output underneath.

---

## Milestone 6 — Diagnose and improve

- [ ] 6.1 **Mark each criterion** in the run log — **MET** or **MISSED**. A criterion that passed is worth as much thought as one that failed: if you can't say *why* it passed, you don't know whether it was the system or a warm cache.
- [ ] 6.2 **One paragraph per miss:** *at which stage did it happen* (`stage_ms` should tell you — bad_input / retrieve / gate / generate), *and what mechanism do you think is responsible* (name the line). If `error_kind` was missing or wrong for a miss, say so — that's an instrumentation failure, not a pipeline failure, and it's still a diagnosis.
- [ ] 6.3 **Pick exactly one fix**, aimed at the *weakest* criterion — the one furthest from its target, usually the one with the least room between the bad path and the target. Candidates this system is likely to hand you: **If nothing missed:** the rubric accepts naming which target was set too low and the tighter number it should have been (`unit9_rubric.txt:46`), but the brief still requires one measured improvement — so record the underlying metric (p95 latency, refusal rate in degraded mode), not just pass/fail, in both result sets, and aim the fix at the criterion with the least headroom.

| If this missed | Where to look | The one fix | What it will cost |
|---|---|---|---|
| Bad path (timeout / empty / malformed / missing index) | `serve.py:65-104`, `generate.py:241-271`, `store.py:284` | the timeout in 2.2, **or** moving validation inside the protected region in 2.6 | low — but check the 400/504 body is *legible*, not just the status code |
| Warm latency | the `stage_ms` split | cut `TOP_K = 7` (`config.py:36`) | ⚠️ **the trap:** it moves a retrieval criterion — permitted only under the exception declared in out-of-scope item 1: re-run everything, name what got worse, and cite the item 1 wording already committed in Milestone 1 (no new scope exception is invented here) |
| Every `/ask` request incl. failures leaves a record | `serve.py` — is the write in a `finally`? do 400s write? | move/extend the `finally` | low |
| Degraded reranker | `store.py:154-169` | fix the degrade branch and its flag | low |

- [ ] 6.4 **One fix only.** The cap is the point; a second fix in the same commit makes before/after unreadable. Commit separately, naming the criterion.
- [ ] 6.5 **Re-run every criterion, three trials, fresh log** (a new `AI201_LOG_DIR` per trial, e.g. `logs/after-t1`), saved as `results/run_<stamp2>_unit9-after.md` next to the first. Keep **both** sets — one result set is fine; two side by side *is the evidence the loop ran.*
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

- [ ] 7.1 **README → *What It Costs*:** the cost of one run from 3.8 and its method; a **labelled guess** at 100 people a day; a sentence on how you got from one to the other. Do the arithmetic on your own measured numbers and show the multiplication you did:
  ```
  mean prompt tokens/run ≈ ____   × 100 runs/day = ____ in/day
  mean output tokens/run ≈ ____   × 100 runs/day = ____ out/day
  × published rate for gemini-flash      = $____/day, ≈ $____/30 days
  ```
  Say plainly that the tokens came from the API response, and that the money is **arithmetic on a published rate, not a bill**.
- [ ] 7.2 **README → *What's Still Broken*, honestly:** each remaining miss with what you'd do about it and why you stopped, **and the one thing you'd do first given more time, with why that one rather than the others** (`unit9.txt:395`, `unit9_rubric.txt:56` — it asks for a first, not a list). The honest leftovers are already written down in this plan: the abandoned timeout thread (2.2); the fact that the bound covers the **model call** and not the whole request, so wall-clock can reach `GENERATION_TIMEOUT_S` × attempts + backoff when the limiter paces first (2.2, W7); the per-process `LAST_RETRIEVAL` global that is only safe single-user (2.3); no queue or backpressure, so retrieval degrades silently under load — unmeasured here, because no load test is declared (§3); the reranker dependency question (3.4); `run_eval.py` still aborting a whole eval on one bad upstream (W9 — named, deliberately not fixed, out-of-scope item 4); and the fact that `TOP_K = 7` was tuned to the five test questions rather than derived, so the numbers don't generalise beyond them — unit 2's own *What's Still Broken* says that in its closing paragraph (`README.md:755-757`, under the heading at `:745`). Fold in where-this-goes-next: a hosted version, a real corpus instead of the fictional `city_guides` guides, and the fixes unit 2 names for itself — a larger question set and a re-derived `TOP_K` (`README.md:755-757`), and tightening its own criterion 1 and criterion 3 targets to 5/5 (`README.md:765-770`) — then re-running `run_eval.py`. "No auth yet" is fine here. "It works" is not.
- [ ] 7.3 **README structure — the real situation, checked.** The brief does **not** ask you to reorganise the README; it asks for **nine named sections, "added to what's already there"**: *What This Extends · The Shape · Running It · Instrumentation · What It Costs · Run Log and Verdicts · The Improvement · What's Still Broken · How I Used AI*. Those exact names are what a grader greps for. What the file actually looks like today: `# Unit 1` (`:8`: *What This Does, Chunking Strategy, Sample Answer, How I Used AI*…) then `# Unit 2` (`:309`: *Run Log — Before, Verdicts, Diagnoses, The Improvement, What's Still Broken* at `:745`) — unit 2 already used several of the nine names **inside its own block**, which is exactly why the unit 9 block must repeat them under its own heading rather than lean on them.
  - **The move:** finish the `# Unit 9` block started in 1.1, in place at the end of the file, with the nine sub-headings spelled **exactly** as the brief spells them (`unit9.txt:388`–`:396` — *What This Extends · The Shape · Running It · Instrumentation · What It Costs · Run Log and Verdicts · The Improvement · What's Still Broken · How I Used AI*, capitalised and apostrophised exactly as printed there, not approximately): three drafted in Milestone 1, the other six filled from Milestones 3, 5, 6 and 7.1/7.2/7.6. Where a unit 2 section is now superseded, add a pointer line under it (*"unit 2's list, kept as history — the current one is under `# Unit 9`"*) instead of editing it: overwriting unit 2's verdicts destroys before/after evidence unit 2 earned (ground rule 6).
  - **Everything pasted as text** — the ten log records (3.7), both run-log tables, the cost arithmetic. The brief says it twice: **no screenshots, no video.** What you saw scroll past your terminal is *not* the evidence — paste the JSON the request returned and the log line it wrote instead.
- [ ] 7.4 **Justify Path B under *Running It*, and claim the A half while you're there.** Not required as a confession, but the brief says a path switch deserves a sentence and Path B has to carry "the environment it needs." Write: "The retriever runs two local models — an ONNX embedder and a cross-encoder — so a 512 MB free tier cannot hold both; the honest move was to keep it local, make it observable, and say so." Then say, under the same heading, that shape A's requirements were **carried, not skipped**: one documented start command, a service a stranger can drive from the doc's own `curl` examples, one structured record per request including failures, a log that answers questions without new code, and a measured cost per run — and point at the `server`/`pid`/`port` fields on the pasted records as the proof those runs happened under the documented server process. Close with the two sentences the text-only scope earns: one line naming the interface as **out of scope** — no page, no `GET /`, no production server; the service has served JSON text over the two routes unit 2 shipped and still does — and one line saying why that's the right weight here (a single-user local run; `unit9.txt:143`'s "I'm not rebuilding the interface", taken literally: there was never one to rebuild). Path B is a smaller *deployment*, never a smaller *set of requirements*.
- [ ] 7.5 **Re-read the README as a stranger** who has never seen this repo and cannot ask you anything. That's who it's written for.
- [ ] 7.6 **Fill *How I Used AI* — the ninth section, and the one no other step in this plan writes.** Two specific moments (`unit9.txt:396`): what you asked, what you came back, and **what you changed because of it**. Pick moments with a turn in them — the criteria review that found a target you couldn't defend, the 2.2 timeout variant you rejected after weighing the other, the W6 finding that rewrote `RUNNING.md`. Name what you did *differently* as a result, not what the model produced. Nothing named negatively (the brief's own rule for this section), no invented dialogue, and no claim you can't point to in the history: the criteria-before-results ordering, the `TOP_K` amendment in the same commit as the fix, and the abandoned-thread comment are all moments with receipts. Write it before the final commit, not after it.
## Final self-check — actually perform these, don't assume

- [ ] The system runs: `./run.sh`, then a real question answered by the `curl` example printed in `RUNNING.md`'s rewritten unit 9 section (3.2 rewrote `:195-222`; that section is the checklist a stranger follows).
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
  - [ ] **The service is exactly the text it claims to be:** no page ships (`grep -rn "static/" . --include="*.py"` prints nothing, `git check-ignore -v static/` prints nothing), `GET /` returns 404 and the README says that's the declared scope rather than a gap, `grep -rn gunicorn requirements.txt serve.py RUNNING.md` prints **nothing** (a regression guard now, not a to-do — the pin and both mentions went together before Milestone 0), and *Running It* carries the one-line scope statement in `unit9.txt:143`'s terms.
  - [ ] The cost of one run is a measured number with its method beside it, and the README says the cache was off while measuring.
- [ ] **The four submission files exist by name:** `criteria.md`, `RUNNING.md`, `README.md`, and the commit history. Nothing else substitutes for them.
- [ ] All nine of the brief's README sections are present under `# Unit 9`, spelled as the brief spells them, **and none of them is still a scaffold**: `grep -n "filled in Milestone" README.md` must print nothing (1.1 leaves six placeholders precisely so they can't be forgotten, and a heading with a placeholder under it reads as a heading alone). **Everything pasted as text — zero screenshots, zero video links.**
- [ ] `git log --oneline | wc -l` grows by **≥ 8** since `d43f3e0`, and the two named commits sit in the right order.
- [ ] Nothing sensitive: `.env` still untracked (`git check-ignore -v .env` reports a hit), `git log --all --name-only | grep -x .env` prints nothing, and the key appears in **no** README/log/results line — check without echoing it: `grep -rqF "$GEMINI_API_KEY" README.md RUNNING.md logs/ results/ && echo LEAK || echo clean`.
- [ ] Same repository, not a copy: `git remote -v` still points at the repo you submitted for units 1–2, and `d43f3e0` is still an ancestor of `HEAD` (no history rewrite, no re-created repo).

## Submission

- [ ] `git add -A`, then `git status` — are `logs/` **and `results/`** in it, and `serve.py`/`run.sh` changes staged? is `.env` *not*? `.gitignore` already handles `.env`, `.venv/`, `chroma_db/`, `chroma/` and `.cache/`, and deliberately does **not** ignore `results/` (`:26-27`) — `logs/` isn't mentioned either way, so it commits fine (confirm with `git check-ignore -v logs/runs.jsonl`, which must print nothing). `static/` should not exist to be staged — if `git status` lists it, something was built against the declared scope.
- [ ] ⚠️ **Check what `git add -A` is about to sweep in, by name: `git status --short`.** Two files in this repo are course material rather than your work, and they are in *opposite* states, so check both: **`unit9_rubric.txt` (67 lines, untracked — this is the one `git add -A` will silently commit)**, and **`unit9.txt` (416 lines), which is already tracked — it went in with the `ef11850` planning commit**, so there is nothing to remove at Submission and `rm`ing it now would only add a deletion to the history you're being graded on. Decide on purpose, once: either both stay (defensible — the prompt and the rubric are the spec you built against, and they were committed openly at planning time) or `unit9_rubric.txt` moves out of the repo before the final commit. What you must not do is let it arrive by accident in the same commit as your code, which reads as an unstaged-stray rather than a decision.
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
  "pid": 41807, "port": 5000,                             // ◆ which process answered, on which port (`PORT` default, serve.py:114)
  "endpoint": "/ask",
  "question": "How expensive is it to stay at Thornby Wells?",  // ★ input, truncated to 200 chars
  "outcome": "answered",                              // ★ answered|refused|degraded_answered|error
  "error_kind": null,                                 // ★ null | bad_input | no_index | model_timeout
                                                      //   | upstream | internal
  "reason": null,                                     // upstream only: api_error|rate_limited|quota|empty_response
  "stage": null,                                      // where it failed: bad_input|retrieve|gate|generate
  "http_status": 200,
  "degraded": {"rerank": "ok"},                       // ★ ok|degraded, plus any other flag later
  "duration_ms": 1240.5,                              // ★ whole request
  "stage_ms": {"retrieve": 812.4, "gate": 0.1, "generate": 414.9},
  "n_results": 7, "n_candidates": 16,
  "refused": false, "refusal_reason": null,           // gate decision, kept separate from error_kind
  "answer_chars": 412,                                // ★ output summary, not the whole answer
  "tokens_in": 1893, "tokens_out": 96,                // from generate.token_counts()
  "attempts": 1,
  "pacing_ms": 0,                                       // time spent inside _wait_for_slot (2.2) — nonzero means this run's duration_ms is the limiter's, not the pipeline's
  "model": "gemini-3.5-flash-lite"                     // whatever config.MODEL resolves to (config.py:88)
}
```

The `//` notes are for reading only — what `metrics.py` writes is **strict JSON with no comments**, one object per line, so `json.loads` on every line of `logs/runs.jsonl` must succeed. `test.py`'s style of assertion is a fine place to prove it: read the file back and parse every line.

Deliberate choices, all defensible in the README:
- **`outcome` and `error_kind` separate** — a refusal is a *correct* outcome with no error; an error is never a refusal. Conflating them is how W2's empty answer looks like a pass.
- **Timestamp with timezone** (`datetime.now().astimezone()`), because a log without a zone can't be compared to a run log entry.
- **`server` / `pid` / `port`** — Path B's requirement is *a record of it running* somewhere that isn't your editor (`unit9.txt:49`–`:52`, `:410`). A record with no process provenance cannot make that claim: the identical line could have come from `python serve.py` in a terminal or from `app.py ask` inside an editor. Resolve `server` once per process at import (`app.run` vs the CLI paths are distinguishable without guessing), stamp `pid` and the bound port, and keep `model` for *what answered* so the two never blur. Three lines, and the only provenance field a reviewer can check without trusting your prose.
- **`server` is provenance; there is no `channel` field.** Under the documented run path every record is `server: "flask-dev"`; the CLI writes `"cli"`. No client header is recorded — a header the client sends is *claimed* provenance, not evidence, and with a single documented surface there is nothing to distinguish. If a reviewer asks "did browser traffic fail differently from curl traffic?", the answer is that there is no browser traffic: one route, one client, one kind of record.
- **Never raises.** A logging failure must not become a 500. Copy the repo's own attitude at `generate.py:145-146` — `except Exception: pass  # accounting never breaks the thing it is accounting for` — but add the one line to stderr that the rate-limit notice at `generate.py:262-266` already models, so a silent logging failure is still findable (checked once by hand at 2.8).

## Appendix B — fault-injection recipes for `tools/faults.py`

Every fault is injected from the harness, never by an `if FAULT:` branch inside production code. Each prints: name → injection → status + body → whether a `logs/runs.jsonl` record appeared. **Run F4 and F6 against the server with the harness's `curl` and paste the full JSON response body plus the log line** into your run log: those two are the faults a reviewer can see working without reading a line of code, and "`upstream` (reason `empty_response`) came back with a `request_id`, and the log line matches it" is stronger evidence than a status code only you looked at.

| # | Fault | Injection | Expected after M2 |
|---|---|---|---|
| F1 | Missing / non-string question | POST `{}`, `{"question": 123}`, `{"question": ""}`, `{"question": "x"*5000}`, non-JSON body | **400** `bad_input`, logged |
| F2 | Index missing | `mv chroma_db chroma_db.bak` → POST → `mv` back (in a `finally`) | **503** `no_index`, message names `python app.py index` |
| F3 | Invalid API key | set `GEMINI_API_KEY=AI201_invalid_key_for_testing` in the harness's `env` for a subprocess server | **502** `upstream`; body must **not** quote the provider |
| F4 | Empty model response | monkeypatch `generate._get_client` to return an object whose `models.generate_content(**kw)` returns `SimpleNamespace(text=None, usage_metadata=None)`; run the server as a subprocess so the patch is in-process | **502** `upstream` (reason `empty_response`), never a 200 with `answer: ""` |
| F5 | Hung upstream | same stub, but `generate_content` does `time.sleep(120)` before returning text | **504** `model_timeout` in ≲ `GENERATION_TIMEOUT_S`; measure client-side wall-clock, that's the number criterion N needs |
| F6 | Reranker unavailable | run server with `PYTHONPATH` pointed at a temp dir containing a `sentence_transformers.py` that raises `ImportError` on import | **200**, `degraded.rerank == "degraded"`, answer still cites sources |

F1/F2/F3 need no code changes and can also produce your Milestone 2.0 "before" evidence. **F3 is the one that tests 2.2's wrapping**, not the taxonomy's existence — until provider exceptions are wrapped in `UpstreamError`, `classify()` hands them to `internal` and it comes back 500, so it belongs in the 2.8 regression pass and not first in Milestone 5. The harness is **F1–F6**: F7 (internal 500), F8 (rate-limit retry), F9 (body abuse) and F10 (blocked log dir) were pruned at review. The never-raises claim for the logger is checked once by hand at 2.8 with `AI201_LOG_DIR=/root/nowhere`. The rate-limit pattern list at `generate.py:252-258` is untouched; leave a comment there so unit 10 doesn't "fix" the retry by rewording it.

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
| `config.py` | edit | `GENERATION_TIMEOUT_S`, `MAX_QUESTION_CHARS`, `LOG_DIR`/`LOG_FILE`, each env-overridable |
| `generate.py` | edit, inside `generate()` only | timeout wrapper; empty → retry once → raise; expose attempts |
| `store.py` | edit, two spots | `NoIndexError` at `:284`; reranker degrade at `:154-169`; `LAST_RETRIEVAL` flag |
| `app.py` | edit, `ask_pipeline` only | `request_id`, `stage_ms`, `duration_ms`, `error_kind`, `degraded` — additive keys |
| `serve.py` | edit | validation + status mapping + `finally` log write; `/health` gains reranker state; **no new routes** — the service stays JSON text over the routes unit 2 shipped (frontend is out of scope) |
| `criteria.md` | append | the `## Unit 9 criteria` block |
| `RUNNING.md` | rewrite `:195-228` + env section | Path B, one command, worked `curl` examples, error-body shape, log reader, model downloads; gunicorn half **already done** (pre-M0): `:204-213` names one command and says why — keep that paragraph, don't reintroduce a second path |
| `README.md` | edit | the `# Unit 9` block carrying the brief's nine sections — nine names scaffolded in 1.1, then the measured cost, both run logs, the honest "still broken", Path B justification |
| `requirements.txt` | one-line decision | **leave as-is** per 3.4 (reranker becomes optional via the degrade path) — or add `sentence-transformers>=3.4,<3.5` and say why you reversed the starter's reasoning. **done before Milestone 0:** the `gunicorn>=23.0,<24.0` pin (was `:51`) and both places advertising it came out in one pre-M0 commit, because the documented run path is the Flask dev server and production serving is declared out of scope (`unit9.txt:143`); the file now ends at `flask>=3.0,<3.2` (`:46`) |
| `unit9.txt` | already tracked | the assignment text is **committed** (it arrived in `ef11850`), so it needs no action at Submission — see the corrected Submission note |
| `unit9_rubric.txt` | decide | 67 lines, **untracked**: the grading rubric. `git add -A` sweeps it in — commit it deliberately or move it out, don't let it arrive by accident |

Untouched on purpose: `app.py` CLI surface, `chunker.py`, `gate.py`, `scorer.py`, `corpus_info.py`, `ingest.py`, `run_eval.py` (W9 stays W9 — out-of-scope item 4), `questions.py` (units 1–2's ten questions are the baseline's inputs; 3.8's five cost probes live in `RUNNING.md`, not here), `test.py`, `tools/smoke_test.py`, `corpora/`, `criteria.md`'s unit 1/2 blocks, `.gitignore`.

## Appendix D — the commit ledger you should be able to read afterwards

```
unit 9 — already in history before the build starts:
  ef11850 Unit 9 - planning docs                        ← counts toward the ≥8
  b851c4e refactor plan to change scope -- no frontend  ← counts toward the ≥8
  (due now, not yet committed) drop the gunicorn pin + both places advertising it  ← also counts

unit 9 milestone 1: scope …                                    (before any code)
unit 9 milestone 2a: error taxonomy, timeout, empty-response failure, reranker degrade
unit 9 milestone 2b: structured JSONL log, timings, status mapping
unit 9 milestone 2c: fault-injection harness
add unit 9 capstone criteria            ← BEFORE every results commit
unit 9 milestone 3a: run path rewrite (run.sh → serve.py, RUNNING.md)  ← the A half
unit 9 milestone 3b: committed run log, instrumentation extract, measured cost  ← the A half
unit 9 results — run log before fix     ← the pair the history is graded on
unit 9 milestone 6a: <fix> for criterion <n>                   (exactly one)
unit 9 milestone 6b: run log after fix
unit 9 capstone: hardening the RAG system against failure
```
**The brief's floor is eight new commits from this unit**, with `criteria.md` committed before any results and **both** of those commits named in their messages (`unit9.txt:384`). **Two of the eight are already banked** — `ef11850` and `b851c4e`, the planning commits, which are new commits from this unit on top of `d43f3e0` — and the **eleven** commits listed above clear the floor with room to spare even if two of them are ever combined. Read the ledger top to bottom; that order is the evidence. The "at least three commits in this milestone alone" ask (`unit9.txt:180`) sits on **Milestone 2**, which is why M2 carries 2a/2b/2c; M3 lands as the two named checkpoints above. Roughly 550–710 added lines: `errors.py` ~60, `metrics.py` ~90, `tools/faults.py` ~140, `serve.py` ~75, `generate.py` ~40, `store.py` ~30, `app.py` ~25, `run.sh` ~25, plus docs. Docs count.

## Appendix E — what could still go wrong

| Risk | Consequence | Check | Mitigation |
|---|---|---|---|
| Local `python3` is 3.9.6, which cannot even parse this codebase (`config.py:110` uses PEP 604 union syntax); supported range is 3.11–3.13 and **3.14 is out** | nothing runs, or the 2 GB torch install breaks halfway | 0.1 | build the venv with `/opt/homebrew/bin/python3.12` (3.13 is also present); treat the install as the unit's biggest download |
| No index and you forget to rebuild | every criterion fails at once | 0.2 | `run.sh` builds if missing and says so first (3.1); it's step one of every trial |
| Response cache answers three "trials" identically | a false MET you can't defend | 3.8 | `AI201_CACHE=0` for all measurement; say so in the run log |
| The rate limiter's sleep lands inside a measured run | a latency or cost number that describes `REQUESTS_PER_MINUTE` instead of the pipeline, and is indefensible under questioning | 3.8, 5.2 | keep model-touching runs under ~20/rolling minute per server process; read `pacing_ms` and drop or label any run where it is nonzero; restart the server between blocks so `_call_times`/`_session_calls` reset |
| A provider exception is never wrapped, so `classify()` sends it to `internal`/500 | F3 comes back 500 instead of 502 — the taxonomy looks implemented and isn't, and the criterion fails in Milestone 5 rather than here | 2.1, 2.2 | run F3 at the end of M2, not M5; assert the `error_kind`, not just the status |
| Timeout thread left running | resource leak under load | 2.2 | name it in *What's Still Broken*; the documented run is single-user local, so nobody's request queues behind the leak |
| `LAST_RETRIEVAL` global misreports under concurrency | an observability lie | 2.3 | the documented run is single-user local and no load test is declared (§3), so the caveat is written into the README rather than exercised — write it before a reviewer asks |
| `logs/runs.jsonl` accidentally ignored | the evidence isn't committed | 3.6, 3.7 | `git status` after the first write; `git check-ignore -v logs/runs.jsonl` prints nothing — the path doesn't appear in `.gitignore` today |
| The one fix is TOP_K and it moves a retrieval criterion | a worse system wearing a better score | 6.3 | re-run everything; report what got worse — the move is sanctioned by the exception declared in out-of-scope item 1 at Milestone 1, and the fix commit cites it |
| Criteria committed after results | milestone 4 reads as unmet regardless of quality | 2.9, Final self-check | write criteria at end of M2; read `git log --oneline` before pushing |
| A 400 body leaks an exception string | the W3 leak reopens at a new edge | 2.6 | F1 assertions check the body has no traceback |
| README headings drift from the brief's nine names | a grader can't find the sections and marks them absent | 1.1, 7.3 | scaffold the exact names in M1; `grep -n '^#' README.md` before pushing |
| Fault harness leaves the repo dirty (renamed `chroma_db`, stray `.env`) | the next session starts broken | Appendix B | each fault restores its state in a `finally`; `git status` clean at the end of every fault run |
| A request errors but leaves no record (an early return skips the `finally`) | "every request leaves exactly one record" stops being countable and the log understates traffic | 2.6, 3.7's line count | the log write lives only in `ask`'s `finally`; count new lines against `curl` invocations in the F1–F10 run |
| Port 5000 is held by macOS AirPlay Receiver | `run.sh` fails to bind, or `curl` gets a 403 from the wrong process | 2.6, 3.5 | default moved to 5001 in `serve.py`; `PORT` documented in `RUNNING.md` |
| `with ThreadPoolExecutor()` blocks on exit | the timeout never fires; F5 hangs for the stub's full 120 s | 2.2 | `shutdown(wait=False)` or a daemon thread; run F5 at the end of M2 |

## Not doing, and why (say this out loud if asked)

Retrieval tuning (chunks, weights, model swap) — those are unit 1's dials and moving them would make the new criteria unattributable, which is why they are out outright; `TOP_K` is the single declared exception (out-of-scope item 1): it may move once, as the Milestone 6 improvement, if and only if the diagnosis points there. A new CLI surface — `app.py ask` already does everything; new verbs are surface, not capability. A frontend — out by declaration, no exceptions and no thinnest-possible-page compromise: no browser page, no `GET /`, no production server; the service stays the JSON text API unit 2 shipped, and every interaction is `curl` against the documented examples (ground rule 10). The interface wasn't rebuilt — it was never on the board (`unit9.txt:143`). **Three of four stretch items declined** (second improvement, load observation, both run paths); the fourth, the latency breakdown the design already produces, is declared at Milestone 1 and pasted under *Instrumentation* (§3's stretch block). A hardened `run_eval.py` — W9 is real and stays; rewriting the harness mid-unit would move the instrument the unit 1/2 baseline is read from (out-of-scope item 4). Redis, a queue, auth, rate limiting — none is a bottleneck in this system, and inventing a fix for a bottleneck you haven't hit is the shape of work this course is asking you to stop doing. A second shape *as a choice* — breadth is explicitly worth less than one loop completed; note that this does **not** mean shape A was skipped, since only shape A *as an alternative* is out, while its run path, log, instrumentation and measured cost are in, because `unit9.txt:40` demands them of B and C too. Hosted deployment — see out-of-scope item 2; the system still runs as a service a stranger can reach, just on the machine in front of you.
