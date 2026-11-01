"""Orquestra o fluxo RAG completo: pergunta → recuperação → contexto → resposta."""

from dataclasses import dataclass

from voc_rag import config
from voc_rag.generation import build_context, generate_answer
from voc_rag.retrieval import Evidence, retrieve

NO_EVIDENCE_ANSWER = (
    "Não encontrei avaliações suficientes na base para responder a essa pergunta com segurança."
)


@dataclass
class RagResult:
    answer: str
    evidences: list[Evidence]
    has_evidence: bool


def answer(question: str, filters: dict | None = None) -> RagResult:
    evidences = [
        e for e in retrieve(question, config.TOP_K, filters) if e.score >= config.MIN_SIMILARITY
    ]
    if not evidences:
        return RagResult(NO_EVIDENCE_ANSWER, [], has_evidence=False)

    response = generate_answer(question, build_context(evidences))
    return RagResult(response, evidences, has_evidence=True)
