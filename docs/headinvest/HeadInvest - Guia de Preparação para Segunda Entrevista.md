# HeadInvest — Guia de Preparação para Segunda Entrevista

> Material para um **desenvolvedor backend Python** entender o negócio da HeadInvest, seus produtos, seu mercado e onde a tecnologia se encaixa.
> Foco: **negócio → processo → tecnologia**. Não é um curso de investimentos.
> Tempo de leitura: 30–60 min.

**Convenções neste guia:**
- ✅ = fato confirmado no site oficial / fontes públicas.
- 🔵 = inferência plausível de mercado (não afirmar como fato na entrevista).

---

## 0. Resumo em 60 segundos (o "elevator pitch" para você)

A HeadInvest é uma **gestora de recursos (asset management) independente** focada em **crédito estruturado**. Em termos de engenharia: pense nela como uma empresa que **origina, empacota, precifica e monitora "dívidas"** (recebíveis) de terceiros e as transforma em **fundos** que investidores compram.

- ✅ Empresa nova (constituída em **nov/2024**), mas montada por sócios com **+30 anos somados** de mercado de capitais.
- ✅ Atua em **sinergia com a BSI Capital**: a BSI **estrutura e origina** as operações; a HeadInvest **gere** os fundos.
- ✅ Sede em São Paulo (Av. das Nações Unidas, 14401 — região da Berrini/Chucri Zaidan).
- ✅ Produtos centrais: **FIDCs** (fundos de recebíveis) e **crédito imobiliário** (CRIs).

O gancho de tecnologia mais importante: **crédito estruturado é, no fundo, um problema de dados**. Originar, analisar, precificar e monitorar milhares de recebíveis pulverizados exige software — não dá para fazer no Excel em escala. É exatamente aí que um backend Python entra.

---

## 1. Quem é a HeadInvest

**O que faz:** é uma **gestora de fundos de investimento** especializada em **crédito** (dívida privada), com ênfase em **crédito estruturado** e **crédito imobiliário**.

**Como ganha dinheiro (o modelo de receita de uma gestora):**
- ✅ **Taxa de administração/gestão**: um % ao ano sobre o patrimônio sob gestão (AUM — *Assets Under Management*). É a receita recorrente principal.
- 🔵 **Taxa de performance**: um % sobre o retorno que exceder um benchmark (ex.: CDI). Comum em fundos de crédito.
- 🔵 Ganhos ligados à **estruturação/originação** via ecossistema BSI Capital.

> Para um dev: a receita escala com o **AUM**. Quanto mais dinheiro sob gestão e mais operações ativas, mais a operação precisa de **automação e controle** — porque a equipe não cresce na mesma velocidade que o volume de dados.

**Quem são os clientes:**
- ✅ **Investidores institucionais** e **fundos exclusivos**.
- 🔵 Investidores qualificados/profissionais (crédito estruturado costuma ser restrito a esse público por regulação da CVM).

**Como se posiciona:** gestora **independente**, técnica, com discurso de **governança, disciplina e transparência**. O diferencial declarado é a **análise profunda de crédito** e o **lastro pulverizado** (diversificar o risco em muitos devedores pequenos em vez de poucos grandes).

**Diferenciais (✅ do site):**
- Curadoria técnica das operações e mitigação de risco.
- Expertise em crédito imobiliário (CRIs, CRAs, ativos reais).
- Sinergia com a BSI Capital (estruturação + gestão no mesmo ecossistema).

---

## 2. Como funciona o negócio de uma gestora (o fluxo)

Pense no fluxo como um **pipeline de dados** com etapas bem definidas (✅ o site descreve 4 etapas):

```
Originação → Análise/Modelagem → Implementação/Estruturação → Monitoramento
  (filtro)      (precificação)        (contratos)               (covenants)
```

1. **Originação e filtro** — chegam oportunidades de crédito (ex.: uma empresa quer antecipar recebíveis). Faz-se um filtro inicial da estrutura.
2. **Análise e modelagem** — avaliação econômica: simulação de cenários, **TIR** (taxa interna de retorno), **VPL** (valor presente líquido), análise de sensibilidade, avaliação de garantias.
3. **Implementação** — negociação de termos, instrumentos contratuais, mecanismos de mitigação de risco. É aqui que a operação vira um ativo dentro de um fundo.
4. **Monitoramento** — acompanhamento contínuo de fluxos de pagamento, indicadores de risco e **covenants** (cláusulas que o devedor tem de cumprir).

**Como chegam clientes/operações:**
- **Lado do ativo (operações):** originação própria + parceria com a **BSI Capital**, que traz e estrutura as operações de crédito.
- **Lado do passivo (investidores):** distribuição das cotas dos fundos para institucionais e investidores qualificados.

> Analogia de engenharia: a gestora é uma **plataforma de dois lados**. De um lado entram recebíveis (matéria-prima); do outro entram investidores (capital). O software fica no meio, transformando dados brutos em ativos monitorados e em relatórios confiáveis.

---

## 3. Produtos da empresa (só o que aparece no site)

### 3.1 Fundos de Investimento — FIDCs

**O que é:** um **FIDC** (Fundo de Investimento em Direitos Creditórios) é um fundo cujo patrimônio é composto majoritariamente por **direitos creditórios** — ou seja, **recebíveis**: parcelas de crédito consignado, duplicatas, aluguéis, financiamentos etc.

- **Problema que resolve:** quem tem recebíveis a receber no futuro quer **dinheiro agora**; quem tem capital quer **rendimento**. O FIDC conecta os dois e empacota o risco.
- **Quem participa:** gestora (HeadInvest), administradora fiduciária, custodiante, cedentes (quem vende os recebíveis), sacados (quem deve), investidores (cotistas).
- **Estrutura típica:** cotas **sênior** (menor risco, retorno alvo) e **subordinada** (absorve as primeiras perdas — funciona como "colchão"/margem de segurança).

**FIDCs específicos (✅):**
| Fundo | Foco |
|---|---|
| **STERN FIDC** | Recebíveis imobiliários, foco em **CRIs** de boa qualidade de crédito. |
| **HEAD Crédito ao Trabalhador FIDC** | **Consignado privado** para trabalhadores CLT — fluxo de caixa previsível. |
| **Crédito ao Trabalhador FIC FIDC** | **FIC** (fundo de cotas): investe nas cotas do fundo acima, dando acesso à estratégia. |

**Onde a tecnologia entra (FIDC):** é o produto **mais intensivo em dados**. Cada fundo tem **milhares de recebíveis** com CPF do devedor, valor, vencimento, taxa, status de pagamento. Precisa: importar arquivos de cedentes (**CNAB**, CSV, planilhas), validar, calcular a "esteira" (elegibilidade de cada recebível segundo o regulamento), consolidar posições e gerar relatórios. → **backend Python clássico**.

---

### 3.2 Produtos Estruturados

**O que é:** operações de crédito **desenhadas sob medida**, empacotadas em títulos:
- **CRI** — Certificado de Recebíveis Imobiliários (lastro imobiliário; isento de IR p/ PF).
- **CRA** — Certificado de Recebíveis do Agronegócio.
- **CCB** — Cédula de Crédito Bancário (título de dívida direto).
- **CR** — Certificado de Recebíveis (lastro geral).

- **Problema que resolve:** dar acesso a operações de crédito específicas com **garantias e mitigadores** desenhados caso a caso.
- **Quem participa:** estruturador (BSI/HeadInvest), securitizadora, devedor, investidores.
- **Alto nível:** origina-se a dívida → analisa-se garantia → estrutura-se o título → coloca-se no mercado/fundo → monitora-se.

**Onde a tecnologia entra:** cada operação gera **documentos** (contratos, escrituras, laudos, matrículas). Aqui entram **OCR + extração de dados de documentos**, workflow de aprovação, e a modelagem de fluxo de caixa (juros, amortização) para precificar.

---

### 3.3 Acompanhamento / Gestão de Crédito

**O que é:** ✅ gestão ativa da carteira **depois** que o investimento é feito — monitoramento contínuo.

- **O que envolve:** indicadores de risco, relatórios de performance, e **gestão de covenants** (verificar se o devedor cumpre as cláusulas; disparar alertas se não).
- **Onde a tecnologia entra:** este é o coração da automação. **Dashboards**, **jobs agendados** que recalculam risco diariamente, **alertas** por e-mail/Slack quando um covenant é violado ou uma parcela atrasa, e cálculo de **inadimplência** (aging da carteira).

> 🔵 Um recebível que atrasa hoje vira perda amanhã. O valor de negócio de detectar isso **automaticamente e cedo** é enorme — é o argumento perfeito para justificar investimento em software.

---

## 4. Onde a tecnologia entra (visão geral)

Empresas de crédito estruturado desse porte normalmente têm um **estoque de sistemas internos** parecido com isto:

| Camada | O que faz | Stack típico (🔵) |
|---|---|---|
| **Ingestão de dados** | Importar carteiras de cedentes/servicers (CNAB, CSV, XML, planilhas), APIs de parceiros | Python, pandas, workers/filas |
| **Motor de regras** | Validar elegibilidade de recebíveis (a "esteira"), aplicar critérios do regulamento | Python, PostgreSQL |
| **Cálculo/modelagem** | Fluxo de caixa, TIR/VPL, marcação, curvas, inadimplência/aging | Python (numpy/pandas) |
| **Monitoramento** | Covenants, alertas, indicadores de risco | Jobs agendados, cron, notificações |
| **Documentos** | Extrair dados de contratos/laudos, organizar, versionar | OCR, IA/LLM, S3 |
| **APIs internas** | Expor dados para dashboards e integrações | **Flask/FastAPI** |
| **Dashboards/relatórios** | Visão de gestor, risco e compliance; relatórios regulatórios | BI ou front próprio |
| **Integrações externas** | Administrador fiduciário, custodiante, B3, bureaus (Serasa) | REST, arquivos, webhooks |
| **Infra** | Hospedagem, storage, banco, filas | **AWS** (EC2/ECS, RDS PostgreSQL, S3, Lambda, SQS) |

**Por que Python encaixa perfeitamente aqui:** o trabalho é **dado + regra + cálculo + integração**. É pandas para manipular carteiras, Flask/FastAPI para expor APIs, PostgreSQL para persistir posições, e AWS para rodar. Nada de latência de microssegundos (isso é trading de alta frequência, **não** é o caso aqui) — o foco é **correção, rastreabilidade e automação**.

**Compliance é um driver técnico, não burocracia:** ✅ a HeadInvest publica um conjunto grande de políticas (risco, segregação de atividades, controles internos, LGPD). Traduzindo para engenharia: **trilhas de auditoria**, **controle de acesso**, **segregação de ambientes**, **logs imutáveis** e **relatórios regulatórios** são requisitos de sistema — não opcionais.

> **Sinal concreto (✅):** o sócio **Riquelme Avelino** já "desenvolveu sistemas de gestão" numa asset anterior (BDR Asset). Isso indica que a HeadInvest **valoriza construir software próprio** de operações — bom sinal para uma vaga de backend.

---

## 5. O que você provavelmente desenvolveria (hipóteses 🔵)

> Nada aqui é projeto confirmado da empresa. São hipóteses plausíveis dado o perfil.

1. **Esteira de recebíveis (motor de elegibilidade)** 🔵
   Importa a carteira de um cedente, aplica as regras do regulamento do FIDC (prazo, concentração por sacado, score mínimo) e decide o que o fundo pode comprar. → Python + PostgreSQL + regras.

2. **Pipeline de ingestão de carteiras** 🔵
   Ler arquivos **CNAB/CSV/planilhas** de vários parceiros, normalizar formatos diferentes, validar e carregar. → parsing, filas, jobs idempotentes.

3. **Motor de monitoramento e covenants** 🔵
   Job diário que recalcula inadimplência, concentração e razões de garantia; dispara **alertas** quando limites são violados. → cron/Lambda + notificações.

4. **Cálculo de fluxo de caixa e marcação** 🔵
   Projetar recebimentos, calcular TIR/VPL, aging da carteira, PDD (provisão para devedores duvidosos). → numpy/pandas.

5. **APIs internas + dashboards** 🔵
   Backend (Flask/FastAPI) expondo posição dos fundos, risco e performance para telas de gestor/risco/compliance.

6. **Automação de documentos (OCR/IA)** 🔵
   Extrair dados de contratos, CCBs, matrículas e laudos para reduzir digitação manual e erro. → OCR + LLM + validação humana.

7. **Integrações com terceiros** 🔵
   Administrador fiduciário, custodiante, **B3**, bureaus de crédito (Serasa/SPC). → conciliação de posições, reconciliação de arquivos.

8. **Relatórios regulatórios e para investidores** 🔵
   Gerar automaticamente relatórios periódicos (cotistas, CVM/ANBIMA). → templates + geração de PDF/planilha.

**Desafios técnicos que costumam aparecer (🔵, ótimos para comentar):**
- **Conciliação/idempotência:** reprocessar o mesmo arquivo não pode duplicar posições.
- **Precisão monetária:** usar `Decimal`, nunca `float`, para valores financeiros.
- **Rastreabilidade:** cada número de um relatório precisa ser explicável até o dado de origem.
- **Formatos bagunçados:** cada cedente manda dados de um jeito; normalização é 80% do trabalho.
- **Fechamento diário:** a posição do fundo precisa "fechar" todo dia — janelas de processamento e consistência importam.

---

## 6. Glossário (só o essencial)

- **Gestora / Asset Management:** empresa que decide onde o dinheiro dos fundos é investido. Ganha taxa sobre o patrimônio gerido.
- **AUM (Assets Under Management):** total sob gestão. Métrica-chave de tamanho.
- **Crédito estruturado:** empréstimos/recebíveis empacotados sob medida em fundos ou títulos, com garantias específicas.
- **Recebível / Direito creditório:** o direito de receber um valor no futuro (uma parcela, uma duplicata). A "matéria-prima" do negócio.
- **FIDC:** fundo cujo patrimônio são recebíveis. Produto central da HeadInvest.
- **FIC:** fundo que investe em cotas de outro fundo (fundo de fundos).
- **Cota sênior / subordinada:** classes de risco. A subordinada absorve as primeiras perdas e protege a sênior.
- **CRI:** título de recebíveis imobiliários — um dos focos da casa.
- **Cedente:** quem vende os recebíveis ao fundo. **Sacado:** quem deve o recebível.
- **Covenant:** cláusula/condição que o devedor deve manter; violá-la dispara alerta/consequência (bom gancho de automação).
- **Consignado privado:** empréstimo descontado direto do salário de CLT — baixa inadimplência, fluxo previsível.
- **Lastro pulverizado:** risco espalhado em muitos devedores pequenos (diversificação → volume de dados).
- **BSI Capital:** empresa parceira que **estrutura e origina** as operações que a HeadInvest gere.

---

## 7. O que vale comentar na entrevista

> Não decore. Use como sementes de conversa. A ideia é sempre conectar **negócio → processo → tecnologia**.

**Observações que demonstram que você entendeu o negócio:**
- "Entendi que o coração de vocês é crédito estruturado — FIDCs e crédito imobiliário. Do ponto de vista de software, isso me parece essencialmente um problema de **dados e regras**: originar, validar elegibilidade, precificar e monitorar recebíveis em escala."
- "Achei interessante a estratégia de **lastro pulverizado** — pra tecnologia isso significa lidar com **volume**: milhares de recebíveis por fundo, o que torna a automação da esteira e do monitoramento praticamente obrigatória."
- "Vi que vocês têm sinergia com a **BSI Capital** na originação/estruturação. Fiquei curioso sobre como os dados fluem entre estruturação e gestão — imagino que haja um ponto de integração aí."

**Perguntas boas para fazer (mostram interesse real):**
- "Hoje a esteira de elegibilidade dos FIDCs é mais automatizada ou ainda tem bastante planilha? Onde vocês veem o maior gargalo operacional?"
- "O monitoramento de covenants e inadimplência é rodado em batch diário ou em tempo mais próximo do real?"
- "Como funciona a integração com administrador fiduciário e custodiante — é via arquivo ou API? Onde a conciliação costuma doer?"
- "Vocês já usam algo de OCR/IA para extração de dados de contratos e laudos, ou isso ainda é manual?"
- "A stack é mais Flask ou FastAPI? Rodam em AWS com RDS/PostgreSQL? Quanto do processamento é Lambda vs. serviço rodando contínuo?"
- "Como vocês pensam **rastreabilidade e auditoria** — cada número de relatório precisa ser explicável até a origem, certo?"

**Conexões tech ↔ mercado que geram boa conversa:**
- Precisão monetária com `Decimal`, idempotência na ingestão, e trilha de auditoria como requisitos de compliance — não detalhes.
- "Esse é o tipo de sistema onde **correção e rastreabilidade** valem mais que latência — bem diferente de trading de alta frequência."
- Detecção precoce de inadimplência via alertas automáticos como um recurso de **redução de risco real**, não só um dashboard bonito.

---

## 8. O que você NÃO precisa decorar

Para **não** perder tempo — o objetivo é entender o negócio, não virar analista de crédito:

- ❌ **Matemática financeira profunda** (fórmulas fechadas de TIR/VPL, duration, cálculo de curvas). Basta saber **o que significam** e por que importam.
- ❌ **Regulação detalhada da CVM/ANBIMA** (números de instruções, artigos). Saiba que **compliance existe e vira requisito de software** — só isso.
- ❌ **Decorar CNPJs, valores de AUM ou datas exatas.** Saber que a empresa é nova (2024) e ligada à BSI já basta.
- ❌ **Macroeconomia / análise de mercado** (juros, cenário, alocação). Não é uma vaga de economista.
- ❌ **Tributação detalhada** de CRI/CRA/FIDC. Saiba que existe isenção em alguns e siga em frente.
- ❌ **Diferença fina entre todos os títulos** (CRI vs CRA vs CR vs CCB). Entenda o conceito comum: **empacotar dívida com garantia**.
- ❌ **Estratégias de investimento e teses de crédito específicas.** Isso é papel dos sócios/analistas, não do backend.

**Foque em:** o fluxo do negócio (seção 2), onde a tecnologia entra (seções 4 e 5), e as conexões da seção 7.

---

## 9. Como impressionar sem parecer que decorou

> A diferença entre "decorei" e "estudei de verdade" é **curiosidade genuína**. Reaja ao que o entrevistador disser, faça perguntas de acompanhamento, e conecte com sua cabeça de engenheiro. Abaixo, falas naturais — não roteiro fechado.

**Observações que soam espontâneas:**
- "Quando vi que vocês trabalham com lastro pulverizado, meu primeiro pensamento foi 'isso é volume de dados' — imagino que a parte chata não seja um recebível, e sim conciliar milhares deles todo dia."
- "Reparei que vocês são uma casa nova (2024) mas com gente muito rodada de mercado. Fiquei curioso se a stack está sendo construída do zero agora — porque começar sem dívida técnica é raro e bem interessante para quem entra cedo."
- "Achei sacada a divisão BSI estrutura / HeadInvest gere. Do lado de software, isso normalmente vira o ponto mais delicado: o handoff de dados entre quem origina e quem monitora."

**Como transformar em conversa (não em monólogo):**
- Faça a observação → **devolva a bola**: "...é mais ou menos assim que funciona aí, ou eu entendi errado?"
- Se ele explicar algo, puxe o fio: "E quando isso falha, como vocês percebem hoje — alguém olha planilha ou tem alerta?"

**Perguntas que rendem boa conversa técnica:**
- "Qual parte da operação hoje ainda depende de alguém abrir uma planilha na segunda de manhã? Costuma ser o melhor primeiro alvo de automação."
- "Vocês pensam o software mais como 'ferramenta interna do time' ou como algo que também melhora a experiência do investidor?"
- "Numa casa de crédito, o medo número um costuma ser 'um número errado num relatório'. Como vocês pensam confiabilidade e rastreabilidade dos dados?"

**Regra de ouro:** é melhor fazer **uma** pergunta curiosa e ouvir de verdade do que despejar cinco termos financeiros. O objetivo é mostrar que você pensa em **problemas de negócio**, não que você memorizou o glossário.

---

## 10. Como conectar isso com a minha experiência

> Ponte entre o que você já fez e o contexto da HeadInvest. Use as ligações que forem verdadeiras para os seus projetos — não force o que você não construiu.

| O que você já fez | Como conecta com a HeadInvest |
|---|---|
| **Multi-tenant** | Isolamento entre **fundos** (ou entre cedentes/clientes): cada fundo tem regras, carteira e relatórios próprios, sem vazar dados entre eles. Segregação é também requisito de **compliance**. |
| **Dashboards** | Telas de **posição do fundo, risco e inadimplência** para gestor e compliance — indicadores financeiros em vez de métricas de produto. |
| **Jobs automáticos / agendados** | **Monitoramento de operações**: recálculo diário de risco, aging da carteira e disparo de alertas de covenant/atraso. |
| **APIs (Flask/FastAPI)** | **Integração entre sistemas**: expor dados internos para dashboards e conversar com administrador fiduciário, custodiante e bureaus. |
| **PostgreSQL** | **Persistência das operações**: recebíveis, posições, fluxos de pagamento — com integridade e histórico consultável. |
| **Docker** | **Padronização de ambientes**: dev = produção, importante quando um número errado tem custo real. |
| **CI/CD** | **Confiabilidade e rastreabilidade**: deploy previsível e reversível; num contexto financeiro, mudança controlada é praticamente um requisito de governança. |
| **IA / LLM** | **Automação de processos**: extrair/classificar informação de contratos e laudos, resumir, apoiar análise — sempre com validação humana. |
| **OCR** | **Documentos**: transformar contratos, CCBs e matrículas em dados estruturados, reduzindo digitação manual e erro. |
| **Testes automatizados** | **Redução de risco**: garantir que a regra de elegibilidade e o cálculo de fluxo não quebrem em silêncio a cada mudança. |
| **Logs (estruturados)** | **Auditoria**: cada número precisa ser explicável até a origem — trilha de auditoria é compliance, não luxo. |

**Como usar na fala:** não liste a tabela. Escolha 2–3 conexões fortes e conte como história:
> "No projeto X eu fiz um sistema multi-tenant com jobs agendados e dashboards. Pela conversa, isso parece bem próximo do que vocês precisam: cada fundo isolado, um job diário recalculando risco e uma tela de acompanhamento — só que aqui o dado é recebível, e o alerta vale dinheiro."

---

## 11. Se eu fosse contratado amanhã (hipótese 🔵)

> Nada aqui é atribuição confirmada — é um cenário plausível para mostrar que você já pensa em **entregar valor cedo**. Deixe explícito que é hipótese ("imagino que os primeiros meses seriam mais ou menos assim...").

**Primeiras semanas — entender antes de codar:**
- Mapear o **fluxo real** de uma operação: como um recebível entra, é validado, vira posição e é monitorado.
- Descobrir onde ainda há **planilha manual** e retrabalho — normalmente é onde está o maior ganho rápido.
- Entender as fontes de dados (arquivos de cedentes, integrações com administrador/custodiante) e o modelo de dados existente.

**Primeiros 1–2 meses — ganhos pequenos e seguros:**
- Automatizar **uma** dor concreta: por exemplo, ingestão/validação de uma carteira que hoje é feita à mão.
- Adicionar **testes e logs** nas partes críticas de cálculo — reduzir risco sem reescrever nada.
- Melhorar um **relatório** recorrente (para investidor ou compliance) que hoje é montado manualmente.

**Meses seguintes — construir base:**
- Evoluir o **motor de elegibilidade/monitoramento** com regras versionadas e alertas.
- Fortalecer **rastreabilidade** (do número no relatório até o dado de origem) e trilha de auditoria.
- Padronizar ambiente (Docker) e deploy (CI/CD) para dar confiabilidade ao que virou crítico.

**Princípio que dá para verbalizar:** em casa de crédito, prefiro **entregar valor incremental com baixo risco** — automatizar uma dor real, cobrir com teste, deixar auditável — antes de propor grandes reescritas. Confiança primeiro, escala depois.

---

## Apêndice — Ficha rápida da empresa (✅)

- **Nome:** HeadInvest Asset Management Ltda. — CNPJ 58.289.954/0001-46.
- **Fundada:** nov/2024. Gestora **independente**; sócios com +30 anos somados de mercado.
- **Foco:** crédito estruturado — FIDCs e crédito imobiliário (CRIs).
- **Ecossistema:** sinergia com **BSI Capital** (estruturação/originação).
- **Sede:** Av. das Nações Unidas, 14401 — Torre Tarumã, São Paulo/SP.
- **Valores declarados:** governança, integridade, disciplina, confiança, transparência.

**Sócios (só o que ajuda a entender o negócio):**
- **Ricardo Carmo** — Fundador e CEO. Também fundou a **BSI Capital** — é a ponte entre estruturação/originação e a gestão.
- **David Camacho** — Diretor de Gestão. Responsável pela **gestão dos fundos de crédito** (o "lado do ativo").
- **Leonardo Kenzo** — Diretor de **Risco e Compliance**; é também o **encarregado de dados (LGPD)**. Dono dos requisitos de auditoria/controle que viram software.
- **Riquelme Avelino** — Análise e Operações. Já **desenvolveu sistemas de gestão** em asset anterior — sinal de que valorizam software próprio de operações.

> **Como usar isto na conversa:** dá para dizer, com verdade, que você passou o fim de semana estudando o site e o ecossistema BSI/HeadInvest, entendeu que o negócio é crédito estruturado orientado a dados, e chegou com perguntas sobre a esteira de FIDC, monitoramento de covenants e a stack (Python/Flask/PostgreSQL/AWS). Isso é exatamente o nível esperado.
