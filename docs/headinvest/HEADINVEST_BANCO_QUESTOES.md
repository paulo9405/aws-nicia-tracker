# BANCO DE QUESTÕES — TRILHA HEADINVEST (NÍCIA TRACK)

> **Uso:** fonte do importador `import_headinvest_questions` (trilha separada do concurso e da avicultura).
> Todas as seções mapeiam para o **Subject único da trilha** (`headinvest-guia`), criado por
> `import_headinvest` — ver `HEADINVEST_QUESTION_MAP` no comando. As seções abaixo espelham as 6 aulas
> apenas para clareza de autoria; no mini-quiz elas formam um **pool único** da trilha.
>
> **Formato** (reaproveita o parser do banco mestre): questões com 4 alternativas **A–D**, uma correta,
> seguidas da tabela de gabarito. **Não** colocar `---` entre a última questão e o cabeçalho de gabarito.
>
> **Rastreabilidade:** questões derivadas de `docs/headinvest/HEADINVEST_MASTER.md`. A coluna
> "Ref. MASTER" aponta a seção de origem (§). Não cria fatos novos.

# SEÇÃO 1 — HeadInvest: A empresa e o negócio
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Em uma frase, o que **melhor descreve** a HeadInvest?
A) Um banco de varejo focado em crédito consignado ao público geral
B) Uma gestora de recursos independente focada em crédito estruturado (FIDCs e crédito imobiliário)
C) Uma corretora de valores especializada em trading de alta frequência
D) Uma securitizadora que apenas emite CRIs para o mercado

**2.** Qual é a **principal receita recorrente** de uma gestora como a HeadInvest?
A) Taxa de performance sobre o que exceder o CDI
B) Spread de compra e venda de ações
C) Taxa de administração/gestão, um percentual ao ano sobre o AUM
D) Comissão por cada contrato de crédito originado

**3.** A relação entre HeadInvest e **BSI Capital** pode ser resumida como:
A) A HeadInvest estrutura e origina as operações; a BSI gere os fundos
B) A BSI estrutura e origina as operações; a HeadInvest gere os fundos
C) São concorrentes diretas no mesmo mercado
D) A HeadInvest é a administradora fiduciária dos fundos da BSI

**4.** Do ponto de vista de tecnologia, por que crédito estruturado é descrito como "um problema de dados"?
A) Porque exige latência de microssegundos para fechar negócios
B) Porque originar, validar, precificar e monitorar milhares de recebíveis em escala exige software
C) Porque o principal desafio é a interface gráfica para investidores
D) Porque depende essencialmente de planilhas manuais atualizadas à mão

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 1
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | Gestora independente de crédito estruturado — FIDCs e crédito imobiliário (CRIs). | §1.1 |
| 2 | **C** | Receita recorrente principal é a taxa sobre o AUM; performance é complementar. | §1.2 |
| 3 | **B** | BSI estrutura/origina; HeadInvest gere os fundos — sinergia declarada. | §1.1 |
| 4 | **B** | Lastro pulverizado gera volume; automação da esteira e do monitoramento é obrigatória. | §1.1 |

---

# SEÇÃO 2 — HeadInvest: Fluxo e produtos
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** As **4 etapas** do fluxo do negócio, na ordem correta, são:
A) Análise → Originação → Monitoramento → Implementação
B) Originação → Análise/Modelagem → Implementação → Monitoramento
C) Monitoramento → Originação → Análise → Estruturação
D) Originação → Implementação → Monitoramento → Análise

**2.** O que é um **FIDC**?
A) Um fundo cujo patrimônio é composto majoritariamente por recebíveis (direitos creditórios)
B) Um título de dívida bancária emitido diretamente por um banco
C) Um certificado de recebíveis exclusivamente imobiliários
D) Um fundo que só investe em ações de empresas de crédito

**3.** Numa estrutura típica de FIDC, a **cota subordinada**:
A) Tem a menor exposição a risco e retorno-alvo garantido
B) É negociada apenas na B3 em tempo real
C) Absorve as primeiras perdas, funcionando como colchão que protege a cota sênior
D) Representa a dívida do cedente perante o custodiante

**4.** O fundo **HEAD Crédito ao Trabalhador FIDC** tem como lastro o consignado privado, que se caracteriza por:
A) Alta inadimplência e fluxo de caixa imprevisível
B) Empréstimo descontado direto do salário de CLT, com fluxo de caixa previsível
C) Recebíveis do agronegócio com sazonalidade forte
D) Aluguéis comerciais de longo prazo

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 2
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | Originação → Análise/Modelagem → Implementação → Monitoramento (as 4 etapas do site). | §2.1 |
| 2 | **A** | FIDC = Fundo de Investimento em Direitos Creditórios; patrimônio são recebíveis. | §2.2 |
| 3 | **C** | Subordinada absorve as primeiras perdas e protege a sênior (margem de segurança). | §2.2 |
| 4 | **B** | Consignado privado é descontado do salário CLT — baixa inadimplência, fluxo previsível. | §2.2 |

---

# SEÇÃO 3 — HeadInvest: Onde a tecnologia entra
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Por que Python encaixa bem no trabalho de uma gestora de crédito estruturado?
A) Porque garante latência de microssegundos, essencial nesse negócio
B) Porque o trabalho é dado + regra + cálculo + integração, com foco em correção e rastreabilidade
C) Porque elimina a necessidade de banco de dados relacional
D) Porque substitui totalmente os requisitos de compliance

**2.** A chamada **"esteira de recebíveis"** é, em essência:
A) Uma esteira física de transporte de documentos no escritório
B) Um relatório mensal enviado à CVM
C) Um motor de elegibilidade que valida cada recebível segundo as regras do regulamento do fundo
D) Um dashboard de marketing para investidores

**3.** Ao lidar com valores financeiros em código, a prática recomendada é:
A) Usar `float` por ser mais rápido
B) Usar `Decimal`, nunca `float`, para evitar erros de arredondamento
C) Armazenar tudo como texto e converter na exibição
D) Usar números inteiros de centavos sem qualquer padronização

**4.** Por que se diz que **compliance é um driver técnico**, não apenas burocracia?
A) Porque impede qualquer automação de processos
B) Porque exige apenas documentação em PDF, sem impacto no software
C) Porque vira requisitos de sistema: trilhas de auditoria, controle de acesso e logs imutáveis
D) Porque é responsabilidade exclusiva do time jurídico

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 3
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | Dado + regra + cálculo + integração; foco em correção/rastreabilidade, não latência. | §3.1 |
| 2 | **C** | Esteira = motor de elegibilidade que aplica as regras do regulamento a cada recebível. | §3.2 |
| 3 | **B** | Precisão monetária: sempre `Decimal`, nunca `float`. | §3.2 |
| 4 | **C** | Compliance vira requisito de software: auditoria, controle de acesso, logs imutáveis. | §3.1 |

---

# SEÇÃO 4 — HeadInvest: Preparação para a entrevista
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Qual destes assuntos você **NÃO precisa decorar** para a entrevista?
A) O fluxo do negócio (originação a monitoramento)
B) As fórmulas fechadas de TIR/VPL e os números das instruções da CVM
C) Onde a tecnologia entra na operação
D) A relação entre HeadInvest e BSI Capital

**2.** A melhor postura para "impressionar sem parecer que decorou" é:
A) Despejar o máximo de termos financeiros possível
B) Evitar fazer perguntas para não parecer inseguro
C) Fazer uma pergunta curiosa, ouvir de verdade e conectar negócio → processo → tecnologia
D) Focar só em salário e benefícios

**3.** Qual é um **bom exemplo de pergunta** para fazer ao entrevistador?
A) "Qual é o valor exato do AUM e o CNPJ da holding?"
B) "A esteira de elegibilidade dos FIDCs já é automatizada ou ainda tem bastante planilha?"
C) "Vocês pagam hora extra em fechamento de mês?"
D) "Quais ações vocês recomendam comprar agora?"

**4.** No contexto de ingestão de carteiras, **idempotência** significa que:
A) Cada cedente deve enviar dados no mesmo formato
B) Reprocessar o mesmo arquivo não pode duplicar posições
C) O sistema deve rodar apenas uma vez por ano
D) Os dados devem ser apagados após cada importação

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 4
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | Não decore fórmulas de TIR/VPL nem números de instruções; saiba o que significam. | §4.2 |
| 2 | **C** | Curiosidade genuína e a ponte negócio → processo → tecnologia valem mais que jargão. | §4.3 |
| 3 | **B** | Perguntar sobre automação da esteira e gargalos mostra interesse real e técnico. | §4.1 |
| 4 | **B** | Idempotência: reprocessar o mesmo arquivo não duplica posições. | §3.2 |

---

# SEÇÃO 5 — HeadInvest: Conectando com a sua experiência
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** Como **multi-tenant** se conecta ao contexto da HeadInvest?
A) Isolamento entre fundos (ou cedentes/clientes) — segregação que também é requisito de compliance
B) Aumento da latência de processamento
C) Substituição do banco de dados por planilhas
D) Eliminação da necessidade de relatórios

**2.** Um bom uso de **jobs agendados** nesse negócio seria:
A) Enviar e-mails de marketing para novos investidores
B) Recalcular risco/aging diariamente e disparar alertas de covenant ou atraso
C) Reiniciar o servidor toda madrugada por precaução
D) Gerar aleatoriamente novas operações de crédito

**3.** Sobre os "primeiros meses" (hipótese) de um backend recém-contratado, o princípio recomendado é:
A) Propor uma grande reescrita da stack logo na primeira semana
B) Entregar valor incremental com baixo risco antes de grandes reescritas — confiança primeiro
C) Evitar adicionar testes para não atrasar entregas
D) Automatizar tudo de uma vez, sem mapear o fluxo real

**4.** Onde **OCR/IA** agrega valor na operação?
A) Substituindo completamente a análise humana de crédito
B) Extraindo dados de contratos, CCBs e laudos, sempre com validação humana
C) Precificando ações em tempo real
D) Gerando os regulamentos jurídicos dos fundos automaticamente

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 5
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **A** | Multi-tenant = isolamento entre fundos; segregação é também requisito de compliance. | §5.1 |
| 2 | **B** | Monitoramento: recálculo diário de risco/aging e alertas de covenant/atraso. | §5.1 |
| 3 | **B** | Valor incremental com baixo risco antes de reescritas — confiança primeiro, escala depois. | §5.2 |
| 4 | **B** | OCR/IA extrai dados de documentos, com validação humana no laço. | §5.1 |

---

# SEÇÃO 6 — HeadInvest: Glossário e revisão rápida
### 4 questões | Base: `HEADINVEST_MASTER.md`

**1.** O que significa **AUM**?
A) O lucro anual da gestora
B) O total de recursos sob gestão (Assets Under Management)
C) A taxa de administração cobrada
D) O número de fundos ativos

**2.** Um **covenant** é:
A) O nome da cota sênior de um FIDC
B) Um relatório enviado ao investidor
C) Uma cláusula que o devedor deve manter; violá-la dispara alerta ou consequência
D) A taxa de performance do fundo

**3.** A estratégia de **lastro pulverizado** significa:
A) Concentrar o risco em poucos grandes devedores
B) Espalhar o risco em muitos devedores pequenos, o que aumenta o volume de dados
C) Investir apenas em títulos públicos
D) Eliminar totalmente o risco de inadimplência

**4.** A diferença entre **cedente** e **sacado** é:
A) Cedente e sacado são o mesmo participante
B) O cedente vende os recebíveis ao fundo; o sacado é quem deve o recebível
C) O sacado vende os recebíveis; o cedente é a administradora
D) Ambos são cotistas do fundo

### 🔑 GABARITO E COMENTÁRIOS — SEÇÃO 6
| Q | Gab | Comentário resumido | Ref. MASTER |
|---|-----|---------------------|-------------|
| 1 | **B** | AUM = Assets Under Management, total sob gestão; métrica-chave de tamanho. | §6.1 |
| 2 | **C** | Covenant = cláusula que o devedor mantém; violação dispara alerta (gancho de automação). | §6.1 |
| 3 | **B** | Lastro pulverizado espalha o risco em muitos devedores pequenos → volume de dados. | §6.1 |
| 4 | **B** | Cedente vende os recebíveis; sacado é quem deve. | §6.1 |
