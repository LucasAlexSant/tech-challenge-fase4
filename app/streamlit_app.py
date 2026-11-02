"""Interface para perguntas sobre a voz do cliente.

Uso: streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from voc_rag.data_prep import DOCUMENTS_FILE  # noqa: E402
from voc_rag.pipeline import answer  # noqa: E402
from voc_rag.retrieval import build_filters  # noqa: E402

DELIVERY_LABELS = {"no_prazo": "No prazo", "atrasado": "Atrasado", "nao_entregue": "Não entregue"}

EXAMPLES = [
    "Quais são os principais problemas relatados pelos clientes?",
    "O que os clientes relatam sobre problemas relacionados à entrega?",
    "Quais aspectos da experiência de compra são mais elogiados pelos clientes?",
    "Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?",
    "Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?",
]


@st.cache_data
def load_categories() -> list[str]:
    return sorted(pd.read_parquet(DOCUMENTS_FILE, columns=["product_category"])["product_category"].unique())


st.set_page_config(page_title="Voice of Customer Intelligence", layout="wide")
st.title("Voice of Customer Intelligence")
st.caption("Perguntas sobre as avaliações de clientes da Olist, respondidas com base em evidências.")

with st.sidebar:
    st.header("Filtros")
    min_score, max_score = st.slider("Nota da avaliação", 1, 5, (1, 5))
    categories = st.multiselect("Categoria do produto", load_categories())
    delivery = st.multiselect("Situação da entrega", list(DELIVERY_LABELS), format_func=DELIVERY_LABELS.get)

    st.header("Exemplos")
    for example in EXAMPLES:
        if st.button(example, use_container_width=True):
            st.session_state.question = example

question = st.text_input("Faça uma pergunta", key="question")

if question:
    filters = build_filters(min_score, max_score, categories, delivery)
    with st.spinner("Buscando avaliações..."):
        result = answer(question, filters)

    st.markdown(result.answer)

    if result.evidences:
        st.subheader(f"Evidências ({len(result.evidences)} avaliações recuperadas)")
        for i, e in enumerate(result.evidences, start=1):
            m = e.metadata
            label = (
                f"[R{i}] nota {m.get('review_score')} · {DELIVERY_LABELS.get(m.get('delivery_status'), '-')}"
                f" · {m.get('product_category')} · similaridade {e.score:.3f}"
            )
            with st.expander(label):
                st.write(e.text)
                st.caption(f"review_id: {e.review_id} · pedido: {m.get('order_id')} · data: {m.get('review_date')}")
