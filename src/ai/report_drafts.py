"""AI feature 5: generated report summary (AI-09, AI-10, design section 4).

The database calculates every figure (sustainability.indicators). Claude only writes a short
summary from those figures. Before a reviewer can publish it, every number in the text must
match a figure the database gave; otherwise it stays a draft (section 4: "report figures equal
the conventional totals").
"""

import re
from decimal import Decimal

from django.conf import settings
from pydantic import BaseModel

from .adapter import in_language, PROMPT_VERSION, ClaudeAdapter, Deadline
from .models import AiSuggestion, ModelVersion, Task

SYSTEM = (
    "You write a short summary for a university sustainability dashboard. Use only the figures given, "
    "copied exactly with the same units and written in digits. Do not calculate new numbers. Say that carbon "
    "figures are an estimated range and that the data is synthetic. Write 3 to 4 plain sentences, no headings or lists."
)


class ReportAnswer(BaseModel):
    summary: str


def scope_labels(scope):
    """The period and department a summary covers; a summary is shown only on a dashboard with the same scope."""
    return (f"{scope.date_from:%d %b %Y} to {scope.date_to:%d %b %Y}",
            str(scope.department or "All departments"))


def plain(value):
    """The figure as text, the way it should appear in the summary."""
    if value is None:
        return "N/A"
    if isinstance(value, Decimal):
        value = float(value)
    if isinstance(value, float):
        return f"{value:,.0f}" if abs(value) >= 100 else f"{value:,.1f}".rstrip("0").rstrip(".")
    return f"{value:,}"


def figures_text(totals, period, department):
    rate = totals["reuse_rate_percent"]
    rows = [
        ("Period", period), ("Department", department),
        ("Completed transfers", plain(totals["completed_transfers"])),
        ("Items reused", plain(totals["items_reused"])),
        ("Waste diverted (kg)", plain(totals["waste_diverted_kg"])),
        ("Confirmed avoided purchases (requests)", plain(totals["avoided_purchase_requests"])),
        ("Avoided purchase value (AED)", plain(totals["avoided_purchase_aed"])),
        ("Net financial savings (AED)", plain(totals["net_savings_aed"])),
        ("Carbon saved, low estimate (kg CO2e)", plain(totals["co2e_low_kg"])),
        ("Carbon saved, high estimate (kg CO2e)", plain(totals["co2e_high_kg"])),
        ("Reuse rate (%)", "N/A" if rate is None else plain(rate)),
    ]
    return "\n".join(f"{name}: {value}" for name, value in rows)


# A number with an optional minus sign, thousands separators and decimals, for example -150, 41,200 or 253.6.
NUMBER = re.compile(r"(?<![\w.])-?\d+(?:,\d{3})*(?:\.\d+)?")
MONTHS = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*"
# A day with a month name ("5 November", "Nov 5") or a full date ("2026-11-05") is not a figure.
DAY = re.compile(r"\b\d{1,2} " + MONTHS + r"\b|\b" + MONTHS + r" \d{1,2}\b|\b\d{4}-\d{2}-\d{2}\b")
UNIT_NAMES = re.compile(r"CO2e?|CO₂e?")
NUMBER_WORDS = re.compile(
    r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
    r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|"
    r"million|dozen)\b", re.IGNORECASE)


def unsupported_numbers(text, figures):
    """Numbers in the summary that are not among the database figures, plus numbers written in words.
    Only the years of the chosen period may appear besides the figures."""
    lines = figures.splitlines()
    period = next((line for line in lines if line.startswith("Period:")), "")
    figure_lines = "\n".join(line for line in lines if not line.startswith(("Period:", "Department:")))
    allowed = {n.replace(",", "") for n in NUMBER.findall(UNIT_NAMES.sub(" ", figure_lines))}
    years = set(re.findall(r"\b20\d\d\b", period))
    found = [word for word in NUMBER_WORDS.findall(text)]
    for raw in NUMBER.findall(DAY.sub(" ", UNIT_NAMES.sub(" ", text))):
        number = raw.replace(",", "")
        if number in allowed or number in years:
            continue
        # The same value written with a different number of decimals is fine (253.6 for 253.56).
        if any(abs(float(number) - float(a)) < 0.05 for a in allowed):
            continue
        found.append(raw)
    return found


def report_instructions():
    """In Arabic the dates of the period are left out: the figures check only knows English month names."""
    system = in_language(SYSTEM)
    if system != SYSTEM:
        system += ' Do not write the dates of the period; say "this period" instead.'
    return system


class ReportDraftService:
    def __init__(self, adapter=None):
        self.adapter = adapter or ClaudeAdapter()
        self.model = settings.AI["REPORT_MODEL"]

    def draft(self, totals, period, department, user):
        figures = figures_text(totals, period, department)
        answer = self.adapter.ask(Task.REPORT, self.model, report_instructions(), f"Figures:\n{figures}", ReportAnswer,
                                  Deadline(), max_tokens=2000)
        problems = unsupported_numbers(answer.summary, figures)
        return AiSuggestion.objects.create(
            task=Task.REPORT,
            model_version=ModelVersion.current(Task.REPORT, self.model, PROMPT_VERSION),
            suggestion={"summary": answer.summary.strip(), "figures": figures, "period": period,
                        "department": department},
            confidence=None,
            confidence_basis="No numeric confidence for report drafts (section 4)",
            explanation="Figures check: " + ("all numbers match the database" if not problems
                                             else "numbers not in the database: " + ", ".join(problems)),
            created_by=user,
        )
