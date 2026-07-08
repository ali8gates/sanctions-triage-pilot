"""
Run: python demo.py

Written by Ali Gates.

Seven tickets, chosen to cover the exact three categories named in the
prioritization deck: password resets, software installs, access
requests, and every decision path within them.

  1-2. Password resets:        always auto-approve, but always logged
  3.   Software install:       on the approved catalog, clean approve
  4.   Software install:       off-catalog, agent approves via justification
  5.   Access request:         standard allowlist, clean approve
  6.   Access request:         high-sensitivity system, instant human escalation
  7.   Access request:         off-domain, unclear justification, agent defers to human
"""

from agent.orchestrator import HUMAN_REVIEW_QUEUE, process_ticket, print_outcome
from agent.policy import ITTicket, TicketType

tickets = [
    ITTicket(
        ticket_id="TKT-001",
        ticket_type=TicketType.PASSWORD_RESET,
        requester_role="sales",
        requester_tenure_days=600,
        justification="Locked out after vacation, need to reset.",
    ),
    ITTicket(
        ticket_id="TKT-002",
        ticket_type=TicketType.PASSWORD_RESET,
        requester_role="engineer",
        requester_tenure_days=5,
        justification="Forgot password during onboarding setup.",
    ),
    ITTicket(
        ticket_id="TKT-003",
        ticket_type=TicketType.SOFTWARE_INSTALL,
        requester_role="engineer",
        requester_tenure_days=400,
        software_name="VS Code",
        justification="Standard dev environment setup.",
    ),
    ITTicket(
        ticket_id="TKT-004",
        ticket_type=TicketType.SOFTWARE_INSTALL,
        requester_role="engineer",
        requester_tenure_days=200,
        software_name="Postman",
        justification="Needed for an engineering spike on the new integrations API.",
    ),
    ITTicket(
        ticket_id="TKT-005",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="engineer",
        requester_tenure_days=400,
        system_requested="github",
        justification="Standard day-to-day engineering work.",
    ),
    ITTicket(
        ticket_id="TKT-006",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="engineer",
        requester_tenure_days=400,
        system_requested="production_db",
        justification="Debugging an incident, need to inspect prod data directly.",
    ),
    ITTicket(
        ticket_id="TKT-007",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="contractor",
        requester_tenure_days=90,
        system_requested="commission_dashboard",
        justification="Wanted to see how it works out of curiosity.",
    ),
]

if __name__ == "__main__":
    outcomes = []
    for t in tickets:
        outcome = process_ticket(t)
        outcomes.append(outcome)
        print_outcome(outcome)

    auto_count = sum(1 for o in outcomes if o.final_decision.value.startswith("auto"))
    print(f"\n\n{len(HUMAN_REVIEW_QUEUE)} ticket(s) in the human review queue "
          f"after {len(tickets)} total tickets ({auto_count} resolved automatically). "
          f"Every one, automated or escalated, has a full, pre-written audit trail attached.")
    print("\nThis is the prioritization from the deck, running as code:")
    print("  - Password resets: automated by default, always logged")
    print("  - Software installs: catalog match auto-approves; everything else gets a purpose check")
    print("  - Access requests: the one category where role + sensitivity genuinely gate the decision\n")
