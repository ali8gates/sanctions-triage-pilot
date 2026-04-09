"""Turn an attribute comparison into a match/mismatch tally and a single
displayed confidence score.

The rule an analyst actually applies is not a black box formula, it is
closer to a checklist: how many distinguishing attributes actually line up,
how many actively contradict, and whether the name overlap is doing any
real work on its own. A shared last name with a different date of birth,
different country, and different address is not a match, no matter how the
name looks. This module makes that checklist explicit.
"""

from dataclasses import dataclass

from .attributes import AttributeComparison

COMMON_NAME_SIMILARITY_THRESHOLD = 0.34


@dataclass(frozen=True)
class AttributeTally:
    match_count: int
    mismatch_count: int
    entity_type_mismatch: bool
    name_only_signal: bool
    score: float


def tally(comparison: AttributeComparison) -> AttributeTally:
    checks = (
        comparison.dob_match,
        comparison.address_match,
        comparison.nationality_match,
        comparison.occupation_match,
    )
    match_count = sum(1 for c in checks if c is True)
    mismatch_count = sum(1 for c in checks if c is False)
    entity_type_mismatch = not comparison.entity_type_match

    # When every other attribute is missing entirely, the only thing left
    # to go on is name similarity. That is a much weaker signal on its own
    # than any single confirmed attribute match, and should never carry a
    # case past a confirmed match or mismatch.
    name_only_signal = match_count == 0 and mismatch_count == 0

    score = float(match_count - mismatch_count)
    if entity_type_mismatch:
        score -= 3.0
    if name_only_signal:
        score += comparison.name_similarity * 2 - 1

    return AttributeTally(
        match_count=match_count,
        mismatch_count=mismatch_count,
        entity_type_mismatch=entity_type_mismatch,
        name_only_signal=name_only_signal,
        score=score,
    )


def confidence_score(comparison: AttributeComparison) -> float:
    return tally(comparison).score
