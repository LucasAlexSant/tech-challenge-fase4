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


def find_evidences(question: str, filters: dict | None = None) -> list[Evidence]:
    """Recupera as avaliações se a mais similar passar do limiar; caso contrário, não há evidência.

    O limiar decide se a base tem algo relevante (foi calibrado com a melhor avaliação de cada
    pergunta). Aplicado a cada avaliação, cortaria evidências úteis de perguntas abstratas, cujos
    scores ficam todos próximos do limiar.
    """
    evidences = retrieve(question, config.TOP_K, filters)
    if not evidences or evidences[0].score < config.MIN_SIMILARITY:
        return []
    return evidences


def answer_from_evidences(question: str, evidences: list[Evidence]) -> RagResult:
    """Gera a resposta; sem evidências, responde sem chamar o LLM."""
    if not evidences:
        return RagResult(NO_EVIDENCE_ANSWER, [], has_evidence=False)

    response = generate_answer(question, build_context(evidences))
    return RagResult(response, evidences, has_evidence=True)


def answer(question: str, filters: dict | None = None) -> RagResult:
    return answer_from_evidences(question, find_evidences(question, filters))
