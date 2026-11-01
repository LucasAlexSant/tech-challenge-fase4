import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from voc_rag.data_prep import build_documents, clean_text  # noqa: E402


def _frames():
    reviews = pd.DataFrame(
        {
            "review_id": ["r1", "r2", "r3", "r1"],
            "order_id": ["o1", "o2", "o3", "o4"],
            "review_score": [1, 5, 4, 1],
            "review_comment_title": ["Atrasou", None, None, "Atrasou"],
            "review_comment_message": ["Chegou\r\ndepois  do prazo", None, "OK", "Chegou\r\ndepois  do prazo"],
            "review_creation_date": ["2018-01-10 00:00:00"] * 4,
            "review_answer_timestamp": ["2018-01-11 00:00:00"] * 4,
        }
    )
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c2", "c3", "c4"],
            "order_status": ["delivered"] * 4,
            "order_purchase_timestamp": ["2017-12-20 10:00:00"] * 4,
            "order_approved_at": [None] * 4,
            "order_delivered_carrier_date": [None] * 4,
            "order_delivered_customer_date": ["2018-01-09 15:00:00", None, None, None],
            "order_estimated_delivery_date": ["2018-01-05 00:00:00"] * 4,
        }
    )
    items = pd.DataFrame({"order_id": ["o1"], "order_item_id": [1], "product_id": ["p1"]})
    products = pd.DataFrame({"product_id": ["p1"], "product_category_name": ["moveis"]})
    translation = pd.DataFrame({"product_category_name": ["moveis"], "product_category_name_english": ["furniture"]})
    return reviews, orders, items, products, translation


def test_clean_text_normaliza_espacos_e_ausentes():
    assert clean_text("  a\r\nb   c ") == "a b c"
    assert clean_text(None) == ""


def test_build_documents():
    docs = build_documents(*_frames())

    # r2 sem texto e r3 com texto curto demais são descartados; r1 duplicado vira um só
    assert docs["review_id"].tolist() == ["r1"]

    doc = docs.iloc[0]
    assert doc["text"] == "Atrasou. Chegou depois do prazo"
    assert doc["delivery_status"] == "atrasado"
    assert doc["delivery_delay_days"] == 4
    assert doc["purchase_month"] == "2017-12"
    assert doc["product_category"] == "moveis"
