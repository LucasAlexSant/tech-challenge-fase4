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
- Se as avaliações não forem suficientes ou não tiverem relação com a pergunta, diga claramente
  que não há evidências suficientes na base para responder.
- Responda em português, de forma objetiva."""


def build_context(evidences: list[Evidence]) -> str:
    """Formata as evidências com identificadores para que a resposta possa citá-las."""
    raise NotImplementedError


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
