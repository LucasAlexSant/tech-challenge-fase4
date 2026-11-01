"""Configurações centrais do projeto (caminhos, modelos e parâmetros do RAG)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
INDEX_DIR = ROOT_DIR / "data" / "index"

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")

# Quantidade de avaliações recuperadas por pergunta
TOP_K = 10
# Similaridade mínima para uma avaliação contar como evidência
MIN_SIMILARITY = 0.0
