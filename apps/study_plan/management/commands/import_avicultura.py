"""
Management command: import_avicultura

Trilha de estudo de **Avicultura** (Etapa 2 da base documental em
docs/avicultura/). É autocontido e **não toca** no plano de estudos do concurso
(import_study_plan / populate_chapter_content): define sua própria disciplina,
módulo, capítulos e extrai o conteúdo dos arquivos MASTER de avicultura.

Fonte de verdade: os MASTER em docs/avicultura/ESTUDO_NICIA/, estruturados em
seções `## N.` (mesmo padrão dos MASTER do concurso). Cada módulo de avicultura
usa ordens a partir de 15 (o concurso ocupa 1–14).

Idempotente: rodar múltiplas vezes não duplica (update_or_create por slug/order).

Uso:
    python manage.py import_avicultura
    python manage.py import_avicultura --dry-run
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from apps.questions.models import Subject
from apps.study_plan.models import StudyChapter, StudyModule

# Ordem inicial da trilha de avicultura (concurso ocupa 1–14).
AVICULTURA_ORDER_BASE = 15


@dataclass
class ChapterDef:
    order: int
    title: str
    section: int  # número da seção `## N.` no MASTER
    estimated_minutes: int
    tags: list[str]


@dataclass
class ModuleDef:
    order: int
    title: str
    slug: str
    master_file: str  # relativo a docs/
    subject_name: str
    subject_slug: str
    subject_color: str
    study_phase: str
    estimated_hours: float
    icon: str
    description: str
    chapters: list[ChapterDef] = field(default_factory=list)


# ── Mapa da trilha de Avicultura (adicionar novos módulos aqui) ──────────────
AVICULTURA_MAP: list[ModuleDef] = [
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 2,  # 17 (Doenças após o eixo ovo→pintinho)
        title="Avicultura — Doenças",
        slug="avicultura-doencas",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_DOENCAS_MASTER.md",
        subject_name="Avicultura — Doenças",
        subject_slug="avicultura-doencas",
        subject_color="#b5651d",
        study_phase="1",
        estimated_hours=14.0,
        icon="🐔",
        description=(
            "Doenças das aves com foco em reconhecimento de sinais, lesões, "
            "diagnóstico diferencial e conduta. Condensado do Módulo 9 da base "
            "documental de avicultura (32 doenças + matrizes)."
        ),
        chapters=[
            ChapterDef(1, "Raciocínio diagnóstico e coleta de amostras", 1, 25,
                       ["diagnostico", "amostras", "necropsia", "avicultura"]),
            ChapterDef(2, "Notificação obrigatória: Influenza Aviária e Newcastle", 2, 35,
                       ["influenza-aviaria", "newcastle", "notificacao-obrigatoria", "hpai"]),
            ChapterDef(3, "Viroses respiratórias e imunossupressoras", 3, 40,
                       ["bronquite", "laringotraqueite", "gumboro", "marek", "cav"]),
            ChapterDef(4, "Bacterianas de maior impacto", 4, 40,
                       ["salmoneloses", "colibacilose", "micoplasmose", "coriza", "colera"]),
            ChapterDef(5, "Clostridioses, botulismo e outras bacterianas", 5, 30,
                       ["enterite-necrotica", "botulismo", "ort", "enterococcus", "campylobacter"]),
            ChapterDef(6, "Parasitárias e fúngicas", 6, 30,
                       ["coccidiose", "histomonose", "helmintos", "aspergilose", "candidiase"]),
            ChapterDef(7, "Diagnóstico diferencial por síndrome", 7, 30,
                       ["diagnostico-diferencial", "sindrome-respiratoria", "sindrome-neurologica"]),
            ChapterDef(8, "Revisão rápida e flashcards", 8, 20,
                       ["revisao", "flashcards", "avicultura"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 1,  # 16
        title="Avicultura — Incubação e Incubatórios",
        slug="avicultura-incubacao",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_INCUBACAO_MASTER.md",
        subject_name="Avicultura — Incubação",
        subject_slug="avicultura-incubacao",
        subject_color="#c98a3a",
        study_phase="1",
        estimated_hours=12.0,
        icon="🥚",
        description=(
            "Do ovo fértil ao pintinho de um dia: estrutura do incubatório, "
            "desenvolvimento embrionário, temperatura/umidade/ventilação, viragem, "
            "nascimento, qualidade de pintinhos e embriodiagnóstico. Condensado do "
            "Módulo 7 da base documental de avicultura."
        ),
        chapters=[
            ChapterDef(1, "Estrutura e fluxo do incubatório", 1, 20,
                       ["incubatorio", "fluxo-limpo-sujo", "biosseguranca", "zonas"]),
            ChapterDef(2, "Desenvolvimento embrionário dia a dia", 2, 30,
                       ["desenvolvimento-embrionario", "21-dias", "embriao", "camara-de-ar"]),
            ChapterDef(3, "Princípios da incubação (4 fatores e estágio único × múltiplo)", 3, 30,
                       ["principios-incubacao", "setter", "hatcher", "single-stage", "multi-stage"]),
            ChapterDef(4, "Temperatura, umidade e ventilação", 4, 40,
                       ["temperatura", "umidade", "perda-de-peso-do-ovo", "ventilacao", "co2"]),
            ChapterDef(5, "Viragem, transferência e nascimento", 5, 30,
                       ["viragem", "transferencia", "nascimento", "janela-de-nascimento", "bicagem"]),
            ChapterDef(6, "Processamento, sexagem e vacinação no incubatório", 6, 30,
                       ["processamento", "sexagem", "vacinacao-in-ovo", "marek", "refugagem"]),
            ChapterDef(7, "Qualidade e expedição de pintinhos", 7, 30,
                       ["qualidade-pintinho", "escore-pasgar", "umbigo", "expedicao", "transporte"]),
            ChapterDef(8, "Falhas, mortalidade embrionária e embriodiagnóstico", 8, 35,
                       ["falhas-incubacao", "mortalidade-embrionaria", "embriodiagnostico", "breakout"]),
            ChapterDef(9, "Revisão rápida e flashcards", 9, 20,
                       ["revisao", "flashcards", "incubacao"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 0,  # 15 (início do eixo: matriz → ovo fértil)
        title="Avicultura — Reprodução e Ovos Férteis",
        slug="avicultura-reproducao",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_REPRODUCAO_MASTER.md",
        subject_name="Avicultura — Reprodução",
        subject_slug="avicultura-reproducao",
        subject_color="#c06c3a",
        study_phase="1",
        estimated_hours=10.0,
        icon="🐓",
        description=(
            "Matrizes e machos, fertilidade, produção e qualidade dos ovos férteis, "
            "coleta/armazenamento e falhas reprodutivas. Base do elo matriz → ovo "
            "fértil. Condensado do Módulo 6 da base documental de avicultura."
        ),
        chapters=[
            ChapterDef(1, "Fisiologia reprodutiva aplicada (maturidade e fotoestimulação)", 1, 25,
                       ["fisiologia-reprodutiva", "fotoestimulacao", "maturidade-sexual", "dark-out"]),
            ChapterDef(2, "Manejo de matrizes (fêmeas)", 2, 30,
                       ["matrizes", "restricao-alimentar", "uniformidade", "cv", "peso"]),
            ChapterDef(3, "Manejo de machos", 3, 25,
                       ["machos", "relacao-macho-femea", "spiking", "alimentacao-sexada"]),
            ChapterDef(4, "Fertilidade e fecundação", 4, 30,
                       ["fertilidade", "eclodibilidade", "ssts", "curva-de-fertilidade"]),
            ChapterDef(5, "Produção e qualidade dos ovos férteis", 5, 30,
                       ["producao-ovos-ferteis", "ovos-incubaveis", "qualidade-do-ovo", "ovos-de-chao"]),
            ChapterDef(6, "Coleta, armazenamento e transporte de ovos férteis", 6, 25,
                       ["coleta", "armazenamento", "zero-fisiologico", "sanitizacao", "transporte"]),
            ChapterDef(7, "Falhas reprodutivas — diagnóstico de causa-raiz", 7, 25,
                       ["falhas-reprodutivas", "queda-fertilidade", "queda-postura", "breakout"]),
            ChapterDef(8, "Revisão rápida e flashcards", 8, 20,
                       ["revisao", "flashcards", "reproducao"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 3,  # 18
        title="Avicultura — Nutrição",
        slug="avicultura-nutricao",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_NUTRICAO_MASTER.md",
        subject_name="Avicultura — Nutrição",
        subject_slug="avicultura-nutricao",
        subject_color="#8a9a3a",
        study_phase="1",
        estimated_hours=14.0,
        icon="🌽",
        description=(
            "Nutrientes (água, energia, proteína, vitaminas, minerais), formulação, "
            "alimentação por categoria, micotoxinas e diagnóstico diferencial "
            "nutricional. Condensado do Módulo 4 da base documental de avicultura."
        ),
        chapters=[
            ChapterDef(1, "Fundamentos da nutrição (nutrientes, energia, consumo × energia)", 1, 25,
                       ["fundamentos-nutricao", "energia-metabolizavel", "proteina-ideal", "aminoacido-limitante"]),
            ChapterDef(2, "Água — o nutriente mais crítico", 2, 20,
                       ["agua", "qualidade-agua", "cloracao", "biofilme"]),
            ChapterDef(3, "Energia e lipídios", 3, 25,
                       ["energia", "lipidios", "acido-linoleico", "rancidez"]),
            ChapterDef(4, "Proteínas e aminoácidos", 4, 30,
                       ["proteina", "aminoacidos", "lisina", "metionina", "aminoacidos-digestiveis"]),
            ChapterDef(5, "Vitaminas e minerais", 5, 40,
                       ["vitaminas", "minerais", "deficiencias", "perose", "calcio-fosforo"]),
            ChapterDef(6, "Formulação de rações e alimentação por categoria", 6, 35,
                       ["formulacao", "alimentacao-por-categoria", "poedeira", "matriz", "pintinho"]),
            ChapterDef(7, "Micotoxinas, adsorventes e controle", 7, 35,
                       ["micotoxinas", "aflatoxina", "adsorventes", "imunossupressao", "limite-mapa"]),
            ChapterDef(8, "Deficiências nutricionais e diagnóstico diferencial", 8, 35,
                       ["diagnostico-diferencial", "deficiencias-nutricionais", "nutricional-vs-infeccioso"]),
            ChapterDef(9, "Revisão rápida e flashcards", 9, 20,
                       ["revisao", "flashcards", "nutricao"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 4,  # 19
        title="Avicultura — Biossegurança",
        slug="avicultura-biosseguranca",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_BIOSSEGURANCA_MASTER.md",
        subject_name="Avicultura — Biossegurança",
        subject_slug="avicultura-biosseguranca",
        subject_color="#3a8a6a",
        study_phase="1",
        estimated_hours=10.0,
        icon="🛡️",
        description=(
            "O escudo sanitário: conceitos, barreira sanitária, limpeza e "
            "desinfecção, controle de pragas, insumos, rigor por setor e "
            "monitoramento/contingência. Condensado do Módulo 8 da base."
        ),
        chapters=[
            ChapterDef(1, "Conceitos e princípios", 1, 25,
                       ["biosseguranca", "bioexclusao", "biocontencao", "compartimentacao"]),
            ChapterDef(2, "Controle de acesso e barreira sanitária", 2, 25,
                       ["barreira-sanitaria", "fluxo-limpo-sujo", "rodoluvio", "pediluvio", "downtime"]),
            ChapterDef(3, "Limpeza, desinfecção e vazio sanitário", 3, 35,
                       ["limpeza-desinfeccao", "materia-organica", "desinfetantes", "vazio-sanitario"]),
            ChapterDef(4, "Controle de pragas e vetores", 4, 30,
                       ["pragas", "roedores", "cascudinho", "aves-silvestres", "mip"]),
            ChapterDef(5, "Biossegurança de insumos e ambiente", 5, 25,
                       ["insumos", "agua", "racao", "cama", "carcacas", "residuos"]),
            ChapterDef(6, "Biossegurança por setor (diferenciação de rigor)", 6, 20,
                       ["por-setor", "matrizes", "incubatorio", "pnsa", "elo-mais-fraco"]),
            ChapterDef(7, "Monitoramento, auditoria e contingência", 7, 25,
                       ["monitoramento", "auditoria", "rastreabilidade", "plano-de-contingencia"]),
            ChapterDef(8, "Revisão rápida e flashcards", 8, 20,
                       ["revisao", "flashcards", "biosseguranca"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 5,  # 20
        title="Avicultura — Manejo",
        slug="avicultura-manejo",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_MANEJO_MASTER.md",
        subject_name="Avicultura — Manejo",
        subject_slug="avicultura-manejo",
        subject_color="#6a8ab5",
        study_phase="1",
        estimated_hours=10.0,
        icon="🌡️",
        description=(
            "O dia a dia da granja: brooding do pintinho, ambiência (temperatura/"
            "ventilação/ar), cama, água, luz, densidade e falhas de manejo. "
            "Condensado do Módulo 5 da base documental de avicultura."
        ),
        chapters=[
            ChapterDef(1, "Manejo inicial e do pintinho de um dia (brooding)", 1, 30,
                       ["brooding", "pintinho", "crop-fill", "pre-aquecimento", "arranque"]),
            ChapterDef(2, "Ambiência (temperatura, umidade, ventilação, qualidade do ar)", 2, 35,
                       ["ambiencia", "temperatura", "ventilacao", "amonia", "pressao-negativa"]),
            ChapterDef(3, "Cama", 3, 25,
                       ["cama", "umidade", "amonia", "cascudinho", "reutilizacao"]),
            ChapterDef(4, "Água (manejo)", 4, 20,
                       ["agua", "bebedouros", "cloro", "biofilme", "vacina-na-agua"]),
            ChapterDef(5, "Luz (programas de iluminação)", 5, 25,
                       ["luz", "fotoperiodo", "intensidade", "dark-out", "escuro"]),
            ChapterDef(6, "Densidade de alojamento", 6, 20,
                       ["densidade", "kg-por-m2", "lotacao", "bem-estar", "uniformidade"]),
            ChapterDef(7, "Falhas de manejo e causa-raiz", 7, 25,
                       ["falhas-manejo", "manejo-vs-doenca", "causa-raiz"]),
            ChapterDef(8, "Revisão rápida e flashcards", 8, 20,
                       ["revisao", "flashcards", "manejo"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 6,  # 21
        title="Avicultura — Programas Vacinais",
        slug="avicultura-vacinas",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_VACINAS_MASTER.md",
        subject_name="Avicultura — Programas Vacinais",
        subject_slug="avicultura-vacinas",
        subject_color="#7a5aa8",
        study_phase="1",
        estimated_hours=8.0,
        icon="💉",
        description=(
            "Tipos de vacina (viva, inativada, vetorizada, autógena), vias de "
            "aplicação, interferência do anticorpo materno e timing, princípios de "
            "programas e falhas vacinais. Condensado do Módulo 10 da base."
        ),
        chapters=[
            ChapterDef(1, "Tipos de vacina", 1, 30,
                       ["tipos-vacina", "viva-atenuada", "inativada", "vetorizada-hvt", "autogena"]),
            ChapterDef(2, "Vias de aplicação", 2, 30,
                       ["vias-aplicacao", "spray", "agua", "in-ovo", "subcutanea", "wing-web"]),
            ChapterDef(3, "Interferência de anticorpos maternos e timing", 3, 25,
                       ["anticorpo-materno", "mda", "timing", "janela-suscetibilidade", "sorologia"]),
            ChapterDef(4, "Princípios de programas vacinais", 4, 25,
                       ["programas-vacinais", "por-categoria", "sem-protocolo-universal", "biosseguranca"]),
            ChapterDef(5, "Erros e falhas de vacinação", 5, 25,
                       ["falha-vacinal", "cadeia-de-frio", "uniformidade", "cepa-vs-variante"]),
            ChapterDef(6, "Revisão rápida e flashcards", 6, 20,
                       ["revisao", "flashcards", "vacinas"]),
        ],
    ),
    ModuleDef(
        order=AVICULTURA_ORDER_BASE + 7,  # 22
        title="Avicultura — Diagnóstico",
        slug="avicultura-diagnostico",
        master_file="avicultura/ESTUDO_NICIA/AVICULTURA_DIAGNOSTICO_MASTER.md",
        subject_name="Avicultura — Diagnóstico",
        subject_slug="avicultura-diagnostico",
        subject_color="#3a7a9a",
        study_phase="1",
        estimated_hours=8.0,
        icon="🔬",
        description=(
            "Raciocínio diagnóstico de lote, coleta/amostragem, métodos diretos "
            "(PCR, isolamento, histopatologia, antibiograma, sequenciamento), "
            "sorologia/monitoramento e interpretação de laudos. Condensado do Módulo 11."
        ),
        chapters=[
            ChapterDef(1, "Abordagem diagnóstica (investigação do lote)", 1, 25,
                       ["abordagem-diagnostica", "anamnese", "necropsia", "hipoteses"]),
            ChapterDef(2, "Coleta, amostragem e cadeia de custódia", 2, 30,
                       ["coleta", "amostragem", "cadeia-de-custodia", "cadeia-de-frio", "formol"]),
            ChapterDef(3, "Métodos diretos (detecção do agente)", 3, 35,
                       ["metodos-diretos", "pcr", "isolamento", "histopatologia", "antibiograma", "sequenciamento"]),
            ChapterDef(4, "Sorologia e monitoramento sorológico", 4, 30,
                       ["sorologia", "elisa", "hi", "titulo", "cv", "soroconversao"]),
            ChapterDef(5, "Interpretação de laudos e integração", 5, 25,
                       ["interpretacao-laudos", "falso-positivo", "falso-negativo", "coinfeccao"]),
            ChapterDef(6, "Revisão rápida e flashcards", 6, 20,
                       ["revisao", "flashcards", "diagnostico"]),
        ],
    ),
]


def _parse_numbered_sections(file_content: str) -> dict[int, str]:
    """Divide o MASTER em seções `## N.` → {n: conteúdo}."""
    lines = file_content.split("\n")
    sections: dict[int, str] = {}
    current: int | None = None
    buf: list[str] = []
    header = re.compile(r"^## (\d+)\.")
    for line in lines:
        m = header.match(line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).rstrip()
            current = int(m.group(1))
            buf = [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).rstrip()
    return sections


class Command(BaseCommand):
    help = "Popula a trilha de estudo de Avicultura (disciplina + módulos + capítulos + conteúdo)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula sem gravar no banco.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        docs_dir = Path(settings.BASE_DIR) / "docs"

        if dry_run:
            self.stdout.write(self.style.WARNING("Modo --dry-run: nada será gravado.\n"))

        stats = {"modules": 0, "chapters": 0, "empty": 0, "missing_files": 0}

        with transaction.atomic():
            for mod in AVICULTURA_MAP:
                path = docs_dir / mod.master_file
                if not path.exists():
                    self.stderr.write(self.style.ERROR(f"  MASTER não encontrado: {path}"))
                    stats["missing_files"] += 1
                    continue
                sections = _parse_numbered_sections(path.read_text(encoding="utf-8"))

                subject, _ = Subject.objects.update_or_create(
                    slug=mod.subject_slug,
                    defaults={
                        "name": mod.subject_name,
                        "category": "specific",
                        "color": mod.subject_color,
                        "is_active": True,
                    },
                )

                module, _ = StudyModule.objects.update_or_create(
                    slug=mod.slug,
                    defaults={
                        "title": mod.title,
                        "order": mod.order,
                        "master_file": mod.master_file,
                        "subject": subject,
                        "category": "specific",
                        "study_phase": mod.study_phase,
                        "estimated_hours": mod.estimated_hours,
                        "icon": mod.icon,
                        "description": mod.description,
                        "is_active": True,
                    },
                )
                stats["modules"] += 1
                self.stdout.write(f"  Módulo [{mod.order}] {mod.title}")

                for ch in mod.chapters:
                    content = sections.get(ch.section, "")
                    if not content.strip():
                        self.stderr.write(
                            self.style.WARNING(f"    ⚠ Cap {ch.order}: seção {ch.section} vazia no MASTER")
                        )
                        stats["empty"] += 1

                    chapter, _ = StudyChapter.objects.update_or_create(
                        module=module,
                        order=ch.order,
                        defaults={
                            "title": ch.title,
                            "slug": slugify(ch.title),
                            "content": content,
                            "key_points": "",
                            "estimated_minutes": ch.estimated_minutes,
                            "tags": ch.tags,
                            "sections_source": f"§{ch.section}",
                            "is_active": True,
                        },
                    )
                    chapter.related_subjects.add(subject)
                    stats["chapters"] += 1
                    self.stdout.write(f"    ✓ Cap {ch.order}: {ch.title} ({len(content):,} chars)")

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{'DRY RUN | ' if dry_run else ''}"
                f"Módulos: {stats['modules']} | Capítulos: {stats['chapters']} | "
                f"Vazios: {stats['empty']} | MASTER ausentes: {stats['missing_files']}"
            )
        )
