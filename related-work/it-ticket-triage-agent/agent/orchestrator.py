"""Orchestration layer: run a ticket through policy, log it, route it.

Every ticket gets a written outcome, whether it auto-resolves or lands in
the human review queue. Nothing here is silent. This is the same shape as
the sanctions triage agent elsewhere in this repo: a policy layer that
returns a decision and a reason, and an orchestrator that turns that into
an auditable outcome and, when needed, a queue entry for a person.
"""

from dataclasses import dataclass
from enum import Enum

from .policy import ITTicket, PolicyDecision, evaluate

HUMAN_REVIEW_QUEUE: list["TicketOutcome"] = []


class FinalDecision(Enum):
    AUTO_APPROVED = "auto_approved"
    AUTO_APPROVED_WITH_JUSTIFICATION = "auto_approved_with_justification"
    ESCALATED_TO_HUMAN = "escalated_to_human"


_POLICY_TO_FINAL = {
    PolicyDecision.AUTO_APPROVE: FinalDecision.AUTO_APPROVED,
    PolicyDecision.AUTO_APPROVE_WITH_JUSTIFICATION: FinalDecision.AUTO_APPROVED_WITH_JUSTIFICATION,
    PolicyDecision.ESCALATE: FinalDecision.ESCALATED_TO_HUMAN,
}

_TAGS = {
    FinalDecision.AUTO_APPROVED: "AUTO APPROVED",
    FinalDecision.AUTO_APPROVED_WITH_JUSTIFICATION: "AUTO APPROVED, JUSTIFIED",
    FinalDecision.ESCALATED_TO_HUMAN: "ESCALATED TO HUMAN",
}


@dataclass(frozen=True)
class TicketOutcome:
    ticket: ITTicket
    final_decision: FinalDecision
    rationale: str


def process_ticket(ticket: ITTicket) -> TicketOutcome:
    """Runs one ticket through policy and records the outcome.

    Escalated tickets are appended to the human review queue so nothing
    that needed a person gets lost between the agent and the inbox.
    """

    policy_decision, rationale = evaluate(ticket)
    final_decision = _POLICY_TO_FINAL[policy_decision]
    outcome = TicketOutcome(ticket=ticket, final_decision=final_decision, rationale=rationale)
    if final_decision is FinalDecision.ESCALATED_TO_HUMAN:
        HUMAN_REVIEW_QUEUE.append(outcome)
    return outcome


def print_outcome(outcome: TicketOutcome) -> None:
    ticket = outcome.ticket
    tag = _TAGS[outcome.final_decision]
    print(f"[{tag}] {ticket.ticket_id}  type={ticket.ticket_type.value}  role={ticket.requester_role}")
    print(f"    justification: {ticket.justification}")
    print(f"    note:          {outcome.rationale}")
    print()
