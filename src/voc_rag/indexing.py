"""Armazenamento e indexação dos documentos no banco vetorial."""

import pandas as pd


def build_index(documents: pd.DataFrame) -> None:
    """Gera os embeddings dos documentos e persiste o índice em config.INDEX_DIR."""
    raise NotImplementedError
