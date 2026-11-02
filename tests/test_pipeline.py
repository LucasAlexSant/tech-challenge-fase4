import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from voc_rag import pipeline  # noqa: E402


def test_sem_evidencias_nao_chama_llm(monkeypatch):
    monkeypatch.setattr(pipeline, "retrieve", lambda *args, **kwargs: [])

    def fail(*args, **kwargs):
        raise AssertionError("LLM não deveria ser chamado sem evidências")

    monkeypatch.setattr(pipeline, "generate_answer", fail)

    result = pipeline.answer("Qual a previsão do tempo?")

    assert not result.has_evidence
    assert result.answer == pipeline.NO_EVIDENCE_ANSWER


def _evidence(score):
    return pipeline.Evidence(review_id=f"r{score}", text="texto", score=score)


def test_limiar_avalia_a_melhor_evidencia(monkeypatch):
    limiar = pipeline.config.MIN_SIMILARITY

    monkeypatch.setattr(pipeline, "retrieve", lambda *a, **k: [_evidence(limiar - 0.01), _evidence(limiar - 0.02)])
    assert pipeline.find_evidences("pergunta") == []

    # Acima do limiar, mantém todas as recuperadas, inclusive as abaixo dele
    acima = [_evidence(limiar + 0.01), _evidence(limiar - 0.01)]
    monkeypatch.setattr(pipeline, "retrieve", lambda *a, **k: acima)
    assert pipeline.find_evidences("pergunta") == acima
