from sanctions_triage.pipeline import run_batch
from sanctions_triage.sample_data import SAMPLE_ALERTS


def test_run_batch_covers_every_alert():
    results, summary = run_batch(SAMPLE_ALERTS)
    assert len(results) == len(SAMPLE_ALERTS)
    assert summary.total == len(SAMPLE_ALERTS)
    assert summary.auto_closed + summary.escalated == summary.total


def test_summary_minutes_saved_is_nonnegative():
    _, summary = run_batch(SAMPLE_ALERTS)
    assert summary.estimated_analyst_minutes_saved >= 0
