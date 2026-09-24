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
