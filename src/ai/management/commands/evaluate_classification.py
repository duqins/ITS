"""Evaluate AI classification on the fixed set of 20 labelled assets (AI-01.5).

Each asset in ai/evaluation/classification_set.json is saved as a draft, classified by the real
Claude API exactly as the Register page does it, and compared with its expected category. A
missing, invalid or failed AI answer counts as incorrect (AI-01.5). Nothing stays in the
database: every change is rolled back at the end.

Usage:  python manage.py evaluate_classification [--output results.json]
"""

import json
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from ai.adapter import AIUnavailable, ClaudeAdapter
from ai.classification import PROMPT_VERSION, ClassificationService
from assets.models import Asset, Category

SET_FILE = Path(__file__).resolve().parents[2] / "evaluation" / "classification_set.json"
NEEDED = 16  # AI-01.5: at least 16 of the 20 assets


class Command(BaseCommand):
    help = "Classify the 20 labelled test assets with the real AI and report how many are correct (AI-01.5)."

    def add_arguments(self, parser):
        parser.add_argument("--output", help="Also save the results as a JSON file.")

    def handle(self, *args, **options):
        if not ClaudeAdapter.is_configured():
            raise CommandError("Set ANTHROPIC_API_KEY first. This evaluation calls the real AI.")
        items = json.loads(SET_FILE.read_text(encoding="utf-8"))
        allowed = {str(c) for c in Category.objects.filter(is_active=True)}
        unknown = sorted({item["expected"] for item in items} - allowed)
        if unknown:
            raise CommandError("Expected categories that do not exist: " + ", ".join(unknown))
        custodian = User.objects.filter(username="eng.custodian").first()
        if custodian is None:
            raise CommandError("Run seed_demo first: the evaluation saves the drafts as the demo custodian.")

        service, rows = ClassificationService(), []
        with transaction.atomic():
            for number, item in enumerate(items, start=1):
                asset = Asset(name=item["name"], description=item["description"],
                              specifications=item["specifications"])
                asset.register(custodian, custodian.department)
                started = time.monotonic()
                try:
                    suggestion = service.suggest(asset, custodian)
                    answer = suggestion.suggestion
                    row = {"suggested": answer["category"], "runs": answer["runs"],
                           "confidence": float(suggestion.confidence), "error": ""}
                except AIUnavailable as error:
                    row = {"suggested": "", "runs": [], "confidence": None, "error": str(error)}
                row.update(number=number, name=item["name"], expected=item["expected"],
                           seconds=round(time.monotonic() - started, 1))
                row["correct"] = row["suggested"] == item["expected"]
                rows.append(row)
                self.stdout.write(f"{number:>2}  {'correct' if row['correct'] else 'WRONG  '}  "
                                  f"{item['name'][:32]:32}  expected {item['expected']:30}  "
                                  f"got {row['suggested'] or row['error']} "
                                  f"(confidence {row['confidence']}, {row['seconds']} s)")
            transaction.set_rollback(True)  # leave no evaluation records behind

        correct = sum(row["correct"] for row in rows)
        confident = sum(1 for row in rows if row["confidence"] is not None and row["confidence"] >= 0.60)
        summary = {
            "run_at": timezone.localtime().strftime("%Y-%m-%d %H:%M"),
            "model": service.model, "prompt_version": PROMPT_VERSION, "runs_per_asset": service.runs,
            "assets": len(rows), "correct": correct, "needed": NEEDED, "passed": correct >= NEEDED,
            "failed_answers": sum(1 for row in rows if row["error"]),
            "at_or_above_060": confident,
            "slowest_seconds": max(row["seconds"] for row in rows),
        }
        self.stdout.write(f"\nCorrect: {correct} of {len(rows)} (needed: {NEEDED}). "
                          f"{'PASS' if summary['passed'] else 'FAIL'}")
        self.stdout.write(f"Failed answers: {summary['failed_answers']}. Confidence 0.60 or above: {confident}. "
                          f"Slowest: {summary['slowest_seconds']} s. Model: {service.model}, {PROMPT_VERSION}.")
        if options["output"]:
            Path(options["output"]).write_text(json.dumps({"summary": summary, "assets": rows}, indent=1),
                                               encoding="utf-8")
            self.stdout.write("Saved to " + options["output"])
