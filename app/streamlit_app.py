"""Interface para perguntas sobre a voz do cliente.

Uso: streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402
from citations import cited_answer  # noqa: E402

from voc_rag import config  # noqa: E402
from voc_rag.data_prep import DOCUMENTS_FILE  # noqa: E402
from voc_rag.pipeline import answer_from_evidences, find_evidences  # noqa: E402
from voc_rag.retrieval import build_filters  # noqa: E402

DELIVERY_LABELS = {"no_prazo": "No prazo", "atrasado": "Atrasado", "nao_entregue": "Não entregue"}

EXAMPLES = [
    "Quais são os principais problemas relatados pelos clientes?",
    "O que os clientes relatam sobre problemas relacionados à entrega?",
    "Quais aspectos da experiência de compra são mais elogiados?",
    "Quais os motivos de insatisfação dos clientes?",
    "Existem padrões recorrentes relacionados à qualidade dos produtos?",
]


@st.cache_data
def load_categories() -> list[str]:
    return sorted(pd.read_parquet(DOCUMENTS_FILE, columns=["product_category"])["product_category"].unique())


def describe_filters(min_score: int, max_score: int, categories: list[str], delivery: list[str]) -> str:
    badges = []
    if (min_score, max_score) != (1, 5):
        badges.append(f":blue-badge[:material/star: nota {min_score}–{max_score}]")
    badges += [f":violet-badge[:material/category: {c}]" for c in categories]
    badges += [f":orange-badge[:material/local_shipping: {DELIVERY_LABELS[d]}]" for d in delivery]
    return " ".join(badges)


def evidences_table(evidences) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ID": [f"R{i}" for i in range(1, len(evidences) + 1)],
            "Similaridade": [e.score for e in evidences],
            "Nota": ["★" * int(e.metadata.get("review_score", 0)) for e in evidences],
            "Entrega": [DELIVERY_LABELS.get(e.metadata.get("delivery_status"), "-") for e in evidences],
            "Categoria": [e.metadata.get("product_category") for e in evidences],
            "Avaliação": [e.text for e in evidences],
            "review_id": [e.review_id for e in evidences],
        }
    )


def show_evidences(evidences) -> None:
    st.dataframe(
        evidences_table(evidences),
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn(width="small"),
            "Similaridade": st.column_config.ProgressColumn(
                format="%.3f", min_value=0.75, max_value=1.0, width="small"
            ),
            "Nota": st.column_config.TextColumn(width="small"),
            "Avaliação": st.column_config.TextColumn(width="large"),
        },
        alt="Avaliações recuperadas que fundamentam a resposta",
    )


def show_answer(answer: str, evidences, index: int) -> None:
    if not evidences:
        st.markdown(answer)
        return
    cited_answer(answer, evidences, DELIVERY_LABELS, key=f"answer-{index}")
    with st.expander(f"Evidências ({len(evidences)} avaliações)", icon=":material/fact_check:"):
        show_evidences(evidences)


def show_turn(turn: dict, index: int) -> None:
    with st.chat_message("user"):
        st.markdown(turn["question"])
        if turn["filters_label"]:
            st.markdown(turn["filters_label"])
    with st.chat_message("assistant"):
        if turn.get("error"):
            st.error(turn["error"], icon=":material/error:")
            return
        show_answer(turn["answer"], turn["evidences"], index)


st.set_page_config(page_title="Voice of Customer Intelligence", page_icon=":material/forum:", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("Filtros", icon=":material/filter_list:")
    min_score, max_score = st.slider("Nota da avaliação", 1, 5, (1, 5))
    delivery = st.pills(
        "Situação da entrega", list(DELIVERY_LABELS), format_func=DELIVERY_LABELS.get, selection_mode="multi"
    )
    categories = st.multiselect("Categoria do produto", load_categories(), placeholder="Todas")
    st.caption(
        f"Busca semântica com `{config.EMBEDDING_MODEL.split('/')[-1]}` · top {config.TOP_K} · "
        f"limiar {config.MIN_SIMILARITY} · LLM `{config.LLM_MODEL}`"
    )
    if st.button("Limpar conversa", icon=":material/delete_sweep:", width="stretch"):
        st.session_state.history = []

st.title("Voice of Customer Intelligence", icon=":material/forum:")
st.caption("Pergunte sobre as avaliações de clientes da Olist. Cada resposta cita as avaliações que a sustentam.")

for i, turn in enumerate(st.session_state.history):
    show_turn(turn, i)

example = None
if not st.session_state.history:
    example = st.pills("Exemplos", EXAMPLES, label_visibility="collapsed", key="example")

question = st.chat_input("Faça uma pergunta sobre a experiência dos clientes", submit_mode="disable") or example

if question:
    filters = build_filters(min_score, max_score, categories, delivery)
    turn = {
        "question": question,
        "filters_label": describe_filters(min_score, max_score, categories, delivery),
        "answer": "",
        "evidences": [],
    }

    with st.chat_message("user"):
        st.markdown(question)
        if turn["filters_label"]:
            st.markdown(turn["filters_label"])

    with st.chat_message("assistant"):
        try:
            with st.status("Buscando avaliações", type="step") as status:
                evidences = find_evidences(question, filters)
                if evidences:
                    status.update(
                        label=f"{len(evidences)} avaliações recuperadas "
                        f"(similaridade {evidences[-1].score:.3f}–{evidences[0].score:.3f})",
                        state="complete",
                    )
                else:
                    status.update(
                        label=f"Nenhuma avaliação relevante (similaridade abaixo de {config.MIN_SIMILARITY})",
                        state="complete",
                    )

            with st.status("Gerando resposta", type="step") as status:
                result = answer_from_evidences(question, evidences)
                status.update(
                    label="Resposta gerada com base nas evidências" if result.has_evidence else "LLM não acionado",
                    state="complete",
                )
        except Exception as exc:  # falhas do LLM (cota, rede) não devem derrubar a interface
            turn["error"] = f"Não foi possível gerar a resposta: {exc}"
            st.error(turn["error"], icon=":material/error:")
        else:
            turn["answer"], turn["evidences"] = result.answer, result.evidences
            show_answer(result.answer, result.evidences, len(st.session_state.history))

    st.session_state.history.append(turn)
