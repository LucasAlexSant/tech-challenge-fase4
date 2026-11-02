"""Processamento da pergunta e recuperação semântica das avaliações."""

import re
from dataclasses import dataclass, field

from voc_rag.embeddings import embed_query
from voc_rag.indexing import get_collection

# Busca mais candidatos que o necessário para compensar textos repetidos ("Muito bom", "Recomendo")
OVERFETCH_FACTOR = 3


@dataclass
class Evidence:
    review_id: str
    text: str
    score: float
    metadata: dict = field(default_factory=dict)


def transform_query(question: str) -> str:
    """Normaliza espaços; o prefixo "query: " exigido pelo e5 é aplicado em embed_query."""
    return re.sub(r"\s+", " ", question).strip()


def build_filters(
    min_score: int = 1,
    max_score: int = 5,
    categories: list[str] | None = None,
    delivery_statuses: list[str] | None = None,
) -> dict | None:
    """Monta o filtro "where" do ChromaDB a partir dos metadados selecionados."""
    conditions = []
    if min_score > 1:
        conditions.append({"review_score": {"$gte": min_score}})
    if max_score < 5:
        conditions.append({"review_score": {"$lte": max_score}})
    if categories:
        conditions.append({"product_category": {"$in": categories}})
    if delivery_statuses:
        conditions.append({"delivery_status": {"$in": delivery_statuses}})

    if not conditions:
        return None
    # O ChromaDB exige ao menos duas condições dentro de "$and"
    return conditions[0] if len(conditions) == 1 else {"$and": conditions}


def retrieve(question: str, top_k: int, filters: dict | None = None) -> list[Evidence]:
    """Busca as avaliações mais relevantes, sem textos repetidos.

    filters segue a sintaxe "where" do ChromaDB, ex.: {"review_score": {"$lte": 2}}.
    """
    result = get_collection().query(
        query_embeddings=[embed_query(transform_query(question))],
        n_results=top_k * OVERFETCH_FACTOR,
        where=filters or None,
    )

    evidences = []
    seen_texts = set()
    for review_id, text, metadata, distance in zip(
        result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        key = text.casefold().strip(" .!")
        if key in seen_texts:
            continue
        seen_texts.add(key)
        evidences.append(Evidence(review_id, text, score=1 - distance, metadata=metadata))
        if len(evidences) == top_k:
            break
    return evidences
