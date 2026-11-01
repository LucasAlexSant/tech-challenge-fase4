# Voice of Customer Intelligence com RAG

Tech Challenge — Fase 4 (POSTECH IA para Devs).

Solução baseada em **Retrieval-Augmented Generation (RAG)** para explorar, em linguagem natural, as avaliações de clientes do
[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data),
com respostas fundamentadas nas avaliações recuperadas e exibição das evidências usadas.

## Equipe

| Nome | RM | GitHub |
|------|----|--------|
|      |    |        |

## Problema de negócio

Gestores e analistas precisam identificar rapidamente os principais problemas, elogios e padrões presentes em milhares de
avaliações textuais. A solução transforma esses comentários em uma base de conhecimento consultável, permitindo perguntas como:

- Quais são os principais problemas relatados pelos clientes?
- Quais reclamações relacionadas à entrega aparecem com maior frequência?
- O que os clientes mais elogiam em suas experiências de compra?
- Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?

## Arquitetura

```
Pergunta do usuário
  → Processamento da pergunta            (src/voc_rag/retrieval.py)
  → Embedding da pergunta                (src/voc_rag/embeddings.py)
  → Recuperação das avaliações           (src/voc_rag/retrieval.py → banco vetorial)
  → Construção do contexto               (src/voc_rag/generation.py)
  → Geração da resposta com LLM          (src/voc_rag/generation.py)
  → Resposta + evidências                (app/streamlit_app.py)
```

Construção da base (offline): `data/raw` → `data_prep.py` → `data/processed` → `indexing.py` → `data/index`.

> TODO: inserir diagrama da arquitetura final.

## Estrutura do repositório

```
.
├── app/                    # Interface (Streamlit)
├── data/
│   ├── raw/                # CSVs do Kaggle (não versionados)
│   ├── processed/          # Documentos preparados (não versionados)
│   └── index/              # Banco vetorial persistido (não versionado)
├── docs/                   # Exemplos de perguntas/respostas e material de apoio
├── notebooks/              # Análise exploratória e experimentos
├── scripts/                # Scripts de linha de comando (preparação e indexação)
├── src/voc_rag/            # Código-fonte do pipeline RAG
└── tests/                  # Testes
```

## Tecnologias e bibliotecas

| Componente | Escolha | Justificativa |
|------------|---------|---------------|
| Linguagem | Python 3.11+ | |
| Manipulação de dados | pandas | |
| Embeddings | _a definir_ | |
| Banco vetorial | _a definir_ | |
| LLM | _a definir_ | |
| Interface | Streamlit | |

## Preparação da base de conhecimento

Descrever e justificar cada decisão:

- **Seleção dos dados:** _(ex.: `olist_order_reviews_dataset.csv` + junções com pedidos, itens e produtos)_
- **Limpeza e preparação dos textos:**
- **Tratamento de valores ausentes:** _(ex.: avaliações sem título/comentário)_
- **Organização dos documentos:** _(o que é um documento, quais metadados acompanham)_
- **Criação dos embeddings:**
- **Armazenamento e indexação:**

## Estratégia do pipeline RAG

- **Transformação da pergunta:**
- **Recuperação semântica:** _(top-k, métrica de similaridade)_
- **Seleção dos conteúdos mais relevantes:** _(limiar de similaridade, reranking, deduplicação)_
- **Construção do contexto:** _(formato das evidências, IDs para citação)_
- **Geração da resposta:** _(prompt, instrução de citar evidências)_

### Perguntas sem evidências suficientes

Descrever como o sistema detecta e responde quando não há avaliações relevantes, quando as evidências são insuficientes ou
quando a pergunta está fora do escopo (ex.: limiar mínimo de similaridade + instrução explícita no prompt).

### Desafio adicional: metadados (opcional)

Descrever os metadados usados (nota, período, pedido, entrega, categoria) e como contribuem para a recuperação.

## Instalação e execução

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher as chaves
```

1. Baixe o dataset no [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data) e extraia os CSVs em `data/raw/`.
2. Construa a base de conhecimento:
   ```bash
   python scripts/build_index.py
   ```
3. Rode a interface:
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Exemplos de perguntas e respostas

Ver [docs/exemplos.md](docs/exemplos.md).

## Principais decisões técnicas e desafios

## Vídeo de apresentação

> TODO: link do vídeo (até 7 minutos).
