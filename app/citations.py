"""Resposta com citações interativas: cada [R1], [R2]... mostra a avaliação ao passar o mouse.

Componente customizado (Streamlit Custom Components v2), porque o Markdown nativo não
suporta tooltips dentro do texto. Funciona com mouse, teclado (foco) e toque.
"""

import html
import re

import markdown
import streamlit as st

# Aceita "[R1]" e "[R1, R2, R6]"
CITATION_RE = re.compile(r"\[(R\d+(?:\s*,\s*R\d+)*)\]")

_HTML = """<div class="answer"></div><div class="card" role="tooltip" hidden></div>"""

_CSS = """
:host { display: block; }
.answer { color: var(--st-text-color); font-family: var(--st-font); font-size: var(--st-base-font-size); line-height: 1.6; }
.answer p { margin: 0 0 0.75rem; }
.answer ul, .answer ol { margin: 0 0 0.75rem; padding-left: 1.5rem; }
.answer li { margin-bottom: 0.25rem; }
.cite {
  font: inherit; font-size: 0.75em; font-weight: 600; line-height: 1;
  padding: 0.15em 0.4em; margin: 0 0.1em; vertical-align: 0.1em;
  border: 1px solid var(--st-primary-color); border-radius: 999px;
  background: var(--st-blue-background-color); color: var(--st-blue-text-color);
  cursor: pointer;
}
.cite:hover, .cite:focus-visible, .cite[aria-expanded="true"] {
  background: var(--st-primary-color); color: var(--st-background-color); outline: none;
}
.card {
  position: fixed; z-index: 1000; max-width: 380px; padding: 0.75rem 0.9rem;
  background: var(--st-secondary-background-color); color: var(--st-text-color);
  border: 1px solid var(--st-border-color); border-radius: var(--st-base-radius);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18); font-family: var(--st-font); font-size: 0.85rem; line-height: 1.5;
}
.card .head { display: flex; justify-content: space-between; gap: 0.75rem; font-weight: 600; margin-bottom: 0.35rem; }
.card .stars { color: var(--st-yellow-color); letter-spacing: 1px; }
.card .meta { color: var(--st-gray-text-color); font-size: 0.78rem; margin-top: 0.5rem; }
"""

_JS = """
export default function (component) {
  const { data, parentElement } = component
  const answer = parentElement.querySelector(".answer")
  const card = parentElement.querySelector(".card")
  if (!answer || !card) return

  if (answer.dataset.html !== data.html) {
    answer.innerHTML = data.html
    answer.dataset.html = data.html
  }

  let pinned = null

  const fill = (ev) => {
    card.replaceChildren()
    const head = document.createElement("div")
    head.className = "head"
    const id = document.createElement("span")
    id.textContent = ev.id + " · " + ev.delivery
    const stars = document.createElement("span")
    stars.className = "stars"
    stars.textContent = "★".repeat(ev.score) + "☆".repeat(5 - ev.score)
    stars.setAttribute("aria-label", "nota " + ev.score + " de 5")
    head.append(id, stars)
    const text = document.createElement("div")
    text.textContent = "“" + ev.text + "”"
    const meta = document.createElement("div")
    meta.className = "meta"
    meta.textContent = ev.category + " · " + ev.date + " · similaridade " + ev.similarity
    card.append(head, text, meta)
  }

  const show = (btn) => {
    const ev = data.evidences[Number(btn.dataset.i)]
    if (!ev) return
    fill(ev)
    card.hidden = false
    const r = btn.getBoundingClientRect()
    const c = card.getBoundingClientRect()
    const left = Math.max(8, Math.min(r.left, window.innerWidth - c.width - 8))
    const below = r.bottom + 6
    const top = below + c.height > window.innerHeight - 8 ? r.top - c.height - 6 : below
    card.style.left = left + "px"
    card.style.top = top + "px"
  }

  const hide = () => {
    if (pinned) return
    card.hidden = true
  }

  answer.querySelectorAll(".cite").forEach((btn) => {
    btn.onmouseenter = () => show(btn)
    btn.onmouseleave = hide
    btn.onfocus = () => show(btn)
    btn.onblur = () => {
      if (pinned === btn) { pinned.setAttribute("aria-expanded", "false"); pinned = null }
      hide()
    }
    btn.onclick = () => {
      if (pinned === btn) {
        btn.setAttribute("aria-expanded", "false")
        pinned = null
        hide()
        return
      }
      if (pinned) pinned.setAttribute("aria-expanded", "false")
      pinned = btn
      btn.setAttribute("aria-expanded", "true")
      show(btn)
    }
    btn.onkeydown = (e) => {
      if (e.key !== "Escape") return
      if (pinned) pinned.setAttribute("aria-expanded", "false")
      pinned = null
      card.hidden = true
    }
  })
}
"""

_COMPONENT = st.components.v2.component("voc_cited_answer", html=_HTML, css=_CSS, js=_JS)


def _render_html(answer: str, n_evidences: int) -> str:
    # O texto do LLM pode repetir conteúdo de avaliações: escapa HTML antes de converter o Markdown
    body = markdown.markdown(html.escape(answer, quote=False))

    def to_buttons(match: re.Match) -> str:
        parts = []
        for ref in re.split(r"\s*,\s*", match.group(1)):
            n = int(ref[1:])
            if 1 <= n <= n_evidences:
                parts.append(
                    f'<button type="button" class="cite" data-i="{n - 1}" '
                    f'aria-label="Ver evidência {ref}" aria-expanded="false">{ref}</button>'
                )
            else:
                parts.append(f"[{ref}]")
        return "".join(parts)

    return CITATION_RE.sub(to_buttons, body)


def cited_answer(answer: str, evidences: list, delivery_labels: dict, *, key: str) -> None:
    """Exibe a resposta com as citações [R*] interativas."""
    _COMPONENT(
        key=key,
        data={
            "html": _render_html(answer, len(evidences)),
            "evidences": [
                {
                    "id": f"R{i}",
                    "text": e.text,
                    "score": int(e.metadata.get("review_score", 0)),
                    "delivery": delivery_labels.get(e.metadata.get("delivery_status"), "-"),
                    "category": e.metadata.get("product_category", "-"),
                    "date": e.metadata.get("review_date", "-"),
                    "similarity": f"{e.score:.3f}",
                }
                for i, e in enumerate(evidences, start=1)
            ],
        },
    )
