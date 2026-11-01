"""Configurações centrais do projeto (caminhos, modelos e parâmetros do RAG)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
INDEX_DIR = ROOT_DIR / "data" / "index"
COLLECTION_NAME = "reviews"

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")

# Quantidade de avaliações recuperadas por pergunta
TOP_K = 10
# Similaridade mínima para uma avaliação contar como evidência. O e5 concentra os scores em
# faixa alta: perguntas do escopo ficaram entre 0.857 e 0.96 e perguntas sem relação entre
# 0.80 e 0.877. O limiar barra as claramente fora do escopo; o prompt do LLM trata o restante.
MIN_SIMILARITY = 0.85
