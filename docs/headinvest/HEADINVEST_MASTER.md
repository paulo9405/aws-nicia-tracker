# HEADINVEST — MATERIAL MASTER DE ESTUDO (PREPARAÇÃO PARA ENTREVISTA)

> **Trilha:** HeadInvest · **Módulo:** Guia de Preparação para a Entrevista · **Fase:** material de
> estudo (Fase 1 — conteúdo).
>
> **Origem/rastreabilidade:** condensado e reorganizado de
> `docs/headinvest/HeadInvest - Guia de Preparação para Segunda Entrevista.md`. Reorganiza o guia
> em 6 aulas equilibradas para estudo — **não cria fatos novos**.
>
> **Convenções:** ✅ = fato confirmado (site oficial / fontes públicas). 🔵 = inferência plausível de
> mercado (não afirmar como fato na entrevista).
>
> 💡 **Foco do material:** entender o **negócio → processo → tecnologia**. Não é um curso de
> investimentos; é a base para uma conversa técnica de backend Python com contexto de negócio.

## ÍNDICE
1. A empresa e o negócio
2. Como funciona: o fluxo e os produtos
3. Onde a tecnologia entra
4. Preparação para a entrevista
5. Conectando com a sua experiência
6. Glossário e revisão rápida

---

## 1. A empresa e o negócio

### 1.1 Elevator pitch (o resumo em 60 segundos)
A **HeadInvest** é uma **gestora de recursos (asset management) independente** focada em **crédito
estruturado**. Em termos de engenharia: uma empresa que **origina, empacota, precifica e monitora
"dívidas"** (recebíveis) de terceiros e as transforma em **fundos** que investidores compram.

- ✅ Empresa nova (constituída em **nov/2024**), montada por sócios com **+30 anos somados** de mercado de capitais.
- ✅ Atua em **sinergia com a BSI Capital**: a BSI **estrutura e origina** as operações; a HeadInvest **gere** os fundos.
- ✅ Sede em São Paulo (Av. das Nações Unidas, 14401 — região da Berrini/Chucri Zaidan).
- ✅ Produtos centrais: **FIDCs** (fundos de recebíveis) e **crédito imobiliário** (CRIs).

> **O gancho de tecnologia:** crédito estruturado é, no fundo, um **problema de dados**. Originar,
> analisar, precificar e monitorar milhares de recebíveis pulverizados exige software — não dá para
> fazer no Excel em escala. É exatamente aí que um backend Python entra.

### 1.2 O que a HeadInvest faz e como ganha dinheiro
É uma **gestora de fundos de investimento** especializada em **crédito** (dívida privada), com ênfase
em **crédito estruturado** e **crédito imobiliário**.

- ✅ **Taxa de administração/gestão:** % ao ano sobre o patrimônio sob gestão (**AUM** — *Assets Under Management*). Receita recorrente principal.
- 🔵 **Taxa de performance:** % sobre o retorno que exceder um benchmark (ex.: CDI). Comum em fundos de crédito.
- 🔵 Ganhos ligados à **estruturação/originação** via ecossistema BSI Capital.

> Para um dev: a receita escala com o **AUM**. Quanto mais dinheiro sob gestão e mais operações
> ativas, mais a operação precisa de **automação e controle** — a equipe não cresce na mesma
> velocidade que o volume de dados.

### 1.3 Clientes e posicionamento
- ✅ **Investidores institucionais** e **fundos exclusivos**.
- 🔵 Investidores qualificados/profissionais (crédito estruturado costuma ser restrito a esse público por regulação da CVM).

Posiciona-se como gestora **independente**, técnica, com discurso de **governança, disciplina e
transparência**. Diferenciais declarados (✅): curadoria técnica das operações e mitigação de risco;
expertise em crédito imobiliário (CRIs, CRAs, ativos reais); **lastro pulverizado** (diversificar o
risco em muitos devedores pequenos em vez de poucos grandes); sinergia com a BSI Capital.

### 1.4 Ficha rápida da empresa (✅)
| Item | Dado |
|---|---|
| Nome | HeadInvest Asset Management Ltda. — CNPJ 58.289.954/0001-46 |
| Fundada | nov/2024. Gestora **independente**; sócios com +30 anos somados |
| Foco | Crédito estruturado — FIDCs e crédito imobiliário (CRIs) |
| Ecossistema | Sinergia com **BSI Capital** (estruturação/originação) |
| Sede | Av. das Nações Unidas, 14401 — Torre Tarumã, São Paulo/SP |
| Valores | Governança, integridade, disciplina, confiança, transparência |

**Sócios (só o que ajuda a entender o negócio):**
- **Ricardo Carmo** — Fundador e CEO. Também fundou a **BSI Capital**: a ponte entre estruturação/originação e a gestão.
- **David Camacho** — Diretor de Gestão. Responsável pela **gestão dos fundos de crédito** (o "lado do ativo").
- **Leonardo Kenzo** — Diretor de **Risco e Compliance**; **encarregado de dados (LGPD)**. Dono dos requisitos de auditoria/controle que viram software.
- **Riquelme Avelino** — Análise e Operações. Já **desenvolveu sistemas de gestão** em asset anterior (BDR Asset) — sinal de que valorizam software próprio de operações.

---

## 2. Como funciona: o fluxo e os produtos

### 2.1 O fluxo do negócio (um pipeline de dados)
✅ O site descreve **4 etapas**. Pense nelas como um pipeline com etapas bem definidas:

```
Originação → Análise/Modelagem → Implementação/Estruturação → Monitoramento
  (filtro)      (precificação)        (contratos)               (covenants)
```

1. **Originação e filtro** — chegam oportunidades de crédito (ex.: uma empresa quer antecipar recebíveis). Filtro inicial da estrutura.
2. **Análise e modelagem** — avaliação econômica: simulação de cenários, **TIR**, **VPL**, análise de sensibilidade, avaliação de garantias.
3. **Implementação** — negociação de termos, instrumentos contratuais, mitigadores de risco. A operação vira um ativo dentro de um fundo.
4. **Monitoramento** — acompanhamento contínuo de fluxos de pagamento, indicadores de risco e **covenants** (cláusulas que o devedor deve cumprir).

**Os dois lados da plataforma:**
- **Lado do ativo (operações):** originação própria + parceria com a **BSI Capital**, que traz e estrutura as operações.
- **Lado do passivo (investidores):** distribuição das cotas dos fundos para institucionais e investidores qualificados.

> Analogia de engenharia: a gestora é uma **plataforma de dois lados**. De um lado entram recebíveis
> (matéria-prima); do outro entram investidores (capital). O software fica no meio, transformando
> dados brutos em ativos monitorados e relatórios confiáveis.

### 2.2 FIDCs — o produto central
Um **FIDC** (Fundo de Investimento em Direitos Creditórios) é um fundo cujo patrimônio é composto
majoritariamente por **recebíveis**: parcelas de consignado, duplicatas, aluguéis, financiamentos etc.

- **Problema que resolve:** quem tem recebíveis futuros quer **dinheiro agora**; quem tem capital quer **rendimento**. O FIDC conecta os dois e empacota o risco.
- **Quem participa:** gestora (HeadInvest), administradora fiduciária, custodiante, cedentes (vendem recebíveis), sacados (devem), investidores (cotistas).
- **Estrutura típica:** cotas **sênior** (menor risco) e **subordinada** (absorve as primeiras perdas — o "colchão"/margem de segurança).

**FIDCs específicos (✅):**
| Fundo | Foco |
|---|---|
| **STERN FIDC** | Recebíveis imobiliários, foco em **CRIs** de boa qualidade de crédito. |
| **HEAD Crédito ao Trabalhador FIDC** | **Consignado privado** para trabalhadores CLT — fluxo de caixa previsível. |
| **Crédito ao Trabalhador FIC FIDC** | **FIC** (fundo de cotas): investe nas cotas do fundo acima. |

> **Tecnologia (FIDC):** é o produto **mais intensivo em dados**. Cada fundo tem **milhares de
> recebíveis** com CPF, valor, vencimento, taxa e status. Importar arquivos de cedentes (**CNAB**,
> CSV, planilhas), validar, calcular a "esteira" (elegibilidade segundo o regulamento), consolidar
> posições e gerar relatórios → **backend Python clássico**.

### 2.3 Produtos estruturados
Operações de crédito **desenhadas sob medida**, empacotadas em títulos:
- **CRI** — Certificado de Recebíveis Imobiliários (lastro imobiliário; isento de IR p/ PF).
- **CRA** — Certificado de Recebíveis do Agronegócio.
- **CCB** — Cédula de Crédito Bancário (título de dívida direto).
- **CR** — Certificado de Recebíveis (lastro geral).

Alto nível: origina-se a dívida → analisa-se a garantia → estrutura-se o título → coloca-se no
mercado/fundo → monitora-se. **Tecnologia:** cada operação gera **documentos** (contratos, escrituras,
laudos, matrículas) → **OCR + extração de dados**, workflow de aprovação e modelagem de fluxo de caixa.

### 2.4 Acompanhamento / gestão de crédito
✅ Gestão ativa da carteira **depois** que o investimento é feito: indicadores de risco, relatórios de
performance e **gestão de covenants** (verificar cumprimento de cláusulas; disparar alertas).

> **Tecnologia:** o coração da automação. **Dashboards**, **jobs agendados** que recalculam risco
> diariamente, **alertas** quando um covenant é violado ou uma parcela atrasa, e cálculo de
> inadimplência (aging da carteira). 🔵 Um recebível que atrasa hoje vira perda amanhã — detectar
> isso **automaticamente e cedo** é valor de negócio enorme.

---

## 3. Onde a tecnologia entra

### 3.1 O estoque de sistemas típico (visão de camadas)
Empresas de crédito estruturado desse porte costumam ter um conjunto de sistemas internos assim (🔵):

| Camada | O que faz | Stack típico (🔵) |
|---|---|---|
| **Ingestão de dados** | Importar carteiras de cedentes/servicers (CNAB, CSV, XML, planilhas), APIs | Python, pandas, workers/filas |
| **Motor de regras** | Validar elegibilidade de recebíveis (a "esteira"), critérios do regulamento | Python, PostgreSQL |
| **Cálculo/modelagem** | Fluxo de caixa, TIR/VPL, marcação, inadimplência/aging | Python (numpy/pandas) |
| **Monitoramento** | Covenants, alertas, indicadores de risco | Jobs agendados, cron, notificações |
| **Documentos** | Extrair dados de contratos/laudos, organizar, versionar | OCR, IA/LLM, S3 |
| **APIs internas** | Expor dados para dashboards e integrações | **Flask/FastAPI** |
| **Dashboards/relatórios** | Visão de gestor, risco e compliance; relatórios regulatórios | BI ou front próprio |
| **Integrações externas** | Administrador fiduciário, custodiante, B3, bureaus (Serasa) | REST, arquivos, webhooks |
| **Infra** | Hospedagem, storage, banco, filas | **AWS** (EC2/ECS, RDS PostgreSQL, S3, Lambda, SQS) |

**Por que Python encaixa:** o trabalho é **dado + regra + cálculo + integração**. pandas para carteiras,
Flask/FastAPI para APIs, PostgreSQL para posições, AWS para rodar. Sem latência de microssegundos
(isso é trading de alta frequência, **não** é o caso) — o foco é **correção, rastreabilidade e automação**.

**Compliance é driver técnico, não burocracia:** ✅ a HeadInvest publica muitas políticas (risco,
segregação de atividades, controles internos, LGPD). Em engenharia isso vira **trilhas de auditoria**,
**controle de acesso**, **segregação de ambientes**, **logs imutáveis** e **relatórios regulatórios** —
requisitos de sistema, não opcionais.

> **Sinal concreto (✅):** o sócio **Riquelme Avelino** já "desenvolveu sistemas de gestão" numa asset
> anterior. Indica que a HeadInvest **valoriza construir software próprio** — bom sinal para backend.

### 3.2 O que você provavelmente desenvolveria (hipóteses 🔵)
> Nada aqui é projeto confirmado — são hipóteses plausíveis dado o perfil.

1. **Esteira de recebíveis (motor de elegibilidade)** — importa a carteira de um cedente, aplica regras do regulamento (prazo, concentração por sacado, score mínimo) e decide o que o fundo pode comprar.
2. **Pipeline de ingestão de carteiras** — ler **CNAB/CSV/planilhas** de vários parceiros, normalizar formatos, validar e carregar (parsing, filas, jobs idempotentes).
3. **Motor de monitoramento e covenants** — job diário que recalcula inadimplência, concentração e razões de garantia; dispara **alertas**.
4. **Cálculo de fluxo de caixa e marcação** — projetar recebimentos, TIR/VPL, aging, PDD (provisão para devedores duvidosos).
5. **APIs internas + dashboards** — backend (Flask/FastAPI) expondo posição dos fundos, risco e performance.
6. **Automação de documentos (OCR/IA)** — extrair dados de contratos, CCBs, matrículas e laudos, com validação humana.
7. **Integrações com terceiros** — administrador fiduciário, custodiante, **B3**, bureaus (Serasa/SPC); conciliação de posições.
8. **Relatórios regulatórios e para investidores** — gerar relatórios periódicos (cotistas, CVM/ANBIMA).

**Desafios técnicos que costumam aparecer (🔵, ótimos para comentar):**
- **Conciliação/idempotência:** reprocessar o mesmo arquivo não pode duplicar posições.
- **Precisão monetária:** usar `Decimal`, nunca `float`, para valores financeiros.
- **Rastreabilidade:** cada número de um relatório precisa ser explicável até o dado de origem.
- **Formatos bagunçados:** cada cedente manda dados de um jeito; normalização é 80% do trabalho.
- **Fechamento diário:** a posição do fundo precisa "fechar" todo dia — janelas de processamento e consistência importam.

---

## 4. Preparação para a entrevista

### 4.1 O que vale comentar (negócio → processo → tecnologia)
> Não decore. Use como sementes de conversa.

**Observações que mostram que você entendeu o negócio:**
- "O coração de vocês é crédito estruturado — FIDCs e crédito imobiliário. Em software, isso me parece essencialmente um problema de **dados e regras**: originar, validar elegibilidade, precificar e monitorar recebíveis em escala."
- "A estratégia de **lastro pulverizado** significa, para a tecnologia, lidar com **volume**: milhares de recebíveis por fundo, o que torna a automação da esteira e do monitoramento praticamente obrigatória."
- "Vi a sinergia com a **BSI Capital** na originação/estruturação. Fiquei curioso sobre como os dados fluem entre estruturação e gestão — imagino que haja um ponto de integração aí."

**Perguntas boas para fazer (mostram interesse real):**
- "A esteira de elegibilidade dos FIDCs já é automatizada ou ainda tem bastante planilha? Onde está o maior gargalo operacional?"
- "O monitoramento de covenants e inadimplência roda em batch diário ou mais próximo do tempo real?"
- "A integração com administrador fiduciário e custodiante é via arquivo ou API? Onde a conciliação costuma doer?"
- "Já usam OCR/IA para extrair dados de contratos e laudos, ou ainda é manual?"
- "A stack é mais Flask ou FastAPI? Rodam em AWS com RDS/PostgreSQL? Quanto é Lambda vs. serviço contínuo?"
- "Como pensam **rastreabilidade e auditoria** — cada número de relatório explicável até a origem?"

### 4.2 O que você NÃO precisa decorar
O objetivo é entender o negócio, não virar analista de crédito:
- ❌ **Matemática financeira profunda** (fórmulas de TIR/VPL, duration, curvas). Saiba **o que significam** e por que importam.
- ❌ **Regulação detalhada da CVM/ANBIMA** (números de instruções, artigos). Saiba que **compliance vira requisito de software**.
- ❌ **Decorar CNPJs, valores de AUM ou datas exatas.** Basta: empresa nova (2024), ligada à BSI.
- ❌ **Macroeconomia / análise de mercado.** Não é vaga de economista.
- ❌ **Tributação detalhada** de CRI/CRA/FIDC. Saiba que há isenção em alguns e siga.
- ❌ **Diferença fina entre CRI/CRA/CR/CCB.** Entenda o conceito comum: **empacotar dívida com garantia**.
- ❌ **Teses de crédito específicas.** Papel dos sócios/analistas, não do backend.

> **Foque em:** o fluxo do negócio (Aula 2), onde a tecnologia entra (Aula 3) e as conexões (Aula 5).

### 4.3 Como impressionar sem parecer que decorou
A diferença entre "decorei" e "estudei de verdade" é **curiosidade genuína**. Reaja ao que o
entrevistador disser, faça perguntas de acompanhamento e conecte com sua cabeça de engenheiro.

**Observações que soam espontâneas:**
- "Quando vi 'lastro pulverizado', meu primeiro pensamento foi 'isso é volume de dados' — a parte chata não é um recebível, é conciliar milhares deles todo dia."
- "Vocês são uma casa nova (2024) mas com gente rodada de mercado. Fiquei curioso se a stack está sendo construída do zero — começar sem dívida técnica é raro e interessante para quem entra cedo."
- "Achei sacada a divisão BSI estrutura / HeadInvest gere. Em software, isso normalmente vira o ponto mais delicado: o handoff de dados entre quem origina e quem monitora."

**Transforme em conversa (não em monólogo):** faça a observação → **devolva a bola** ("...é assim que
funciona aí, ou entendi errado?"). Se ele explicar algo, puxe o fio ("e quando isso falha, alguém
olha planilha ou tem alerta?"). **Regra de ouro:** melhor **uma** pergunta curiosa e ouvir de verdade
do que despejar cinco termos financeiros.

---

## 5. Conectando com a sua experiência

### 5.1 Ponte entre o que você já fez e o contexto da HeadInvest
> Use só as ligações que forem **verdadeiras** para os seus projetos — não force o que não construiu.

| O que você já fez | Como conecta com a HeadInvest |
|---|---|
| **Multi-tenant** | Isolamento entre **fundos** (ou cedentes/clientes): cada fundo com regras, carteira e relatórios próprios, sem vazar dados. Segregação também é **compliance**. |
| **Dashboards** | Telas de **posição do fundo, risco e inadimplência** para gestor e compliance. |
| **Jobs agendados** | **Monitoramento**: recálculo diário de risco, aging e alertas de covenant/atraso. |
| **APIs (Flask/FastAPI)** | **Integração**: expor dados internos e conversar com administrador fiduciário, custodiante e bureaus. |
| **PostgreSQL** | **Persistência**: recebíveis, posições, fluxos — com integridade e histórico consultável. |
| **Docker** | **Padronização de ambientes**: dev = produção, importante quando um número errado tem custo real. |
| **CI/CD** | **Confiabilidade**: deploy previsível e reversível; mudança controlada é requisito de governança. |
| **IA / LLM** | **Automação**: extrair/classificar informação de contratos e laudos, resumir — com validação humana. |
| **OCR** | **Documentos**: transformar contratos, CCBs e matrículas em dados estruturados. |
| **Testes automatizados** | **Redução de risco**: garantir que elegibilidade e cálculo não quebrem em silêncio. |
| **Logs estruturados** | **Auditoria**: cada número explicável até a origem — compliance, não luxo. |

**Como usar na fala:** não liste a tabela. Escolha 2–3 conexões fortes e conte como história:
> "No projeto X fiz um sistema multi-tenant com jobs agendados e dashboards. Isso parece próximo do
> que vocês precisam: cada fundo isolado, um job diário recalculando risco e uma tela de
> acompanhamento — só que aqui o dado é recebível, e o alerta vale dinheiro."

### 5.2 Se eu fosse contratado amanhã (hipótese 🔵)
> Deixe explícito que é hipótese ("imagino que os primeiros meses seriam mais ou menos assim...").

**Primeiras semanas — entender antes de codar:**
- Mapear o **fluxo real** de uma operação: como um recebível entra, é validado, vira posição e é monitorado.
- Descobrir onde ainda há **planilha manual** e retrabalho — normalmente o maior ganho rápido.
- Entender as fontes de dados e o modelo de dados existente.

**Primeiros 1–2 meses — ganhos pequenos e seguros:**
- Automatizar **uma** dor concreta (ex.: ingestão/validação de uma carteira feita à mão).
- Adicionar **testes e logs** nas partes críticas de cálculo — reduzir risco sem reescrever.
- Melhorar um **relatório** recorrente (investidor ou compliance) hoje montado manualmente.

**Meses seguintes — construir base:**
- Evoluir o **motor de elegibilidade/monitoramento** com regras versionadas e alertas.
- Fortalecer **rastreabilidade** e trilha de auditoria.
- Padronizar ambiente (Docker) e deploy (CI/CD).

> **Princípio para verbalizar:** em casa de crédito, prefiro **entregar valor incremental com baixo
> risco** — automatizar uma dor real, cobrir com teste, deixar auditável — antes de grandes
> reescritas. **Confiança primeiro, escala depois.**

---

## 6. Glossário e revisão rápida

### 6.1 Glossário (só o essencial)
- **Gestora / Asset Management:** decide onde o dinheiro dos fundos é investido. Ganha taxa sobre o patrimônio gerido.
- **AUM (Assets Under Management):** total sob gestão. Métrica-chave de tamanho.
- **Crédito estruturado:** empréstimos/recebíveis empacotados sob medida em fundos ou títulos, com garantias específicas.
- **Recebível / Direito creditório:** direito de receber um valor no futuro (parcela, duplicata). A "matéria-prima" do negócio.
- **FIDC:** fundo cujo patrimônio são recebíveis. Produto central da HeadInvest.
- **FIC:** fundo que investe em cotas de outro fundo (fundo de fundos).
- **Cota sênior / subordinada:** classes de risco. A subordinada absorve as primeiras perdas e protege a sênior.
- **CRI:** título de recebíveis imobiliários — um dos focos da casa.
- **Cedente:** quem vende os recebíveis ao fundo. **Sacado:** quem deve o recebível.
- **Covenant:** cláusula que o devedor deve manter; violá-la dispara alerta/consequência (bom gancho de automação).
- **Consignado privado:** empréstimo descontado direto do salário de CLT — baixa inadimplência, fluxo previsível.
- **Lastro pulverizado:** risco espalhado em muitos devedores pequenos (diversificação → volume de dados).
- **BSI Capital:** empresa parceira que **estrutura e origina** as operações que a HeadInvest gere.
- **TIR / VPL:** medidas de retorno/valor de um fluxo de caixa — saiba o que significam, não as fórmulas.
- **Aging / inadimplência:** quanto da carteira está atrasado e há quanto tempo.

### 6.2 Flashcards de revisão (pergunte-se)
- O que a HeadInvest faz, em uma frase? → Gestora independente de **crédito estruturado** (FIDCs + crédito imobiliário).
- Como ela ganha dinheiro? → Taxa sobre o **AUM** (recorrente) + performance (🔵).
- Qual a relação com a BSI Capital? → BSI **estrutura/origina**; HeadInvest **gere** os fundos.
- Quais as 4 etapas do fluxo? → Originação → Análise/Modelagem → Implementação → Monitoramento.
- Por que é "problema de dados"? → Lastro pulverizado = **milhares de recebíveis** por fundo para validar, precificar e monitorar.
- 3 requisitos técnicos que vêm do compliance? → Trilha de auditoria, controle de acesso, rastreabilidade (logs imutáveis).
- 3 armadilhas técnicas em sistema financeiro? → `Decimal` (não `float`), idempotência na ingestão, rastreabilidade do número até a origem.
- Qual a stack provável? → Python (pandas), Flask/FastAPI, PostgreSQL, AWS.

> **Fecho:** você passou o tempo estudando o site e o ecossistema BSI/HeadInvest, entendeu que o
> negócio é **crédito estruturado orientado a dados**, e chegou com perguntas sobre a esteira de FIDC,
> monitoramento de covenants e a stack (Python/Flask/PostgreSQL/AWS). Esse é exatamente o nível esperado.
