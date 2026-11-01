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
| Embeddings | `intfloat/multilingual-e5-small` (sentence-transformers) | Treinado para busca (query → documento), multilíngue com bom desempenho em português, gratuito, roda localmente em CPU e garante reprodutibilidade sem chave de API |
| Banco vetorial | ChromaDB (persistido em `data/index/`) | Volume (~41 mil avaliações) não justifica servidor; armazena vetor, texto e metadados juntos; filtro nativo por metadados (nota, data, categoria); roda localmente, facilitando a reprodução |
| LLM | Gemini Flash (camada gratuita) via API compatível com OpenAI (`openai` SDK) | Sem custo para o desenvolvimento; a interface compatível com OpenAI permite trocar de provedor (OpenAI, Ollama, Groq etc.) apenas alterando `LLM_BASE_URL`, `LLM_API_KEY` e `LLM_MODEL` no `.env` |
| Interface | Streamlit | |

## Preparação da base de conhecimento

Descrever e justificar cada decisão:

Implementado em `src/voc_rag/data_prep.py`, `embeddings.py` e `indexing.py`; executado por `scripts/build_index.py`.

- **Seleção dos dados:** a base textual vem de `olist_order_reviews_dataset.csv` (99.224 avaliações). Ela é enriquecida com
  `olist_orders_dataset.csv` (datas de compra e entrega), `olist_order_items_dataset.csv` + `olist_products_dataset.csv`
  (categoria do produto) e `product_category_name_translation.csv`. Clientes, vendedores, pagamentos e geolocalização não
  contribuem para as perguntas do desafio e foram descartados.
- **Limpeza e preparação dos textos:** título e comentário são unidos em um único texto (o título costuma resumir a
  avaliação). Quebras de linha (`\r\n`) e espaços repetidos são normalizados. Acentos e caixa são preservados, pois o e5
  é treinado com texto natural.
- **Tratamento de valores ausentes:** 57% das avaliações têm apenas a nota, sem texto, e são descartadas porque não
  contribuem com conteúdo para o RAG. Textos com menos de 3 letras ("A", "10", "OK") também são descartados. Metadados
  ausentes recebem um valor explícito (categoria `desconhecida`, entrega `nao_entregue`) ou são omitidos (dias de atraso
  de pedidos não entregues).
- **Organização dos documentos:** 1 documento = 1 avaliação, resultando em **41.973 documentos**. Os comentários são
  curtos (mediana de 53 caracteres, máximo de 208), então não há chunking. O mesmo `review_id` aparece em mais de um
  pedido com o mesmo texto e é deduplicado. Metadados por documento: `review_score`, `review_date`, `purchase_month`,
  `order_status`, `delivery_status` (`no_prazo` / `atrasado` / `nao_entregue`), `delivery_delay_days` e
  `product_category` (do primeiro item do pedido; cerca de 3% dos pedidos têm mais de um produto).
- **Criação dos embeddings:** `intfloat/multilingual-e5-small`, com o prefixo `passage: ` nos documentos e `query: ` nas
  perguntas, conforme o treinamento do modelo. Os vetores são normalizados. A indexação completa leva cerca de 4 minutos em CPU.
- **Armazenamento e indexação:** ChromaDB persistido em `data/index/`, com similaridade de cosseno (HNSW). Cada registro
  guarda o vetor, o texto e os metadados, permitindo filtros como `review_score <= 2` ou uma categoria específica.
  O índice é recriado a cada execução de `build_index.py`.

## Estratégia do pipeline RAG

Implementado em `src/voc_rag/retrieval.py`, `generation.py` e `pipeline.py`.

- **Transformação da pergunta:** normalização de espaços e prefixo `query: ` exigido pelo e5.
- **Recuperação semântica:** busca por similaridade de cosseno no ChromaDB, com filtros opcionais por metadados.
  São buscados 30 candidatos (3× o top-k) para compensar textos repetidos.
- **Seleção dos conteúdos mais relevantes:** remoção de textos idênticos (ex.: vários "Muito bom"), que ocupariam
  espaço no contexto sem trazer informação nova; ficam as **10** avaliações mais similares acima do limiar.
- **Construção do contexto:** cada avaliação recebe um identificador (`[R1]`, `[R2]`...) e vai acompanhada de nota,
  situação da entrega e categoria, para que o modelo relacione o comentário ao contexto do pedido.
- **Geração da resposta:** o prompt de sistema exige resposta baseada exclusivamente nas avaliações, com citação dos
  identificadores em cada afirmação. Temperatura 0 para respostas estáveis e menos criativas.

### Perguntas sem evidências suficientes

São usadas duas camadas, porque a similaridade sozinha não separa bem as perguntas:

1. **Limiar de similaridade (0,85):** se nenhuma avaliação passa do limiar, o sistema responde que não há evidências
   e **não chama o LLM**. Calibração: perguntas do escopo tiveram similaridade entre 0,857 e 0,96, e perguntas sem relação
   entre 0,80 e 0,877. O e5 concentra os scores em faixa alta, e uma pergunta como "previsão do tempo" casa com "previsão
   de entrega", por isso as faixas se sobrepõem.
2. **Instrução no prompt:** para perguntas que passam do limiar sem ter relação real, o modelo é instruído a declarar
   que as avaliações não respondem à pergunta, em vez de usar conhecimento externo.

| Pergunta | Similaridade (top 1) | Resultado |
|---|---|---|
| Qual a capital da França? | 0,816 | Barrada pelo limiar, sem chamar o LLM |
| Qual a previsão do tempo para amanhã? | 0,877 | Passa do limiar; o LLM declara que não há evidências |

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
