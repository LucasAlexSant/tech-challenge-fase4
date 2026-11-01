"""Construção da base de conhecimento: seleção, limpeza e organização das avaliações."""

import pandas as pd

from voc_rag.config import PROCESSED_DIR, RAW_DIR

REVIEWS_FILE = RAW_DIR / "olist_order_reviews_dataset.csv"
DOCUMENTS_FILE = PROCESSED_DIR / "documents.parquet"


def load_reviews() -> pd.DataFrame:
    """Lê as avaliações brutas do Kaggle."""
    return pd.read_csv(REVIEWS_FILE)


def clean_text(text: str) -> str:
    """Limpa e normaliza o texto de uma avaliação."""
    raise NotImplementedError


def build_documents(reviews: pd.DataFrame) -> pd.DataFrame:
    """Gera os documentos indexáveis (texto + metadados) a partir das avaliações.

    Decisões a documentar no README: tratamento de ausentes, junção de título e
    comentário, metadados mantidos (nota, data, categoria, entrega).
    """
    raise NotImplementedError


def run() -> pd.DataFrame:
    documents = build_documents(load_reviews())
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    documents.to_parquet(DOCUMENTS_FILE, index=False)
    return documents
