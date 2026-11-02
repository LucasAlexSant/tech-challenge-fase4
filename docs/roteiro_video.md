# Roteiro do vídeo (até 7 minutos)

O PDF pede que o vídeo mostre o raciocínio técnico, não só a aplicação funcionando. Tempos sugeridos somam 6:30,
deixando margem.

## 1. Problema de negócio (0:00 – 0:45)

- E-commerce com ~100 mil avaliações; a nota mostra *se* o cliente está satisfeito, mas não *por quê*.
- Os motivos estão nos comentários, e ler milhares manualmente não escala.
- Objetivo: gestor pergunta em linguagem natural e recebe uma resposta **fundamentada em avaliações reais**, com as
  evidências visíveis.

## 2. Arquitetura (0:45 – 1:45)

Mostrar o diagrama do README.

- Fase offline: CSVs → limpeza → embeddings e5 → ChromaDB.
- Fase online: pergunta → embedding → busca → limiar → contexto com [R1..R10] → Gemini → resposta + evidências.
- Tecnologias e por quê, em uma frase cada: e5 (busca multilíngue, local, gratuito), ChromaDB (simples, filtros
  por metadados), Gemini via API compatível com OpenAI (gratuito e trocável pelo `.env`).

## 3. Preparação da base (1:45 – 2:45)

- 99 mil avaliações → 41.973 documentos: 57% só tinham nota; descartados textos sem conteúdo ("A", "OK").
- Título + comentário em um texto; sem chunking porque o maior comentário tem 208 caracteres.
- Metadados: nota, categoria e situação da entrega **derivada** (data real × estimada).
- Prefixos `passage:` / `query:` exigidos pelo e5.

## 4. Pipeline RAG e recuperação (2:45 – 3:45)

- Busca 30 candidatos, remove repetidos ("Muito bom" ×N), mantém 10 acima do limiar.
- Contexto numerado [R1..R10] com metadados; prompt exige citar e proíbe conhecimento externo.
- Calibração do limiar: mostrar a tabela (escopo 0,857–0,96 × fora 0,80–0,877) e explicar as duas camadas.

## 5. Demonstração (3:45 – 5:45)

Com `streamlit run app/streamlit_app.py`:

1. **"O que os clientes relatam sobre problemas relacionados à entrega?"**: abrir 2 ou 3 evidências e mostrar que os
   [R] citados batem com o texto.
2. **"Quais aspectos da experiência de compra são mais elogiados?"**: o lado positivo.
3. **"Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?"**: mostrar que a busca traz
   "como vou avaliar se não recebi?" (o termo "avaliações" domina). Em seguida, **"Quais os motivos de insatisfação dos
   clientes?"** com filtro nota ≤ 2: reclamações reais. Ótimo para explicar uma limitação e o próximo passo.
4. **Categoria `moveis_decoracao` + nota ≥ 4 + "O que os clientes mais elogiam nos produtos?"**.
5. **"Qual a capital da França?"**: barrada pelo limiar, sem evidências.
6. **"Qual a previsão do tempo para amanhã?"**: passa do limiar ("previsão de entrega"), mas o LLM recusa.

## 6. Desafios e decisões (5:45 – 6:30)

- Similaridades do e5 concentradas em faixa alta → limiar + prompt.
- Termos da pergunta que não são o assunto ("avaliações") distorcem a busca → reformulação da pergunta; filtros por
  metadados para restringir sentimento/segmento.
- Alias `gemini-flash-latest` travando → modelo fixo e timeout.
- Próximos passos: avaliação quantitativa, busca híbrida com reranking, agrupamento de temas para frequência.

## Dicas de gravação

- Rodar `build_index.py` antes de gravar; na gravação, apenas a interface.
- A camada gratuita do Gemini tem limite diário por modelo: testar as perguntas antes, mas sem repetir demais.
- Deixar o navegador com zoom maior para as evidências ficarem legíveis.
