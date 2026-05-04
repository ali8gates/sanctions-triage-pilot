"""Batch triage over a list of alerts, plus the summary stats that made the
business case for building this instead of buying a license.
"""

from dataclasses import dataclass

from .decision import Disposition, TriageResult, triage
from .models import Alert

# Illustrative time estimates, drawn from the discovery notes: a very quick
# false positive is about 2 minutes of analyst time, a case that needed
# escalation and research runs closer to 15 to 20 minutes.
MINUTES_PER_AUTO_CLOSED_CASE_BY_HAND = 2.0
MINUTES_PER_ESCALATED_CASE = 17.0


@dataclass(frozen=True)
class BatchSummary:
    total: int
    auto_closed: int
    escalated: int
    estimated_analyst_minutes_saved: float

    @property
    def auto_close_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.auto_closed / self.total


def run_batch(alerts: list[Alert]) -> tuple[list[TriageResult], BatchSummary]:
    results = [triage(alert) for alert in alerts]
    auto_closed = sum(1 for r in results if r.disposition is Disposition.AUTO_CLOSED_FALSE_POSITIVE)
    escalated = len(results) - auto_closed
    # Minutes saved is the time an analyst would have spent confirming the
    # same obvious false positives by hand, since those are the only cases
    # this pipeline resolves without a human.
    minutes_saved = auto_closed * MINUTES_PER_AUTO_CLOSED_CASE_BY_HAND
    summary = BatchSummary(
        total=len(results),
        auto_closed=auto_closed,
        escalated=escalated,
        estimated_analyst_minutes_saved=minutes_saved,
    )
    return results, summary
