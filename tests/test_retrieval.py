import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from voc_rag.retrieval import build_filters  # noqa: E402


def test_sem_filtros():
    assert build_filters() is None


def test_condicao_unica_nao_usa_and():
    assert build_filters(max_score=2) == {"review_score": {"$lte": 2}}


def test_multiplas_condicoes():
    assert build_filters(min_score=4, categories=["moveis_decoracao"], delivery_statuses=["atrasado"]) == {
        "$and": [
            {"review_score": {"$gte": 4}},
            {"product_category": {"$in": ["moveis_decoracao"]}},
            {"delivery_status": {"$in": ["atrasado"]}},
        ]
    }
