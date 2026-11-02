# Exemplos de perguntas e respostas

Respostas geradas pela solução (`grok-4.20-0309-non-reasoning`, `multilingual-e5-large`, top-k = 10, limiar = 0.8).
Para cada pergunta são exibidas as 5 primeiras evidências recuperadas; a resposta pode citar
as 10 (a interface mostra todas). Os identificadores [R1], [R2]... da resposta correspondem às evidências abaixo.

## Investigação de reclamações

**Pergunta:** Quais são os principais problemas relatados pelos clientes em suas avaliações?

**Filtros:** nenhum

**Resposta:**

Os principais problemas relatados nas avaliações são:

- **Atraso na entrega ou não entrega do produto**: mencionado em [R1], [R2], [R3], [R4], [R6], [R7], [R8] e [R10].
- **Falta de respeito, consideração ou compromisso com o cliente**: citado em [R1], [R2], [R3], [R4], [R8] e [R10].
- **Dificuldade de rastreio ou falta de satisfação/comunicação**: apontado em [R2], [R6] e [R8].
- **Produto errado ou incompleto**: relatado em [R5] e [R7].
- **Problemas de qualidade em alguns produtos**: mencionado em [R9].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.869 | 1 | atrasado | esporte_lazer | Entrega do produto. Falta de atenção e respeito com cliente |
| R2 | 0.858 | 1 | atrasado | moveis_decoracao | Atraso na entrega sem dar satisfação ao cliente, que com certeza escolheu o produto com cuidado e com as melhores expectativas. Falta de consideração. |
| R3 | 0.858 | 1 | nao_entregue | consoles_games | Não entrega do produto. Falta de respeito com o cliente. |
| R4 | 0.857 | 1 | atrasado | ferramentas_jardim | Desrespeito com o cliente. Falta de respeito com o cliente |
| R5 | 0.857 | 1 | no_prazo | relogios_presentes | Produto errado. Mais responsabilidade com os clientes quanto origem do produto,qualidade,certeza de que o produto entregue é de acordo com o pedido |

## Investigação de um tema específico

**Pergunta:** O que os clientes relatam sobre problemas relacionados à entrega?

**Filtros:** nenhum

**Resposta:**

**Os clientes relatam os seguintes problemas relacionados à entrega:**

- Problemas genéricos na entrega sem explicação clara do que ocorreu ou como seria resolvido, gerando preocupação e frustração desnecessária [R1].
- Problemas na entrega atribuídos aos Correios [R2], [R9].
- Falta de atenção e respeito com o cliente na entrega [R3].
- Dificuldades na entrega causadas por transportadoras parceiras que não estão preparadas para localizar endereços [R4].
- Problemas no envio/transcurso do pedido [R5].
- Repetição de problemas com entregas (segunda vez) [R6].
- Desencontro na entrega por o cliente não estar em casa, sem contato prévio por telefone [R7].
- Problemas na entrega combinados com o não envio de todos os produtos comprados [R8].
- Problemas no transporte que geraram grande atraso [R10].

Essas avaliações indicam que os problemas de entrega envolvem tanto questões logísticas (transportadoras, Correios, desencontros, atrasos) quanto falhas de comunicação e respeito ao cliente.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.877 | 3 | no_prazo | cama_mesa_banho | Foi falado que houve problemas na entrega mas não falava o que e nem como seria resolvido. Me causou uma preocupação e frustração desnecessária já que o mesmo chegou antes do prazo estipulado. |
| R2 | 0.876 | 5 | no_prazo | esporte_lazer | So houve problemas na entrega, mas foi por causa dos Correios. Ainda sim foi entregue no prazo |
| R3 | 0.874 | 1 | atrasado | esporte_lazer | Entrega do produto. Falta de atenção e respeito com cliente |
| R4 | 0.872 | 4 | no_prazo | moveis_decoracao | SEMPRE COMPREI COM VCS, E NUNCA TINHA DADO PROBLEMA NA DIFICULDADES DA ENTREGA.. ALGUNS PARCEIROS SEUS TRABALHAM COM TRANSPORTADORAS QUE NAO ESTÃO PREPARADAS PARA ENTREGAR E ACHAR ENDERÇOS PARA ENTRE |
| R5 | 0.872 | 3 | no_prazo | esporte_lazer | o envio apresentou problema no transcurso do pedido. Contudo, o produto foi entregue dentro do longo prazo dado. |

## Busca por experiências positivas

**Pergunta:** Quais aspectos da experiência de compra são mais elogiados pelos clientes?

**Filtros:** nenhum

**Resposta:**

Os aspectos mais elogiados nas avaliações são:

- **Entrega rápida ou antes do prazo**: mencionada em [R4], [R6], [R8], [R9] e [R10].
- **Qualidade do produto e conformidade com o anúncio**: citada em [R1], [R3], [R5] e [R6].
- **Facilidade e rapidez no processo de compra**: destacada em [R6], [R7] e [R10].
- **Atendimento, comunicação e respeito ao cliente**: presente em [R1], [R2], [R3] e [R7].
- **Bom preço e ausência de abuso no valor**: apontada em [R4] e [R8].
- **Embalagem segura e proteção do produto**: referida em [R4] e [R9].

Essas avaliações indicam os temas recorrentes de satisfação na experiência de compra.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.860 | 5 | no_prazo | utilidades_domesticas | Excelente 👍🏽. Respeito ao cliente, qualidade, satisfação. Cliente Feliz!!! |
| R2 | 0.859 | 5 | no_prazo | pcs | Comunicação e respeito com o consumidor. É raro,comprar aqui sempre |
| R3 | 0.855 | 5 | no_prazo | relogios_presentes | Vendedor e produto. Vendedor pontual e o produto satisfez minha expectativa. |
| R4 | 0.855 | 5 | no_prazo | telefonia | Preço adequado ao produto. Entrega do produto feita em um prazo menor que o estabelecido no momento da compra. Chegou bem embalado e bem protegido. |
| R5 | 0.854 | 4 | no_prazo | esporte_lazer | Satisfação da compra. Produto recebido de acordo com o anuncio. |

## Investigação de insatisfação

**Pergunta:** Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?

**Filtros:** nenhum

**Resposta:**

**Padrões identificados nas avaliações de clientes insatisfeitos:**

- **Falta de respeito, descaso ou desatenção com o cliente**: mencionado explicitamente em [R1], [R3], [R4], [R5] e [R10].
- **Problemas com a entrega** (atraso, não entrega ou entrega incompleta): relatados em [R1], [R3], [R4], [R5], [R6], [R8] e [R10].
- **Insatisfação com a qualidade ou descrição do produto**: presente em [R2] (qualidade), [R9] (produto com riscos e descrição que não condiz com a realidade) e [R6] (produto incompleto).
- **Nota 1 (insatisfação extrema)**: predomina nas avaliações que citam os problemas acima, aparecendo em [R1], [R2], [R3], [R4], [R5], [R6], [R8], [R9] e [R10].

Essas avaliações indicam os padrões mencionados, mas não medem sua frequência na base completa de avaliações.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.852 | 1 | atrasado | ferramentas_jardim | Desrespeito com o cliente. Falta de respeito com o cliente |
| R2 | 0.849 | 1 | no_prazo | relogios_presentes | Insatisfação. Não estou satisfeita com a qualidade do produto |
| R3 | 0.848 | 1 | atrasado | esporte_lazer | Entrega do produto. Falta de atenção e respeito com cliente |
| R4 | 0.848 | 1 | nao_entregue | consoles_games | Não entrega do produto. Falta de respeito com o cliente. |
| R5 | 0.848 | 1 | nao_entregue | desconhecida | Produto não entregue. Produto não entregue e sem dar satisfação ao cliente. |

## Exploração baseada em evidências

**Pergunta:** Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

**Filtros:** nenhum

**Resposta:**

**Não há evidências suficientes na base para sustentar a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega.**

As avaliações que mencionam problemas com prazo ou entrega são:

- [R1]: menciona que “Demorou de entregar” apesar de ter sido entregue no prazo.
- [R3]: relata problema no envio, mas o produto foi entregue “dentro do longo prazo”.
- [R5]: produto não entregue no prazo e falta de satisfação do fornecedor.
- [R6]: produto não entregue no prazo e dificuldade de rastreio.
- [R7]: relata um grande atraso por problema no transporte, mas afirma que “foi a primeira vez que ocorreu” e que “os produtos sempre são entregues antes do prazo”.
- [R8]: recebeu o produto no prazo, mas recebeu e-mail apontando problema na entrega.
- [R10]: solicita melhorias no prazo de entrega.

Essas avaliações indicam relatos individuais de problemas ou insatisfação com o prazo, mas não sustentam a conclusão de recorrência, especialmente porque [R7] reforça explicitamente que o atraso foi um caso isolado.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.859 | 2 | no_prazo | cool_stuff | Demorou de entregar geralmente chega bem antes do prazo teve algo que atrapalhou a entrega! |
| R2 | 0.858 | 5 | no_prazo | cool_stuff | Pontualidade. Entrega rápida. |
| R3 | 0.857 | 3 | no_prazo | esporte_lazer | o envio apresentou problema no transcurso do pedido. Contudo, o produto foi entregue dentro do longo prazo dado. |
| R4 | 0.857 | 5 | no_prazo | esporte_lazer | So houve problemas na entrega, mas foi por causa dos Correios. Ainda sim foi entregue no prazo |
| R5 | 0.857 | 1 | atrasado | moveis_decoracao | Produto comprado e não entregue no prazo. O fornecedor não deu satisfação a respeito do atraso. |

## Metadados: avaliações com nota baixa

**Pergunta:** Quais são os principais problemas relatados nas avaliações com nota baixa?

**Filtros:** nota ≤ 2

**Resposta:**

Os principais problemas relatados nas avaliações com nota baixa (1 ou 2) são:

- **Problemas de entrega**: atraso na entrega, produto não entregue ou não entregue no prazo [R1], [R4], [R5], [R6], [R8], [R9], [R10].
- **Falta de comunicação e respeito com o cliente**: ausência de satisfação, posicionamento ou consideração por parte do vendedor/fornecedor [R1], [R5], [R6], [R8], [R9], [R10].
- **Qualidade ruim do produto**: menções diretas à baixa qualidade ou péssima qualidade [R2], [R7].
- **Problemas com nota fiscal**: falta de emissão de NF ou emissão com valor muito inferior ao pago [R3].

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.850 | 1 | atrasado | esporte_lazer | Entrega do produto. Falta de atenção e respeito com cliente |
| R2 | 0.844 | 1 | no_prazo | automotivo | Avaliação. Loja recomendada. Produto de péssima qualidade. |
| R3 | 0.840 | 2 | no_prazo | beleza_saude | FALTA NF. NF COM VALOR EXTREMAMENTE INFERIOR AO VALOR PAGO |
| R4 | 0.840 | 1 | atrasado | moveis_sala | Produto nao entregue no prazo. Dificuldade de rastreio |
| R5 | 0.839 | 1 | nao_entregue | consoles_games | Não entrega do produto. Falta de respeito com o cliente. |

## Metadados: elogios em uma categoria

**Pergunta:** O que os clientes mais elogiam nos produtos?

**Filtros:** nota ≥ 4; categoria = moveis_decoracao

**Resposta:**

**Os clientes mais elogiam a qualidade e o acabamento dos produtos.**

As avaliações que sustentam isso são:

- [R4]: “Produtos conforme descrição do anúncio. Qualidade satisfatória.”
- [R6]: “Produto superou as expectativas. De ótima qualidade é muito bem acabado.”
- [R7]: “O produto é bem bonito e de boa qualidade.”
- [R10]: “Ótimo perfeito gostei do produto ótimo qualidade.”

Outros elogios recorrentes incluem o **design/beleza** dos itens, mencionados em [R3] (“Amei os produtos”), [R7] (“bem bonito”), [R9] (“Lindos produtos”) e [R1] (satisfação geral com a honestidade da loja). 

Não há menções negativas ou críticas aos produtos nas avaliações fornecidas.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.848 | 5 | no_prazo | moveis_decoracao | 10. Cada vez que compro mais fico satisfeita parabéns pela honestidade com seus clientes 👏👏👏👏? |
| R2 | 0.846 | 4 | no_prazo | moveis_decoracao | GOSTEI DO PRODUTO |
| R3 | 0.844 | 5 | no_prazo | moveis_decoracao | Amei os produtos |
| R4 | 0.844 | 4 | no_prazo | moveis_decoracao | Produtos conforme descrição do anúncio. Qualidade satisfatória. |
| R5 | 0.840 | 4 | no_prazo | moveis_decoracao | Entrega. Bom produto e entregue no prazo |

## Metadados: entregas insatisfatórias

**Pergunta:** Quais temas aparecem nas avaliações de entregas atrasadas?

**Filtros:** entrega = atrasado

**Resposta:**

**Temas que aparecem nas avaliações de entregas atrasadas:**

- **Atraso na entrega sem justificativa ou comunicação do vendedor/fornecedor**: mencionado em [R1], [R3], [R4], [R6], [R7] e [R8].
- **Falta de satisfação ou esclarecimento ao cliente sobre o atraso**: mencionado em [R3], [R4], [R6] e [R8].
- **Frustração por ter escolhido o produto com expectativa e não receber no prazo**: mencionado em [R3] e [R8].
- **Impacto negativo por ser um presente que não chegou na data esperada**: mencionado em [R8].
- **Dificuldade ou impossibilidade de avaliar o produto em si por causa do atraso**: mencionado em [R2].
- **Recebimento do produto correto, porém com atraso significativo**: mencionado em [R10].
- **Sensação geral de que receber com atraso é ruim**: mencionado em [R9].

Não há menções a outros temas além do atraso na entrega nas avaliações fornecidas.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.855 | 1 | atrasado | utilidades_domesticas | Produto atrasado. O produto não foi recebido no prazo sem nenhuma justificativa explicando o motivo do atraso |
| R2 | 0.853 | 1 | atrasado | esporte_lazer | como posso avaliar o produto? só posso avaliar o tempo de entrega que por sinal está atrasado. |
| R3 | 0.852 | 1 | atrasado | moveis_decoracao | Atraso na entrega sem dar satisfação ao cliente, que com certeza escolheu o produto com cuidado e com as melhores expectativas. Falta de consideração. |
| R4 | 0.851 | 1 | atrasado | moveis_decoracao | Produto comprado e não entregue no prazo. O fornecedor não deu satisfação a respeito do atraso. |
| R5 | 0.849 | 2 | atrasado | desconhecida | Demora na entrega. Demora na entrega |

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

Não há evidências suficientes na base de avaliações para responder à pergunta, pois nenhuma delas trata de previsão do tempo ou temas relacionados.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.834 | 3 | no_prazo | moveis_decoracao | Não recebi meu pedido, como devo proceder para uma nova postagem ? Grata, |
| R2 | 0.833 | 1 | no_prazo | cama_mesa_banho | ? Ainda não recebi |
| R3 | 0.833 | 3 | no_prazo | fashion_bolsas_e_acessorios | Não posso avaliar ainda. Meu pedido veio errado. No aguardo da correção. |
| R4 | 0.833 | 2 | atrasado | perfumaria | Não posso dizer ainda. Não recebi o produto ainda |
| R5 | 0.832 | 5 | no_prazo | cama_mesa_banho | Como no anunciado. Belíssima. |

## Fora do escopo com similaridade alta (recusada pelo LLM)

**Pergunta:** Me recomende um filme

**Filtros:** nenhum

**Resposta:**

Não há evidências suficientes na base para responder.

**Evidências recuperadas:**

| ID | Similaridade | Nota | Entrega | Categoria | Avaliação |
|---|---|---|---|---|---|
| R1 | 0.889 | 5 | no_prazo | cama_mesa_banho | Recomendo |
