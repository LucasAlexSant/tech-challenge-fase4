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

- Fase offline: CSVs → limpeza → embeddings e5-large → ChromaDB.
- Fase online: pergunta → embedding → busca → limiar → contexto com [R1..R10] → Gemini → resposta + evidências.
- Tecnologias e por quê, em uma frase cada: e5 (busca multilíngue, local, gratuito), ChromaDB (simples, filtros
  por metadados), Gemini via API compatível com OpenAI (gratuito e trocável pelo `.env`).

## 3. Preparação da base (1:45 – 2:30)

- 99 mil avaliações → 41.973 documentos: 57% só tinham nota; descartados textos sem conteúdo ("A", "OK").
- Título + comentário em um texto; sem chunking porque o maior comentário tem 208 caracteres.
- Metadados: nota, categoria e situação da entrega **derivada** (data real × estimada).
- Prefixos `passage:` / `query:` exigidos pelo e5.

## 4. Pipeline RAG, recuperação e escolha do modelo (2:30 – 3:45)

- Busca 30 candidatos, remove repetidos ("Muito bom" ×N), mantém 10 acima do limiar.
- Contexto numerado [R1..R10] com metadados; prompt exige citar e proíbe conhecimento externo.
- **Comparação e5-small × e5-large** (tabela do README): com o small, "clientes insatisfeitos" trazia "como vou
  avaliar?" e "principais problemas" trazia avaliação nota 5; o large captura a intenção. Custo: indexação de 3,5 → 31
  min, feita uma vez.
- **Calibração do limiar:** 15 + 15 perguntas mostraram que as faixas se sobrepõem ("Me recomende um filme" 0,889);
  com 0,85 duas perguntas válidas eram recusadas. Limiar 0,80 + LLM como camada principal de recusa.

## 5. Demonstração (3:45 – 5:45)

Com `streamlit run app/streamlit_app.py`. Mostrar as etapas "Buscando avaliações" e "Gerando resposta" e abrir a tabela
de evidências.

1. **"O que os clientes relatam sobre problemas relacionados à entrega?"**: conferir 2 ou 3 [R] citados na tabela.
2. **"Quais aspectos da experiência de compra são mais elogiados?"**: o lado positivo.
3. **"Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?"**: reclamações reais
   (comentar que o e5-small falhava aqui).
4. **Filtro nota ≥ 4 + categoria `moveis_decoracao` + "O que os clientes mais elogiam nos produtos?"**: badges dos
   filtros e evidências só do segmento.
5. **"Quais avaliações sustentam que existem problemas recorrentes com o prazo de entrega?"**: o modelo lista as
   avaliações, mas não confirma a recorrência sem suporte (uma delas diz que foi "a primeira vez").
6. **"Qual a capital da França?"**: "Nenhuma avaliação relevante", "LLM não acionado". Depois **"Me recomende um filme"**:
   passa do limiar (0,889), e o LLM recusa.
7. **Passar o mouse sobre um [R]** para mostrar a avaliação completa no cartão.

## 6. Desafios e decisões (5:45 – 6:30)

- Similaridades do e5 concentradas em faixa alta → calibração do limiar; a primeira (0,85) recusava perguntas válidas.
- e5-small confundia palavras com intenção → comparação e troca para o e5-large.
- LLM generalizava a partir de 10 avaliações ("a maioria") → prompt proíbe quantidades.
- Cota gratuita do Gemini esgotada → troca para o Grok só pelo `.env`, mostrando o provedor desacoplado.
- Próximos passos: avaliação quantitativa, busca híbrida com reranking, agrupamento de temas para frequência.

## Dicas de gravação

- Rodar `build_index.py` antes de gravar (~30 min); na gravação, apenas a interface.
- Se usar o Gemini gratuito, o limite diário é baixo: ensaiar com o Grok ou em outro dia.
- Deixar o navegador com zoom maior para as evidências ficarem legíveis.
