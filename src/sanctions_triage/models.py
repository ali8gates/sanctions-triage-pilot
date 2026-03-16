"""Data shapes for an alert and the watchlist hit attached to it.

This mirrors the attribute set analysts actually compare during review: name,
date of birth, address, nationality, occupation, and entity type. See
docs in the wiki for where this list came from.
"""

from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    PERSON = "person"
    BUSINESS = "business"


class AlertSource(Enum):
    NAME_SANCTIONS_PEP = "name_sanctions_pep"
    ADVERSE_MEDIA = "adverse_media"
    PAYMENT_SCREENING = "payment_screening"


@dataclass(frozen=True)
class ScreeningRecord:
    """The customer, transaction, vendor, or employee record being screened."""

    full_name: str
    date_of_birth: str | None
    address: str | None
    nationality: str | None
    occupation: str | None
    entity_type: EntityType


@dataclass(frozen=True)
class WatchlistHit:
    """The watchlist record the screening engine matched against."""

    list_name: str
    matched_name: str
    date_of_birth: str | None
    address: str | None
    nationality: str | None
    occupation: str | None
    entity_type: EntityType
    source_links: tuple[str, ...] = ()


@dataclass(frozen=True)
class Alert:
    """One alert as it would arrive from the screening engine."""

    alert_id: str
    source: AlertSource
    record: ScreeningRecord
    hit: WatchlistHit
