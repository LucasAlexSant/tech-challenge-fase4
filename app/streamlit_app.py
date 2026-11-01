"""Interface para perguntas sobre a voz do cliente.

Uso: streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import streamlit as st  # noqa: E402

from voc_rag.pipeline import answer  # noqa: E402

st.set_page_config(page_title="Voice of Customer Intelligence", layout="wide")
st.title("Voice of Customer Intelligence")
st.caption("Perguntas sobre as avaliações de clientes da Olist, respondidas com base em evidências.")

question = st.text_input("Faça uma pergunta")

if question:
    with st.spinner("Buscando avaliações..."):
        result = answer(question)

    st.markdown(result.answer)

    if result.evidences:
        st.subheader("Evidências")
        for e in result.evidences:
            with st.expander(f"{e.review_id} · similaridade {e.score:.2f}"):
                st.write(e.text)
                st.json(e.metadata)
