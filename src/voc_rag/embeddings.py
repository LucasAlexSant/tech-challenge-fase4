"""Geração de embeddings para documentos e perguntas com o modelo e5.

O e5 foi treinado com prefixos distintos para perguntas ("query: ") e
documentos ("passage: "); omiti-los degrada a qualidade da busca.
Os vetores são normalizados, então similaridade de cosseno = produto escalar.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from voc_rag import config


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer(config.EMBEDDING_MODEL)


def embed_documents(texts: list[str], show_progress: bool = False) -> list[list[float]]:
    vectors = _model().encode(
        [f"passage: {t}" for t in texts],
        batch_size=64,
        normalize_embeddings=True,
        show_progress_bar=show_progress,
    )
    return vectors.tolist()


def embed_query(question: str) -> list[float]:
    return _model().encode(f"query: {question}", normalize_embeddings=True).tolist()
