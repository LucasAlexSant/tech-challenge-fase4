"""Armazenamento e indexação dos documentos no ChromaDB."""

import chromadb
import pandas as pd

from voc_rag import config
from voc_rag.embeddings import embed_documents

# Limite de registros por chamada de inserção no ChromaDB
BATCH_SIZE = 5000

METADATA_COLUMNS = [
    "order_id",
    "review_score",
    "review_date",
    "purchase_month",
    "order_status",
    "delivery_status",
    "delivery_delay_days",
    "product_category",
    "product_category_en",
]


def get_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(config.INDEX_DIR))
    return client.get_or_create_collection(config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def _metadata(row: dict) -> dict:
    # ChromaDB não aceita valores nulos: campos ausentes são omitidos
    meta = {}
    for col in METADATA_COLUMNS:
        value = row[col]
        if pd.isna(value):
            continue
        meta[col] = value.item() if hasattr(value, "item") else value
    return meta


def build_index(documents: pd.DataFrame) -> None:
    """Gera os embeddings dos documentos e recria o índice em config.INDEX_DIR."""
    client = chromadb.PersistentClient(path=str(config.INDEX_DIR))
    if config.COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(config.COLLECTION_NAME)
    collection = get_collection()

    vectors = embed_documents(documents["text"].tolist(), show_progress=True)
    records = documents.to_dict("records")

    for start in range(0, len(records), BATCH_SIZE):
        batch = records[start : start + BATCH_SIZE]
        collection.add(
            ids=[r["review_id"] for r in batch],
            documents=[r["text"] for r in batch],
            embeddings=vectors[start : start + BATCH_SIZE],
            metadatas=[_metadata(r) for r in batch],
        )
