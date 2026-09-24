"""
Settings for The Unofficial Guide.

Everything you're likely to change lives here, at the top, on purpose.
You'll edit THRESHOLD in Milestone 4 and the chunking numbers in Milestone 3.

Anything you set in your .env file wins over the defaults here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")


# ─── The corpus you're working with ──────────────────────────────────────────
# Change this to switch corpora, or pass --corpus on the command line.
# Options are the folder names inside corpora/. See corpora/README.md.

CORPUS = os.getenv("AI201_CORPUS", "campus_life")


# ─── Chunking (Milestone 3) ──────────────────────────────────────────────────
# These are deliberately plain, generic numbers. Milestone 3 is where you
# replace them with numbers that fit the documents you actually read.

CHUNK_SIZE = 800  # characters per chunk
CHUNK_OVERLAP = 120  # characters shared between neighbouring chunks


# ─── Retrieval (Milestone 4) ─────────────────────────────────────────────────

TOP_K = 7  # how many chunks to pull back per question

# Criterion 5 fix: the bi-encoder ranks true-positive chunks unevenly when a
# question's wording doesn't echo a chunk's — see guide_accessibility.md's
# "Straightforward" section. Retrieval is hybrid (bi-encoder cosine + BM25
# keyword ranking, fused with Reciprocal Rank Fusion — see store.py::search),
# so a chunk BM25 finds via shared wording (e.g. a heading) can surface even
# when cosine alone ranks it far too low. A cross-encoder then reranks the
# fused pool down to TOP_K, scoring (question, chunk) pairs jointly instead of
# comparing two independently-computed vectors.
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_CANDIDATES = 25  # fused candidate pool size to pull before reranking

# The relevance gate. If the best chunk is further away than this, the system
# refuses to answer instead of handing the model thin material.
#
# LOWER IS BETTER: 0.3 is a close match, 0.9 is unrelated.
#
# 0.6 is a reasonable starting point, not a right answer. Milestone 4 has you
# measure your own two groups of distances and put the cutoff in the gap.
# Most corpora land somewhere between 0.45 and 0.75.
THRESHOLD = 0.65


# ─── Conversational memory (stretch feature) ─────────────────────────────────
# How many prior Q&A turns the interactive `ask` loop keeps as context for
# query rewriting and the generation prompt. Older turns are dropped.
HISTORY_TURNS = 3


# ─── Models ──────────────────────────────────────────────────────────────────
# Embeddings run on your own machine and cost no API quota.
# Only generation calls out to a service.

# This is the model Chroma bundles, and leaving it alone is the fast path: it
# downloads about 80 MB from Chroma's own CDN and needs nothing else installed.
#
# Setting it to any other name — unit 2's "try a second embedding model"
# stretch option — switches to loading that model from Hugging Face instead,
# which needs `pip install 'sentence-transformers>=3.4,<3.5'` first. store.py
# says so with a real error message rather than a stack trace if you forget.

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# For Stretch 3 - change the embedding model

# This is commented out since it is pointing to a locally downloaded model, the
# original huggingface model is "BAAI/bge-large-en-v1.5"

# Also, the sample runs in readme.md are based on the default model

# EMBEDDING_MODEL = "/Volumes/Data/embedding_models/bge-large-en-v1.5"
MODEL = os.getenv("AI201_MODEL", "gemini-3.5-flash-lite")


# ─── Rate limiting and quota guards ──────────────────────────────────────────
# You should not need to touch these. They exist so that a runaway loop costs
# you a warning instead of your whole day's allowance.

REQUESTS_PER_MINUTE = 30  # outgoing calls the limiter will allow per minute
SESSION_REQUEST_BUDGET = 300  # stop and warn rather than draining the daily quota
MAX_RETRIES = 4  # on 429 / resource-exhausted, with backoff

CACHE_ENABLED = os.getenv("AI201_CACHE", "1") != "0"
CACHE_DIR = ROOT / ".cache"


# ─── Paths ───────────────────────────────────────────────────────────────────

CORPORA_DIR = ROOT / "corpora"
CHROMA_DIR = ROOT / "chroma_db"
RESULTS_DIR = ROOT / "results"


def corpus_path(name: str | None = None) -> Path:
    """Folder holding the documents for a corpus."""
    return CORPORA_DIR / (name or CORPUS) / "documents"


def collection_name(name: str | None = None, variant: str = "default") -> str:
    """
    Name of the vector-store collection for a corpus.

    `variant` lets you index the same corpus two different ways and query both
    without deleting anything — you'll want that in unit 2 when you compare
    chunking strategies.

    Chroma is fussy about collection names: 3 to 63 characters, starting and
    ending with a letter or digit, and nothing but letters, digits, underscores
    and hyphens in between. If you bring your own corpus and name the folder
    something Chroma won't accept, this cleans it up rather than failing.
    """
    import re

    raw = f"{name or CORPUS}__{variant}"
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "-", raw)
    cleaned = cleaned.strip("_-")  # must start and end alphanumeric
    if not cleaned or not cleaned[0].isalnum():
        cleaned = f"c{cleaned}"
    if not cleaned[-1].isalnum():
        cleaned = f"{cleaned}0"
    return cleaned[:63].rstrip("_-") or "collection"
