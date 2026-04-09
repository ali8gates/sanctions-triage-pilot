"""The decision layer: close as false positive, or escalate for a human.

Nothing in here closes a confirmed or ambiguous true match automatically,
and nothing here removes a human from the loop for anything above the
confident false positive line. The goal was never to remove L1 review, it
was to stop spending analyst minutes confirming the obvious cases by hand
so the harder cases got more attention, not less.

An alert auto closes only when the evidence against it is unambiguous:
either the entity type itself does not match (a business flagged against a
person, or vice versa), or at least two attributes actively contradict the
watchlist hit with no attribute actually confirming it. A shared or similar
name is never enough on its own, and any real, confirmed match on date of
birth, address, nationality, or occupation always routes to a human.
"""

from dataclasses import dataclass
from enum import Enum

from .attributes import AttributeComparison, compare
from .models import Alert
from .scoring import AttributeTally, tally

MIN_CONTRADICTIONS_TO_AUTO_CLOSE = 2


class Disposition(Enum):
    AUTO_CLOSED_FALSE_POSITIVE = "auto_closed_false_positive"
    ESCALATED_FOR_REVIEW = "escalated_for_review"


@dataclass(frozen=True)
class TriageResult:
    alert: Alert
    comparison: AttributeComparison
    score: float
    disposition: Disposition
    rationale: str


def _decide(comparison: AttributeComparison, counts: AttributeTally) -> Disposition:
    if counts.entity_type_mismatch:
        return Disposition.AUTO_CLOSED_FALSE_POSITIVE
    if counts.match_count == 0 and counts.mismatch_count >= MIN_CONTRADICTIONS_TO_AUTO_CLOSE:
        return Disposition.AUTO_CLOSED_FALSE_POSITIVE
    if counts.name_only_signal and comparison.name_similarity < 0.5:
        return Disposition.AUTO_CLOSED_FALSE_POSITIVE
    return Disposition.ESCALATED_FOR_REVIEW


def _build_rationale(comparison: AttributeComparison, counts: AttributeTally, disposition: Disposition) -> str:
    parts = [f"name similarity {comparison.name_similarity:.2f}"]
    if comparison.dob_match is not None:
        parts.append(f"date of birth {'matches' if comparison.dob_match else 'does not match'}")
    else:
        parts.append("date of birth not available")
    if comparison.address_match is not None:
        parts.append(f"address {'matches' if comparison.address_match else 'does not match'}")
    if comparison.nationality_match is not None:
        parts.append(f"nationality {'matches' if comparison.nationality_match else 'does not match'}")
    if comparison.occupation_match is not None:
        parts.append(f"occupation {'matches' if comparison.occupation_match else 'does not match'}")
    if counts.entity_type_mismatch:
        parts.append("entity type does not match (person vs business)")
    if not comparison.has_source_links:
        parts.append("no supporting source links on the hit")

    summary = ", ".join(parts)
    if disposition is Disposition.AUTO_CLOSED_FALSE_POSITIVE:
        return f"Auto closed. {summary}."
    return f"Escalated for L1 review. {summary}."


def triage(alert: Alert) -> TriageResult:
    comparison = compare(alert)
    counts = tally(comparison)
    disposition = _decide(comparison, counts)
    rationale = _build_rationale(comparison, counts, disposition)
    return TriageResult(
        alert=alert,
        comparison=comparison,
        score=counts.score,
        disposition=disposition,
        rationale=rationale,
    )
