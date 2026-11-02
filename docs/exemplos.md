# Exemplos de perguntas e respostas

Respostas geradas pela solução (`gemini-2.5-flash`, `multilingual-e5-small`, top-k = 10, limiar = 0,85).
Para cada pergunta são exibidas as 5 primeiras evidências recuperadas; a resposta pode citar
as 10 (a interface mostra todas). Os identificadores [R1], [R2]... da resposta correspondem às evidências abaixo.

## Investigação de reclamações

**Pergunta:** Quais são os principais problemas relatados pelos clientes em suas avaliações?

**Filtros:** nenhum

**Resposta:**

Os principais problemas relatados pelos clientes em suas avaliações são:

1.  **Problemas na entrega:**
    *   Atraso na entrega dos produtos [R1], [R7], [R8].
    *   Produto não recebido, mesmo com o status indicando entrega [R2], [R4], [R6], [R9].
    *   Entrega parcial ou divergências na quantidade de produtos entregues [R10].

2.  **Falta de comunicação e dificuldade no atendimento ao cliente:**
    *   Dificuldade em obter respostas ou contato da empresa após tentativas por e-mail, WhatsApp e telefone [R4], [R5], [R7], [R8].
    *   Falta de informações ou satisfação sobre o status do pedido ou problemas [R4], [R8].
    *   Incapacidade de resolver problemas ou obter uma solução para questões pendentes, mesmo após atendimento aberto [R3], [R5], [R7], [R10].
    *   Sistema de reclamação ineficaz [R7].

3.  **Problemas com o produto:**
    *   Falta de manual de instrução [R5].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.882 | 5 | no_prazo | alimentos | Atenciosos,ligam para dar acompanhamento. Bom prazo de validade. Demorou de chegar. Agora é verificar a qualidade do produto. |
| R2 | 0.878 | 1 | atrasado | beleza_saude | Informação\preocupada. Minha avaliação ta sendo esta pq aqui aparece q recebi o produto e ainda não chegou em casa.Por favor, queria saber o q está acontecendo ??? Atenciosamente, Juliana |
| R3 | 0.877 | 1 | nao_entregue | cama_mesa_banho | Estou há mais de 01 mês esperando a solução do problema conforme atendimento aberto . Quanto tempo mais terei que aguardar ? Tenho que buscar ajuda no procon ou juizados de pequenas causas ?? |
| R4 | 0.874 | 1 | nao_entregue | desconhecida | Total falta de respeito com o consumidor. Além de não realizar a entrega que tinha um prazo enorme, ao longo do período, pedi mais detalhes do status para acompanhar o processo e nunca ligaram. |
| R5 | 0.874 | 3 | no_prazo | moveis_decoracao | Problemas na comunicação. Bom dia. Não veio manual de instrução, estou com dúvidas de como usar. Já enviei email, whatsapp e telefonemas e ninguém responde. Como podemos resolver isso? |

## Investigação de um tema específico

**Pergunta:** O que os clientes relatam sobre problemas relacionados à entrega?

**Filtros:** nenhum

**Resposta:**

Os clientes relatam os seguintes problemas relacionados à entrega:

*   **Não entrega ou entrega incompleta:** Alguns clientes não receberam seus produtos [R2], [R5], [R8], ou receberam apenas parte do pedido, mesmo constando como entregue [R4], [R10].
*   **Falta de comunicação e informações:** Há reclamações sobre a ausência de detalhes sobre problemas na entrega [R1], falta de retorno sobre o status do pedido [R2], [R9], informações conflitantes em e-mails [R6], e falta de informações no rastreamento [R8].
*   **Atrasos e dificuldades na entrega:** Clientes mencionam datas de entrega não cumpridas [R3] e problemas na distribuição [R5].
*   **Discrepância de informações:** E-mails de confirmação de entrega são recebidos, mas o produto não chega [R6], ou o status indica entrega completa quando apenas parte do pedido foi entregue [R4].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.878 | 3 | no_prazo | cama_mesa_banho | Foi falado que houve problemas na entrega mas não falava o que e nem como seria resolvido. Me causou uma preocupação e frustração desnecessária já que o mesmo chegou antes do prazo estipulado. |
| R2 | 0.874 | 1 | nao_entregue | desconhecida | Total falta de respeito com o consumidor. Além de não realizar a entrega que tinha um prazo enorme, ao longo do período, pedi mais detalhes do status para acompanhar o processo e nunca ligaram. |
| R3 | 0.873 | 1 | no_prazo | cool_stuff | Primeiro marcaram uma data e nao cumpriram depois disseram ter dificuldade na entrega quando recebemos pelo menos 50 encomendas por dia |
| R4 | 0.870 | 1 | no_prazo | cool_stuff | Em partes. Sou cliente há anos, porém sempre há divergências e problemas na entrega, consta como produto entregue, porém foi entregue apenas 1 produto, aguardo solução! |
| R5 | 0.869 | 1 | atrasado | utilidades_domesticas | produto nao entregue. recebi um email das lannister informando que haviam problemas na distribuicao, e agora outro perguntando se recebi a compra o que ate o momento nao aconteceu, nao sei o que aconteceu ou a que atribu |

## Busca por experiências positivas

**Pergunta:** Quais aspectos da experiência de compra são mais elogiados pelos clientes?

**Filtros:** nenhum

**Resposta:**

Os aspectos da experiência de compra mais elogiados pelos clientes são:

*   **Agilidade e pontualidade na entrega**, com várias menções de entrega antes do prazo [R1, R2, R6, R7, R8, R10].
*   **Atendimento, serviço e compromisso com o cliente**, incluindo respeito, consideração e atenção [R1, R3, R4, R6, R7, R8].
*   A **experiência de compra geral** também é frequentemente elogiada como satisfatória [R3, R5, R9, R10].
*   A **qualidade do produto** é mencionada em uma avaliação [R2].
*   A **confiança na loja** é destacada em uma avaliação [R4].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.880 | 5 | no_prazo | esporte_lazer | Perfeito! Agilidade e compromisso com o cliente. Recomendo de olhos fechados. Parabéns! |
| R2 | 0.875 | 5 | no_prazo | moveis_escritorio | Elogio. Entrega bem antes do prazo. Produto de excelente qualidade. Recomendo o produto e a loja. |
| R3 | 0.872 | 5 | no_prazo | telefonia | bom serviço. Satisfatória, é a palavra que define minha experiência de compra com essa loja. obrigado pelo atendimento. Pode atuar no mercado com esse nível de compromisso. |
| R4 | 0.871 | 5 | no_prazo | cool_stuff | Lojas ótimas e de confiança. Recomendo sim. Compro a anos e é de confiança. Obrigada pelo atendimentos e a atenção. |
| R5 | 0.871 | 5 | no_prazo | cama_mesa_banho | Excelente. Como sou cliente, minha satisfação só aumenta. Grata a toda equipe. |

## Investigação de insatisfação

**Pergunta:** Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?

**Filtros:** nenhum

**Resposta:**

Os padrões identificados nas avaliações de clientes insatisfeitos são:

1.  **Produto não recebido / Impossibilidade de avaliar**: A maioria dos clientes insatisfeitos relata não ter recebido o produto e, por isso, não consegue avaliá-lo [R1], [R2], [R3], [R4], [R5], [R6], [R8], [R9].
2.  **Atraso na entrega**: Há menções explícitas de atraso na entrega ou de que o produto demorou para chegar [R3], [R4], [R5], [R8].
3.  **Falta de comunicação/resposta**: Um cliente insatisfeito relatou ter enviado um e-mail e não ter obtido resposta sobre o produto não entregue [R5].
4.  **Qualidade do produto**: Um cliente insatisfeito avaliou o produto como de "péssima qualidade" [R10].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.863 | 3 | no_prazo | malas_acessorios | ?? Como vou avaliar se ainda não foi entregue? |
| R2 | 0.863 | 1 | no_prazo | utilidades_domesticas | COMO VOU AVALIAR UM PRODUTO QUE NÃO RECEBI |
| R3 | 0.863 | 1 | atrasado | relogios_presentes | Só posso fazer avaliação depois que receber o meu produto!!! No momento todas as respostas são negativa |
| R4 | 0.860 | 1 | atrasado | telefonia | Nao posso avalia um produto que ainda nao recebi se fosse para avalia eu daria 0 |
| R5 | 0.859 | 1 | atrasado | cama_mesa_banho | Mandei um email até agora não obtive resposta. Meu produto não chegou... |

## Exploração baseada em evidências

**Pergunta:** Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

**Filtros:** nenhum

**Resposta:**

As avaliações que sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega são:

*   **Não cumprimento do prazo:** [R1], [R4], [R6]
*   **Prazo de entrega problemático ou muito longo:** [R2], [R10]
*   **Não recebimento do produto, indicando atraso ou falha na entrega:** [R7], [R9]

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.903 | 1 | atrasado | relogios_presentes | Ñ compriu seu prazo de entrega |
| R2 | 0.903 | 4 | no_prazo | moveis_escritorio | o que mata é o prazo da entrega! |
| R3 | 0.901 | 5 | no_prazo | bebes | O prazo de entrega foi super rápido, mais tive problemas com a portaria para receber. Como posso solicitar nova entregar .. |
| R4 | 0.898 | 4 | no_prazo | eletroportateis | Achei vwue o prazo de entrega nåo foi respeitado. |
| R5 | 0.898 | 1 | no_prazo | ferramentas_jardim | Pedi duas cubas so recebi uma estou aguardando resposta de como posso resolver isso no mais a entrega foi no prazo e a que recebi e de boa qualidade |

## Metadados: avaliações com nota baixa

**Pergunta:** Quais são os principais problemas relatados nas avaliações com nota baixa?

**Filtros:** nota ≤ 2

**Resposta:**

Os principais problemas relatados nas avaliações com nota baixa são:

*   **Não recebimento do produto ou atraso na entrega:** Muitos clientes relatam que o produto não chegou ou está com a entrega muito atrasada [R2], [R4], [R5], [R6], [R8]. Em alguns casos, o sistema informa que o produto foi recebido, mas o cliente ainda não o recebeu [R6].
*   **Recebimento de pedidos incompletos ou com itens faltando:** Há relatos de produtos que vieram faltando unidades ou itens de um pedido [R1], [R3], [R10].
*   **Dificuldade de contato e resolução de problemas:** Clientes enfrentam problemas para entrar em contato com a empresa para resolver questões como atrasos, itens faltantes ou cancelamentos, e não obtêm retorno ou solução [R4], [R5], [R9], [R10].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.870 | 1 | no_prazo | brinquedos | Dei nota baixa pois sao dois pedidos e o outro do aparelho celular veio faltando 1 e até agora não recebi 😡 |
| R2 | 0.868 | 1 | atrasado | moveis_escritorio | - a compra foi efetuada em 30/01 - a emissão da nota fiscal emitida em 05/02 - até 16/03 ainda não recebemos a mercadoria - que avaliação deveríamos dar a isto? - desonestos? ineficientes? etc, et |
| R3 | 0.858 | 1 | no_prazo | bebidas | Como podem emitir uma nota com os dois produtos e só enviarem 1 pedi a troca explicando o.motivo ,mas até agora nada |
| R4 | 0.857 | 1 | atrasado | moveis_escritorio | Produto mais que passou do prazo de entregar, tento resolver o problema com a empresa e não consigo falar com ninguém. Tudo que fazem é me passar para reclamar num sistema que não funciona. |
| R5 | 0.857 | 1 | atrasado | cama_mesa_banho | Mandei um email até agora não obtive resposta. Meu produto não chegou... |

## Metadados: elogios em uma categoria

**Pergunta:** O que os clientes mais elogiam nos produtos?

**Filtros:** nota ≥ 4; categoria = moveis_decoracao

**Resposta:**

Os clientes elogiam a **qualidade** dos produtos [R2], [R8], [R9]. Também mencionam que os produtos são "ótimos" ou "muito bons" [R3], [R4], [R10] e que superaram as expectativas [R8].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.886 | 5 | no_prazo | moveis_decoracao | 10. Cada vez que compro mais fico satisfeita parabéns pela honestidade com seus clientes 👏👏👏👏? |
| R2 | 0.875 | 5 | no_prazo | moveis_decoracao | Produto devidamente recebido. Dentro das expectativas. Produto de ótima qualidade. Recomendo para todos. |
| R3 | 0.873 | 5 | no_prazo | moveis_decoracao | Nota 10. Parabéns pela loja. Ótimo produto, ótimo preço, ótimo prazo de entrega. |
| R4 | 0.872 | 4 | no_prazo | moveis_decoracao | Recomendo a loja e o prod. MUito bom produto. Recomendo. |
| R5 | 0.872 | 5 | no_prazo | moveis_decoracao | Amei os produtos |

## Metadados: entregas insatisfatórias

**Pergunta:** Quais temas aparecem nas avaliações de entregas atrasadas?

**Filtros:** entrega = atrasado

**Resposta:**

Os temas que aparecem nas avaliações de entregas atrasadas são:

*   **Atraso na entrega em si**: A principal queixa é o atraso no recebimento do produto [R1], [R2], [R3], [R4], [R5], [R6], [R7], [R8], [R9], [R10].
*   **Falta de comunicação ou justificativa**: Clientes reclamam de não receber retorno ou contato para justificar o atraso [R5], [R7].
*   **Impacto na avaliação do produto**: O atraso impede o cliente de avaliar o produto comprado [R1], [R4].
*   **Impacto em ocasiões especiais**: O produto não chegou na data esperada para um presente de aniversário [R2].
*   **Causas percebidas ou comunicadas**:
    *   **Correios**: O atraso é atribuído ou especulado como sendo dos Correios [R3], [R4].
    *   **Problemas no transporte**: Menção de "algo durante o transporte" ou "impedimento relatado" [R7], [R10].
*   **Status da entrega**:
    *   **Produto ainda não recebido**: Muitos clientes ainda não receberam a compra apesar do atraso [R1], [R4], [R5], [R6], [R7], [R9], [R10].
    *   **Produto recebido com atraso**: Em um caso, o produto foi entregue, mas com atraso [R8].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.888 | 1 | atrasado | esporte_lazer | como posso avaliar o produto? só posso avaliar o tempo de entrega que por sinal está atrasado. |
| R2 | 0.881 | 1 | atrasado | relogios_presentes | Atraso na entrega. Quero saber quando entregarão o produto? Era presente de aniversário e não chegou na data. |
| R3 | 0.880 | 1 | atrasado | brinquedos | Entrega atrasada sera que é correios em greve? |
| R4 | 0.876 | 4 | atrasado | telefonia | Atraso na entrega. Ainda não tenho como avaliar a compra pois os Correios atrasaram a entrega e ainda não recebi o produto. |
| R5 | 0.875 | 1 | atrasado | utilidades_domesticas | ATRASO ENORME NA ENTREGA. A entrega está muuuuito atrasada e não recebi nenhum retorno a respeito. |

## Fora do escopo (barrada pelo limiar)

**Pergunta:** Qual a capital da França?

**Filtros:** nenhum

**Resposta:**

Não encontrei avaliações suficientes na base para responder a essa pergunta com segurança.

_Nenhuma avaliação acima do limiar de similaridade: o LLM não foi chamado._

## Fora do escopo (recusada pelo LLM)

**Pergunta:** Qual a previsão do tempo para amanhã?

**Filtros:** nenhum

**Resposta:**

Não há evidências suficientes na base de avaliações para responder à pergunta sobre a previsão do tempo para amanhã. As avaliações fornecidas tratam exclusivamente de experiências de entrega de produtos.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.877 | 2 | no_prazo | utilidades_domesticas | previsão de entrega será até 28/07, não posso opinar sobre este serviço prestado pois estamos no dia 03/07 hoje. Não recebi mais feedback do fornecedor até no momento, obrigado! |
| R2 | 0.877 | 1 | atrasado | brinquedos | Estou esperando a agora. O q acham? |
| R3 | 0.875 | 5 | no_prazo | moveis_decoracao | excelente. Pedi em24/07/2018, A previsão era até o dia 24.08.18 e recebi 27.08.18 muito rápido adorei . |
| R4 | 0.873 | 1 | atrasado | automotivo | A PREVISÃO PARA ENTREGA ERA DIA 12/04. HOJE SÃO 17/04 E AINDA NÃO RECEBI E NÃO CONSIGO RASTREAR O PRODUTO. A EMPRESA |
| R5 | 0.872 | 1 | atrasado | informatica_acessorios | quanto tempo mais de espera? |
