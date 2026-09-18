# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
Henry Lee, Corpus: city_guides

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

I picked the city_guides corpus. The system answers questions a visitor might have about the
places in the region — how to get around, what to see, where to eat and stay, when to visit, 
and which places are accessible. A user can ask a question in plain language, the system retrieves 
the relevant information from the guides, and it answers using only that information, citing its 
source. If nothing in the corpus is relevant, it says it doesn't have enough information rather 
than guessing.

## Chunking Strategy

**Chunk size:**
Variable — one paragraph per chunk. No fixed character target. 
On this corpus, 269 characters on average (shortest 120, longest 505).

**Overlap:**
None (0 characters).

After reading the documents in the city_guides corpus, I noticed that every document
is clearly organized by heading / subheading (optional) / paragraph. Thus,
my chunking strategy is to keep the heading/subheading context, and then have each paragraph
as a chunk. Therefore, there is no fixed chunk size. Additionally, my chunker splits on paragraph
boundaries, so no sentence is ever cut, and no overlap is needed.

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#4` — produced by: `chunker.py::split_documents`

```
Corry Vale — What to see

The valley itself is the attraction. The footpath network is dense and well marked, and a circuit taking in three of the four villages is about nine miles with 500 metres of ascent. The chapel in the second village is 12th century and always unlocked.
```

**Chunk 3** — source: `guide_givens_mill.md#4` — produced by: `chunker.py::split_documents`

```
Givens Mill — What to see

The mill runs tours on the hour from 11 to 3 and the machinery is operating during them, which is loud and much more impressive than a static exhibit. The church has a Saxon doorway. The river walk downstream reaches Brightwater in about three hours.
```

**Chunk 4** — source: `guide_marchwood.md#3` — produced by: `chunker.py::split_documents`

```
Marchwood — Eat and drink

The best eating is in the Northgate district, a 12-minute tram ride from the station, where about thirty restaurants sit within four streets. The area immediately around the station is uniformly poor and expensive. Marchwood keeps later hours than anywhere else in the region — kitchens serve until 10:30pm, and until midnight on Fridays and Saturdays.
```

**Chunk 5** — source: `guide_seasons.md#2` — produced by: `chunker.py::split_documents`

```
When to visit the region — Summer, June to August

June is excellent everywhere. July and August split: Halden Bay becomes very
busy and the parking problem dominates, Kestrelford fills with walkers, and
Brightwater goes quiet to the point of dullness with the university empty.
```

## Sample Answer

**Question:**
Where can I go to eat at Givens Mill?

**Answer:**

```
At Givens Mill, you can eat at the tearoom attached to the mill or at the village's one pub (where food is served at lunchtimes and Thursday to Saturday evenings). 

Source: `guide_givens_mill.md` (also mentioned in `guide_eating.md`)

Sources retrieved: guide_eating.md, guide_givens_mill.md
```

**My relevance cutoff:**

I chose the cutoff at 0.65. On the test questions the worst best distance was 0.601,
and on the out of scope questiosn the best best distance was 0.808. 0.65 is a conservative
boundary for relevance, though 0.7 would also be reasonable. A larger set of test and out
of scope questions might help determine a more precise boundary.

| Question | In corpus? | Best distance |
|----|---|-------|
| 1  | y | 0.355 |
| 2  | y | 0.316 |
| 3  | y | 0.196 |
| 4  | y | 0.468 |
| 5  | y | 0.601 |
| 6  | n | 0.808 |
| 7  | n | 0.881 |
| 8  | n | 0.982 |
| 9  | n | 0.835 |
| 10 | n | 0.859 |

My in-corpus questions had best distances from 0.196 to 0.601. My out-of-scope questions
had best distances from 0.808 to 0.982. The gap between the two groups is 0.207 wide.


## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

I pasted my five acceptance criteria into AI web chat and asked it to describe how 
it would test each one using only what the sentence says. It couldn't turn my initial 
criterion 4 ("at least 4 of 5 sampled chunks have a coherent fact") into a test — 
"coherent" wasn't measurable. I rewrote it as "every retrieved chunk is prefixed with 
the source document's heading and subheadings," which is a format check. I kept the 
criterion's intent but replaced the unmeasurable word.

**2.**

I asked Claude to write the split_documents function based on my description of the
intended behavior. After a few rounds, it suggested prepending each chunk paragraph
with the context from the heading and subheading by creating a helper function to parse
each document first, and then creating the chunks from this. Claude then wrote the code
and the tests, and I manually approved each change and test.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->
## Stretch features

**1.**
Metadata filtering - let people narrow results by source or date.
City guides has not date data, so filter on source only (filename)
Also include a way to see the valid sources to filter on.

python app.py sources                list source documents in the current index

--source on retrieve/ask narrows results to one exact source document
example usage:
python app.py ask "what's the best time of year to visit?" --source guide_seasons.md

Claude was used to plan out the approach, including adding a way to see the sources, and
then to implement the code change.

**2.**
Conversational memory — let the next question build on the last one.

Only the interactive ask loop (running python app.py ask with no question argument) 
gets memory; a one-shot python app.py ask "..." remains stateless.

Inside the interactive loop, the last 3 Q&A turns are kept (defined in config.py). 
A follow-up question is first rewritten into a standalone search query with one extra 
model call, while the prior turns are also handed to the model as context when answering.

Claude was used to discuss design tradeoffs (e.g. whether to rewrite the
retrieval query or just pass history to the answering prompt) before planning
and implementing the change.

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
