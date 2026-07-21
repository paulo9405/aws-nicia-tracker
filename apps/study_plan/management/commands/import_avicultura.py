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
        order=AVICULTURA_ORDER_BASE + 0,  # 15
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
        order=AVICULTURA_ORDER_BASE + 2,  # 17
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
