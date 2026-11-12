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

**3.**

I asked Claude to help me refactor the prompt for Milestone 4 (failure of generation).

**4.**

I used Claude to plan, implement, test, and iterate over the stretch feature for Unit 2
(fix the retrieval pipeline for criterion 5). It initially measured where each target chunk 
ranked by cosine distance across the full 115-chunk corpus (Thornby Wells: 4th, Marchwood: 17th, 
Brightwater: 35th), suggesting that increasing top-k alone wouldn't work.

We then discussed the options, and opted for BM-25 hybrid retrieval followed by reranking
using a cross-encoder.

After running the eval, there was a regression in Q3, which Claude attributed to ordinary LLM 
sampling variance. I suspected it was actually caused by the top_k increase itself, and asked 
Claude to test that directly — a controlled comparison (5 trials at top_k=5 vs. top_k=7, same 
top-ranked chunk) confirmed the omission rate rose from 3/5 to 1/5, which is what led to the 
added grounding-instruction rule.

**5.**

Claude was helpful in helping me to draft much of the written text of this report, as well
as to identify errors in my writing.

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

## Original ask

python app.py ask "What is there to do at Givens Mills?"
  (best distance 0.394, cutoff 0.65)

Based on the provided documents, visitors can visit the working watermill that commercially grinds flour, take a mill tour, go to the tearoom attached to the mill, and visit the market and the riverside. (Source: `guide_givens_mill.md` and `guide_accessibility.md`)

Sources retrieved: guide_accessibility.md, guide_givens_mill.md

## With source flag - negative example

python app.py ask "What is there to do at Givens Mills?" --source guide_seasons.md
  (best distance 0.771, cutoff 0.65)

I don't have enough information about that.

0 model calls this session

Because we've constrained the source to one that doesn't answer the question, the model no longer has access to any relevant documents.

## With source flat - positive example

python app.py ask "What is there to do at Givens Mills?" --source guide_givens_mill.md 
  (best distance 0.394, cutoff 0.65)

Based on the provided document, visitors can visit the working watermill that still grinds flour commercially, and eat at the tearoom attached to the mill or the village pub (guide_givens_mill.md).

Sources retrieved: guide_givens_mill.md

1 model calls this session, 504 tokens (460 in, 44 out)

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

## Sample two turn conversation

python app.py ask
Ask a question, or press Enter on an empty line to quit.

> Where should I go to eat in Kestrelford?
  (best distance 0.256, cutoff 0.65)

In Kestrelford, you can eat at the four pubs, two cafés, or the bakery (though the bakery sells out by 11am). (Source: `guide_kestrelford.md`)

Sources retrieved: guide_eating.md, guide_kestrelford.md

> How do I get around there?
  (best distance 0.268, cutoff 0.65)

Everything in Kestrelford is within a ten-minute walk of the market square, as there is no local transport or bus service within the town itself (`guide_kestrelford.md` and `guide_accessibility.md`).

Sources retrieved: guide_accessibility.md, guide_kestrelford.md

The second question requires context from the first turn in order to be answered (that it's still referring to Kestrelford), 
showing that the conversation has memory between turns.

**3.**
A second embedding model — swap one in and write down what changed.

I'm using BAAI/bge-large-en-v1.5 as my embedding model, which is a 1024 dimension model. 
With this new embedder, rerunning the same questions as before, I get:

| Question | In corpus? | Best distance |
|----|---|-------|
| 1  | y | 0.213 |
| 2  | y | 0.235 |
| 3  | y | 0.156 |
| 4  | y | 0.291 |
| 5  | y | 0.375 |
| 6  | n | 0.584 |
| 7  | n | 0.622 |
| 8  | n | 0.667 |
| 9  | n | 0.587 |
| 10 | n | 0.555 |

My in-corpus questions had best distances from 0.156 to 0.375. My out-of-scope questions
had best distances from 0.555 to 0.667. The gap between the two groups is 0.180 wide.
Interestingly, the cutoff changes from 0.65 to 0.40-0.50 with a new embedder, but
the gap actually narrowed modestly instead of expanding. 

Another interesting artifact is that on the question "What are good places to visit with 
limited mobility?" (test question 4), the RAG model fails to find the correct answer unless
the top-k is increased from the default of 5 (which works with the default embedder). With
a top-k of 6, it finds an answer (Brightwater, which is a correct answer, but not the 
expected answer -- this is the difference between acceptance criteria 1 and 5). Only when
top-k is increased to 9, does it give the expected answer (Thornby Wells).

This suggests that, at least for these queries, the larger embedder actually performed 
somewhat worse than the default embedder -- it did not increase the separation between in
scope and out of scope questions, and it did not consistently embed the "best"
chunks as nearest the query vector (requiring a larger top-k to find the "answer" chunk).

PLEASE NOTE that I've commented OUT the new embedder in config.py for the submission, since 
it would break the system on anyone else's machine (it points at a locally downloaded model), 
and the sample runs are based on the default model.

This stretch feature was primarily done manually, using Claude only to identify the relevant
sections in code that needed to be adjusted to use the second embedder.

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

From run log:

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Where can I go to eat at Givens Mill? | pass | pass | pass |
| How expensive is it to stay at Thornby Wells? | pass | pass | pass |
| What is the tram schedule in Marchwood on the weekend? | fail | fail | fail |
| What are good places to visit with limited mobility? | pass | pass | pass |
| Where can I go for bird watching? | pass | pass | pass |

Criteria table:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks include context | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Q4 names Thornby Wells, Marchwood, and Brightwater  | 3 of 3 | 1/3 | 1/3 | 1/3 | MISSED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Where can I go to eat at Givens Mill? — run 1

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
At Givens Mill, you can eat at the tearoom attached to the mill or at the village pub, which serves food at lunchtimes and from Thursday to Saturday evenings (source: `guide_givens_mill.md`).
```

### How expensive is it to stay at Thornby Wells? — run 1

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_thornby_wells.md

```
Prices for places to stay in Thornby Wells are moderate and remain stable throughout the year (guide_thornby_wells.md).
```

### What is the tram schedule in Marchwood on the weekend? — run 1

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md

```
The tram network runs every 15 minutes at weekends. 

Source: `guide_marchwood.md`
```

### What are good places to visit with limited mobility? — run 1

- Best distance: 0.4684 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_walking.md

```
**Thornby Wells** is described as the easiest town in the region for those with limited mobility, as it is flat, compact, and the pump room and gardens are level throughout. 

This information comes from `guide_accessibility.md` and `guide_walking.md`.
```

### Where can I go for bird watching? — run 1

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_eating.md, guide_elder_ness.md, guide_kestrelford.md

```
You can go to Elder Ness for bird watching, particularly during the spring and autumn migration seasons (April to May and September to October). This information comes from `guide_elder_ness.md`.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | I checked the retrieved chunks for each answer manually, and checked that it included the chunk with the answer. |
| 2 | Every answer names a source | MET | I checked each of the (15) answers manually to confirm that they all included a source. |
| 3 | Gate stops out-of-corpus questions | MET | All 5 of the out-of-corpus questions had a best distance higher than the cut-off, and were algorithmically refused by the gate. |
| 4 | Retrieved chunks include context | MET | I checked the retrieved chunks for each answer manually, and verified that they all have the correct format of Heading / [Subheading] / Paragraph. |
| 5 | Q4 names Thornby Wells, Marchwood, and Brightwater | MISSED | Each of the answers for Q4 only included Thornby Wells, but not Marchwood or Brightwater.

Retrieved chunks artifact:

Question: Where can I go to eat at Givens Mill?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.3546     guide_givens_mill.md             Givens Mill — Eat and drink  A tearoom attached to t...
2   0.4307     guide_givens_mill.md             Givens Mill — Where to stay  Nothing in the village ...
3   0.4373     guide_eating.md                  Eating across the region — Local specifics  Halden B...
4   0.4547     guide_givens_mill.md             Givens Mill  Givens Mill is a village of 700 built a...
5   0.4656     guide_eating.md                  Eating across the region — Opening hours  Sunday eve...

Gate: best distance 0.355 is under the 0.65 cutoff

---

Question: How expensive is it to stay at Thornby Wells?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.3158     guide_thornby_wells.md           Thornby Wells — Where to stay  Two large hotels from...
2   0.3806     guide_thornby_wells.md           Thornby Wells — Eat and drink  Better than a town th...
3   0.3999     guide_thornby_wells.md           Thornby Wells — Getting around  Flat and compact — 1...
4   0.4191     guide_thornby_wells.md           Thornby Wells  Thornby Wells was a spa town for abou...
5   0.4327     guide_thornby_wells.md           Thornby Wells — Practical notes  Cash is still usefu...

Gate: best distance 0.316 is under the 0.65 cutoff

---

Question: What is the tram schedule in Marchwood on the weekend?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2075     guide_marchwood.md               Marchwood — Getting around  A tram network of four l...
2   0.2494     guide_accessibility.md           Getting around the region with limited mobility — St...
3   0.3247     guide_marchwood.md               Marchwood — Eat and drink  The best eating is in the...
4   0.4207     guide_eating.md                  Eating across the region — The pattern worth knowing...
5   0.4367     guide_marchwood.md               Marchwood — When to go  Any time. This is the one pl...

Gate: best distance 0.208 is under the 0.65 cutoff

---

Question: What are good places to visit with limited mobility?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.4684     guide_walking.md                 Walking in the region — Easy, on good surfaces  **Th...
2   0.4979     guide_accessibility.md           Getting around the region with limited mobility — Pr...
3   0.5070     guide_accessibility.md           Getting around the region with limited mobility  An ...
4   0.5074     guide_accessibility.md           Getting around the region with limited mobility — St...
5   0.5947     guide_accessibility.md           Getting around the region with limited mobility — Di...

Gate: best distance 0.468 is under the 0.65 cutoff

---

Question: Where can I go for bird watching?

#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.6006     guide_elder_ness.md              Elder Ness — What to see  The bird observatory takes...
2   0.6082     guide_elder_ness.md              Elder Ness — When to go  April to May and September ...
3   0.6785     guide_kestrelford.md             Kestrelford — What to see  The market square on a Sa...
4   0.6805     guide_eating.md                  Eating across the region — Opening hours  This catch...
5   0.6923     guide_elder_ness.md              Elder Ness — Where to stay  The pub has four rooms a...

Gate: best distance 0.601 is under the 0.65 cutoff

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

Question 3 failed 3/3 runs. The expectation was that it would include both every 15 minutes, and the fact that the
tram stops running at midnight. This is a failure in generation, as the retrieved chunk includes this information, thus
the generation is not sufficiently precise.

Criterion 5 failed. This is a failure in retrieval, as the retrieved chunks only includes the chunk for Thornby Wells,
and not for Marchwood and Brightwater. It is correct since Thornby Wells is easiest (hence it passes Q4), but it is
incomplete. We need to also retrieve the other Accessibility/Straightforward chunks.

## The Improvement

Fix for Question 3 generation failure.

**What I changed:**

I changed the grounding instruction that makes up the system prompt. I added 3 bullet points:

- Include every fact from the excerpts that directly answers the question. Do not omit relevant details.
- Preserve all specific qualifiers that change the answer.
- Be concise but complete. Completeness is more important than brevity.

and I removed:

- Be brief. Two or three sentences is usually enough.

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

Question 3 was getting the correct chunk, but was not providing all of the necessary information (every 15 minute AND until
midnight). So we needed to adjust the prompt for the LLM to include this relevant information.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

From run log:

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Where can I go to eat at Givens Mill? | pass | pass | pass |
| How expensive is it to stay at Thornby Wells? | pass | pass | pass |
| What is the tram schedule in Marchwood on the weekend? | pass | pass | pass |
| What are good places to visit with limited mobility? | pass | pass | pass |
| Where can I go for bird watching? | pass | pass | pass |

Criteria table:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks include context | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Q4 names Thornby Wells, Marchwood, and Brightwater  | 3 of 3 | 1/3 | 1/3 | 1/3 | MISSED |

### Where can I go to eat at Givens Mill? — run 1

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, at Givens Mill you can go to:

* **A tearoom** attached to the mill, which sells bread made from the flour ground twenty metres away.
* **One pub**, where food is served lunchtimes and Thursday to Saturday evenings.

Source: `guide_givens_mill.md` (and also mentioned in `guide_eating.md` regarding the tearoom).
```

### How expensive is it to stay at Thornby Wells? — run 1

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_thornby_wells.md

```
Prices to stay at Thornby Wells are moderate and stable year-round.

Source: guide_thornby_wells.md
```

### What is the tram schedule in Marchwood on the weekend? — run 1

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes on weekends (until midnight).

Source: guide_marchwood.md
```

### What are good places to visit with limited mobility? — run 1

- Best distance: 0.4684 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_walking.md

```
Based on the provided documents:

* **Thornby Wells** is the region's most accessible town on foot (guide_walking.md) and the easiest town in the region for limited mobility. It is flat, compact, everything is within three minutes of everything else, parking is free for two hours anywhere in town, the station is central, and the pump room and gardens are level throughout (guide_accessibility.md). Additionally, Thornby Wells has flat, formal gardens and level streets (guide_walking.md).
```

### Where can I go for bird watching? — run 1

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_eating.md, guide_elder_ness.md, guide_kestrelford.md

```
Based on the provided documents, you can go for bird watching at:

* **Elder Ness**, specifically during the spring migration (April to May) and autumn migration (September to October), which is the reason to come and what most visitors come for. You can visit the bird observatory, where day visitors are taken and the wardens are generous with their time. *(Source: guide_elder_ness.md)*
```

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

Adjusting the prompt resolved the failure in question 3 in 3/3 runs. Interestingly, it also improved
the completeness of some of the other answers as well.

## Stretch Feature Improvement

Fix for Criterion 5 failure. This requires a change to retrieval, since all the relevant chunks aren't being found to fully
answer the question.

**What I changed:**

I changed the retrieval from a simple bi-encoder, to a hybrid BM-25/bi-encoder with a subsequent reranker
using a cross-encoder.

Running the evaluation after this change caused a regression in Question 3, where it failed to include both the
required details (every 15 minutes, until midnight) that constitute a correct answer. Therefore, I also needed
to further adjust the prompt to correct this regression.

**Why I picked it:**

The initial retrieval was only finding the Thornby Wells chunk, not Marchwood or Brightwater — the 
bi-encoder alone ranked those two too low to reach any reasonable `top_k` (17th and 35th of 115). Hybrid retrieval 
and reranking are the standard fix for this failure mode.

The grounding-instruction addition was a direct response to a side effect this fix caused, not a separate change.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

From `results/run_2026-09-24_1538_after-hybrid-rerank-v2.md`:

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Where can I go to eat at Givens Mill? | pass | pass | pass |
| How expensive is it to stay at Thornby Wells? | pass | pass | pass |
| What is the tram schedule in Marchwood on the weekend? | pass | pass | pass |
| What are good places to visit with limited mobility? | pass | pass | pass |
| Where can I go for bird watching? | pass | pass | pass |

Criteria table:

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks include context | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Q4 names Thornby Wells, Marchwood, and Brightwater | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |

### Where can I go to eat at Givens Mill? — run 1

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to:

* A tearoom attached to the mill (which sells bread made from the flour ground twenty metres away) (*guide_givens_mill.md* and *guide_eating.md*).
* One pub, where food is served at lunchtimes and Thursday to Saturday evenings (*guide_givens_mill.md*).
```

### How expensive is it to stay at Thornby Wells? — run 1

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices for staying in Thornby Wells (which includes two large hotels and several small guesthouses) are moderate and stable year-round (guide_thornby_wells.md).
```

### What is the tram schedule in Marchwood on the weekend? — run 1

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends, until midnight (*guide_marchwood.md*).
```

### What are good places to visit with limited mobility? — run 1

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the places described regarding limited mobility are:

* **Thornby Wells:** Described as the easiest town in the region because it is flat, compact, and everything is within three minutes of everything else; the pump room and gardens are level throughout. (Source: `guide_accessibility.md`)
* **Brightwater:** Described as level along the river and through the centre, with a step-free mill museum. (Source: `guide_accessibility.md`)
* **Marchwood:** Features a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and both the city museum and covered market are step-free, though the distances between districts are the main consideration. (Source: `guide_accessibility.md`)
* **Givens Mill:** Described as one flat street along the river, where the tearoom and riverside are accessible (though the mill tour involves stairs and the machinery floor is not accessible). (Source: `guide_accessibility.md`)
```

### Where can I go for bird watching? — run 1

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided document, you can go to Elder Ness for bird watching during the spring and autumn migration, specifically from April to May and September to October (guide_elder_ness.md).
```

**Did it help?**

Yes, on both fronts. Criterion 5 went from 1/3 to 3/3 — every run now names all 3 towns (Thornby Wells,
Marchwood, and Brightwater), plus a bonus, correct mention of Givens Mill from the neighboring "Mixed"
section. Question 3's regression (introduced by raising `TOP_K`, not by the retrieval changes themselves —
the correct chunk was always retrieved at rank 1) is also back to 3/3, confirmed by the empirical before/after
test in `generate.py`'s grounding instruction rather than by assumption.


## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

All of the test questions, and all of the criteria now pass. However, the fixes were primarily empirical --
for instance, increasing top-K to 7 (from 5) was tuned to the test question, and not a principled value. Future work would include
additional testing with a larger set of questions to see whether top_k=7 generalizes.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
Criterion 1's target(4/5 questions retrieve a chunk with an answer) was set looser than the system actually achieves. It should be
tightened to 5/5.

Criterion 3's target (4/5 gate refusals) was overly loose, and identifies a substantial failure case. If an out of context
question is not refused at the gate, then we are relying on the llm to either identify this, or risk a hallucination. It should be
5/5 gate refusals for this small question set.

---

*Unit 2's "What's Still Broken" above is kept as history; the current list is under `# Unit 9` → What's Still Broken.*

# Unit 9

## What This Extends

This extends **The Unofficial Guide**, the retrieval-augmented question-answering system over the `city_guides` corpus that I built in units 1 and 2: chunking, hybrid BM25 + vector retrieval with a cross-encoder rerank, a relevance gate that refuses out-of-scope questions before the model is called, and a grounded Gemini answer that names its sources.

What's new this unit is a hardening layer plus the operational layer around it. Every request to `POST /ask` now returns a grounded answer, a gate refusal, or a *classified* failure (a status code and a machine-readable `error_kind`, never a raw traceback), and in all three cases leaves one structured record in `logs/runs.jsonl`. Answer quality is unchanged on purpose: retrieval, chunking, the gate threshold and the prompt are exactly what unit 2 left behind.

## The Shape

**Shape B: harden against failure.** Unit 9 adds a layer around the existing five-stage pipeline. A request is bounded by a wall-clock timeout on the model call, an empty model response is treated as a failure instead of returned as a `200`, malformed input gets a `400` instead of a `500`, a missing index gets a `503` that names the fix, and retrieval still answers (flagged as degraded) if the cross-encoder reranker can't load.

The brief requires the run path and the log in every shape, so the operational layer of shape A is carried alongside: one documented start command (`run.sh`), a service that answers JSON over `curl`, one structured record per request including failures, a summary reader for the log, and a measured cost per run.

**Out of scope:**

1. **Retrieval quality.** I'm not touching the chunker, `THRESHOLD`, BM25/RRF fusion or the cross-encoder choice, and no retrieval dial moves before the criteria are measured. The one exception is the Milestone 6 improvement, which the brief requires to follow the diagnosis: if a measured miss points at a retrieval dial such as `TOP_K`, that dial moves once, everything is re-run three trials each, what got worse is named, and this item is amended in the same commit as the fix.
2. **Hosted deployment (Path A).** The system is deployed, on Path B (local with logs). I'm not signing up for a host, writing a Dockerfile or a Procfile.
3. **Traffic handling.** No auth, API keys, per-client limits, queueing or cache changes, and no 10× load test. The existing `REQUESTS_PER_MINUTE` pacing stays a guard rail, not a dial.
4. **The CLI and the local harnesses.** `app.py` subcommands behave as before (only the shared `ask_pipeline` gains fields). `run_eval.py` stays unhardened, so one bad upstream still aborts a whole eval; that is named, not fixed, because changing it would move the instrument unit 1/2's numbers came from. `questions.py` stays exactly as shipped.
5. **The interface.** I'm not rebuilding the interface. The service serves JSON over `POST /ask` and `GET /health` (as it has since unit 2), exercised with `curl`, plus the `app.py` CLI. No browser page, no `GET /`, no `static/`, no production server.

**Stretch:** one stretch feature is added this unit, declared before it is built: a **latency breakdown**, the measured per-stage (`stage_ms`) table over the cost runs, with a sentence on which stage dominates. The other three optional items (a second measured improvement, a 10× load observation, both run paths) are declined: a second fix would make the before/after ambiguous, a load run would measure Flask's dev server and a single-user global rather than this system as scoped, and both run paths means hosted deployment, which item 2 rules out.

## Running It

*Path B — local with logs: one documented start command, a committed run record, text only.* The retriever loads two local models (Chroma's ONNX embedder, about 80 MB, and a `sentence-transformers` cross-encoder that pulls in PyTorch, about 2 GB), which will not fit the 512 MB free hosting tier. The brief directs that case to Path B, which is worth the same as hosting. The start command, the Python version, dependencies and model downloads are in [RUNNING.md](RUNNING.md). The service answers `POST /ask` as JSON text, driven with the `curl` examples in that file. Path A is out of scope by decision (scope item 2), and the interface is out of scope by declaration (scope item 5).

**Run path, tested from a clean copy.** I copied the tree (without `.venv`, `chroma_db/`, `logs/`) to a fresh folder outside the project, built a venv from `requirements.txt` alone — so **without** `sentence-transformers`, deliberately — and followed `RUNNING.md` verbatim: `./run.sh` without a `.env` stops with `GEMINI_API_KEY is not set…`; with the key it printed the first-run index message, built 115 chunks in 4.1 s, and served; the doc's own `curl` examples then returned a grounded answer with `"degraded": {"rerank": "degraded"}` and a matching log record. Before this unit that clean install failed every question. Two honest caveats: nothing in the document turned out to be missing on this machine, but the ONNX embedder was already cached in `~/.cache/chroma`, so the ~80 MB first-run download was not exercised; and the copy used this repo's own `.env`. The environment (Python 3.12, pinned dependencies, the two models and their sizes) is in `RUNNING.md`.

## Instrumentation

Every `/ask` call — answered, refused or failed — appends exactly one JSON line to `logs/runs.jsonl`. It is written by `metrics.py::record`, called from the `finally` block of `serve.py::ask`, so a 400, a 5xx and a timeout leave a record just as a 200 does, and it never raises (a failed write prints one line to stderr instead of breaking the request). `python metrics.py --summary` answers questions about the log without new code.

**What each record holds:** `ts` (ISO-8601 with timezone), `request_id` (also returned to the caller and in `X-Request-Id`), `server`/`pid`/`port` (which process answered, which is what shows this ran as the documented `flask-dev` server and not from an editor), `endpoint`, `question` (input, first 200 characters), `outcome` (`answered | refused | degraded_answered | error`), `error_kind`, `reason` (for `upstream`: `api_error | rate_limited | quota | empty_response`), `stage` (where a failure happened), `http_status`, `degraded` (reranker state), `duration_ms` (whole request), `stage_ms` (`retrieve`/`gate`/`generate`), `n_results`, `n_candidates`, `refused`, `answer_chars` (output summary, not the whole answer), `tokens_in`/`tokens_out`, `attempts`, `pacing_ms` (time the rate limiter made the request wait — nonzero means the latency is the limiter's), `detail` (raw exception text, log only), `model`.

**Where the 22 records came from:** `AI201_CACHE=0 ./run.sh`, then `curl` against it — 2 out-of-scope questions (refused) and the 10 cost questions (see What It Costs) — followed by `python tools/faults.py --all` (F1–F6, 10 records, each fault on its own server process). Reranker mode: `ok` (sentence-transformers installed) for all except F6, which removes it deliberately.

Eleven of the 22 records, verbatim (lines 1, 2, 3, 4, 13, 16, 18, 19, 20, 21, 22 of `logs/runs.jsonl`: two refusals, two answers, then six failures — two `bad_input`, `no_index`, `upstream`/`api_error` from an invalid key, `upstream`/`empty_response`, `model_timeout` — and one degraded answer):

```json
{"ts": "2026-11-12T08:46:05.127-05:00", "server": "flask-dev", "pid": 58339, "port": 5001, "request_id": "74333807", "endpoint": "/ask", "outcome": "refused", "error_kind": null, "http_status": 200, "degraded": {"rerank": "ok"}, "stage_ms": {"retrieve": 3112.3, "gate": 0.0}, "n_results": 7, "n_candidates": 25, "refused": true, "answer_chars": 43, "tokens_in": 0, "tokens_out": 0, "attempts": 0, "pacing_ms": 0.0, "question": "What is the capital of Mongolia?", "duration_ms": 3112.9, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:46:05.205-05:00", "server": "flask-dev", "pid": 58339, "port": 5001, "request_id": "613ef172", "endpoint": "/ask", "outcome": "refused", "error_kind": null, "http_status": 200, "degraded": {"rerank": "ok"}, "stage_ms": {"retrieve": 67.9, "gate": 0.0}, "n_results": 7, "n_candidates": 25, "refused": true, "answer_chars": 43, "tokens_in": 0, "tokens_out": 0, "attempts": 0, "pacing_ms": 0.0, "question": "Who won the 1994 World Cup?", "duration_ms": 68.0, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:46:11.136-05:00", "server": "flask-dev", "pid": 58339, "port": 5001, "request_id": "52f394d7", "endpoint": "/ask", "outcome": "answered", "error_kind": null, "http_status": 200, "degraded": {"rerank": "ok"}, "stage_ms": {"retrieve": 57.1, "gate": 0.0, "generate": 5863.7}, "n_results": 7, "n_candidates": 25, "refused": false, "answer_chars": 349, "tokens_in": 713, "tokens_out": 93, "attempts": 1, "pacing_ms": 0.0, "question": "Where can I go to eat at Givens Mill?", "duration_ms": 5920.9, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:46:19.281-05:00", "server": "flask-dev", "pid": 58339, "port": 5001, "request_id": "8ae8ac02", "endpoint": "/ask", "outcome": "answered", "error_kind": null, "http_status": 200, "degraded": {"rerank": "ok"}, "stage_ms": {"retrieve": 83.3, "gate": 0.0, "generate": 8049.2}, "n_results": 7, "n_candidates": 25, "refused": false, "answer_chars": 128, "tokens_in": 712, "tokens_out": 30, "attempts": 1, "pacing_ms": 0.0, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 8132.7, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:47:49.586-05:00", "server": "flask-dev", "pid": 59441, "port": 59201, "request_id": "6ebd7825", "endpoint": "/ask", "outcome": "error", "error_kind": "bad_input", "reason": null, "stage": "bad_input", "http_status": 400, "detail": null, "stage_ms": null, "question": null, "duration_ms": 0.0, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:47:49.588-05:00", "server": "flask-dev", "pid": 59441, "port": 59201, "request_id": "db15ad46", "endpoint": "/ask", "outcome": "error", "error_kind": "bad_input", "reason": null, "stage": "bad_input", "http_status": 400, "detail": null, "stage_ms": null, "question": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "duration_ms": 0.0, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:47:50.480-05:00", "server": "flask-dev", "pid": 59442, "port": 59210, "request_id": "5263d13b", "endpoint": "/ask", "outcome": "error", "error_kind": "no_index", "reason": null, "stage": "retrieve", "http_status": 503, "detail": "InvalidCollectionException: Collection city_guides__default does not exist.", "stage_ms": {"retrieve": 1.2}, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 1.6, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:47:54.836-05:00", "server": "flask-dev", "pid": 59461, "port": 59215, "request_id": "be4451f0", "endpoint": "/ask", "outcome": "error", "error_kind": "upstream", "reason": "api_error", "stage": "generate", "http_status": 502, "detail": "ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', 'status': 'INVALID_ARGUMENT', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'API_KEY_INVALID', 'domain': 'googleapis.com', 'metadata': {'service': 'g", "stage_ms": {"retrieve": 3094.8, "gate": 0.0, "generate": 385.8}, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 3480.9, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:47:58.759-05:00", "server": "flask-dev", "pid": 59508, "port": 59223, "request_id": "47f48c87", "endpoint": "/ask", "outcome": "error", "error_kind": "upstream", "reason": "empty_response", "stage": "generate", "http_status": 502, "detail": "empty model response after 2 attempts", "stage_ms": {"retrieve": 3057.3, "gate": 0.0, "generate": 0.2}, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 3057.9, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:48:32.675-05:00", "server": "flask-dev", "pid": 59550, "port": 59229, "request_id": "f0021d8f", "endpoint": "/ask", "outcome": "error", "error_kind": "model_timeout", "reason": null, "stage": "generate", "http_status": 504, "detail": "no response within 30s", "stage_ms": {"retrieve": 3041.5, "gate": 0.0, "generate": 30005.4}, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 33047.3, "model": "gemini-3.5-flash-lite"}
{"ts": "2026-11-12T08:48:37.622-05:00", "server": "flask-dev", "pid": 59868, "port": 59235, "request_id": "de4c701d", "endpoint": "/ask", "outcome": "degraded_answered", "error_kind": null, "http_status": 200, "degraded": {"rerank": "degraded"}, "stage_ms": {"retrieve": 487.9, "gate": 0.0, "generate": 3582.1}, "n_results": 7, "n_candidates": 25, "refused": false, "answer_chars": 130, "tokens_in": 677, "tokens_out": 31, "attempts": 1, "pacing_ms": 0.0, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 4070.4, "model": "gemini-3.5-flash-lite"}
```

`python metrics.py --summary` over the full 22 records (the question it answers: *which stage do the failures come from, and where does the time go?*):

```
22 records
outcome: answered=10, degraded_answered=1, error=9, refused=2
error_kind: None=13, bad_input=5, model_timeout=1, no_index=1, upstream=2
http_status: 200=13, 400=5, 502=2, 503=1, 504=1
duration_ms (all):      mean 6253  median 4996  max 33047  (n=22)
duration_ms (answered): mean 8617  median 8133  max 14081  (n=11)
stage_ms.retrieve      mean 808  median 93  max 3112  (n=17)
stage_ms.gate          mean 0  median 0  max 0  (n=16)
stage_ms.generate      mean 8844  median 7863  max 30005  (n=14)
failures by stage:error_kind: bad_input:bad_input=5, generate:model_timeout=1, generate:upstream=2, retrieve:no_index=1
degraded rerank: 1/22
tokens_in:  mean 714  median 713  max 803  (n=11)
tokens_out: mean 64  median 46  max 201  (n=11)
runs with pacing_ms > 0: 0  (those latencies include the rate limiter)
```

**Latency breakdown (declared stretch).** The 10 cost runs, warm server, cache off, `pacing_ms == 0` on every one — `stage_ms` per stage, from the log:

| Stage | mean | median | max |
|---|---|---|---|
| retrieve (embed + BM25 + rerank) | 88 ms | 92 ms | 96 ms |
| gate | 0.0 ms | 0.0 ms | 0.0 ms |
| generate (the Gemini call) | 8,984 ms | 8,169 ms | 13,992 ms |
| **whole request (`duration_ms`)** | **9,072 ms** | **8,258 ms** | **14,081 ms** |

The model call is 99% of a warm request; everything this system does locally is under a tenth of a second. (Before the Milestone 6 fix, the first request after start-up was slower: about 3.1 s of retrieval while the cross-encoder loaded; it now loads at start-up — see The Improvement.)

## What It Costs

**Measured, not estimated.** One run is one `POST /ask` that reaches the model. I started the service with the response cache off (`AI201_CACHE=0 ./run.sh` — with it on, a repeated question reports 0 tokens and a rerun legitimately costs nothing), warmed it with two refused questions, then sent 10 different real questions over HTTP with the same `curl` loop printed in `RUNNING.md`: the five from `questions.py` plus five new `city_guides` probes that are measurement inputs, not criteria (each was screened first with `app.py retrieve`, which makes no model call, to confirm the gate passes it). Tokens are read back from the model's own responses (`generate.py::_record_tokens`) into each record's `tokens_in`/`tokens_out`; all 10 runs had `attempts == 1` and `pacing_ms == 0`, so the rate limiter is not in any number. Reranker mode: `ok`.

| Per run (n = 10) | mean | median | min | max |
|---|---|---|---|---|
| prompt tokens (`tokens_in`) | **718** | 717 | 639 | 803 |
| output tokens (`tokens_out`) | **68** | 46 | 30 | 201 |
| wall-clock (`duration_ms`) | **9.07 s** | 8.26 s | 5.92 s | 14.08 s |

The prompt dominates: 7 retrieved chunks plus the grounding instruction are about 91% of the tokens. A refused question costs nothing in tokens (the gate answers before the model is called) and about 60 ms of local compute. About 99% of the wall-clock is the Gemini call; local retrieval, reranking and gating are under 0.1 s warm.

**For 100 questions a day** (the dollar figure is added in Milestone 7, as arithmetic on a published rate): 718 prompt tokens × 100 = **71,800 in/day**; 68 output tokens × 100 = **6,800 out/day**.

## Run Log and Verdicts

Three trials of the five criteria in `criteria.md`, nothing changed between trials, cache off, a fresh log directory per criterion (`logs/before-tN/cK/`), run by `tools/run_criteria.py`. Reranker mode `ok` except criterion 3, which removes it deliberately. The full file with the pasted output is `results/run_2026-11-12_0938_unit9-before.md`; raw trial output is in `results/unit9-before-trial{1,2,3}.txt`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Injected failures come back classified, nothing leaked (F1 ×5, F2, F3, F4) | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| 2. A hung model call is abandoned within 35 s (F5) | 504 `model_timeout` in ≤ 35 s, every trial | 1/1 (33.1 s) | 1/1 (33.2 s) | 1/1 (33.1 s) | MET |
| 3. Without the reranker, all 5 test questions still answer, grounded and flagged | 5 of 5 | 4/5 | 5/5 | 4/5 | MISSED |
| 4. Every `/ask` leaves exactly one complete log record | 12 of 12 (and 12 lines for 12 requests) | 8/12 (12 lines) | 8/12 (12 lines) | 8/12 (12 lines) | MISSED |
| 5. First request after start-up retrieves in ≤ 500 ms | 3 of 3 restarts | 0/3 (3,070 / 3,124 / 3,107 ms) | 0/3 (3,147 / 3,137 / 3,140 ms) | 0/3 (3,125 / 3,051 / 3,051 ms) | MISSED |

Real output from trial 1, under each criterion (producing code: `tools/run_criteria.py::c1`–`c5`, driving `tools/faults.py`; log lines from `metrics.py::record` via `serve.py::ask`):

**Criterion 1** — `tools/run_criteria.py::c1`
```
  [PASS] f1 {}: 400 bad_input  (0.0s)  {"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}","error_kind":"bad_input","message":"Send JSON with a question in it, l
  [PASS] f1 {"question": 123}: 400 bad_input  (0.0s)  {"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}","error_kind":"bad_input","message":"Send JSON with a question in it, l
  [PASS] f1 {"question": ""}: 400 bad_input  (0.0s)  {"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}","error_kind":"bad_input","message":"Send JSON with a question in it, l
  [PASS] f1 {"question": "x"*5000}: 400 bad_input  (0.0s)  {"error":"Question is too long (max 1000 characters).","error_kind":"bad_input","message":"Question is too long (max 1000 characters).","request_id":"1d5ffcbf"}
  [PASS] f1 not json: 400 bad_input  (0.0s)  {"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}","error_kind":"bad_input","message":"Send JSON with a question in it, l
  [PASS] f2 no_index: 503 no_index  (0.0s)  {"error":"No index called 'city_guides__default'. Run `python app.py index` first.","error_kind":"no_index","message":"No index called 'city_guides__default'. Run `python
  [PASS] f3 invalid_key: 502 upstream  (3.6s)  {"error":"The model service failed to produce an answer. Try again shortly.","error_kind":"upstream","message":"The model service failed to produce an answer. Try again s
  [PASS] f4 empty_response: 502 upstream  (3.1s)  {"error":"The model service failed to produce an answer. Try again shortly.","error_kind":"upstream","message":"The model service failed to produce an answer. Try again s
  -> criterion 1: 8/8  [10s]
```

**Criterion 2** — `tools/run_criteria.py::c2`
```
  [PASS] f5 hung upstream: 504 model_timeout in 33.1s (limit 35 s)  {"error":"The model did not answer in time. Try again.","error_kind":"model_timeout","message":"The model did not answer in time. Try again.","request_id":"4fa250d0"}
  -> criterion 2: 1/1 (33.1s)  [34s]
```

**Criterion 3** — `tools/run_criteria.py::c3` (trial 1; one request hit the 30 s timeout)
```
  [PASS] 'Where can I go to eat at Givens Mill?': 200 degraded={'rerank': 'degraded'} sources=3 names_source=True (15.1s)  Based on the provided documents, you can go to: - A tearoom attached to the mill (which sells bread made from 
  [FAIL] 'How expensive is it to stay at Thornby Wells?': 504 degraded=None sources=0 names_source=False (30.1s)  
  [PASS] 'What is the tram schedule in Marchwood on the we': 200 degraded={'rerank': 'degraded'} sources=3 names_source=True (18.9s)  Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends, until midnig
  [PASS] 'What are good places to visit with limited mobil': 200 degraded={'rerank': 'degraded'} sources=5 names_source=True (14.4s)  Based on the provided documents, there are no places explicitly recommended as "good places to visit with limi
  [PASS] 'Where can I go for bird watching?': 200 degraded={'rerank': 'degraded'} sources=3 names_source=True (0.8s)  Based on the provided documents, you can go for bird watching at Elder Ness (from guide_elder_ness.md).
  -> criterion 3: 4/5  [80s]
```
Its log record (`logs/before-t1/c3/runs.jsonl`):
```json
{"ts": "2026-11-12T09:39:38.311-05:00", "server": "flask-dev", "pid": 87803, "port": 60074, "request_id": "3dcd356b", "endpoint": "/ask", "outcome": "error", "error_kind": "model_timeout", "reason": null, "stage": "generate", "http_status": 504, "detail": "no response within 30s", "stage_ms": {"retrieve": 54.1, "gate": 0.0, "generate": 30006.0}, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 30060.3, "model": "gemini-3.5-flash-lite"}
```
and the trial 3 miss (a provider 503):
```json
{"ts": "2026-11-12T09:44:42.840-05:00", "server": "flask-dev", "pid": 90834, "port": 60269, "request_id": "e6edcde4", "endpoint": "/ask", "outcome": "error", "error_kind": "upstream", "reason": "api_error", "stage": "generate", "http_status": 502, "detail": "ServerError: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "stage_ms": {"retrieve": 57.6, "gate": 0.0, "generate": 18547.8}, "question": "What are good places to visit with limited mobility?", "duration_ms": 18605.6, "model": "gemini-3.5-flash-lite"}
```

**Criterion 4** — `tools/run_criteria.py::c4`
```
  requests sent: 12   log lines: 12   unparseable: 0   complete: 8/12
    incomplete: request_id=a1ede48e outcome=error missing=['question']
    incomplete: request_id=0e555132 outcome=error missing=['question']
    incomplete: request_id=23a779fa outcome=error missing=['question']
    incomplete: request_id=83ae0b02 outcome=error missing=['question']
  -> criterion 4: 8/12 complete, 12 lines for 12 requests  [10s]
```
```json
{"ts": "2026-11-12T09:40:14.295-05:00", "server": "flask-dev", "pid": 88533, "port": 60085, "request_id": "a1ede48e", "endpoint": "/ask", "outcome": "error", "error_kind": "bad_input", "reason": null, "stage": "bad_input", "http_status": 400, "detail": null, "stage_ms": null, "question": null, "duration_ms": 0.0, "model": "gemini-3.5-flash-lite"}
```

**Criterion 5** — `tools/run_criteria.py::c5`
```
  [FAIL] restart 1: first /ask status 200, stage_ms.retrieve = 3070.0 ms (limit 500)
  [FAIL] restart 2: first /ask status 200, stage_ms.retrieve = 3123.6 ms (limit 500)
  [FAIL] restart 3: first /ask status 200, stage_ms.retrieve = 3106.9 ms (limit 500)
  -> criterion 5: 0/3 restarts  [42s]
```
```json
{"ts": "2026-11-12T09:40:28.817-05:00", "server": "flask-dev", "pid": 88653, "port": 60106, "request_id": "98341489", "endpoint": "/ask", "outcome": "answered", "error_kind": null, "http_status": 200, "degraded": {"rerank": "ok"}, "stage_ms": {"retrieve": 3070.0, "gate": 0.0, "generate": 1082.4}, "n_results": 7, "n_candidates": 25, "refused": false, "answer_chars": 106, "tokens_in": 712, "tokens_out": 27, "attempts": 1, "pacing_ms": 0.0, "question": "How expensive is it to stay at Thornby Wells?", "duration_ms": 4152.9, "model": "gemini-3.5-flash-lite"}
```

### Diagnoses

**Criterion 5 — MISSED (0/3 in every trial; first retrieval 3,051–3,147 ms against ~90 ms warm).** Stage: retrieve; component: `store.py::_cross_encoder()` and `_embedder()`, which load their models lazily on first use. I profiled a fresh process rather than assume: the cross-encoder weights load in 2,526 ms, its first `predict` takes another 824 ms (framework warm-up), and the ONNX embedder takes 484 ms; once those have happened a full search is 57–82 ms. The mechanism is that all of that happens inside the first request after start-up, so a model load is billed to whoever asks first. My criterion's 500 ms target assumed retrieval cost was the same on every request.

**Criterion 4 — MISSED (8/12 complete in every trial; 12 lines for 12 requests, all parseable).** Stage: the HTTP edge, in the logging code in `serve.py::ask`, not in the pipeline. `question_text` is only assigned once the body has been validated as a usable question, so the four malformed bodies that have no usable question (`{}`, `{"question": 123}`, `{"question": ""}`, non-JSON) are logged with `question: null`. The fifth (5,000 characters) *is* a string, so it was logged. Every request did leave exactly one record, so the `finally` works; what's missing is the input on exactly the requests whose input is least obvious. This is an instrumentation failure, not a pipeline failure.

**Criterion 3 — MISSED (4/5, 5/5, 4/5).** Stage: generate, and in neither miss was it the degraded-reranker path: every request that got a 200 was flagged `degraded`, had sources and named one (14 of 14 successful answers before the fix). Trial 1: one real model call took longer than `GENERATION_TIMEOUT_S` = 30 s (`stage_ms.generate` = 30,006 ms) and was answered 504 `model_timeout` — the timeout I built, firing on a legitimately slow provider response (I saw a trivial 32-token prompt take 32.9 s outside the pipeline while writing the criteria). Trial 3: the provider returned `503 UNAVAILABLE … high demand` after 18.5 s, and `generate.py`'s retry loop only retries messages matching its rate-limit patterns (`429`, `resource`+`exhaust`, `rate`+`limit`), so a transient 503 went straight to `UpstreamError(reason="api_error")` with no second attempt. The criterion, as I wrote it, measured provider availability through the pipeline as much as it measured the degrade path.

**Pattern.** Three misses, three different stages and no shared cause: criterion 5 is lazy model loading in retrieval, criterion 4 is a log field populated too late at the HTTP edge, and criterion 3 is the model service (a slow call and an un-retried 503). Criteria 1 and 2 were met in every trial.

## The Improvement

**What I changed (one change, aimed at criterion 5):** `store.py::warm_up()` loads the ONNX embedder, loads the cross-encoder and runs one throwaway rerank, and `serve.py::main()` calls it before `app.run`, printing `Loading models…` / `Models ready in N s`. It follows the criterion 5 diagnosis directly: the 3.1 s was model loading and first-call warm-up happening inside the first request, so the fix moves exactly that work to start-up. If the reranker can't be loaded, `warm_up` takes the same degrade path as a request (flags it, remembers it, never raises), so a clean install without `sentence-transformers` still starts. I chose this over fixing criterion 4 because it is the cleanest cause-and-effect and leaves criterion 4's smaller fix for later.

**Before and after, side by side** (same runner, same procedure, three trials each):

*Before the fix* — `results/run_2026-11-12_0938_unit9-before.md`

Three trials of the five criteria in `criteria.md`, nothing changed between them. Produced by
`python tools/run_criteria.py --trial N --phase before` (one trial = one invocation; start
2026-11-12 09:38, 09:41, 09:43). Every server it starts has the response cache off
(`AI201_CACHE=0`) and its own log directory, `logs/before-tN/cK/`. Model: `gemini-3.5-flash-lite`.
Reranker mode: `ok` (sentence-transformers 3.4.1 installed) for criteria 1, 2, 4 and 5; criterion 3
removes it on purpose. Raw per-trial output: `results/unit9-before-trial{1,2,3}.txt`.

*After the fix* — `results/run_2026-11-12_0952_unit9-after.md`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Injected failures come back classified, nothing leaked (F1 ×5, F2, F3, F4) | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| 2. A hung model call is abandoned within 35 s (F5) | 504 `model_timeout` in ≤ 35 s, every trial | 1/1 (30.1 s) | 1/1 (30.1 s) | 1/1 (30.1 s) | MET |
| 3. Without the reranker, all 5 test questions still answer, grounded and flagged | 5 of 5 | 5/5 | 5/5 | 5/5 | MET (not attributable to the fix) |
| 4. Every `/ask` leaves exactly one complete log record | 12 of 12 (and 12 lines for 12 requests) | 8/12 (12 lines) | 8/12 (12 lines) | 8/12 (12 lines) | MISSED |
| 5. First request after start-up retrieves in ≤ 500 ms | 3 of 3 restarts | 3/3 (73.9 / 74.4 / 76.3 ms) | 3/3 (85.1 / 78.8 / 78.8 ms) | 3/3 (76.0 / 80.8 / 74.0 ms) | MET |

**Did it help?** Yes, for the criterion it was aimed at. First-request retrieval went from 3,051–3,147 ms (9 of 9 restarts missed) to 73.9–85.1 ms (9 of 9 met), about 40× faster and now the same as a warm request. I know it's the change and not noise because the two sets of nine numbers don't come close to overlapping, and the profile of the cause (2.5 s + 0.8 s + 0.5 s of loading) accounts for the whole difference.

**What it did elsewhere:**
- *Criterion 2 improved as a side effect:* the hung-call test went from 33.1–33.2 s to 30.1 s in all three trials, because it no longer includes a cold retrieval. The 35 s target now has a 5 s margin instead of under 2.
- *Criterion 4 is unchanged* (8/12 in every trial, same four records). The fix doesn't touch the logging path, and it is still MISSED.
- *Criterion 3 went from 4/5, 5/5, 4/5 to 5/5 in all three trials, but I can't credit the fix.* The change doesn't touch `generate.py`, and the earlier misses were a provider timeout and a provider 503. Fifteen of fifteen calls succeeding this time is the provider being steadier, not evidence that the degrade path or my change improved. I'm reporting it as MET against the target while saying the verdict is not attributable.
- *The cost:* start-up is about 3.5 s slower (`warm_up` took 3.46 s in a fresh process), and the server does not answer `/health` until the models are loaded. Locally that is the right trade; behind a host that health-checks quickly it would not be. The same models end up resident in memory either way: before, loaded by the first request; now, by start-up.

## What's Still Broken

_(filled in Milestone 7)_

## How I Used AI

_(filled in Milestone 7)_
