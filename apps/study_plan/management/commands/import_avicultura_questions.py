"""
Management command: import_avicultura_questions

Importa o **banco de questões da trilha de Avicultura** — separado e isolado do
banco do concurso (import_questions):

- Reaproveita o parser validado do banco mestre (BancoMestreParser): valida 4
  alternativas A–D, uma correta, e a tabela de gabarito.
- Cada `# SEÇÃO N` do markdown mapeia para um **Subject de avicultura** já criado
  por `import_avicultura` (slug `avicultura-*`) — ver AVICULTURA_QUESTION_MAP.
- external_id com prefixo próprio (`avicultura-q-...`) — **nunca colide** com o
  `banco-mestre-...` do concurso.
- **Não** dispara o guard de 800 questões do concurso: só toca em Subjects/Questions
  de avicultura.
- Idempotente (update_or_create por external_id; content_hash detecta edição).

Como o MiniQuizService cai no `module.subject` (tentativa 2), as questões aqui
importadas aparecem automaticamente no mini-quiz de cada capítulo de avicultura.

Uso:
    python manage.py import_avicultura_questions
    python manage.py import_avicultura_questions --dry-run
    python manage.py import_avicultura_questions --strict
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.questions.importer.parser import BancoMestreParser, ParsedQuestion
from apps.questions.models import Alternative, Question, Subject

# Banca própria da trilha de avicultura (não confundir com "Instituto UniFil" do concurso).
AVICULTURA_BOARD = "Nícia Track — Avicultura"

# Arquivo-fonte padrão (relativo a docs/).
DEFAULT_BANK = "avicultura/ESTUDO_NICIA/AVICULTURA_BANCO_QUESTOES.md"


@dataclass(frozen=True)
class QuestionSectionMap:
    section_index: int
    subject_slug: str  # Subject de avicultura já existente (criado por import_avicultura)


# Mapa: seção do banco → Subject de avicultura. Adicionar novas seções aqui.
AVICULTURA_QUESTION_MAP: dict[int, QuestionSectionMap] = {
    1: QuestionSectionMap(1, "avicultura-doencas"),
}


def _external_id(parsed: ParsedQuestion) -> str:
    """Chave natural isolada do concurso."""
    return f"avicultura-q-s{parsed.section_index:02d}-q{parsed.number:03d}"


def _compose_explanation(parsed: ParsedQuestion) -> str:
    if parsed.master_ref:
        return f"{parsed.explanation}\n\nRef.: {parsed.master_ref}".strip()
    return parsed.explanation.strip()


class Command(BaseCommand):
    help = "Importa o banco de questões da trilha de avicultura (isolado do concurso)."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "path",
            nargs="?",
            default=DEFAULT_BANK,
            help=f"Caminho do markdown relativo a docs/ (padrão: {DEFAULT_BANK}).",
        )
        parser.add_argument("--dry-run", action="store_true",
                            help="Analisa e relata, sem gravar.")
        parser.add_argument("--strict", action="store_true",
                            help="Encerra com erro se houver erro de parsing ou seção sem mapa.")

    def handle(self, *args, **options) -> None:
        docs_dir = Path(settings.BASE_DIR) / "docs"
        path = docs_dir / options["path"]
        if not path.exists():
            raise CommandError(f"Arquivo não encontrado: {path}")

        dry_run = options["dry_run"]
        strict = options["strict"]

        self.stdout.write(self.style.MIGRATE_HEADING(f"Importando questões de avicultura: {path}"))
        if dry_run:
            self.stdout.write(self.style.WARNING("Modo dry-run: nada será gravado."))

        result = BancoMestreParser().parse_file(str(path))

        if result.errors:
            self.stdout.write(self.style.ERROR("Erros de parsing:"))
            for err in result.errors[:50]:
                self.stdout.write(f"  - {err}")
            if strict:
                raise CommandError("Importação abortada (--strict).")
            return

        # Valida cobertura de mapeamento seção → subject.
        sections = sorted({q.section_index for q in result.questions})
        faltando = [s for s in sections if s not in AVICULTURA_QUESTION_MAP]
        if faltando:
            msg = f"Seções sem mapeamento em AVICULTURA_QUESTION_MAP: {faltando}"
            if strict:
                raise CommandError(msg)
            self.stdout.write(self.style.ERROR(msg))
            return

        created = updated = unchanged = 0
        subjects_touched: set[str] = set()

        for parsed in result.questions:
            slug = AVICULTURA_QUESTION_MAP[parsed.section_index].subject_slug
            subject = Subject.objects.filter(slug=slug).first()
            if subject is None:
                msg = (f"Subject '{slug}' não existe — rode import_avicultura antes "
                       f"(seção {parsed.section_index}).")
                if strict:
                    raise CommandError(msg)
                self.stdout.write(self.style.ERROR(msg))
                return
            subjects_touched.add(slug)

            if dry_run:
                exists = Question.objects.filter(external_id=_external_id(parsed)).first()
                if exists is None:
                    created += 1
                elif exists.content_hash != parsed.content_hash:
                    updated += 1
                else:
                    unchanged += 1
                continue

            outcome = self._upsert(parsed, subject)
            if outcome == "created":
                created += 1
            elif outcome == "updated":
                updated += 1
            else:
                unchanged += 1

        self.stdout.write(self.style.SUCCESS("Parsing OK."))
        self.stdout.write(f"  Criadas    : {created}")
        self.stdout.write(f"  Atualizadas: {updated}")
        self.stdout.write(f"  Inalteradas: {unchanged}")
        self.stdout.write(f"  Disciplinas: {', '.join(sorted(subjects_touched))}")
        self.stdout.write(self.style.SUCCESS("Concluído."))

    @transaction.atomic
    def _upsert(self, parsed: ParsedQuestion, subject: Subject) -> str:
        ext = _external_id(parsed)
        explanation = _compose_explanation(parsed)
        existing = (
            Question.objects.filter(external_id=ext).select_for_update().first()
        )

        if existing is None:
            question = Question.objects.create(
                subject=subject,
                external_id=ext,
                content_hash=parsed.content_hash,
                text=parsed.statement,
                context_text=parsed.context_text,
                explanation=explanation,
                source=parsed.source_file,
                board=AVICULTURA_BOARD,
                is_active=True,
            )
            Alternative.objects.bulk_create([
                Alternative(question=question, letter=a.letter,
                            text=a.text, is_correct=a.is_correct)
                for a in parsed.alternatives
            ])
            return "created"

        if existing.content_hash == parsed.content_hash:
            return "unchanged"

        existing.subject = subject
        existing.content_hash = parsed.content_hash
        existing.text = parsed.statement
        existing.context_text = parsed.context_text
        existing.explanation = explanation
        existing.source = parsed.source_file
        existing.board = AVICULTURA_BOARD
        existing.is_active = True
        existing.save()
        # Regrava alternativas (simples e seguro dentro da transação).
        existing.alternatives.all().delete()
        Alternative.objects.bulk_create([
            Alternative(question=existing, letter=a.letter,
                        text=a.text, is_correct=a.is_correct)
            for a in parsed.alternatives
        ])
        return "updated"
