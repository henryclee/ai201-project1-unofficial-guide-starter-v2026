"""
Stages 3 and 4 of the pipeline: embedding chunks and retrieving them.

Three things in here are worth knowing about, because they'd quietly break the
rest of the project if they were wrong:

1. The Chroma collection is created with cosine distance, explicitly. Chroma
   defaults to squared L2, and the 0.6 threshold the course uses is calibrated
   against cosine. Getting this wrong makes every distance number meaningless.

2. `search` returns the distance alongside each chunk. Milestone 4 has you
   compare distances, so they have to be visible.

3. The embedding model is the one Chroma bundles, not one loaded through
   `sentence-transformers`. It is the same model — `all-MiniLM-L6-v2`, 384
   dimensions — but it arrives as an ONNX build from Chroma's own CDN, so the
   install needs neither PyTorch nor a reachable Hugging Face. See `_embedder`.
"""

import os
import re
import shutil
from dataclasses import dataclass

# Must be set BEFORE chromadb is imported. Without it, some Chroma versions
# print "Failed to send telemetry event ..." on every single call — which looks
# exactly like a real error, isn't one, and cost a previous cohort a lot of
# confused help-channel messages.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb  # noqa: E402
from rank_bm25 import BM25Okapi  # noqa: E402

import config
from chunker import Chunk


@dataclass
class Result:
    """One retrieved chunk and how far it was from the question."""

    text: str
    source: str
    label: str
    distance: float   # LOWER IS BETTER. 0.3 is close, 0.9 is unrelated.
    produced_by: str


_model = None
_reranker = None

# The model Chroma bundles. Anything else in config.EMBEDDING_MODEL means
# "fetch that one from Hugging Face instead" — see `_embedder`.
BUNDLED_MODEL = "all-MiniLM-L6-v2"


class _OnnxEmbedder:
    """
    Chroma's built-in embedder, wrapped to look like the other two.

    Chroma's embedding functions are called directly and hand back numpy
    arrays. The rest of this file wants `.encode(texts)`, so the adapter lives
    here rather than making every caller care which embedder it got.
    """

    def __init__(self):
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

        self._ef = ONNXMiniLM_L6_V2()

    def encode(self, texts, show_progress_bar: bool = False):
        return [vector.tolist() for vector in self._ef(list(texts))]


def _sentence_transformer(name: str):
    """
    The escape hatch: any model that isn't the bundled one.

    Unit 2's "try a second embedding model" stretch option comes through here,
    and so does anything you set `EMBEDDING_MODEL` to. This path *does* need
    `sentence-transformers` and a reachable Hugging Face, neither of which the
    default install has — which is the whole point of the default install.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            f"config.EMBEDDING_MODEL is set to {name!r}, which isn't the model "
            f"Chroma bundles ({BUNDLED_MODEL!r}), so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'\n"
            f"Or set EMBEDDING_MODEL back to {BUNDLED_MODEL!r}."
        ) from exc

    return SentenceTransformer(name)


def _embedder():
    """
    Load the embedding model once and keep it.

    First call is slow — it downloads about 80 MB. That's why setup happens
    before class.
    """
    global _model

    if _model is not None:
        return _model

    # Used only by this repo's own smoke test, which runs where no model can be
    # downloaded at all. Never set this yourself.
    if os.getenv("AI201_FAKE_EMBEDDINGS") == "1":
        from _smoke_embedder import FakeEmbedder

        _model = FakeEmbedder()
    elif config.EMBEDDING_MODEL == BUNDLED_MODEL:
        _model = _OnnxEmbedder()
    else:
        _model = _sentence_transformer(config.EMBEDDING_MODEL)

    return _model


def _cross_encoder():
    """
    Load the reranking model once and keep it.

    Same escape-hatch shape as `_sentence_transformer`: this needs
    `sentence-transformers` (and the PyTorch it drags in), which isn't part of
    the default install for the same reasons the alt-embedding-model path
    isn't. First call downloads the model.
    """
    global _reranker

    if _reranker is not None:
        return _reranker

    try:
        from sentence_transformers import CrossEncoder
    except ImportError as exc:
        raise RuntimeError(
            f"Reranking needs a cross-encoder model ({config.RERANK_MODEL!r}), "
            f"which isn't the model Chroma bundles, so it has to be downloaded "
            f"from Hugging Face.\n"
            f"Install the optional dependency first:\n"
            f"    pip install 'sentence-transformers>=3.4,<3.5'"
        ) from exc

    _reranker = CrossEncoder(config.RERANK_MODEL)
    return _reranker


def _rerank(question: str, results: list["Result"]) -> list["Result"]:
    """
    Reorder retrieved chunks by how relevant a cross-encoder judges each one
    to be to `question`, best first.

    Unlike the bi-encoder (`embed`), which scores the question and a chunk
    independently and compares the two vectors, a cross-encoder reads the pair
    together — so it catches chunks that are genuinely relevant but don't share
    much wording with the question, which is exactly where cosine similarity
    ranks true positives unevenly (see config.RERANK_CANDIDATES).
    """
    if not results:
        return results

    scores = _cross_encoder().predict([(question, r.text) for r in results])
    return [r for _, r in sorted(zip(scores, results), key=lambda pair: -pair[0])]


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _fuse_rankings(*rankings: list[str], k: int = 60) -> dict[str, float]:
    """
    Reciprocal Rank Fusion: combine several best-first ranked-id lists into one
    score per id, without needing the lists' scores to be on the same scale.

    Cosine distance and a BM25 score aren't comparable numbers, so averaging
    them directly would be meaningless — RRF sidesteps that by only using each
    list's *rank order*. An id absent from a list simply gets no contribution
    from it, so a chunk that only one method finds can still surface, which is
    the point: BM25 catches the lexical match (the shared "limited mobility"
    heading) that cosine similarity ranks too low to reach.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, chunk_id in enumerate(ranking):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank)
    return scores


def embed(texts: list[str]) -> list[list[float]]:
    """Turn text into vectors. Runs on your machine, costs no API quota."""
    vectors = _embedder().encode(texts, show_progress_bar=False)
    # sentence-transformers and the smoke stand-in return something with a
    # .tolist(); _OnnxEmbedder has already done that conversion itself.
    return vectors.tolist() if hasattr(vectors, "tolist") else vectors


def _client():
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DIR),
        settings=chromadb.config.Settings(anonymized_telemetry=False),
    )


def build_index(
    chunks: list[Chunk],
    corpus: str | None = None,
    variant: str = "default",
) -> int:
    """
    Embed every chunk and store it.

    `variant` lets you keep more than one index of the same corpus at the same
    time. In unit 2, when you compare two chunking strategies, index the second
    one as variant="v2" and you can query both instead of deleting the first
    and starting over.
    """
    name = config.collection_name(corpus, variant)
    client = _client()

    try:
        client.delete_collection(name)
    except Exception:
        pass

    collection = client.create_collection(
        name=name,
        # ⚠️ Do not remove. Chroma defaults to squared L2, and every distance
        # number in this course assumes cosine.
        metadata={"hnsw:space": "cosine"},
    )

    batch = 256
    for start in range(0, len(chunks), batch):
        window = chunks[start : start + batch]
        collection.add(
            ids=[f"{c.source}#{c.index}" for c in window],
            documents=[c.text for c in window],
            embeddings=embed([c.text for c in window]),
            metadatas=[
                {"source": c.source, "index": c.index, "produced_by": c.produced_by}
                for c in window
            ],
        )

    return len(chunks)


def search(
    question: str,
    top_k: int | None = None,
    corpus: str | None = None,
    variant: str = "default",
    source: str | None = None,
) -> list[Result]:
    """
    Retrieve the chunks closest in meaning to a question.

    `source`, when given, restricts results to chunks from that exact source
    filename, using Chroma's metadata filter.

    Returns them nearest-first by relevance, each with its (bi-encoder cosine)
    distance. Retrieval is hybrid: a bi-encoder ranking and a BM25 keyword
    ranking are fused (see `_fuse_rankings`), the fused pool is reranked with a
    cross-encoder (see `_rerank`), and the result is truncated to `top_k`. Pure
    cosine similarity alone ranks some true positives too low to reach a small
    top_k — see config.RERANK_CANDIDATES — and BM25 catches ones that share a
    question's wording (e.g. a heading) even when their own body doesn't.
    """
    top_k = top_k or config.TOP_K
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    # n_results=collection.count(): every chunk, ranked, with a real cosine
    # distance for each one. Cheap at this corpus's scale, and it means BM25
    # scores against the exact same candidate set instead of a separate fetch.
    raw = collection.query(
        query_embeddings=embed([question]),
        n_results=collection.count(),
        where={"source": source} if source else None,
    )

    by_id: dict[str, Result] = {}
    embedding_ranking: list[str] = []
    texts_in_rank_order: list[str] = []
    for text, meta, distance in zip(
        raw["documents"][0], raw["metadatas"][0], raw["distances"][0]
    ):
        chunk_id = f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}"
        by_id[chunk_id] = Result(
            text=text,
            source=str(meta.get("source", "unknown")),
            label=chunk_id,
            distance=float(distance),
            produced_by=str(meta.get("produced_by", "unknown")),
        )
        embedding_ranking.append(chunk_id)
        texts_in_rank_order.append(text)

    if not by_id:
        return []

    bm25 = BM25Okapi([_tokenize(t) for t in texts_in_rank_order])
    bm25_scores = bm25.get_scores(_tokenize(question))
    bm25_ranking = [
        chunk_id
        for chunk_id, _ in sorted(
            zip(embedding_ranking, bm25_scores), key=lambda pair: -pair[1]
        )
    ]

    fused = _fuse_rankings(embedding_ranking, bm25_ranking)
    candidate_ids = sorted(fused, key=lambda cid: -fused[cid])
    candidate_ids = candidate_ids[: min(config.RERANK_CANDIDATES, len(candidate_ids))]

    candidates = [by_id[cid] for cid in candidate_ids]
    return _rerank(question, candidates)[:top_k]


def list_sources(corpus: str | None = None, variant: str = "default") -> list[str]:
    """The distinct source filenames present in an index, sorted.

    Reads straight from the collection rather than the corpus folder, so it
    stays accurate to whatever `--source` can actually filter on right now —
    including a non-default `variant` — even if the corpus on disk has since
    changed.
    """
    name = config.collection_name(corpus, variant)

    try:
        collection = _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc

    raw = collection.get(include=["metadatas"])
    return sorted({str(meta.get("source", "unknown")) for meta in raw["metadatas"]})


def index_exists(corpus: str | None = None, variant: str = "default") -> bool:
    """Is there an index here to search, without searching it?

    `serve.py`'s health check asks this. It deliberately does not embed
    anything: loading the embedding model takes 80 MB and a few seconds, and a
    health check that heavy is a health check nobody can afford to call.
    """
    try:
        collection = _client().get_collection(config.collection_name(corpus, variant))
        return collection.count() > 0
    except Exception:
        return False


def reset():
    """Delete every index. Occasionally the fastest way out of a mess."""
    if config.CHROMA_DIR.exists():
        shutil.rmtree(config.CHROMA_DIR)
