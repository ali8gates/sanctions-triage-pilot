from sanctions_triage.decision import Disposition, triage
from sanctions_triage.sample_data import SAMPLE_ALERTS


def _find(alert_id):
    return next(a for a in SAMPLE_ALERTS if a.alert_id == alert_id)


def test_mismatched_dob_and_country_auto_closes():
    result = triage(_find("ALERT-1001"))
    assert result.disposition is Disposition.AUTO_CLOSED_FALSE_POSITIVE


def test_person_vs_business_auto_closes():
    result = triage(_find("ALERT-1002"))
    assert result.disposition is Disposition.AUTO_CLOSED_FALSE_POSITIVE


def test_close_match_on_every_available_attribute_escalates():
    result = triage(_find("ALERT-1004"))
    assert result.disposition is Disposition.ESCALATED_FOR_REVIEW


def test_missing_dob_never_auto_closes_on_dob_alone():
    result = triage(_find("ALERT-1003"))
    # Nationality and name line up and DOB is unknown, so this should not be
    # treated as confidently resolved either way.
    assert result.disposition is Disposition.ESCALATED_FOR_REVIEW


def test_every_disposition_has_a_rationale():
    for alert in SAMPLE_ALERTS:
        result = triage(alert)
        assert len(result.rationale) > 0
