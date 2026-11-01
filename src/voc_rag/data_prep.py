"""Construção da base de conhecimento: seleção, limpeza e organização das avaliações.

Cada documento é uma avaliação com texto (título + comentário) e metadados do
pedido usados para filtros e para exibir as evidências.
"""

import re

import pandas as pd

from voc_rag.config import PROCESSED_DIR, RAW_DIR

DOCUMENTS_FILE = PROCESSED_DIR / "documents.parquet"

# Textos com menos letras que isso ("A", "10", "OK") não carregam informação útil para a busca
MIN_LETTERS = 3


def clean_text(text) -> str:
    """Normaliza espaços e quebras de linha; preserva acentos e caixa (o e5 lida com ambos)."""
    if pd.isna(text):
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def _join_title_and_message(title: str, message: str) -> str:
    if title and message:
        separator = " " if title.endswith((".", "!", "?")) else ". "
        return f"{title}{separator}{message}"
    return title or message


def _delivery_status(orders: pd.DataFrame) -> pd.Series:
    delivered = orders["order_delivered_customer_date"]
    estimated = orders["order_estimated_delivery_date"]
    status = pd.Series("nao_entregue", index=orders.index)
    status[delivered.notna()] = "no_prazo"
    status[delivered.dt.normalize() > estimated] = "atrasado"
    return status


def _order_features(orders: pd.DataFrame) -> pd.DataFrame:
    orders = orders.copy()
    for col in ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]:
        orders[col] = pd.to_datetime(orders[col])

    delay = (orders["order_delivered_customer_date"].dt.normalize() - orders["order_estimated_delivery_date"]).dt.days
    return pd.DataFrame(
        {
            "order_id": orders["order_id"],
            "order_status": orders["order_status"],
            "purchase_month": orders["order_purchase_timestamp"].dt.strftime("%Y-%m"),
            "delivery_status": _delivery_status(orders),
            # Positivo = dias de atraso; negativo = entregue antes do previsto
            "delivery_delay_days": delay.astype("Int64"),
        }
    )


def _order_category(items: pd.DataFrame, products: pd.DataFrame, translation: pd.DataFrame) -> pd.DataFrame:
    """Categoria do primeiro item do pedido (cerca de 3% dos pedidos têm produtos de mais de uma categoria)."""
    first_items = items.sort_values(["order_id", "order_item_id"]).drop_duplicates("order_id")
    merged = (
        first_items[["order_id", "product_id"]]
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(translation, on="product_category_name", how="left")
    )
    return pd.DataFrame(
        {
            "order_id": merged["order_id"],
            "product_category": merged["product_category_name"].fillna("desconhecida"),
            "product_category_en": merged["product_category_name_english"].fillna("unknown"),
        }
    )


def build_documents(
    reviews: pd.DataFrame,
    orders: pd.DataFrame,
    items: pd.DataFrame,
    products: pd.DataFrame,
    translation: pd.DataFrame,
) -> pd.DataFrame:
    """Gera os documentos indexáveis (texto + metadados) a partir das avaliações."""
    reviews = reviews.copy()
    title = reviews["review_comment_title"].map(clean_text)
    message = reviews["review_comment_message"].map(clean_text)
    reviews["text"] = [_join_title_and_message(t, m) for t, m in zip(title, message)]

    # Avaliações só com nota (~57%) não têm conteúdo textual para o RAG
    has_content = reviews["text"].str.count(r"[^\W\d_]") >= MIN_LETTERS
    reviews = reviews[has_content]

    # O mesmo review_id aparece em pedidos diferentes com o mesmo texto: mantém uma ocorrência
    reviews = reviews.drop_duplicates("review_id")

    documents = (
        reviews.merge(_order_features(orders), on="order_id", how="left")
        .merge(_order_category(items, products, translation), on="order_id", how="left")
    )
    documents["review_date"] = pd.to_datetime(documents["review_creation_date"]).dt.strftime("%Y-%m-%d")
    documents["product_category"] = documents["product_category"].fillna("desconhecida")
    documents["product_category_en"] = documents["product_category_en"].fillna("unknown")

    return documents[
        [
            "review_id",
            "order_id",
            "text",
            "review_score",
            "review_date",
            "purchase_month",
            "order_status",
            "delivery_status",
            "delivery_delay_days",
            "product_category",
            "product_category_en",
        ]
    ].reset_index(drop=True)


def run() -> pd.DataFrame:
    documents = build_documents(
        reviews=pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv"),
        orders=pd.read_csv(RAW_DIR / "olist_orders_dataset.csv"),
        items=pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv"),
        products=pd.read_csv(RAW_DIR / "olist_products_dataset.csv"),
        translation=pd.read_csv(RAW_DIR / "product_category_name_translation.csv"),
    )
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    documents.to_parquet(DOCUMENTS_FILE, index=False)
    return documents
