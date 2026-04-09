"""Synthetic sample alerts.

Every name, address, and date of birth below is invented for this repo.
None of it reflects a real Varo customer, a real watchlist record, or a
real true match. The shape of the data, one screening record and one
watchlist hit per alert, mirrors what actually comes back from a screening
engine like Bridger, but the content is fiction end to end.
"""

from .models import Alert, AlertSource, EntityType, ScreeningRecord, WatchlistHit

SAMPLE_ALERTS: list[Alert] = [
    # Obvious false positive: shared last name only, everything else differs.
    Alert(
        alert_id="ALERT-1001",
        source=AlertSource.NAME_SANCTIONS_PEP,
        record=ScreeningRecord(
            full_name="Maria Alvarez",
            date_of_birth="1994-03-02",
            address="118 Larkspur Ln, Austin, TX",
            nationality="United States",
            occupation="Retail associate",
            entity_type=EntityType.PERSON,
        ),
        hit=WatchlistHit(
            list_name="OFAC SDN",
            matched_name="Alvarez, Maria",
            date_of_birth="1958-11-19",
            address="Calle 42, Caracas, Venezuela",
            nationality="Venezuela",
            occupation="Government official",
            entity_type=EntityType.PERSON,
            source_links=("https://example.gov/sdn/example-entry",),
        ),
    ),
    # Obvious false positive: business vs person, no other overlap.
    Alert(
        alert_id="ALERT-1002",
        source=AlertSource.PAYMENT_SCREENING,
        record=ScreeningRecord(
            full_name="Summit Hardware Supply LLC",
            date_of_birth=None,
            address="4400 Industrial Pkwy, Reno, NV",
            nationality=None,
            occupation=None,
            entity_type=EntityType.BUSINESS,
        ),
        hit=WatchlistHit(
            list_name="Consolidated Sanctions List",
            matched_name="Summit Trading",
            date_of_birth=None,
            address=None,
            nationality=None,
            occupation=None,
            entity_type=EntityType.PERSON,
        ),
    ),
    # Genuinely ambiguous: name and nationality line up, DOB unknown, needs a human.
    Alert(
        alert_id="ALERT-1003",
        source=AlertSource.NAME_SANCTIONS_PEP,
        record=ScreeningRecord(
            full_name="David Chen",
            date_of_birth=None,
            address="88 Riverside Dr, Seattle, WA",
            nationality="China",
            occupation="Import export consultant",
            entity_type=EntityType.PERSON,
        ),
        hit=WatchlistHit(
            list_name="Foreign PEP List",
            matched_name="Chen, David",
            date_of_birth=None,
            address=None,
            nationality="China",
            occupation="Trade official",
            entity_type=EntityType.PERSON,
            source_links=("https://example.org/news/example-official",),
        ),
    ),
    # Close match on everything available: should escalate, not auto close.
    Alert(
        alert_id="ALERT-1004",
        source=AlertSource.ADVERSE_MEDIA,
        record=ScreeningRecord(
            full_name="Anton Petrov",
            date_of_birth="1979-06-14",
            address="12 Birch St, Newark, NJ",
            nationality="Russia",
            occupation="Freight logistics manager",
            entity_type=EntityType.PERSON,
        ),
        hit=WatchlistHit(
            list_name="Adverse Media",
            matched_name="Anton Petrov",
            date_of_birth="1979-06-14",
            address="12 Birch St, Newark, NJ",
            nationality="Russia",
            occupation="Logistics executive",
            entity_type=EntityType.PERSON,
            source_links=("https://example.com/news/example-case",),
        ),
    ),
    # Payment screening false positive: common name, mismatched country and DOB.
    Alert(
        alert_id="ALERT-1005",
        source=AlertSource.PAYMENT_SCREENING,
        record=ScreeningRecord(
            full_name="John Smith",
            date_of_birth="1988-01-22",
            address="220 Oak Ave, Denver, CO",
            nationality="United States",
            occupation="Software engineer",
            entity_type=EntityType.PERSON,
        ),
        hit=WatchlistHit(
            list_name="OFAC SDN",
            matched_name="Smith, John",
            date_of_birth="1962-09-05",
            address="Unit 4, Lagos, Nigeria",
            nationality="Nigeria",
            occupation="Arms broker",
            entity_type=EntityType.PERSON,
            source_links=("https://example.gov/sdn/example-entry-2",),
        ),
    ),
    # Nightly ongoing screening false positive: address and DOB both differ.
    Alert(
        alert_id="ALERT-1006",
        source=AlertSource.NAME_SANCTIONS_PEP,
        record=ScreeningRecord(
            full_name="Fatima Hassan",
            date_of_birth="2001-05-30",
            address="77 Cedar Ct, Minneapolis, MN",
            nationality="United States",
            occupation="Nursing student",
            entity_type=EntityType.PERSON,
        ),
        hit=WatchlistHit(
            list_name="Global Sanctions",
            matched_name="Hassan, Fatima",
            date_of_birth="1970-02-11",
            address="Sector 4, Karachi, Pakistan",
            nationality="Pakistan",
            occupation="Unknown",
            entity_type=EntityType.PERSON,
        ),
    ),
]
