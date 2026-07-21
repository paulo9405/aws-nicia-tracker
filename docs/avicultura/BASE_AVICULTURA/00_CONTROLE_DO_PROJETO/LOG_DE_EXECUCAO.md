# LOG DE EXECUÇÃO

Registro cronológico das etapas. Ao final de cada etapa: data, módulo, arquivos criados/modificados,
fontes principais, decisões, dificuldades, pendências e próximo passo.

---

## 2026-07-20 — Etapa 0: Estrutura de controle

- **Módulo trabalhado:** 00 — Controle do Projeto.
- **Arquivos criados:**
  - Estrutura completa de 20 diretórios em `BASE_AVICULTURA/`.
  - `00_CONTROLE_DO_PROJETO/README.md`
  - `00_CONTROLE_DO_PROJETO/PLANO_MESTRE.md`
  - `00_CONTROLE_DO_PROJETO/STATUS_DA_PESQUISA.md`
  - `00_CONTROLE_DO_PROJETO/FONTES_GERAIS.md`
  - `00_CONTROLE_DO_PROJETO/PENDENCIAS_E_LACUNAS.md`
  - `00_CONTROLE_DO_PROJETO/LOG_DE_EXECUCAO.md`
- **Fontes consultadas:** nenhuma (etapa estrutural).
- **Decisões:** seguir a estrutura de 19 módulos + controle conforme `plano_pesquisa.md`;
  registrar fontes em `FONTES_GERAIS.md` apenas após consulta efetiva; adotar 2026-07-20 como
  data de acesso corrente.
- **Dificuldades:** nenhuma.
- **Pendências:** nenhuma.
- **Próximo passo:** planejamento e pesquisa do Módulo 1 — Panorama da Avicultura.

---

## 2026-07-20 — Etapa 1: Módulo 1 — Panorama da Avicultura

- **Módulo trabalhado:** 01 — Panorama da Avicultura.
- **Arquivos criados:**
  - `01_HISTORIA_E_EVOLUCAO.md`
  - `02_AVICULTURA_BRASILEIRA.md`
  - `03_CADEIA_PRODUTIVA.md`
  - `04_SISTEMAS_DE_PRODUCAO.md`
  - `05_CATEGORIAS_GENETICAS_E_PRODUTIVAS.md`
  - `CHECKLIST_DE_COBERTURA.md`
- **Fontes principais consultadas (efetivamente abertas):**
  - FONTE-ABPA-001 (Relatório Anual 2026 / dados 2025, via reprodução Portal AgroMais);
  - FONTE-EMBRAPA-001 (Cadeia Produtiva do Frango de Corte, PDF Infoteca);
  - FONTE-AKECI-001 (pirâmide de produção);
  - FONTE-CERTHUMANE-001 (sistemas de produção de ovos);
  - FONTE-EMBRAPA-002 (portal Embrapa, via síntese de busca).
- **Decisões:**
  - Registrar dados da ABPA como "via reprodução" por a página primária ter truncado;
  - marcar números ilustrativos da pirâmide como não universais;
  - remeter detalhamento a módulos específicos (3, 6, 7, 12, 14) via referência cruzada.
- **Dificuldades:** truncamento das páginas da ABPA; host da Ageitec (agencia.cnptia.embrapa.br)
  não resolveu; artigo O Presente Rural retornou HTTP 403.
- **Pendências:** P-001 a P-007 (ver `PENDENCIAS_E_LACUNAS.md`).
- **Qualidade da cobertura:** boa nos tópicos econômicos e de cadeia/pirâmide; lacunas históricas
  (domesticação, cronologia mundial, incubação artificial) registradas.
- **Próximo passo recomendado:** confirmar dados primários da ABPA (P-001/P-002) OU avançar para
  o Módulo 2 (Anatomia, Fisiologia e Imunologia) — aguardando definição do usuário.

---

## 2026-07-20 — Etapa 2: Módulo 2 — Anatomia, Fisiologia e Imunologia

- **Módulo trabalhado:** 02 — Anatomia, Fisiologia e Imunologia.
- **Arquivos criados (13 + checklist):** 01_SISTEMA_DIGESTORIO, 02_SISTEMA_RESPIRATORIO,
  03_SISTEMA_REPRODUTIVO, 04_SISTEMA_CARDIOVASCULAR, 05_SISTEMA_NERVOSO, 06_SISTEMA_URINARIO,
  07_SISTEMA_LOCOMOTOR, 08_TERMORREGULACAO, 09_FORMACAO_DO_OVO, 10_FISIOLOGIA_REPRODUTIVA,
  11_IMUNOLOGIA_AVIARIA, 12_DESENVOLVIMENTO_EMBRIONARIO, 13_IMUNIDADE_MATERNA, CHECKLIST_DE_COBERTURA.
- **Fontes principais (abertas/consultadas):** Poultry Extension (digestório, imune, reprodutivo);
  Frontiers 2022 e APS 2014 (respiratório); Univ. Kentucky/MSU/Ohio (ovo); PMC (pneumaticidade,
  estresse térmico, timo/bursa, in ovo feeding, CAM); jpsad (imunologia); ScienceDirect/npj
  Vaccines/PMC (imunidade materna). Registradas em FONTES_GERAIS (FONTE-EXTENSION-001/002,
  ARTIGO-001 a 008, LAFEBER-001, HEATSTRESS-001).
- **Decisões:**
  - dividir reprodução em anatomia (03) / formação do ovo (09) / fisiologia (10), com referência
    cruzada ao Módulo 6 para o enfoque produtivo;
  - manter o **desenvolvimento embrionário dia a dia** no Módulo 7 (aqui só fundamentos/membranas);
  - priorizar profundidade em imunologia (11) e imunidade materna (13) por ligarem à vacinação.
- **Dificuldades:** PDF "Avian Embryo" (MSU) ilegível (binário); página de extensão do respiratório
  retornou 404 (contornado com artigos científicos).
- **Pendências:** P-008 a P-012 (ver `PENDENCIAS_E_LACUNAS.md`).
- **Qualidade da cobertura:** alta nos sistemas de maior impacto clínico (digestório, respiratório,
  imune, reprodutivo) e na imunidade materna; sistemas cardiovascular/nervoso/urinário em nível de
  panorama com valores fisiológicos a confirmar.
- **Próximo passo recomendado:** avançar para um módulo de **prioridade máxima** — sugestão:
  **Módulo 9 (Doenças)** ou **Módulo 4 (Nutrição)** — ou seguir a ordem numérica (Módulo 3 —
  Genética). Aguardando definição do usuário.

---

## 2026-07-20 — Etapa 3: Módulo 4 — Nutrição (prioridade máxima)

- **Módulo trabalhado:** 04 — Nutrição.
- **Arquivos criados (11 + checklist):** 01_FUNDAMENTOS_DA_NUTRICAO, 02_AGUA, 03_ENERGIA_E_LIPIDIOS,
  04_PROTEINAS_E_AMINOACIDOS, 05_VITAMINAS, 06_MINERAIS, 07_FORMULACAO_DE_RACOES,
  08_ALIMENTACAO_POR_CATEGORIA, 09_MICOTOXINAS, 10_ADSORVENTES_E_CONTROLE,
  11_DEFICIENCIAS_E_DIAGNOSTICO_DIFERENCIAL, CHECKLIST_DE_COBERTURA.
- **Fontes principais (abertas):** Merck Veterinary Manual (exigências, deficiências de vitaminas e
  minerais — padrão-ouro); SciELO (Micotoxinas e Micotoxicoses na Avicultura); The Poultry Site +
  PMC (água); DSM (micotoxinas, comercial, com cautela); Rostagno 2024 (referência nacional, paga —
  consultada via descrição editorial). Registradas: FONTE-MERCK-001, ROSTAGNO-001, AGUA-001,
  SCIELO-001, DSM-001.
- **Decisões:**
  - dar profundidade elevada a vitaminas/minerais/micotoxinas (deficiências) por serem a
    dificuldade da profissional;
  - construir `11_DEFICIENCIAS_E_DIAGNOSTICO_DIFERENCIAL.md` como matriz de sinal/lesão × causa
    nutricional × diferencial infeccioso (fecha no Módulo 9);
  - manter os valores numéricos (energia/proteína/aa) como **orientativos** (Merck/NRC), remetendo a
    Rostagno 2024 e manuais para os valores atuais por linhagem.
- **Dificuldades:** Aviagen Water Quality (PDF) ilegível; Tabelas Rostagno são publicação paga
  (valores integrais não acessados).
- **Pendências:** P-013 a P-017 (Rostagno pago; limites de água; limites regulatórios de
  micotoxinas → Módulo 14; valores por linhagem; ressalva a fonte comercial de adsorventes).
- **Qualidade da cobertura:** alta em deficiências e micotoxinas (fontes fortes); valores
  quantitativos de exigência dependem de fonte paga (pendência que não impede o uso qualitativo).
- **Próximo passo recomendado:** **Módulo 9 (Doenças)** — prioridade máxima e maior dificuldade;
  será feito em vários sub-blocos (planejamento + doenças virais primeiro). Aguardando definição.

---

## 2026-07-20 — Etapa 4: Módulo 9 — Doenças (sub-bloco 1/5)

- **Módulo trabalhado:** 09 — Doenças (início; construção em sub-blocos).
- **Arquivos criados:** 00_INDICE_E_ORGANIZACAO.md; TEMPLATE_DOENCA.md (54 itens);
  V01_INFLUENZA_AVIARIA.md; V02_NEWCASTLE.md; V03_GUMBORO_IBD.md; CHECKLIST_DE_COBERTURA.md.
- **Fontes principais (abertas):** MSD/Merck Veterinary Manual (Newcastle, IA, Gumboro); WOAH;
  The Poultry Site; PMC. Registradas: FONTE-MERCK-002, WOAH-001, POULTRYSITE-001.
- **Decisões:**
  - dupla organização (etiologia + síndrome/sistema) com convenção de nomes (V/B/P/F/M);
  - priorizar no sub-bloco 1 as **2 doenças de notificação obrigatória** (IA e Newcastle) + a
    principal **imunossupressora** (Gumboro), pela relevância e ligação com Módulos 2/10/14;
  - registrar honestamente incertezas (ex.: transmissão vertical de Newcastle "disputable").
- **Dificuldades:** nenhuma técnica; volume do módulo exige continuação em sub-blocos.
- **Pendências:** P-018 (lista oficial de notificação → Módulo 14); P-019 (estatísticas atuais de
  HPAI → confirmar em boletins oficiais); P-020 (módulo em construção — ~47 doenças + 14 matrizes
  pendentes).
- **Qualidade da cobertura:** alta nas 3 doenças feitas (estrutura de 54 itens, fontes fortes).
- **Próximo sub-bloco (2) sugerido:** virais respiratórias/nervosas — Bronquite Infecciosa, Marek,
  Laringotraqueíte, Encefalomielite, EDS. Aguardando definição do usuário.

---

## 2026-07-20 — Etapa 5: Módulo 9 — Doenças (sub-bloco 2/5)

- **Módulo trabalhado:** 09 — Doenças (virais respiratórias/nervosas/reprodutivas).
- **Arquivos criados (5):** V04_BRONQUITE_INFECCIOSA; V05_MAREK; V06_LARINGOTRAQUEITE;
  V07_ENCEFALOMIELITE_AVIARIA; V08_EDS_QUEDA_DE_POSTURA.
- **Fontes principais (abertas):** MSD/Merck Vet Manual (IB, Marek, ILT, AE, EDS); PMC (revisões de
  IBV e ILT); The Poultry Site. Já registradas (MERCK-002, WOAH-001, POULTRYSITE-001).
- **Decisões:**
  - priorizar doenças com **impacto reprodutivo/embrionário** (BI e EDS → ovo/casca; EA → transmissão
    vertical e mortalidade embrionária) por alinharem ao foco da profissional;
  - detalhar o **diferencial Marek × Leucose Linfoide** (tabela) por ser ponto clássico;
  - marcar Leucose como coberta em nível de DD dentro de V05 (arquivo próprio ainda pendente).
- **Dificuldades:** período de incubação exato de LTI não confirmado (P-021).
- **Pendências:** P-020 atualizada (8/14 virais); P-021 (incubação LTI).
- **Qualidade da cobertura:** alta (estrutura de 54 itens; fontes fortes). Total do módulo: 8 virais.
- **Próximo sub-bloco (3) sugerido:** fechar virais restantes (Bouba, CAV, Reovírus, Metapneumovírus,
  Leucose, Reticuloendoteliose) e/ou iniciar **bacterianas** (salmoneloses, colibacilose,
  micoplasmoses, coriza, cólera, ORT). Aguardando definição do usuário.

---

## 2026-07-20 — Etapa 6: Módulo 9 — Doenças (sub-bloco 3a: fecha virais)

- **Módulo trabalhado:** 09 — Doenças (virais restantes).
- **Arquivos criados (6):** V09_BOUBA_AVIARIA; V10_ANEMIA_INFECCIOSA_CAV; V11_REOVIRUS_ARTRITE_VIRAL;
  V12_METAPNEUMOVIRUS; V13_LEUCOSE_AVIARIA; V14_RETICULOENDOTELIOSE.
- **Resultado:** **14/14 doenças virais concluídas** (V01–V14).
- **Fontes principais (abertas/consultadas):** MSD/Merck Vet Manual (fowlpox, CAV, viral arthritis,
  aMPV, Marek/leucose, reticuloendoteliose); WOAH (fowlpox); ScienceDirect/PMC (reovírus vertical,
  aMPV, ALV-J vertical, coinfecção REV+Marek no Brasil). Já registradas nas fontes do módulo.
- **Decisões:**
  - agrupar as neoplásicas (Marek/Leucose/Reticuloendoteliose) com diferenciação cruzada explícita
    (idade, bursa, nervos, tipo de célula, agente);
  - destacar as de **transmissão vertical** (CAV, Reovírus, Leucose, Reticuloendoteliose, EA, EDS)
    para alimentar o futuro `DOENCAS_COM_TRANSMISSAO_VERTICAL.md`.
- **Dificuldades:** períodos de incubação de LTI/Bouba em faixas (P-021).
- **Pendências:** P-022 (bacterianas, parasitárias, fúngicas, metabólicas + 14 matrizes).
- **Qualidade:** alta; estrutura de 54 itens mantida.
- **Próximo sub-bloco (3b) sugerido:** **bacterianas** — salmoneloses (Pullorum/Gallinarum/
  paratíficas), colibacilose, micoplasmoses (MG/MS), coriza, cólera aviária, ORT, clostridioses,
  Campylobacter. Aguardando definição do usuário.

---

## 2026-07-20 — Etapa 7: Módulo 9 — Doenças (sub-bloco 3b: bacterianas)

- **Módulo trabalhado:** 09 — Doenças (bacterianas).
- **Arquivos criados (9):** B01_PULOROSE_E_TIFO; B02_SALMONELOSES_PARATIFICAS; B03_COLIBACILOSE;
  B04_MICOPLASMOSES; B05_CORIZA_INFECCIOSA; B06_COLERA_AVIARIA; B07_ORT;
  B08_ENTERITE_NECROTICA_CLOSTRIDIOSES; B09_OUTRAS_BACTERIANAS (Campylobacter, Staph, Enterococcus,
  Gallibacterium).
- **Resultado:** todos os **agentes bacterianos do plano** cobertos (14/14 virais + bacterianas).
- **Fontes principais (abertas):** Merck Vet Manual (Pullorum, colibacilose, enterite necrótica,
  MS); WOAH (fowl typhoid/pullorum); PMC (colibacilose+salmonelose, Gallibacterium, coriza,
  Campylobacter, C. perfringens). Já refletidas nas fontes do módulo.
- **Decisões:**
  - agrupar Pullorum+Gallinarum (B01) e as paratíficas móveis (B02) separadamente por diferirem em
    hospedeiro-especificidade, transmissão e **saúde pública**;
  - reunir Campylobacter/Staph/Enterococcus/Gallibacterium em B09 (panorama), com nota de que podem
    virar arquivos próprios em revisão futura;
  - reforçar as de **transmissão vertical/PNSA** (Pullorum, micoplasmoses) por alinharem ao foco de
    matrizes/incubatório.
- **Dificuldades:** cólera e parte de B09 consolidados via síntese de busca (P-023).
- **Pendências:** P-022 atualizada; P-023 (confirmar detalhes de B06/B09 em Merck).
- **Qualidade:** alta nas de maior relevância (salmoneloses, micoplasmoses, colibacilose, EN);
  panorama sólido nas demais.
- **Próximo sub-bloco (4) sugerido:** **parasitárias** (coccidiose — prioritária —, histomonose,
  helmintos, ácaros, piolhos) + **fúngicas** (aspergilose, candidíase) + **metabólicas**. Aguardando
  definição.

---

## 2026-07-20 — Etapa 8: Módulo 9 — Doenças (sub-bloco 4: parasitárias/fúngicas/metabólicas)

- **Módulo trabalhado:** 09 — Doenças.
- **Arquivos criados (8):** P01_COCCIDIOSE; P02_HISTOMONOSE; P03_HELMINTOS; P04_ECTOPARASITAS;
  F01_ASPERGILOSE; F02_CANDIDIASE; M01_ASCITE_MORTE_SUBITA_ESTEATOSE;
  M02_DISTURBIOS_OSSEOS_HIPOCALCEMIA_PROLAPSO.
- **Resultado:** **todas as doenças individuais do Módulo 9 concluídas** (14 virais + 9 bacterianas
  + 4 parasitárias + 2 fúngicas + 2 metabólicas). Nutricionais/micotoxicoses por referência cruzada
  ao Módulo 4.
- **Fontes principais (abertas):** MSD/Merck (coccidiose, histomonose, helmintíase, aspergilose,
  candidíase, ascite); FDA (blackhead); PMC (ácaro vermelho, Aspergillus); ScienceDirect (ascite,
  coccidiose). 
- **Decisões:**
  - agrupar helmintos (P03) e ectoparasitas (P04) por grupo; metabólicos em 2 arquivos temáticos;
  - reforçar ligações: coccidiose→enterite necrótica (B08); Heterakis→histomonose (P02);
    aspergilose (infecção) ≠ micotoxicose (Módulo 4); metabólicos ↔ nutrição (Módulo 4).
- **Dificuldades:** FLHS/cage layer fatigue/prolapso e restrições legais (nitroimidazóis) via síntese
  (P-024).
- **Pendências:** P-024 (fontes/legislação de metabólicos e antiparasitários).
- **Qualidade:** alta na coccidiose/histomonose/aspergilose; panorama sólido nos grupos.
- **Próximo sub-bloco (5) — ÚLTIMO do Módulo 9:** os **14 arquivos comparativos/matrizes** de
  diagnóstico diferencial (respiratório, digestório, neurológico, locomotor, reprodutivo, queda de
  postura, mortalidade embrionária, transmissão vertical, imunossupressoras, notificação, zoonoses,
  e as 3 matrizes sinais/lesões/amostras × doenças). Aguardando definição.

---

## 2026-07-20 — Etapa 9: Módulo 9 — Doenças (sub-bloco 5: matrizes) → MÓDULO CONCLUÍDO

- **Módulo trabalhado:** 09 — Doenças (arquivos comparativos/diagnóstico diferencial).
- **Arquivos criados (14):** DIAGNOSTICO_DIFERENCIAL_{RESPIRATORIO, DIGESTORIO, NEUROLOGICO,
  LOCOMOTOR, REPRODUTIVO, DE_QUEDA_DE_POSTURA, DE_MORTALIDADE_EMBRIONARIA}; DOENCAS_COM_TRANSMISSAO_
  VERTICAL; DOENCAS_IMUNOSSUPRESSORAS; DOENCAS_DE_NOTIFICACAO_OBRIGATORIA; ZOONOSES_AVICOLAS;
  MATRIZ_SINAIS_CLINICOS_X_DOENCAS; MATRIZ_LESOES_X_DOENCAS; MATRIZ_AMOSTRAS_X_DIAGNOSTICOS.
- **Método:** **síntese sem nova pesquisa** — cruzamento dos 31 arquivos de doença já sourced; cada
  matriz remete aos arquivos-fonte (que citam Merck/MSD/WOAH/PMC).
- **Decisões:**
  - toda matriz traz **observação distintiva** (não só marcação), conforme regra do plano;
  - reforço das apresentações do foco da profissional (queda de postura, mortalidade embrionária,
    transmissão vertical);
  - `DOENCAS_DE_NOTIFICACAO_OBRIGATORIA` marcada com alerta para **verificar norma vigente** (P-018).
- **Resultado do MÓDULO 9:** **CONCLUÍDO PARCIALMENTE** (essencialmente completo) — 47 arquivos:
  índice + template + 31 doenças + 14 matrizes + checklist.
- **Pendências remanescentes:** P-018 (lista oficial de notificação — Módulo 14), P-019 (dados HPAI),
  P-021/P-023/P-024 (detalhes finos de algumas doenças); lacuna: **botulismo** sem arquivo próprio.
- **Qualidade:** o "coração" diagnóstico (matrizes) entrega ao público-alvo o diferencial que era a
  maior dificuldade dela, com rastreabilidade aos arquivos-fonte.
- **Próximo passo recomendado:** escolher entre os demais módulos de **prioridade máxima** ainda
  pendentes — **7 (Incubação)**, **8 (Biossegurança)**, **10 (Programas Vacinais)**, **11
  (Diagnóstico)**, **18 (Patologia/Necropsia)**, **19 (Epidemiologia)** — ou avançar em ordem.
  Aguardando definição do usuário.

---

## 2026-07-20 — Etapa 10: Módulo 7 — Incubação e Incubatórios (prioridade máxima)

- **Módulo trabalhado:** 07 — Incubação e Incubatórios (núcleo do foco da profissional).
- **Arquivos criados (12 + checklist):** 01_ESTRUTURA_E_FLUXO; 02_DESENVOLVIMENTO_EMBRIONARIO_DIA_A_DIA;
  03_PRINCIPIOS_DA_INCUBACAO; 04_TEMPERATURA_UMIDADE_E_VENTILACAO; 05_VIRAGEM_TRANSFERENCIA_E_NASCIMENTO;
  06_PROCESSAMENTO_DOS_PINTINHOS; 07_VACINACAO_NO_INCUBATORIO; 08_QUALIDADE_DE_PINTINHOS;
  09_EXPEDICAO_E_TRANSPORTE; 10_FALHAS_DE_INCUBACAO; 11_EMBRIODIAGNOSTICO; 12_MORTALIDADE_EMBRIONARIA.
- **Fontes principais (abertas):** Alabama Extension (dia a dia — fecha P-010); Pas Reform/Petersime
  (qualidade de pintinho/Pasgar/Tona); Lohmann (single/multi-stage); Poultry Site/Hendrix/EmTech
  (temperatura/umidade/CO₂/ventilação); Merck (vias de vacinação). Registradas: ALABAMA-001,
  PASREFORM-001, INCUB-001, MERCK-003.
- **Decisões:** fechou P-010 (dia a dia); valores de incubação como referências de setor (P-025,
  remeter ao manual); amarrar falhas (10) ↔ embriodiagnóstico (11) ↔ mortalidade embrionária (12)
  ↔ Módulos 4/6/9.
- **Pendências:** P-025 (valores de incubação a confirmar em manual), P-026 (transporte/bem-estar →
  Módulo 14).
- **Qualidade:** alta; entrega o núcleo do trabalho (ovo fértil → pintinho de um dia).
- **Próximo passo recomendado:** prioridade máxima restante — **8 (Biossegurança)**, **10 (Vacinas)**,
  **11 (Diagnóstico)**, **18 (Patologia/Necropsia)**, **19 (Epidemiologia)** — ou **6 (Reprodução)**
  para completar o eixo matriz→ovo→incubação. Aguardando definição.

---

## 2026-07-20 — Etapa 11: Módulo 6 — Reprodução

- **Módulo trabalhado:** 06 — Reprodução (completa o eixo matriz→ovo→incubação→pintinho).
- **Arquivos criados (8 + checklist):** 01_FISIOLOGIA_REPRODUTIVA (aplicada); 02_MANEJO_DE_MATRIZES;
  03_MANEJO_DE_MACHOS; 04_FERTILIDADE_E_FECUNDACAO; 05_PRODUCAO_DE_OVOS_FERTEIS;
  06_QUALIDADE_DOS_OVOS_FERTEIS; 07_COLETA_ARMAZENAMENTO_E_TRANSPORTE; 08_FALHAS_REPRODUTIVAS.
- **Fontes principais (abertas/consultadas):** Poultry Site/Cobb/MSU/Aviagen (manejo de matrizes/
  machos, fotoestimulação); PMC (SSTs, curva de fertilidade); Lohmann/ScienceDirect (armazenamento
  de ovos). Registradas: BREEDER-001, SST-001, EGGSTORAGE-001.
- **Decisões:** respeitar a referência cruzada com Módulo 2 (base fisiológica) vs Módulo 6
  (aplicação produtiva); distinguir explicitamente **fertilidade ≠ eclodibilidade**.
- **Pendências fechadas:** **P-008** (anatomia do macho) e **P-009 parcial** (persistência de
  fertilidade ~2–3 sem; curva 65–75%→95%→queda 45–54 sem). Restam metas por linhagem (manual).
- **Qualidade:** alta; fecha o percurso completo do foco da profissional.
- **Próximo passo recomendado:** prioridade máxima restante — **8 (Biossegurança)**, **10 (Vacinas)**,
  **11 (Diagnóstico)**, **18 (Patologia/Necropsia)**, **19 (Epidemiologia)**. Aguardando definição.

---

## 2026-07-20 — Etapa 14: Módulo 11 — Diagnóstico (prioridade máxima)

- **Módulo trabalhado:** 11 — Diagnóstico.
- **Arquivos criados (5 + checklist):** 01_ABORDAGEM_DIAGNOSTICA; 02_COLETA_AMOSTRAGEM_E_CADEIA_DE_
  CUSTODIA; 03_METODOS_DIRETOS; 04_SOROLOGIA_E_MONITORAMENTO; 05_INTERPRETACAO_DE_LAUDOS.
- **Fontes principais (abertas):** Wixbio (coleta/submissão); MDPI (abordagem holística); IDEXX/WATT/
  BioChek (interpretação de sorologia). Registradas: DIAG-001, SOROLOGIA-001.
- **Decisões:** ancorar tudo na **correlação** laboratório×sinais×lesões×epidemiologia; tratar o
  número de amostragem como **princípio** (não citar nº estatístico sem fonte/norma — regra do plano);
  remeter necropsia detalhada ao Módulo 18.
- **Pendências:** nº estatístico de amostragem → norma (Módulos 14/19).
- **Qualidade:** alta; entrega o "como confirmar" referenciado no Módulo 9 e a interpretação de laudos
  (falsos +/–, vacinal × campo).
- **Próximo passo recomendado:** prioridade máxima restante — **18 (Patologia/Necropsia)** e **19
  (Epidemiologia)**. Aguardando definição.

---

## 2026-07-20 — Etapa 13: Módulo 10 — Programas Vacinais (prioridade máxima)

- **Módulo trabalhado:** 10 — Programas Vacinais.
- **Arquivos criados (5 + checklist):** 01_TIPOS_DE_VACINA; 02_VIAS_DE_APLICACAO;
  03_INTERFERENCIA_MATERNA_E_TIMING; 04_PRINCIPIOS_DE_PROGRAMAS_VACINAIS; 05_ERROS_E_FALHAS_DE_VACINACAO.
- **Fontes principais (abertas):** Merck (tipos/vias/programas); The Poultry Site (administração/
  auditoria); IFAS/UF (falha vacinal). Registrada: FONTE-VACINA-001.
- **Decisões:** **não criar protocolos vacinais fechados** (regra do plano — sem prescrição
  universal); exemplos marcados como ilustrativos; amarrar com MDA (Módulo 2/13), incubatório
  (Módulo 7/07) e vacinas por doença (Módulo 9).
- **Pendências:** apenas produtos registrados/restrições legais (IA, MG) → Módulo 14.
- **Qualidade:** alta; fecha o tripé doença + biossegurança + vacinação.
- **Próximo passo recomendado:** prioridade máxima restante — **11 (Diagnóstico)**, **18 (Patologia/
  Necropsia)**, **19 (Epidemiologia)**. Aguardando definição.

---

## 2026-07-20 — Etapa 12: Módulo 8 — Biossegurança (prioridade máxima)

- **Módulo trabalhado:** 08 — Biossegurança (escudo sanitário de toda a base).
- **Estruturação:** o plano não fixava lista de arquivos; criados 7 arquivos cobrindo todo o escopo.
- **Arquivos criados (7 + checklist):** 01_CONCEITOS_E_PRINCIPIOS; 02_CONTROLE_DE_ACESSO_E_BARREIRA_
  SANITARIA; 03_LIMPEZA_E_DESINFECCAO; 04_CONTROLE_DE_PRAGAS_E_VETORES; 05_BIOSSEGURANCA_DE_INSUMOS_E_
  AMBIENTE; 06_BIOSSEGURANCA_POR_SETOR; 07_MONITORAMENTO_AUDITORIA_E_CONTINGENCIA.
- **Fontes principais (abertas):** FAO (estrutura bioexclusão/biocontenção, compartimentação);
  Poultry Biosecurity/UConn/Cobb (C&D, vazio sanitário); MDPI/Veterinaria Digital/UGA/MGK (vetores);
  Merck (programa de biossegurança); Hendrix. Registradas: FAO-001, BIOSSEG-001, VETORES-001.
- **Decisões:** organizar pelos três pilares (segregação/trânsito/higiene) + insumos + setores +
  monitoramento; diferenciar rigor por setor (corte<matrizes<avós/incubatório).
- **Pendências:** apenas de **norma oficial** (destino de carcaças/resíduos, amostragem, contingência
  → Módulo 14); sem pendência técnica.
- **Qualidade:** alta; fecha referências pendentes de vários módulos (higiene de incubatório, água,
  Salmonella/Marek/Aspergillus, cama).
- **Próximo passo recomendado:** prioridade máxima restante — **10 (Vacinas)**, **11 (Diagnóstico)**,
  **18 (Patologia/Necropsia)**, **19 (Epidemiologia)**. Aguardando definição.

---

> **Nota:** algumas entradas de log podem aparecer fora de ordem cronológica (inserções por âncora);
> o `STATUS_DA_PESQUISA.md` reflete o estado consolidado e correto de cada módulo.

## 2026-07-20 — Etapa 15: Módulo 18 — Patologia e Necropsia (prioridade máxima)

- **Módulo trabalhado:** 18 — Patologia e Necropsia Avícola.
- **Arquivos criados (6 + checklist):** 01_TECNICA_DE_NECROPSIA; 02_NOMENCLATURA_E_ALTERACOES_POS_MORTE;
  03_LESOES_POR_SISTEMA; 04_COLETA_E_ENVIO_DE_AMOSTRAS; 05_MATRIZ_ORGAO_X_LESAO;
  06_MATRIZES_LESAO_SINAL_AMOSTRA.
- **Fontes principais (abertas):** Poultry Site/Wiley (técnica de necropsia); TVMDL/WikiVet
  (artefatos/autólise/pós-morte); síntese do Módulo 9 (lesões por doença). Registradas:
  NECROPSIA-001, PATOLOGIA-001.
- **Decisões:** as matrizes lesão×doença/sinais×doenças/amostras×diagnósticos já existiam no Módulo
  9 → no Módulo 18 fiz a **matriz órgão×lesão (nova)** + **sinal×lesão (ponte clínica↔patológica)**,
  com referência cruzada; ênfase na distinção **artefato/autólise × lesão**.
- **Pendências:** nenhuma técnica.
- **Qualidade:** alta; ferramenta prática de campo (necropsia sistemática + matrizes de bancada).
- **Estado geral:** concluídos módulos 1, 2, 4, 6, 7, 8, 9, 10, 11, 18 (10/19). Prioridade máxima
  restante: **19 (Epidemiologia)**. Complementares restantes: 3, 5, 12, 13, 14, 15, 16, 17.
- **Próximo passo recomendado:** **19 (Epidemiologia e Medicina Preventiva)**. Aguardando definição.

---

## 2026-07-20 — Etapa 16: Módulo 19 — Epidemiologia e Medicina Preventiva → ÚLTIMO DE PRIORIDADE MÁXIMA

- **Módulo trabalhado:** 19 — Epidemiologia e Medicina Preventiva.
- **Arquivos criados (5 + checklist):** 01_CONCEITOS_E_MEDIDAS; 02_CADEIA_EPIDEMIOLOGICA;
  03_INVESTIGACAO_DE_SURTOS; 04_VIGILANCIA_E_PROGRAMAS; 05_MEDICINA_PREVENTIVA_E_ONE_HEALTH.
- **Fontes principais (abertas):** MSD Vet Manual (princípios de epidemiologia); WOAH (manual de
  investigação de surtos); PMC (vigilância de HPAI). Registradas: EPIDEMIO-001, WOAH-002.
- **Decisões:** integrar como "medicina preventiva" que amarra Módulos 8/9/10/11/13; tratar programas
  oficiais (PNSA) como princípios (norma → Módulo 14); One Health como síntese (detalhe → Módulo 17).
- **Pendências:** norma PNSA → Módulo 14; aprofundamento One Health → Módulo 17.
- **MARCO:** **TODOS os 8 módulos de prioridade máxima concluídos** (4, 7, 8, 9, 10, 11, 18, 19),
  além dos de prioridade alta 2 e 6 e complementar 1. Total: 11/19 módulos.
- **Restam (complementares/alta):** 3 (Genética), 5 (Manejo), 12 (Bem-estar), 13 (Inspeção/Saúde
  Pública), 14 (Legislação), 15 (Gestão da Produção), 16 (Gestão de Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **Módulo 14 (Legislação)** — fecha muitas pendências (P-006, P-015,
  P-018, PNSA, notificação, restrições) — ou **5 (Manejo)** / **13 (Saúde Pública)**. Aguardando definição.

---

## 2026-07-20 — Etapa 17: Módulo 14 — Legislação

- **Módulo trabalhado:** 14 — Legislação (lista fixa de 7 arquivos do plano).
- **Arquivos criados (7 + checklist):** INDICE_DA_LEGISLACAO; DOENCAS_DE_NOTIFICACAO_OBRIGATORIA;
  PNSA; TRANSITO_E_CERTIFICACAO; BIOSSEGURANCA_LEGAL; ANTIMICROBIANOS_E_PRODUTOS_VETERINARIOS;
  PLANOS_OFICIAIS_DE_CONTINGENCIA.
- **Fontes principais (abertas, oficiais):** gov.br/MAPA (notificação; proibições de aditivos); PNSA;
  wikisda/ADAPAR (planos IA/Newcastle); LegisWeb (IN 56/2007). Registradas: MAPA-LEG-001, MAPA-LEG-002.
- **Normas confirmadas em fonte oficial:** IN 56/2007 (PNSA); IN 50/2013 (notificação; IA/Newcastle
  imediata; critérios ≥5%/72h); IN 09/2003, IN 45/2016, IN SDA 01/2020, Portaria SDA/MAPA 1.617/2026
  (antimicrobianos promotores); IN SDA 17/2006 (contingência IA/Newcastle).
- **Decisões:** cada arquivo com **AVISO DE VIGÊNCIA** no topo (regra do plano); números não
  confirmados (GTA, importação, RIISPOA versão, limites de micotoxinas) marcados como "a confirmar".
- **Pendências fechadas:** **P-006** (Lei 10.831/2003 orgânicos) e **P-018** (notificação/contingência).
  **P-015** (limites de micotoxinas) permanece **parcial**.
- **Qualidade:** alta em rastreabilidade legal (fontes oficiais + números de norma), com ressalvas
  honestas de vigência.
- **Estado geral:** 12/19 módulos concluídos (todos de prioridade máxima + 1, 2, 6, 14). Restam
  complementares: 3, 5, 12, 13, 15, 16, 17.
- **Próximo passo recomendado:** **13 (Inspeção e Saúde Pública)** — conecta com Módulo 14 (RIISPOA/
  SIF, Salmonella, RAM) — ou **5 (Manejo)** / **12 (Bem-estar)**. Aguardando definição.

---

## 2026-07-21 — Etapa 18: Módulo 13 — Inspeção e Saúde Pública

- **Módulo trabalhado:** 13 — Inspeção e Saúde Pública.
- **Arquivos criados (5 + checklist):** 01_INSPECAO_RIISPOA_SIF; 02_APPCC_E_AUTOCONTROLE;
  03_SEGURANCA_DO_ALIMENTO; 04_RESIDUOS_E_ANTIMICROBIANOS; 05_ZOONOSES_E_SAUDE_PUBLICA.
- **Fontes principais (abertas):** auditorias CFIA/GOV.UK sobre o Brasil (SIF/RIISPOA Dec. 9013/2017,
  inspeção 100%, condenações); Pew/Food Safety Mag/ScienceDirect (farm-to-fork Salmonella/
  Campylobacter, multi-hurdle, PAA). Registradas: INSPECAO-001, FOODSAFETY-001.
- **Decisões:** amarrar "segurança do alimento começa na produção primária"; cross-ref forte com
  Módulos 9 (zoonoses), 14 (RIISPOA/antimicrobianos) e 19 (One Health) para não duplicar.
- **Pendências:** versão RIISPOA, programas oficiais de Salmonella e **PNCRC** (nº) a confirmar →
  Módulo 14; P-015 (micotoxinas) segue parcial.
- **Qualidade:** alta; APPCC (7 princípios), inspeção SIF e RAM bem cobertos.
- **Estado geral:** 13/19 módulos concluídos. Restam complementares: 3 (Genética), 5 (Manejo), 12
  (Bem-estar), 15 (Gestão Produção), 16 (Gestão Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **5 (Manejo)** — muito prático (ambiência/cama/água/luz/densidade) —
  ou **17 (Temas Atuais)** / **12 (Bem-estar)**. Aguardando definição.

---

## 2026-07-21 — Etapa 19: Módulo 5 — Manejo

- **Módulo trabalhado:** 05 — Manejo.
- **Arquivos criados (7 + checklist):** 01_MANEJO_INICIAL_PINTINHOS; 02_AMBIENCIA; 03_CAMA; 04_AGUA;
  05_LUZ; 06_DENSIDADE; 07_FALHAS_DE_MANEJO.
- **Fontes principais (abertas):** Aviagen (Ross/Cobb Broiler Handbook 2025) — brooding, ventilação
  mínima (0,71 m³/min por 1000; 30s/5min), cama 2–4 cm, crop fill 24h; The Poultry Site. Registrada:
  MANEJO-001.
- **Decisões:** combinar manejo inicial + pintinhos (arquivo 01); água como manejo prático com
  cross-ref ao Módulo 4; `07_FALHAS_DE_MANEJO` como matriz falha→consequência (diferencial não
  infeccioso).
- **Pendências:** valores por linhagem (temperaturas/lux) e **limites legais de densidade/luz** →
  Módulos 12/14.
- **Qualidade:** alta e prática; forte ligação com recepção de pintinhos (Módulo 7) e ambiência/
  sanidade.
- **Estado geral:** 14/19 módulos concluídos. Restam: 3 (Genética), 12 (Bem-estar), 15 (Gestão
  Produção), 16 (Gestão Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **12 (Bem-estar)** ou **17 (Temas Atuais)** ou **15 (Gestão da
  Produção)**. Aguardando definição.

---

## 2026-07-21 — Etapa 20: Módulo 12 — Bem-estar Animal

- **Módulo trabalhado:** 12 — Bem-estar Animal.
- **Arquivos criados (5 + checklist):** 01_CONCEITOS_E_INDICADORES; 02_BEM_ESTAR_NA_PRODUCAO;
  03_MANEJO_PRE_ABATE_CAPTURA_TRANSPORTE; 04_BEM_ESTAR_INCUBATORIO_E_PINTINHOS; 05_EUTANASIA_E_MERCADO.
- **Fontes principais (abertas):** MDPI/Frontiers/Taylor & Francis (Cinco Liberdades, Cinco Domínios,
  indicadores animal-based: gait score, pododermatite, hock burn). Registrada: BEMESTAR-001.
- **Decisões:** organizar por conceitos → produção → pré-abate → incubatório/pintinhos → eutanásia/
  mercado; **não prescrever método de eutanásia** sem norma (regra do plano); tratar descarte de
  machos/sexagem in ovo como tema de mercado (→ Módulo 17).
- **Pendências:** métodos de eutanásia aprovados, limites de densidade/transporte e status do
  descarte de machos → Módulo 14.
- **Qualidade:** alta; forte ligação com Módulos 5 (manejo), 7 (incubatório), 13 (condenações/mercado).
- **Estado geral:** 15/19 módulos concluídos. Restam: 3 (Genética), 15 (Gestão da Produção), 16
  (Gestão de Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **15 (Gestão da Produção)** — consolida os indicadores citados em
  quase todos os módulos — ou **17 (Temas Atuais)** / **3 (Genética)** / **16 (Gestão de Pessoas)**.

---

## 2026-07-21 — Etapa 21: Módulo 15 — Gestão da Produção

- **Arquivos criados (3 + checklist):** 01_INDICADORES_DE_DESEMPENHO_E_POSTURA;
  02_INDICADORES_DE_REPRODUCAO_E_INCUBACAO; 03_ANALISE_DE_DADOS_E_GESTAO.
- **Fontes:** ResearchGate/Mid South Feeds/Vetypedia (FCR, IEP/EPEF, viabilidade). Registrada: KPI-001.
- **Decisões:** dar **fórmulas** (padrão do setor) e interpretação; **não fixar metas** (variam por
  linhagem — confirmar no manual); arquivo 02 é o núcleo do incubatório (fertilidade, eclodibilidade
  total/de férteis, perda de peso, janela, rendimento de pintinho).
- **Estado geral:** 16/19 concluídos. Restam: 3 (Genética), 16 (Gestão de Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **3 (Genética)**, **16 (Gestão de Pessoas)** ou **17 (Temas Atuais)**.

---

## 2026-07-21 — Etapa 22: Módulo 3 — Genética e Melhoramento

- **Arquivos criados (5 + checklist):** 01_CONCEITOS_DE_GENETICA; 02_ESTRUTURA_DA_PIRAMIDE_GENETICA;
  03_EMPRESAS_E_LINHAGENS; 04_FERTILIDADE_E_ECLODIBILIDADE; 05_UNIFORMIDADE_E_CONSANGUINIDADE.
- **Fontes:** IntechOpen/Springer-PMC/Lohmann/Poultry Scales (seleção, herdabilidade, heterose,
  4-way cross, genômica, pirâmide). Registrada: GENETICA-001.
- **Decisões:** dar conceitos e panorama de linhagens **sem fixar metas comerciais** (regra do plano);
  complementar a pirâmide do Módulo 1 com o "porquê genético".
- **Pendência fechada:** **P-004** (pirâmide genética). Metas por linhagem → manuais.
- **Estado geral:** 17/19 concluídos. Restam: 16 (Gestão de Pessoas), 17 (Temas Atuais).
- **Próximo passo recomendado:** **17 (Temas Atuais)** ou **16 (Gestão de Pessoas)** — os dois
  últimos para completar a etapa 1 (19 módulos).

---

## 2026-07-21 — Etapa 23: Módulo 17 — Temas Atuais

- **Arquivos criados (3 + checklist):** 01_HPAI_ONE_HEALTH_E_VACINAS; 02_TECNOLOGIA_E_DIGITALIZACAO;
  03_SUSTENTABILIDADE_MERCADO_E_CLIMA.
- **Fontes (recentes 2025–2026):** WATTPoultry, ASM, The Poultry Site, CDC (HPAI/vacinação);
  MDPI/PMC/Innovate Animal Ag (PLF/IA, sexagem in ovo, One Health/RAM). Registrada: ATUAIS-001.
- **Decisões:** classificar **maturidade** (já utilizada/em expansão/experimental) e citar
  **exemplos reais** (Zoetis H5, Cheggy/Kipster/Austrália, mercado de IA); ressalva de que dados
  atuais mudam rápido — reconfirmar.
- **Estado geral:** 18/19 concluídos. Falta apenas **16 (Gestão de Pessoas)**.
- **Próximo passo recomendado:** **Módulo 16 (Gestão de Pessoas)** — ÚLTIMO módulo; encerra a etapa 1
  (19 módulos).

---

## 2026-07-21 — Etapa 24: Módulo 16 — Gestão de Pessoas → ETAPA 1 CONCLUÍDA (19/19)

- **Arquivos criados (3 + checklist):** 01_TREINAMENTO_E_POPS; 02_CULTURA_DE_BIOSSEGURANCA_E_GESTAO_
  DE_ERROS; 03_LIDERANCA_INTEGRADOS_E_RESPONSABILIDADE.
- **Fonte:** MDPI VetSci 2025 (fatores da adesão à biossegurança; elemento humano). Registrada:
  PESSOAS-001.
- **MARCO:** **TODOS os 19 módulos concluídos.** Criado `REVISAO_FINAL_ETAPA_1.md` com a conferência
  dos 12 critérios de conclusão (seção 15 do plano): **11/12 plenamente atendidos**; critério 5
  (vigência legal) **parcial** (com AVISO DE VIGÊNCIA e itens "a confirmar" — Módulo 14).
- **Totais:** ~187 arquivos .md; 19 checklists; 31 doenças + 14 matrizes; catálogo de fontes e
  pendências (P-001..P-026) atualizados.
- **Pendências remanescentes (não bloqueantes):** vigência legal/PNCRC (Módulo 14, P-015), valores
  por linhagem (não fixados por regra), estatísticas HPAI (P-019), botulismo sem arquivo próprio.
- **Próximo passo:** **Etapa 2** — transformar a base em material de estudo no Nícia Track (quando o
  usuário solicitar). Reconfirmar dados sensíveis (legislação/limites/metas) nas fontes primárias.

---

## 2026-07-21 — Fechamento de pendências: reconfirmação de legislação (Módulo 14)

- **Objetivo:** fechar a ressalva do critério 5 (vigência legal) e a **P-015** (micotoxinas),
  reconfirmando número/data/situação das normas em **fontes oficiais** (gov.br/MAPA, in.gov.br,
  Planalto). Regra mantida: **não inventar**; **aviso de vigência** permanece em todo o Módulo 14.
- **Arquivos modificados (Módulo 14):** `INDICE_DA_LEGISLACAO` (tabela de situação por norma),
  `PNSA` (Portaria SDA 193/1994; IN SDA 78/2003 e 20/2016), `ANTIMICROBIANOS_E_PRODUTOS_VETERINARIOS`
  (Portaria 1.617/2026 com fonte oficial; micotoxinas MAPA/ANVISA), `PLANOS_OFICIAIS_DE_CONTINGENCIA`
  (Portaria SDA 565/2022), `TRANSITO_E_CERTIFICACAO` (IN MAPA 18/2006 — GTA; Dec. 10.468/2020; PNCRC),
  `DOENCAS_DE_NOTIFICACAO_OBRIGATORIA` (IN 50/2013 em fonte primária), `CHECKLIST_DE_COBERTURA`.
- **Confirmações-chave:** Portaria SDA/MAPA **1.617/2026** é norma **oficial real** (antes só imprensa),
  transição de 180 dias, **não revoga** as INs anteriores; IN SDA 17/2006 **alterada pela Portaria SDA
  565/2022**; RIISPOA (Dec. 9.013/2017) **alterado pelo Dec. 10.468/2020**; GTA = **IN MAPA 18/2006**
  (cobre ovos férteis); micotoxinas em ração = **Portaria MAPA 07/1988** (50 ppb aflatoxinas), alimentos
  = **ANVISA RDC 722/2022 + IN 160/2022**; PNCRC = **IN SDA 42/1999**.
- **Pendências fechadas:** **P-015** (micotoxinas). **P-024** passou a **parcial** (nitrofuranos
  confirmados via IN 09/2003; faltam nitroimidazóis/anti-helmínticos).
- **Fontes registradas:** FONTE-MAPA-LEG-003/004, FONTE-INGOV-001, FONTE-PLANALTO-001, FONTE-LAMIC-001,
  FONTE-DEFESASP-001 (`FONTES_GERAIS.md`).
- **Remanescentes (não bloqueantes):** requisitos de **importação** de material genético; **atos de
  biosseguridade** do PNSA; **indenização/repovoamento** na contingência; **valores por matriz** dos
  anexos de micotoxinas; nitroimidazóis/anti-helmínticos (P-024).
- **Próximo passo sugerido:** fechar **botulismo** (Módulo 9) ou **HPAI atual** (P-019).

---

## 2026-07-21 — Fechamento de pendência: Botulismo (Módulo 9, arquivo B10)

- **Objetivo:** criar o arquivo individual de botulismo que faltava no Módulo 9 (única lacuna de
  arquivo de doença) — a 32ª doença individual.
- **Arquivo criado:** `09_DOENCAS/B10_BOTULISMO.md` — estrutura completa dos **54 itens**
  (toxi-infecção/intoxicação clostridial; BoNT tipos C e C/D; "limberneck"; mecanismo de bloqueio da
  acetilcolina; **ausência de lesões** como marca diagnóstica; diagnóstico por **demonstração da
  toxina**; ciclo carcaça–larva; prevenção pela remoção de carcaças).
- **Arquivos atualizados:** `00_INDICE_E_ORGANIZACAO` (lista de bacterianas), `CHECKLIST_DE_COBERTURA`
  (10 bacterianas; 32 doenças; lacuna resolvida), `DIAGNOSTICO_DIFERENCIAL_NEUROLOGICO` (linha B10,
  fecha a lacuna registrada no próprio arquivo), `MATRIZ_SINAIS_CLINICOS_X_DOENCAS` (paralisia flácida
  ascendente).
- **Fontes:** Merck Vet Manual (Botulism in Poultry), WOAH (ficha de botulismo), PubMed/PMC (toxi-
  infecção em frangos; tipos C/D). Registradas: FONTE-MERCK-003, FONTE-WOAH-002, FONTE-PUBMED-BOT-001.
- **Controle atualizado:** STATUS (Módulo 9: 48 arquivos), REVISAO_FINAL (32 doenças; lacuna do
  botulismo resolvida), FONTES_GERAIS.
- **Nota de classificação:** botulismo entrou como **B10** (clostridial/bacteriana). Consciente de que
  é essencialmente uma **intoxicação/toxi-infecção** — registrado assim no próprio arquivo (item 3).
- **Próximo passo sugerido:** **HPAI atual** (P-019) — confirmar estatísticas em WOAH/MAPA/OMS.

---

## 2026-07-21 — Fechamento de pendência: HPAI atual (P-019)

- **Objetivo:** substituir as estatísticas de HPAI "via Merck/PMC" por **números de boletim oficial**
  (OMS/CDC/MAPA), com foco na **situação do Brasil**.
- **Confirmações (fontes oficiais, acesso 2026-07-21):**
  - **Brasil:** **1º e único foco de IAAP em granja comercial** — poedeiras em **Montenegro/RS,
    16/05/2025**; vazio sanitário a partir de 22/05; **autodeclaração de país livre em 18/06/2025**
    (OMSA/WOAH). Impacto: suspensões/regionalizações de compra por dezenas de países (não reabrem
    automático). IAAP já circulava em silvestres/subsistência desde maio/2023.
  - **OMS:** **993 casos humanos de H5N1 / 477 óbitos** (2003–19/12/2025; letalidade ~48%); 19 casos
    em 2025; sem transmissão sustentada humano-a-humano.
  - **CDC (EUA):** **71 casos humanos** (2024–maio/2026), **1º óbito 06/01/2025** (Louisiana);
    spillover em **bovinos leiteiros** (989 rebanhos/17 estados até mar/2025); >90,9 mi de aves.
- **Arquivos atualizados:** `09/V01_INFLUENZA_AVIARIA` (itens 8 e 50 + fontes), `17/01_HPAI_ONE_HEALTH_
  E_VACINAS` (seção 2 reescrita + fontes oficiais).
- **Fontes registradas:** FONTE-OMS-H5N1-001, FONTE-CDC-H5N1-001, FONTE-MAPA-HPAI-001.
- **Controle:** PENDENCIAS (P-019 fechada), STATUS (Mód. 9 e 17), REVISAO_FINAL, FONTES_GERAIS.
- **Aviso mantido:** dados de HPAI mudam rápido — reconfirmar antes de citar.
- **Situação das pendências:** fechadas nesta sessão — **P-015, P-018, P-019** + lacuna do botulismo;
  **P-024** parcial. Abertas (não bloqueantes): valores por linhagem (regra), P-021/P-023 (detalhes
  finos), importação/biosseguridade/indenização (Módulo 14).

---

## 2026-07-21 — Fechamento de pendências: detalhes finos de doenças (P-021 e P-023)

- **P-021 (períodos de incubação):** confirmados — **LTI 6–12 dias** (exposição natural; 2–4 d
  experimental) [Poultry Site/PMC — *Diseases of Poultry*] e **Bouba 4–10 dias** [Merck, "typically
  4–10 days"]. Removidas as marcações de "confirmar/lacuna" em `V06` e `V09`.
- **P-023 (fontes primárias):** **Cólera aviária (`B06`)** elevada de "síntese de busca" para **fonte
  primária MSD** (agente Gram- bipolar; formas aguda/peraguda e crônica; **focos necróticos múltiplos
  em fígado e baço**; petéquias; tratamento sulfas/tetraciclinas com **recidiva**; controle de
  roedores/carcaças/bacterinas). **Correção factual:** incubação de "horas a poucos dias" → **5–8
  dias** (com morte peraguda sem sinais prévios). No `B09`, ***E. cecorum*** confirmado em **MSD/
  PubMed** (espondilite da **vértebra torácica livre**; paresia simétrica; 5–8 sem; mortalidade até
  ~15%).
- **Fontes registradas:** FONTE-MSD-001, FONTE-PS-INCUB-001, FONTE-PUBMED-ECEC-001.
- **Controle:** PENDENCIAS (P-021 e P-023 fechadas), STATUS (Mód. 9), FONTES_GERAIS.
- **Balanço:** pendências de conteúdo do Módulo 9 essencialmente zeradas. Restam, não bloqueantes:
  **P-024 parcial** (nitroimidazóis/anti-helmínticos) e **valores por linhagem** (abertos por regra).

---
