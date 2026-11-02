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
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")

# Quantidade de avaliações recuperadas por pergunta
TOP_K = 10
# Similaridade mínima da melhor avaliação para a pergunta ser enviada ao LLM. Calibrado com o
# e5-large (15 perguntas do escopo e 15 sem relação): as do escopo ficaram entre 0.832 e 0.948 e as
# sem relação entre 0.773 e 0.889, faixas que se sobrepõem. Em 0.80, nenhuma pergunta válida é
# barrada; o limiar descarta sem custo as muito distantes e o prompt do LLM recusa as demais.
MIN_SIMILARITY = 0.80
