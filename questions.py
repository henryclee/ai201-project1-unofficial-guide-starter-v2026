"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

# Original questions:
# QUESTIONS = [
#     # {"question": "...", "expects": "..."},
#     {"question": "Where can I go to eat at Givens Mill?", "expects": "tearoom"},
#     {
#         "question": "How expensive is it to stay at Thornby Wells?",
#         "expects": "moderate",
#     },
#     {
#         "question": "What is the tram schedule in Marchwood?",
#         "expects": "every 8 minutes on weekdays and every 15 at weekends, until midnight",
#     },
#     {
#         "question": "What are good places to visit with limited mobility?",
#         "expects": "Thornby Wells is the easiest town in the region.",
#     },
#     {
#         "question": "Where can I go for bird watching?",
#         "expects": "The bird observatory takes day visitors",
#     },
# ]

# Questions were adjusted to be mroe specific. Expects were changed to a list of keywords
# that should be in the answer. This is to make the scoring more flexible and less dependent on exact phrasing.

# Question 5 originally required 'bird observatory' in the answer; revised to just 'Elder Ness' because the question
# asks where to go, not for a specific detail about that location — the observatory fact isn't part of what makes an
# answer correct.

QUESTIONS = [
    # {"question": "...", "expects": "..."},
    {"question": "Where can I go to eat at Givens Mill?", "expects": ["tearoom"]},
    {
        "question": "How expensive is it to stay at Thornby Wells?",
        "expects": ["moderate"],
    },
    {
        "question": "What is the tram schedule in Marchwood on the weekend?",
        "expects": ["every 15 minutes", "until midnight"],
    },
    {
        "question": "What are good places to visit with limited mobility?",
        "expects": ["Thornby Wells"],
    },
    {
        "question": "Where can I go for bird watching?",
        "expects": ["Elder Ness"],
    },
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
