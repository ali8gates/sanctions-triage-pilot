from agent.orchestrator import HUMAN_REVIEW_QUEUE, FinalDecision, process_ticket
from agent.policy import ITTicket, TicketType


def test_escalated_ticket_lands_in_the_human_review_queue():
    HUMAN_REVIEW_QUEUE.clear()
    ticket = ITTicket(
        ticket_id="TKT-TEST-1",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="engineer",
        requester_tenure_days=400,
        system_requested="production_db",
        justification="Debugging an incident, need to inspect prod data directly.",
    )
    outcome = process_ticket(ticket)
    assert outcome.final_decision is FinalDecision.ESCALATED_TO_HUMAN
    assert outcome in HUMAN_REVIEW_QUEUE


def test_auto_approved_ticket_never_reaches_the_queue():
    HUMAN_REVIEW_QUEUE.clear()
    ticket = ITTicket(
        ticket_id="TKT-TEST-2",
        ticket_type=TicketType.PASSWORD_RESET,
        requester_role="sales",
        requester_tenure_days=600,
        justification="Locked out after vacation, need to reset.",
    )
    outcome = process_ticket(ticket)
    assert outcome.final_decision is FinalDecision.AUTO_APPROVED
    assert outcome not in HUMAN_REVIEW_QUEUE
