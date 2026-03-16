"""Attribute comparison between a screening record and a watchlist hit.

This is the part that used to live entirely in an analyst's head: compare
name, date of birth, address, nationality, occupation, and entity type, and
decide whether there is enough here to keep looking or enough to close it
out. The functions below make each of those comparisons explicit and
reusable instead of implicit and undocumented.
"""

from dataclasses import dataclass

from .models import Alert


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().lower().replace(",", " ").replace(".", " ")
    return " ".join(cleaned.split())


def name_similarity(name_a: str | None, name_b: str | None) -> float:
    """Return a rough similarity score between two names, 0 to 1.

    A real implementation would use a proper fuzzy matching library tuned
    against known alias patterns. This is a simplified token overlap
    measure, enough to show the shape of the comparison without depending
    on any external library.
    """

    a, b = _normalize(name_a), _normalize(name_b)
    if not a or not b:
        return 0.0
    tokens_a, tokens_b = set(a.split()), set(b.split())
    if not tokens_a or not tokens_b:
        return 0.0
    overlap = len(tokens_a & tokens_b)
    return overlap / max(len(tokens_a), len(tokens_b))


def dob_matches(dob_a: str | None, dob_b: str | None) -> bool | None:
    """True if both dates are present and equal, False if both present and
    different, None if either side is missing (an analyst would need to
    research this, not assume it away)."""

    if dob_a is None or dob_b is None:
        return None
    return _normalize(dob_a) == _normalize(dob_b)


def field_matches(value_a: str | None, value_b: str | None) -> bool | None:
    if value_a is None or value_b is None:
        return None
    return _normalize(value_a) == _normalize(value_b)


@dataclass(frozen=True)
class AttributeComparison:
    """The full set of attribute comparisons for one alert, one place."""

    name_similarity: float
    dob_match: bool | None
    address_match: bool | None
    nationality_match: bool | None
    occupation_match: bool | None
    entity_type_match: bool
    has_source_links: bool


def compare(alert: Alert) -> AttributeComparison:
    record, hit = alert.record, alert.hit
    return AttributeComparison(
        name_similarity=name_similarity(record.full_name, hit.matched_name),
        dob_match=dob_matches(record.date_of_birth, hit.date_of_birth),
        address_match=field_matches(record.address, hit.address),
        nationality_match=field_matches(record.nationality, hit.nationality),
        occupation_match=field_matches(record.occupation, hit.occupation),
        entity_type_match=record.entity_type == hit.entity_type,
        has_source_links=len(hit.source_links) > 0,
    )
