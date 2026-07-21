# Matrizes — Lesão × Doença, Sinal × Lesão, Suspeita × Amostra

> As três matrizes de correlação exigidas pelo plano para o Módulo 18. Para evitar duplicação, as
> matrizes **lesão × doença**, **sinais × doenças** e **amostras × diagnósticos** já existem no
> **Módulo 9** — aqui está a versão **da bancada de necropsia**, com referência cruzada.

## 1. Lesão × Doença (referência)

- Matriz completa em **`09_DOENCAS/MATRIZ_LESOES_X_DOENCAS.md`** (lesão → doenças + observação
  distintiva). Complementada por `18/03_LESOES_POR_SISTEMA` e `18/05_MATRIZ_ORGAO_X_LESAO`.
- **Uso na necropsia:** partir da lesão encontrada → lista de doenças → confirmar por amostra/laboratório.

## 2. Sinal Clínico × Lesão (ponte clínica ↔ patológica)

Liga o que se **vê no lote vivo** (Módulo 9, `MATRIZ_SINAIS_CLINICOS_X_DOENCAS`) ao que se **espera
encontrar na necropsia**:

| Sinal no lote | Lesão esperada na necropsia | Onde olhar |
|---|---|---|
| Dispneia / tosse | Traqueíte (hemorrágica em LTI), aerossaculite | Traqueia, sacos aéreos |
| Diarreia sanguinolenta | Cores cecais | Cecos |
| Diarreia amarelo-enxofre (peru) | Fígado em alvo + cecos | Fígado/cecos |
| Paralisia assimétrica | Aumento de nervo periférico | Nervo isquiático/braquial |
| Tremor (pintinho) | Sem lesão macro (histológica) | Encéfalo (formol) |
| Queda de postura + casca ruim | Oviduto/glândula da casca alterados; ovário | Aparelho reprodutor |
| Palidez/anemia | Medula pálida + timo atrófico (CAV); ou ácaro/aflatoxina | Medula, timo; fígado |
| Claudicação | Tenossinovite (viral) ou artrite purulenta | Tendões/articulações |
| Morte súbita | Ascite (coração direito+líquido) ou SDS (sem lesão) ou focos hepáticos (cólera) | Abdome, coração, fígado |

> Uso: se o sinal **não bate** com a lesão esperada, reavaliar hipótese/artefato (arquivo 02).

## 3. Suspeita × Amostra Recomendada (referência)

- Matriz completa em **`09_DOENCAS/MATRIZ_AMOSTRAS_X_DIAGNOSTICOS.md`** e em
  `18/04_COLETA_E_ENVIO_DE_AMOSTRAS`. Resumo de bancada:

| Suspeita | Amostra na necropsia | Conservação |
|---|---|---|
| Vírus respiratório (BI/Newcastle/LTI/aMPV) | Traqueia/pulmão; swabs | Fresco/refrig. (+formol) |
| Gumboro | Bursa | Fresco + formol |
| Marek/Leucose/REV | Nervo/tumor | Formol (histopatologia/IHQ) |
| CAV | Medula/timo | Fresco/refrig. |
| Coccidiose | Cecos/intestino + raspado | Fresco |
| Bacteriana (E. coli/Salmonela/cólera) | Órgão de sítio estéril | Fresco (cultura) |
| Aspergilose/candidíase | Nódulo pulmonar / mucosa do papo | Fresco + formol |
| Nutricional/micotoxina | Osso/tecido + **ração** | Conforme |

## 4. Fluxo integrado (necropsia → diagnóstico)

```
Sinal no lote (Mód. 9) → Necropsia sistemática (18/01) → Lesão descrita (18/02-03)
   → Órgão×lesão (18/05) → hipóteses (Mód. 9) → amostra certa (18/04, Mód. 11)
   → laboratório (Mód. 11) → interpretação correlacionada (Mód. 11/05) → conduta
```

## 5. Fontes
Módulo 9 (matrizes `MATRIZ_LESOES_X_DOENCAS`, `MATRIZ_SINAIS_CLINICOS_X_DOENCAS`,
`MATRIZ_AMOSTRAS_X_DIAGNOSTICOS`) + arquivos 01–05 deste módulo + Módulo 11 (diagnóstico). Fontes
primárias citadas nos arquivos-fonte (Merck/MSD/WOAH/PMC).
