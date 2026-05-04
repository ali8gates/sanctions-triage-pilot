"""Command line entry point for the sanctions triage pilot demo.

Run it with:

    python -m sanctions_triage.cli

Everything it processes is synthetic sample data. See sample_data.py.
"""

from .decision import Disposition
from .pipeline import run_batch
from .sample_data import SAMPLE_ALERTS

DIVIDER = "-" * 78


def _print_result(result) -> None:
    alert = result.alert
    tag = "AUTO CLOSED " if result.disposition is Disposition.AUTO_CLOSED_FALSE_POSITIVE else "ESCALATED   "
    print(f"[{tag}] {alert.alert_id}  source={alert.source.value}  score={result.score:+.2f}")
    print(f"    record: {alert.record.full_name}")
    print(f"    hit:    {result.alert.hit.matched_name}  ({result.alert.hit.list_name})")
    print(f"    note:   {result.rationale}")
    print()


def main() -> None:
    print(DIVIDER)
    print("Sanctions and PEP alert triage pilot, demo run on synthetic data")
    print(DIVIDER)
    print()

    results, summary = run_batch(SAMPLE_ALERTS)

    for result in results:
        _print_result(result)

    print(DIVIDER)
    print("Batch summary")
    print(DIVIDER)
    print(f"Alerts processed:        {summary.total}")
    print(f"Auto closed (false pos): {summary.auto_closed}  ({summary.auto_close_rate:.0%})")
    print(f"Escalated for review:    {summary.escalated}")
    print(f"Est. analyst minutes saved on this batch: {summary.estimated_analyst_minutes_saved:.0f}")
    print()
    print("At the volumes in the discovery notes, name sanctions/PEP alone runs")
    print("about 3,750 alerts a month with a 99 percent false positive rate.")
    print("Auto closing even a conservative share of the obvious false positives")
    print("at this volume is where the time actually comes back to L1 and L2.")
    print()
    print("This pilot was built and deployed in 90 days, evaluated against")
    print("licensing UiPath or WorkFusion for the same workflow, and runs today")
    print("for under 10,000 dollars a year to maintain, versus a cost avoided")
    print("of more than 1,000,000 dollars over 3 years on the vendor path.")


if __name__ == "__main__":
    main()
