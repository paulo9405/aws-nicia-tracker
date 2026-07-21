# CORREÇÃO DE PALAVRAS ABREVIADAS — Trilha de Avicultura (Nícia Track)

> **Status:** ✅ **APLICADO em 2026-07-21** aos 8 MASTERs de `ESTUDO_NICIA/` (módulos 15–22), via
> script (1ª ocorrência de cada sigla por capítulo → `termo completo (SIGLA)`). ~88 expansões.
> Este arquivo permanece como **glossário-mestre e regra** para os próximos módulos e para (opcional)
> propagar à base `BASE_AVICULTURA/`.
>
> **Motivo:** o leitor iniciante não entende siglas sem o significado (ex.: "PCR", "IA", "HPAI",
> "RT-PCR"). A correção torna o material acessível.
>
> **Script reutilizável:** `scratchpad/expand_siglas.py` (glossário embutido; pula siglas já com
> parênteses; processa capítulo a capítulo). Rodar de novo é seguro/idempotente.

---

## 1. Regra de negócio (como corrigir — e como escrever daqui pra frente)

**Regra:** na **primeira ocorrência** de uma sigla **em cada capítulo**, escrever o **termo completo
seguido da sigla entre parênteses**; nas ocorrências seguintes do mesmo capítulo, pode usar só a sigla.

- ✅ Forma correta: `Influenza Aviária (IA)` · `reação em cadeia da polimerase (PCR)` ·
  `Influenza Aviária de Alta Patogenicidade (HPAI)` · `PCR via transcrição reversa (RT-PCR)`.
- ❌ Evitar: introduzir "IA", "PCR", "HPAI" sem nunca dizer o que significam.
- **Onde a sigla aparece só uma vez** no capítulo, ainda assim expandir na aparição.
- **Termos já autoexplicativos no texto** (ex.: "Doença de Newcastle (DNC)") só precisam garantir o
  par termo+sigla — o que a maioria já tem.
- **Aplicar em toda a pasta `ESTUDO_NICIA/`** (MASTERs). Opcionalmente propagar à base
  `BASE_AVICULTURA/` numa segunda rodada.

> **⚠️ Vale também para módulos NOVOS:** ao autorar qualquer MASTER novo de avicultura, já escrever a
> sigla expandida na primeira ocorrência (não deixar para corrigir depois).

---

## 2. Glossário-mestre (sigla → significado)

### 2.1 Doenças e vírus
| Sigla | Termo completo (expandir assim) | Observação |
|---|---|---|
| **IA** | Influenza Aviária | "gripe aviária" |
| **HPAI** | Influenza Aviária de Alta Patogenicidade (do inglês *Highly Pathogenic Avian Influenza*) | |
| **LPAI** | Influenza Aviária de Baixa Patogenicidade (*Low Pathogenic Avian Influenza*) | se aparecer |
| **H5, H7, H5N1** | subtipos do vírus Influenza A (H = hemaglutinina; N = neuraminidase) | ex.: H5N1 |
| **DNC** | Doença de Newcastle | |
| **APMV-1** | paramixovírus aviário tipo 1 (*Avian Paramyxovirus type 1*) | agente da Newcastle |
| **BI** | Bronquite Infecciosa | |
| **LTI** | Laringotraqueíte Infecciosa | |
| **IBD** | Doença Infecciosa da Bursa / Gumboro (*Infectious Bursal Disease*) | |
| **CAV** | Anemia Infecciosa das Galinhas (vírus — *Chicken Anemia Virus*) | |
| **EDS** | Síndrome da Queda de Postura (*Egg Drop Syndrome*) | |
| **EA** | Encefalomielite Aviária | |
| **aMPV** | metapneumovírus aviário (*avian Metapneumovirus*) | |
| **SHS** | Síndrome da Cabeça Inchada (*Swollen Head Syndrome*) | associada ao aMPV |
| **MG** | *Mycoplasma gallisepticum* | |
| **MS** | *Mycoplasma synoviae* | |
| **ORT** | *Ornithobacterium rhinotracheale* | |
| **APEC** | *Escherichia coli* patogênica para aves (*Avian Pathogenic E. coli*) | |
| **SDS** | Síndrome da Morte Súbita (*Sudden Death Syndrome*) | |
| **FLKS / FLHS** | Síndrome do Fígado e Rim Gordurosos / Fígado Gorduroso Hemorrágico | deficiência de biotina / esteatose |

### 2.2 Diagnóstico e laboratório
| Sigla | Termo completo | Observação |
|---|---|---|
| **PCR** | reação em cadeia da polimerase (*Polymerase Chain Reaction*) | |
| **RT-PCR** | PCR via transcrição reversa (*Reverse Transcription PCR*) | detecta RNA |
| **qPCR** | PCR quantitativa (em tempo real) | se aparecer |
| **ELISA** | ensaio imunoenzimático (*Enzyme-Linked Immunosorbent Assay*) | |
| **HI** | inibição da hemaglutinação (*Hemagglutination Inhibition*) | |
| **AGID** | imunodifusão em ágar-gel (*Agar Gel Immunodiffusion*) | |
| **SVN** | soroneutralização (*Serum Virus Neutralization*) | |
| **IHQ** | imuno-histoquímica | |
| **HPLC** | cromatografia líquida de alta eficiência | análise de micotoxinas |
| **DNA** | ácido desoxirribonucleico | |
| **RNA** | ácido ribonucleico | |
| **SPF** | livre de patógenos específicos (*Specific Pathogen Free*) | ovos SPF |
| **RODAC** | placa de contato para superfície (*Replicate Organism Detection And Counting*) | |
| **UFC** | unidades formadoras de colônia | ex.: UFC/mL |
| **CV** | coeficiente de variação | uniformidade do lote/sorologia |
| **GI** | gastrointestinal / trato digestório | |
| **CAM** | membrana corioalantoide (*Chorioallantoic Membrane*) | respiração do embrião |

### 2.3 Imunologia e vacinas
| Sigla | Termo completo | Observação |
|---|---|---|
| **MDA** | anticorpos maternos (*Maternally Derived Antibodies*) | |
| **HVT** | herpesvírus de peru (*Herpesvirus of Turkeys*) | vetor vacinal |
| **VP2** | proteína VP2 (antígeno protetor do Gumboro) | ex.: HVT-VP2 |
| **DIVA** | diferenciar animais infectados de vacinados (*Differentiating Infected from Vaccinated Animals*) | |
| **CEO** | vacina de origem em embrião de galinha (*Chicken Embryo Origin*) | vacina viva de LTI |
| **SC** | subcutânea (via de aplicação) | |
| **IM** | intramuscular (via de aplicação) | |
| **EPI** | equipamento de proteção individual | |

### 2.4 Nutrição
| Sigla | Termo completo | Observação |
|---|---|---|
| **EM** | energia metabolizável | |
| **EMA / AMEn** | energia metabolizável aparente (corrigida para nitrogênio) | |
| **TMEn** | energia metabolizável verdadeira (corrigida) | se aparecer |
| **NRC** | *National Research Council* (referência internacional de exigências) | |
| **DON** | desoxinivalenol (micotoxina, "vomitoxina") | |
| **ZEA** | zearalenona (micotoxina) | |
| **T-2** | toxina T-2 (tricoteceno) | |
| **DL-metionina** | mistura dos isômeros D e L da metionina | aminoácido sintético |
| **Ca:P** | relação cálcio:fósforo | |
| **mEq/kg** | miliequivalentes por quilo (balanço eletrolítico) | |
| **ppb / ppm** | partes por bilhão / partes por milhão | limites de contaminantes |

### 2.5 Ambiência e química
| Sigla | Termo completo | Observação |
|---|---|---|
| **UR** | umidade relativa | |
| **CO₂** | dióxido de carbono | |
| **CO** | monóxido de carbono | |
| **NH₃** | amônia | |
| **O₂** | oxigênio | |
| **UV** | ultravioleta | |
| **LED** | diodo emissor de luz (*Light Emitting Diode*) | |
| **kg/m²** | quilos por metro quadrado (densidade) | |
| **cfm / m³/min** | pés cúbicos por minuto / metros cúbicos por minuto (ventilação) | |

### 2.6 Órgãos, legislação e programas
| Sigla | Termo completo | Observação |
|---|---|---|
| **MAPA** | Ministério da Agricultura e Pecuária | |
| **ANVISA** | Agência Nacional de Vigilância Sanitária | |
| **PNSA** | Programa Nacional de Sanidade Avícola | |
| **PNCRC** | Plano Nacional de Controle de Resíduos e Contaminantes | |
| **SVO** | Serviço Veterinário Oficial | |
| **SDA** | Secretaria de Defesa Agropecuária (do MAPA) | |
| **IN** | Instrução Normativa | |
| **RDC** | Resolução de Diretoria Colegiada (ANVISA) | |
| **RIISPOA** | Regulamento da Inspeção Industrial e Sanitária de Produtos de Origem Animal | |
| **GTA** | Guia de Trânsito Animal | |
| **WOAH** | Organização Mundial de Saúde Animal (*World Organisation for Animal Health*; ex-OIE) | |
| **OMS** | Organização Mundial da Saúde | |
| **OMSA** | forma em português/espanhol da WOAH (usada pelo MAPA) | |
| **FAO** | Organização das Nações Unidas para Alimentação e Agricultura | |
| **CDC** | Centros de Controle e Prevenção de Doenças dos EUA | |
| **UE** | União Europeia | |
| **RS** | Rio Grande do Sul (estado) | |
| **MA / SNAD / SFA** | Ministério da Agricultura / Secretaria Nacional de Defesa Agropecuária / Secretaria de Fiscalização Agropecuária | na Portaria 07/1988 |

### 2.7 Hormônios e fisiologia
| Sigla | Termo completo | Observação |
|---|---|---|
| **GnRH** | hormônio liberador de gonadotrofinas | |
| **LH** | hormônio luteinizante | |
| **FSH** | hormônio folículo-estimulante | |
| **SSTs** | túbulos de armazenamento de espermatozoides (*Sperm Storage Tubules*) | |

### 2.8 Siglas de fonte/citação (baixa prioridade — só nas seções "Fontes")
Estas aparecem sobretudo como **referências** e podem ser deixadas como estão ou expandidas 1x:
**MSD/Merck** (Merck Veterinary Manual), **PMC** (PubMed Central), **MDPI**, **IDEXX**, **WATT**,
**IFAS/UF** (Universidade da Flórida), **MSU** (Michigan State University), **DSM**, **SciELO**.

---

## 3. Prioridade de aplicação (quando for aplicar)

1. **Alta (aparecem muito e confundem):** IA, HPAI, PCR, RT-PCR, BI, LTI, CAV, EDS, MDA, HVT, MG/MS,
   ORT, CV, ELISA, HI, SC/IM, EM/AMEn, UR, CO₂/NH₃.
2. **Média:** DNC, APMV-1, IBD, aMPV/SHS, SDS, DIVA, CEO, SPF, DON/ZEA/T-2, PNSA, WOAH, SVO, EPI.
3. **Baixa:** siglas de fonte (seção 2.8), H5/H7 (já vêm com contexto), unidades (ppm/ppb/kg/m²).

## 4. Como será a execução (checklist para a rodada de correção)
- [ ] Para cada MASTER em `ESTUDO_NICIA/`, achar a 1ª ocorrência de cada sigla por capítulo e expandir.
- [ ] Conferir se a expansão não quebra tabelas/flashcards (manter conciso).
- [ ] Rodar `import_avicultura` para repopular o conteúdo no banco.
- [ ] (Opcional) Propagar à base `BASE_AVICULTURA/`.
- [ ] Deploy (Local → AWS) conforme o fluxo.

> **Contagem no diagnóstico (2026-07-21):** ~55 siglas reais identificadas em 8 MASTERs. As mais
> frequentes: IA (19), PCR (17), CV (15), BI (15), MDA (14), CAV (14), RT-PCR (11), EDS (10), LTI (9),
> HVT (9), MG (8), HPAI (6).
