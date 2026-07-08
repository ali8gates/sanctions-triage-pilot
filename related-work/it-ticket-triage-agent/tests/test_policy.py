from agent.policy import ITTicket, PolicyDecision, TicketType, evaluate


def test_password_reset_always_auto_approves_even_for_a_new_hire():
    ticket = ITTicket(
        ticket_id="TKT-002",
        ticket_type=TicketType.PASSWORD_RESET,
        requester_role="engineer",
        requester_tenure_days=5,
        justification="Forgot password during onboarding setup.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.AUTO_APPROVE


def test_catalog_software_auto_approves():
    ticket = ITTicket(
        ticket_id="TKT-003",
        ticket_type=TicketType.SOFTWARE_INSTALL,
        requester_role="engineer",
        requester_tenure_days=400,
        software_name="VS Code",
        justification="Standard dev environment setup.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.AUTO_APPROVE


def test_off_catalog_software_with_specific_justification_approves_with_justification():
    ticket = ITTicket(
        ticket_id="TKT-004",
        ticket_type=TicketType.SOFTWARE_INSTALL,
        requester_role="engineer",
        requester_tenure_days=200,
        software_name="Postman",
        justification="Needed for an engineering spike on the new integrations API.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.AUTO_APPROVE_WITH_JUSTIFICATION


def test_standard_allowlist_access_request_auto_approves():
    ticket = ITTicket(
        ticket_id="TKT-005",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="engineer",
        requester_tenure_days=400,
        system_requested="github",
        justification="Standard day-to-day engineering work.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.AUTO_APPROVE


def test_high_sensitivity_system_always_escalates():
    ticket = ITTicket(
        ticket_id="TKT-006",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="engineer",
        requester_tenure_days=400,
        system_requested="production_db",
        justification="Debugging an incident, need to inspect prod data directly.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.ESCALATE


def test_off_domain_request_with_weak_justification_escalates():
    ticket = ITTicket(
        ticket_id="TKT-007",
        ticket_type=TicketType.ACCESS_REQUEST,
        requester_role="contractor",
        requester_tenure_days=90,
        system_requested="commission_dashboard",
        justification="Wanted to see how it works out of curiosity.",
    )
    decision, _ = evaluate(ticket)
    assert decision is PolicyDecision.ESCALATE


def test_every_decision_has_a_written_reason():
    ticket = ITTicket(
        ticket_id="TKT-001",
        ticket_type=TicketType.PASSWORD_RESET,
        requester_role="sales",
        requester_tenure_days=600,
        justification="Locked out after vacation, need to reset.",
    )
    _, reason = evaluate(ticket)
    assert len(reason) > 0
