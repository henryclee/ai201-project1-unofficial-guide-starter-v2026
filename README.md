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
