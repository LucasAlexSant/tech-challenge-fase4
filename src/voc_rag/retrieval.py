"""Processamento da pergunta e recuperação semântica das avaliações."""

from dataclasses import dataclass, field


@dataclass
class Evidence:
    review_id: str
    text: str
    score: float
    metadata: dict = field(default_factory=dict)


def transform_query(question: str) -> str:
    """Prepara a pergunta para a busca (normalização, expansão, etc.)."""
    raise NotImplementedError


def retrieve(question: str, top_k: int, filters: dict | None = None) -> list[Evidence]:
    """Busca as avaliações mais relevantes, opcionalmente filtrando por metadados."""
    raise NotImplementedError
