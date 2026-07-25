"""
Management command: import_headinvest_questions

Importa o **banco de questões da trilha HeadInvest** — separado e isolado do
banco do concurso (import_questions) e do de avicultura:

- Reaproveita o parser validado do banco mestre (BancoMestreParser): valida 4
  alternativas A–D, uma correta, e a tabela de gabarito.
- Todas as `# SEÇÃO N` do markdown mapeiam para o **Subject único da trilha**
  (`headinvest-guia`), criado por `import_headinvest`. As seções espelham as 6
  aulas apenas para autoria; no mini-quiz formam um pool único da trilha.
- external_id com prefixo próprio (`headinvest-q-...`) — **nunca colide** com o
  `banco-mestre-...` do concurso nem com o `avicultura-q-...`.
- **Não** dispara o guard de 800 questões do concurso: só toca no Subject/Questions
  de HeadInvest.
- Idempotente (update_or_create por external_id; content_hash detecta edição).

Como o MiniQuizService cai no `module.subject` (tentativa 2), as questões aqui
importadas aparecem automaticamente no mini-quiz de cada capítulo da trilha.

Uso:
    python manage.py import_headinvest_questions
    python manage.py import_headinvest_questions --dry-run
    python manage.py import_headinvest_questions --strict
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.questions.importer.parser import BancoMestreParser, ParsedQuestion
from apps.questions.models import Alternative, Question, Subject

# Banca própria da trilha HeadInvest (não confundir com bancas do concurso).
HEADINVEST_BOARD = "Nícia Track — HeadInvest"

# Arquivo-fonte padrão (relativo a docs/).
DEFAULT_BANK = "headinvest/HEADINVEST_BANCO_QUESTOES.md"

# Subject único da trilha (criado por import_headinvest). Todas as seções do banco
# mapeiam para ele: no mini-quiz as 6 aulas formam um pool único da trilha.
HEADINVEST_SUBJECT_SLUG = "headinvest-guia"


def _external_id(parsed: ParsedQuestion) -> str:
    """Chave natural isolada do concurso e da avicultura."""
    return f"headinvest-q-s{parsed.section_index:02d}-q{parsed.number:03d}"


def _compose_explanation(parsed: ParsedQuestion) -> str:
    if parsed.master_ref:
        return f"{parsed.explanation}\n\nRef.: {parsed.master_ref}".strip()
    return parsed.explanation.strip()


class Command(BaseCommand):
    help = "Importa o banco de questões da trilha HeadInvest (isolado do concurso)."

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
                            help="Encerra com erro se houver erro de parsing.")

    def handle(self, *args, **options) -> None:
        docs_dir = Path(settings.BASE_DIR) / "docs"
        path = docs_dir / options["path"]
        if not path.exists():
            raise CommandError(f"Arquivo não encontrado: {path}")

        dry_run = options["dry_run"]
        strict = options["strict"]

        self.stdout.write(self.style.MIGRATE_HEADING(f"Importando questões HeadInvest: {path}"))
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

        subject = Subject.objects.filter(slug=HEADINVEST_SUBJECT_SLUG).first()
        if subject is None:
            msg = (f"Subject '{HEADINVEST_SUBJECT_SLUG}' não existe — rode "
                   f"import_headinvest antes.")
            if strict:
                raise CommandError(msg)
            self.stdout.write(self.style.ERROR(msg))
            return

        created = updated = unchanged = 0

        for parsed in result.questions:
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
        self.stdout.write(f"  Disciplina : {HEADINVEST_SUBJECT_SLUG}")
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
                board=HEADINVEST_BOARD,
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
        existing.board = HEADINVEST_BOARD
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
