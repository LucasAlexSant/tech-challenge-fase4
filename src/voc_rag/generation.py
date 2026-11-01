"""Construção do contexto e geração da resposta com o modelo de linguagem."""

from voc_rag.retrieval import Evidence


def build_context(evidences: list[Evidence]) -> str:
    """Formata as evidências com identificadores para que a resposta possa citá-las."""
    raise NotImplementedError


def generate_answer(question: str, context: str) -> str:
    """Chama o LLM instruindo-o a responder apenas com base no contexto."""
    raise NotImplementedError
