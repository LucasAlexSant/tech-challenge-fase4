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
