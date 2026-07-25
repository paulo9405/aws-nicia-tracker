# BANCO DE QUESTÕES — TRILHA HEADINVEST (NÍCIA TRACK)

> **Uso:** fonte do importador `import_headinvest_questions` (trilha separada do concurso e da avicultura).
> Todas as seções mapeiam para o **Subject único da trilha** (`headinvest-guia`), criado por
> `import_headinvest` — ver `HEADINVEST_QUESTION_MAP` no comando. As seções abaixo espelham as 6 aulas
> apenas para clareza de autoria; no mini-quiz elas formam um **pool único** da trilha.
>
> **Formato** (reaproveita o parser do banco mestre): questões com 4 alternativas **A–D**, uma correta,
> seguidas da tabela de gabarito. **Não** colocar `---` entre a última questão e o cabeçalho de gabarito.
>
> **Antiviés de IA:** as alternativas são calibradas para não entregar a resposta pelo formato —
> comprimentos parelhos (a correta não é a mais longa), o "porquê" fica só no gabarito (não dentro da
> opção), sem parênteses exclusivos da correta, sem palavras-tell ("sempre/apenas/completamente") de um
> lado só, e a letra correta é distribuída de forma equilibrada entre A–D.
>
> **Rastreabilidade:** questões derivadas de `docs/headinvest/HEADINVEST_MASTER.md`. A coluna
> "Ref. MASTER" aponta a seção de origem (§). Não cria fatos novos.

# SEÇÃO 1 — HeadInvest: A empresa e o negócio
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Qual alternativa **melhor descreve** a HeadInvest?
A) Banco de varejo que concede crédito consignado a qualquer público
B) Corretora de valores voltada a trading de alta frequência
C) Gestora independente focada em crédito estruturado privado
D) Securitizadora que emite CRIs e os distribui no mercado

**2.** Qual é a **principal receita recorrente** de uma gestora como a HeadInvest?
A) Taxa de administração cobrada a cada ano sobre o patrimônio sob gestão
B) Taxa de performance sobre o retorno que exceder o CDI no período
C) Spread entre a compra e a venda de ações na tesouraria
D) Comissão fixa por cada operação de crédito que é originada

**3.** A relação entre HeadInvest e **BSI Capital** pode ser resumida como:
A) A HeadInvest estrutura e origina as operações e a BSI gere os fundos dela
B) As duas concorrem pelas mesmas operações no mercado de crédito privado
C) A HeadInvest atua como administradora fiduciária dos fundos da BSI
D) A BSI estrutura e origina as operações e a HeadInvest gere os fundos

**4.** Por que crédito estruturado é descrito como "um problema de dados"?
A) Porque exige latência de microssegundos para executar as ordens de compra
B) Porque monitorar milhares de recebíveis em escala depende de software
C) Porque o maior desafio está na interface gráfica para o investidor final
D) Porque a operação depende de planilhas atualizadas manualmente todo dia

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 1
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **C** | Gestora independente de crédito estruturado: FIDCs e crédito imobiliário. | §1.1 |
| 2 | **A** | Receita recorrente principal é a taxa sobre o patrimônio sob gestão (AUM). | §1.2 |
| 3 | **D** | A BSI estrutura e origina; a HeadInvest gere os fundos. | §1.1 |
| 4 | **B** | Lastro pulverizado gera volume; monitorar em escala exige software, não latência. | §1.1 |

---

# SEÇÃO 2 — HeadInvest: Fluxo e produtos
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** As **4 etapas** do fluxo do negócio, na ordem correta, são:
A) Modelagem → Originação → Implementação → Monitoramento
B) Originação → Modelagem → Implementação → Monitoramento
C) Monitoramento → Originação → Modelagem → Implementação
D) Originação → Implementação → Modelagem → Monitoramento

**2.** O que é um **FIDC**?
A) Um título de dívida emitido diretamente por um banco comercial
B) Um certificado de crédito lastreado em recebíveis imobiliários
C) Um fundo que investe em ações de empresas do setor de crédito
D) Um fundo cujo patrimônio é formado sobretudo por recebíveis

**3.** Numa estrutura típica de FIDC, a **cota subordinada**:
A) Tem a menor exposição a risco e retorno-alvo assegurado
B) É negociada na B3 em tempo real ao longo do pregão
C) Absorve as primeiras perdas e protege a cota sênior
D) Corresponde à dívida do cedente perante o custodiante

**4.** O lastro do fundo **HEAD Crédito ao Trabalhador FIDC** é o consignado privado, que consiste em:
A) Recebíveis com alta inadimplência e fluxo de caixa incerto
B) Recebíveis do agronegócio com forte sazonalidade de safra
C) Contratos de aluguel comercial de prazo longo e reajuste anual
D) Empréstimo descontado direto da folha de pagamento do trabalhador CLT

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 2
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | Originação, Modelagem, Implementação e Monitoramento, nessa ordem. | §2.1 |
| 2 | **D** | FIDC: fundo cujo patrimônio são direitos creditórios (recebíveis). | §2.2 |
| 3 | **C** | A subordinada absorve as primeiras perdas e protege a sênior. | §2.2 |
| 4 | **D** | Consignado privado é descontado da folha do CLT: baixa inadimplência, fluxo previsível. | §2.2 |

---

# SEÇÃO 3 — HeadInvest: Onde a tecnologia entra
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Por que Python encaixa bem no trabalho de uma gestora de crédito estruturado?
A) Porque o trabalho é dado, regra, cálculo e integração
B) Porque garante a latência de microssegundos exigida em trading
C) Porque dispensa o uso de banco de dados relacional na operação
D) Porque substitui os controles de compliance por automação total

**2.** A chamada **"esteira de recebíveis"** é, em essência:
A) Uma esteira física que transporta documentos entre as mesas de trabalho
B) Um motor que valida a elegibilidade dos recebíveis pelo regulamento
C) Um relatório periódico enviado à CVM sobre a carteira do fundo
D) Um painel de indicadores usado na captação de novos investidores

**3.** Ao lidar com valores financeiros em código, a prática recomendada é:
A) Usar float por ser o tipo numérico mais rápido em cálculo
B) Guardar os valores como texto e converter só na exibição
C) Usar o tipo Decimal, e não float, em todos os valores monetários
D) Registrar tudo em centavos inteiros, sem um padrão definido

**4.** Por que se diz que **compliance é um driver técnico**, não apenas burocracia?
A) Porque impede qualquer tipo de automação de processos
B) Porque se resolve apenas com documentos em PDF arquivados
C) Porque é responsabilidade exclusiva da área jurídica da casa
D) Porque vira requisito do próprio software da operação

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 3
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **A** | Dado, regra, cálculo e integração; foco em correção e rastreabilidade, não latência. | §3.1 |
| 2 | **B** | Esteira é o motor que valida a elegibilidade dos recebíveis pelo regulamento. | §3.2 |
| 3 | **C** | Precisão monetária: Decimal, nunca float. | §3.2 |
| 4 | **D** | Compliance vira requisito de software: auditoria, controle de acesso e logs imutáveis. | §3.1 |

---

# SEÇÃO 4 — HeadInvest: Preparação para a entrevista
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Qual destes assuntos você **NÃO precisa decorar** para a entrevista?
A) As fórmulas fechadas de TIR/VPL e os artigos da CVM
B) O fluxo do negócio, da originação até o monitoramento
C) O ponto onde a tecnologia entra na operação diária
D) A relação de sinergia entre a HeadInvest e a BSI Capital

**2.** A melhor postura para "impressionar sem parecer que decorou" é:
A) Usar o máximo de termos financeiros que você conseguir citar
B) Perguntar com curiosidade e ligar negócio à tecnologia
C) Evitar fazer perguntas para não demonstrar insegurança
D) Concentrar a conversa em salário, benefícios e horário

**3.** Qual é um **bom exemplo de pergunta** para fazer ao entrevistador?
A) "Qual o valor exato do AUM e o CNPJ da holding do grupo?"
B) "Vocês pagam hora extra no fechamento contábil de fim de mês?"
C) "A esteira dos FIDCs é automatizada ou ainda tem planilha?"
D) "Que ações da bolsa vocês recomendam que eu compre agora?"

**4.** No contexto de ingestão de carteiras, **idempotência** significa:
A) Que todo cedente envie os dados num formato único e fixo
B) Que o sistema seja executado uma única vez em cada ano
C) Que os dados sejam apagados ao fim de cada importação
D) Que reprocessar o mesmo arquivo não duplique as posições

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 4
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **A** | Não decore fórmulas de TIR/VPL nem artigos da CVM; saiba o que significam. | §4.2 |
| 2 | **B** | Curiosidade e a ponte negócio, processo e tecnologia valem mais que jargão. | §4.3 |
| 3 | **C** | Perguntar sobre automação da esteira e gargalos mostra interesse técnico real. | §4.1 |
| 4 | **D** | Idempotência: reprocessar o mesmo arquivo não duplica posições. | §3.2 |

---

# SEÇÃO 5 — HeadInvest: Conectando com a sua experiência
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Como **multi-tenant** se conecta ao contexto da HeadInvest?
A) Isolamento de dados entre os fundos, um por um
B) Aumento da latência no processamento das cargas
C) Troca do banco de dados relacional por planilhas
D) Fim da necessidade de gerar relatórios da carteira

**2.** Um bom uso de **jobs agendados** nesse negócio seria:
A) Enviar e-mails de marketing para captar novos investidores da base
B) Recalcular risco e aging diários e alertar sobre covenant
C) Reiniciar o servidor toda madrugada por precaução geral
D) Gerar de forma aleatória novas operações de crédito

**3.** Sobre os "primeiros meses" de um backend recém-contratado, o princípio recomendado é:
A) Propor a reescrita completa da stack logo na primeira semana
B) Deixar os testes de lado para não atrasar as entregas
C) Entregar valor aos poucos e com baixo risco antes de reescrever
D) Automatizar tudo de uma vez, sem mapear o fluxo real antes

**4.** Onde **OCR/IA** agrega valor na operação?
A) Substituir a análise humana na decisão de conceder crédito
B) Precificar ações e derivativos em tempo real de mercado
C) Gerar de forma automática os regulamentos dos fundos
D) Extrair dados de contratos, CCBs e laudos para estruturar

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 5
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **A** | Multi-tenant isola os fundos entre si; segregação também é requisito de compliance. | §5.1 |
| 2 | **B** | Monitoramento: recálculo diário de risco e aging e alerta de covenant ou atraso. | §5.1 |
| 3 | **C** | Valor incremental com baixo risco antes de reescritas: confiança primeiro, escala depois. | §5.2 |
| 4 | **D** | OCR/IA extrai dados de documentos, sempre com validação humana no laço. | §5.1 |

---

# SEÇÃO 6 — HeadInvest: Glossário e revisão rápida
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** O que significa **AUM**?
A) O total de recursos que a casa administra sob gestão para os cotistas
B) O lucro líquido que a gestora apura ao longo do ano
C) A taxa de administração cobrada dos cotistas
D) A quantidade de fundos que hoje estão ativos

**2.** Um **covenant** é:
A) O nome que se dá à cota sênior de um FIDC
B) Uma cláusula do contrato que o devedor precisa manter durante a operação
C) Um relatório periódico enviado ao investidor sobre a carteira
D) A taxa de performance que é paga ao gestor do fundo

**3.** A estratégia de **lastro pulverizado** significa:
A) Concentrar o risco em poucos grandes devedores
B) Investir o patrimônio da carteira em títulos públicos
C) Espalhar o risco em muitos devedores pequenos
D) Reduzir a zero o risco de inadimplência

**4.** A diferença entre **cedente** e **sacado** é:
A) Cedente e sacado são exatamente o mesmo participante
B) O sacado vende os recebíveis e o cedente é a administradora
C) Cedente e sacado são ambos cotistas do fundo de crédito
D) O cedente vende os recebíveis e o sacado é quem deve

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 6
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **A** | AUM (Assets Under Management) é o total de recursos sob gestão. | §6.1 |
| 2 | **B** | Covenant é cláusula que o devedor mantém; violá-la dispara alerta. | §6.1 |
| 3 | **C** | Lastro pulverizado espalha o risco em muitos devedores pequenos, gerando volume de dados. | §6.1 |
| 4 | **D** | O cedente vende os recebíveis; o sacado é quem deve. | §6.1 |
