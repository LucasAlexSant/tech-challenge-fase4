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
avaliações textuais. A nota (1 a 5) mostra o nível de satisfação, mas não o motivo; ler os comentários manualmente não escala.
A solução transforma esses comentários em uma base de conhecimento consultável, permitindo perguntas como:

- Quais são os principais problemas relatados pelos clientes?
- Quais reclamações relacionadas à entrega aparecem com maior frequência?
- O que os clientes mais elogiam em suas experiências de compra?
- Existem padrões recorrentes nas avaliações relacionadas à qualidade dos produtos?

Cada resposta cita as avaliações que a sustentam, e o sistema declara quando não há evidências suficientes.

## Arquitetura

```mermaid
flowchart TB
    subgraph offline["Construção da base (offline, scripts/build_index.py)"]
        A[CSVs Olist<br/>data/raw] --> B[data_prep.py<br/>seleção, limpeza, metadados]
        B --> C[embeddings.py<br/>multilingual-e5-small<br/>prefixo passage:]
        C --> D[(ChromaDB<br/>data/index<br/>vetor + texto + metadados)]
    end

    subgraph online["Consulta (online, app/streamlit_app.py)"]
        Q[Pergunta + filtros] --> T[retrieval.py<br/>normalização + prefixo query:]
        T --> R[Busca por cosseno<br/>filtros por metadados]
        D --> R
        R --> S[Seleção<br/>deduplicação, top 10, limiar 0,85]
        S -->|nenhuma acima do limiar| N[Sem evidências<br/>LLM não é chamado]
        S --> X[generation.py<br/>contexto R1..R10 + metadados]
        X --> L[LLM Gemini 2.5 Flash<br/>API compatível com OpenAI]
        L --> O[Resposta com citações<br/>+ evidências na interface]
    end
```

| Etapa do fluxo | Implementação |
|---|---|
| Processamento da pergunta | `retrieval.transform_query` |
| Representação vetorial | `embeddings.embed_query` / `embed_documents` |
| Recuperação das avaliações | `retrieval.retrieve` (ChromaDB) |
| Construção do contexto | `generation.build_context` |
| Geração da resposta | `generation.generate_answer` |
| Orquestração e tratamento de falta de evidências | `pipeline.answer` |

## Estrutura do repositório

```
.
├── app/streamlit_app.py    # Interface: pergunta, filtros, resposta e evidências
├── data/
│   ├── raw/                # CSVs do Kaggle (não versionados)
│   ├── processed/          # Documentos preparados (não versionados)
│   └── index/              # Banco vetorial persistido (não versionado)
├── docs/
│   ├── exemplos.md         # Perguntas e respostas reais com evidências
│   └── roteiro_video.md    # Roteiro do vídeo de apresentação
├── notebooks/              # Análise exploratória e experimentos
├── scripts/build_index.py  # Preparação dos dados + indexação
├── src/voc_rag/
│   ├── config.py           # Caminhos, modelos e parâmetros (top-k, limiar)
│   ├── data_prep.py        # Seleção, limpeza e organização dos documentos
│   ├── embeddings.py       # Embeddings com e5
│   ├── indexing.py         # Indexação no ChromaDB
│   ├── retrieval.py        # Transformação da pergunta, filtros e busca
│   ├── generation.py       # Contexto, prompt e chamada ao LLM
│   └── pipeline.py         # Orquestração do fluxo RAG
└── tests/                  # Testes automatizados (pytest)
```

## Tecnologias e bibliotecas

| Componente | Escolha | Justificativa |
|------------|---------|---------------|
| Linguagem | Python 3.11+ | Ecossistema padrão para dados e IA |
| Manipulação de dados | pandas + pyarrow | Junção das tabelas da Olist e persistência dos documentos em Parquet |
| Embeddings | `intfloat/multilingual-e5-small` (sentence-transformers) | Treinado para busca (query → documento), multilíngue com bom desempenho em português, gratuito, roda localmente em CPU e garante reprodutibilidade sem chave de API |
| Banco vetorial | ChromaDB (persistido em `data/index/`) | Volume (~41 mil avaliações) não justifica servidor; armazena vetor, texto e metadados juntos; filtro nativo por metadados (nota, entrega, categoria); roda localmente, facilitando a reprodução |
| LLM | Gemini 2.5 Flash (camada gratuita) via API compatível com OpenAI (`openai` SDK) | Sem custo para o desenvolvimento; a interface compatível com OpenAI permite trocar de provedor (OpenAI, Ollama, Groq etc.) apenas alterando `LLM_BASE_URL`, `LLM_API_KEY` e `LLM_MODEL` no `.env` |
| Interface | Streamlit | Interface web em Python puro, suficiente para perguntas, filtros e exibição das evidências |
| Testes | pytest | Testes da preparação dos dados, dos filtros e do tratamento de falta de evidências |

## Preparação da base de conhecimento

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
- **Rastreabilidade:** a interface lista as evidências com o mesmo identificador citado na resposta, junto com nota,
  situação da entrega, categoria, similaridade, `review_id` e pedido.

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

### Desafio adicional: metadados

A interface oferece filtros por **nota**, **categoria do produto** e **situação da entrega** (`retrieval.build_filters`),
aplicados pelo ChromaDB **antes** da busca semântica. Os demais metadados (datas, dias de atraso, status do pedido)
acompanham cada evidência e entram no contexto enviado ao LLM.

Como os metadados melhoram a recuperação:

- **Precisão:** a similaridade semântica captura o assunto, mas não o sentimento. Uma busca por "problemas com o produto"
  também traz avaliações neutras ou positivas que mencionam o tema; com `nota ≤ 2`, o espaço de busca fica restrito a
  clientes insatisfeitos de forma determinística, sem depender do texto.
- **Análises segmentadas:** perguntas como "o que os clientes elogiam em móveis e decoração?" ou "quais temas aparecem
  em entregas atrasadas?" passam a ser respondidas com evidências apenas do segmento pedido.
- **Contexto para o LLM:** nota, entrega e categoria junto a cada comentário permitem que a resposta relacione o relato ao
  pedido (ex.: distinguir reclamação de atraso real de ansiedade antes do prazo).

A situação da entrega (`no_prazo`, `atrasado`, `nao_entregue`) é derivada comparando a data de entrega real com a estimada,
e não existe pronta na base.

## Instalação e execução

Pré-requisitos: Python 3.11+ e uma chave de API do Gemini ([Google AI Studio](https://aistudio.google.com/apikey),
camada gratuita) ou de outro provedor compatível com a API da OpenAI.

```bash
git clone https://github.com/LucasAlexSant/tech-challenge-fase4.git
cd tech-challenge-fase4

python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # Windows: copy .env.example .env — depois preencha LLM_API_KEY
```

1. Baixe o dataset e extraia os CSVs em `data/raw/`, pelo [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data)
   ou pela linha de comando:
   ```bash
   curl -L -o olist.zip https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce
   unzip olist.zip -d data/raw   # Windows: Expand-Archive olist.zip data/raw
   ```
2. Construa a base de conhecimento (cerca de 4 minutos em CPU; o modelo e5 é baixado na primeira execução):
   ```bash
   python scripts/build_index.py
   ```
3. Rode a interface e acesse http://localhost:8501:
   ```bash
   streamlit run app/streamlit_app.py
   ```
4. Rode os testes:
   ```bash
   pytest
   ```

Parâmetros ajustáveis em `src/voc_rag/config.py`: `TOP_K` (avaliações por pergunta) e `MIN_SIMILARITY` (limiar).

## Exemplos de perguntas e respostas

Respostas reais da solução, com as evidências recuperadas, estão em [docs/exemplos.md](docs/exemplos.md). Resumo:

| Pergunta | Filtros | Resultado |
|---|---|---|
| Quais são os principais problemas relatados pelos clientes? | — | Entrega (atraso, não recebimento, entrega parcial) e falta de resposta do atendimento |
| O que os clientes relatam sobre problemas relacionados à entrega? | — | Não entrega, entrega incompleta, falta de informação no rastreamento, status divergente |
| Quais aspectos da experiência de compra são mais elogiados? | — | Entrega antes do prazo, atendimento e confiança na loja |
| Quais são os principais problemas nas avaliações com nota baixa? | nota ≤ 2 | Atraso/não recebimento, itens faltando, dificuldade de contato |
| O que os clientes mais elogiam nos produtos? | nota ≥ 4, `moveis_decoracao` | Qualidade e produtos acima das expectativas |
| Qual a capital da França? | — | Barrada pelo limiar; o LLM não é chamado |
| Qual a previsão do tempo para amanhã? | — | O LLM declara que não há evidências na base |

## Principais decisões técnicas e desafios

- **1 avaliação = 1 documento, sem chunking:** os comentários têm no máximo 208 caracteres. Dividir não traria ganho e
  quebraria a rastreabilidade (cada evidência corresponde a uma avaliação identificável).
- **Descartar avaliações sem texto:** 57% da base tem apenas a nota. Elas não têm conteúdo para recuperar e, se
  indexadas com texto vazio, poluiriam a busca.
- **Modelos locais para embeddings, LLM via API:** embeddings precisam ser gerados para toda a base (41 mil textos), então
  um modelo local evita custo e limites de requisição; o LLM é chamado uma vez por pergunta, e a camada gratuita do Gemini
  é suficiente.
- **Desafio: calibrar a detecção de perguntas sem evidência.** O e5 produz similaridades concentradas entre 0,80 e 0,96,
  e as faixas de perguntas dentro e fora do escopo se sobrepõem. Por isso o limiar sozinho não basta, e a solução combina
  limiar (barra o óbvio sem custo) com a instrução do prompt (trata o restante).
- **Desafio: textos repetidos.** Avaliações curtas como "Muito bom" aparecem centenas de vezes e ocupavam várias posições
  do top-k com o mesmo conteúdo. A busca recupera 3× mais candidatos e remove duplicatas antes de montar o contexto.
- **Desafio: palavras da pergunta que não são o assunto.** "Quais padrões podem ser identificados nas *avaliações* de
  clientes insatisfeitos?" recupera textos como "como vou *avaliar* se não recebi?": o termo "avaliações" domina o
  embedding. O filtro `nota ≤ 2` não resolve, porque esses textos também têm nota baixa. Reformular para "Quais os
  motivos de insatisfação dos clientes?" recupera reclamações reais (produto errado, cancelamento, falta de atendimento).
  É a principal motivação para a transformação da pergunta com LLM listada nos próximos passos.
- **Desafio: modelo do Gemini sem resposta.** O alias `gemini-flash-latest` não respondia às requisições; a solução fixa
  `gemini-2.5-flash` e define timeout de 60 s na chamada para não travar a aplicação.
- **Provedor de LLM desacoplado:** o uso da API compatível com OpenAI permite trocar de Gemini para OpenAI, Ollama ou
  Groq apenas pelo `.env`.

### Limitações e próximos passos

- **Avaliação quantitativa:** criar um conjunto de perguntas com avaliações relevantes anotadas para medir a recuperação
  (precision@k) e a fidelidade das respostas, em vez de inspeção manual.
- **Busca híbrida e reranking:** combinar BM25 com a busca vetorial e reordenar com um cross-encoder para melhorar a
  precisão em termos específicos (nomes de produtos, prazos).
- **Transformação da pergunta com LLM:** reescrever perguntas abstratas ("quais os principais problemas?") em termos
  próximos aos das avaliações e classificar o escopo antes da busca.
- **Frequência dos temas:** o top-k mostra exemplos representativos, não contagens. Para "o que aparece com maior
  frequência", uma etapa de agrupamento de temas sobre toda a base complementaria o RAG.
- **Escala:** para milhões de avaliações em produção, um banco vetorial servidor (Qdrant, pgvector) seria mais adequado.

## Vídeo de apresentação

> TODO: link do vídeo (até 7 minutos). Roteiro em [docs/roteiro_video.md](docs/roteiro_video.md).
