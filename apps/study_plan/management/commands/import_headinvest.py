"""
Management command: import_headinvest

Trilha de estudo **HeadInvest** (preparação para entrevista). É autocontida e
**não toca** no plano de estudos do concurso nem na trilha de avicultura: define
sua própria disciplina, módulo, capítulos e extrai o conteúdo do MASTER.

Fonte de verdade: o MASTER em docs/headinvest/HEADINVEST_MASTER.md, estruturado
em seções `## N.` (mesmo padrão dos MASTER de avicultura/concurso). A trilha
HeadInvest usa ordens a partir de 40 (concurso 1–14, avicultura 15–32).

Idempotente: rodar múltiplas vezes não duplica (update_or_create por slug/order).

Fase 1: só conteúdo (leitura + aprendizagem ativa + reflexão). O banco de
questões / mini-quiz é a Fase 2.

Uso:
    python manage.py import_headinvest
    python manage.py import_headinvest --dry-run
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

# Ordem inicial da trilha HeadInvest (concurso 1–14, avicultura 15–32).
HEADINVEST_ORDER_BASE = 40


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


# ── Mapa da trilha HeadInvest ────────────────────────────────────────────────
HEADINVEST_MAP: list[ModuleDef] = [
    ModuleDef(
        order=HEADINVEST_ORDER_BASE,  # 40
        title="HeadInvest — Guia de Preparação para a Entrevista",
        slug="headinvest-guia",
        master_file="headinvest/HEADINVEST_MASTER.md",
        subject_name="HeadInvest — Preparação",
        subject_slug="headinvest-guia",
        subject_color="#1f6f8b",
        study_phase="1",
        estimated_hours=3.0,
        icon="💼",
        description=(
            "Entenda o negócio da HeadInvest (gestora de crédito estruturado), seus "
            "produtos e onde um backend Python se encaixa — para chegar preparado a "
            "uma entrevista técnica com contexto de negócio. Condensado do guia de "
            "preparação em docs/headinvest/."
        ),
        chapters=[
            ChapterDef(1, "A empresa e o negócio", 1, 25,
                       ["headinvest", "asset-management", "credito-estruturado", "aum", "bsi-capital"]),
            ChapterDef(2, "Como funciona: o fluxo e os produtos", 2, 30,
                       ["fluxo", "fidc", "cri", "produtos-estruturados", "covenants"]),
            ChapterDef(3, "Onde a tecnologia entra", 3, 30,
                       ["tecnologia", "python", "pandas", "postgresql", "aws", "esteira"]),
            ChapterDef(4, "Preparação para a entrevista", 4, 25,
                       ["entrevista", "perguntas", "o-que-nao-decorar", "negocio-processo-tecnologia"]),
            ChapterDef(5, "Conectando com a sua experiência", 5, 25,
                       ["experiencia", "multi-tenant", "jobs-agendados", "apis", "ocr", "rastreabilidade"]),
            ChapterDef(6, "Glossário e revisão rápida", 6, 20,
                       ["glossario", "revisao", "flashcards", "headinvest"]),
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
    help = "Popula a trilha de estudo HeadInvest (disciplina + módulo + capítulos + conteúdo)."

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
            for mod in HEADINVEST_MAP:
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
