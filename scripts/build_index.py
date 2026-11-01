"""Prepara as avaliações e constrói o índice vetorial.

Uso: python scripts/build_index.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from voc_rag import data_prep, indexing  # noqa: E402

if __name__ == "__main__":
    documents = data_prep.run()
    print(f"{len(documents)} documentos preparados.")
    indexing.build_index(documents)
    print("Índice construído.")
