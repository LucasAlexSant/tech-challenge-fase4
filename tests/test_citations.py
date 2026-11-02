import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from citations import _render_html  # noqa: E402


def test_citacoes_viram_botoes():
    html = _render_html("Atrasos [R1], [R2] e defeitos [R2, R3].", n_evidences=3)
    assert html.count('class="cite"') == 4
    assert 'data-i="0"' in html and 'data-i="2"' in html


def test_citacao_inexistente_permanece_texto():
    assert "[R7]" in _render_html("Sem fonte [R7].", n_evidences=3)


def test_markdown_renderizado_e_html_escapado():
    html = _render_html("**Atraso** <script>alert(1)</script>\n\n- item [R1]", n_evidences=1)
    assert "<strong>Atraso</strong>" in html
    assert "<li>" in html
    assert "<script>" not in html
