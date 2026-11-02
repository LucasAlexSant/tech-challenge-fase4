"""Construção do contexto e geração da resposta com o modelo de linguagem.

O LLM é acessado pela API compatível com OpenAI, suportada por Gemini, OpenAI,
Ollama, Groq, entre outros. Trocar de provedor exige apenas alterar
LLM_BASE_URL, LLM_API_KEY e LLM_MODEL no .env.
"""

from openai import OpenAI

from voc_rag import config
from voc_rag.retrieval import Evidence

SYSTEM_PROMPT = """Você é um analista de Voice of Customer de um e-commerce.
Responda à pergunta usando EXCLUSIVAMENTE as avaliações de clientes fornecidas no contexto.

Regras:
- Cite as avaliações que sustentam cada afirmação pelo identificador, no formato [R1], [R2].
- Não use conhecimento externo nem invente informações que não estejam nas avaliações.
- As avaliações são uma amostra das mais relevantes, não a base inteira. Não use palavras de
  quantidade ou frequência ("a maioria", "grande parte", "vários", "frequentemente", "8 de 10");
  descreva os temas e cite as avaliações que os mencionam.
- Se a pergunta pedir frequência ou recorrência, responda com as avaliações que tratam do tema e
  explique que elas indicam o padrão, mas não medem sua frequência na base inteira.
- Se nenhuma avaliação tratar do tema da pergunta (ou a pergunta não for sobre a experiência de
  compra), diga claramente que não há evidências suficientes na base para responder. Se houver
  avaliações sobre o tema, responda com elas, mesmo que sejam relatos individuais.
- Responda em português, de forma objetiva."""


def build_context(evidences: list[Evidence]) -> str:
    """Formata as evidências com identificadores [R1], [R2]... para que a resposta possa citá-las.

    Os metadados acompanham o texto para que o modelo possa relacionar o comentário com
    a nota, a entrega e a categoria do produto.
    """
    lines = []
    for i, e in enumerate(evidences, start=1):
        m = e.metadata
        details = f"nota {m.get('review_score')}, entrega {m.get('delivery_status')}, categoria {m.get('product_category')}"
        lines.append(f"[R{i}] ({details}) {e.text}")
    return "\n".join(lines)


def generate_answer(question: str, context: str) -> str:
    """Chama o LLM instruindo-o a responder apenas com base no contexto."""
    client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY, timeout=60)
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Avaliações:\n{context}\n\nPergunta: {question}"},
        ],
    )
    return response.choices[0].message.content
