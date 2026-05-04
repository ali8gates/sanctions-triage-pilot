from sanctions_triage.attributes import compare, dob_matches, name_similarity
from sanctions_triage.sample_data import SAMPLE_ALERTS


def test_name_similarity_full_overlap():
    assert name_similarity("David Chen", "Chen, David") == 1.0


def test_name_similarity_no_overlap():
    assert name_similarity("Maria Alvarez", "John Smith") == 0.0


def test_dob_matches_handles_missing_values():
    assert dob_matches(None, "1990-01-01") is None
    assert dob_matches("1990-01-01", "1990-01-01") is True
    assert dob_matches("1990-01-01", "1991-01-01") is False


def test_compare_runs_on_every_sample_alert():
    for alert in SAMPLE_ALERTS:
        result = compare(alert)
        assert 0.0 <= result.name_similarity <= 1.0
