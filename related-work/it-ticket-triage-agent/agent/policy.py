"""Policy layer: the rules an IT ticket is checked against.

Same shape as the sanctions triage agent in this repo, applied to a
different queue. No path here auto-approves a high-sensitivity access
request, and no path denies a request outright. Anything the policy is
not confident about routes to a human, with a written reason attached.
"""

from dataclasses import dataclass
from enum import Enum

APPROVED_SOFTWARE_CATALOG = {
    "vs code",
    "slack",
    "zoom",
    "docker desktop",
    "microsoft office",
}

STANDARD_ACCESS_ALLOWLIST = {
    "github": {"engineer"},
    "jira": {"engineer", "pm"},
    "figma": {"design", "pm"},
}

HIGH_SENSITIVITY_SYSTEMS = {
    "production_db",
    "payroll_system",
    "customer_pii_store",
}

WEAK_JUSTIFICATION_SIGNALS = (
    "curiosity",
    "wanted to see",
    "just because",
    "not sure",
    "no reason",
)

MIN_JUSTIFICATION_WORDS = 6


class TicketType(Enum):
    PASSWORD_RESET = "password_reset"
    SOFTWARE_INSTALL = "software_install"
    ACCESS_REQUEST = "access_request"


class PolicyDecision(Enum):
    AUTO_APPROVE = "auto_approve"
    AUTO_APPROVE_WITH_JUSTIFICATION = "auto_approve_with_justification"
    ESCALATE = "escalate"


@dataclass(frozen=True)
class ITTicket:
    """One IT ticket. Only the fields the policy actually needs."""

    ticket_id: str
    ticket_type: TicketType
    requester_role: str
    requester_tenure_days: int
    justification: str
    software_name: str | None = None
    system_requested: str | None = None


def _justification_is_specific(justification: str) -> bool:
    """A justification counts as specific if it names a real task and is not a
    generic one liner. This is intentionally simple, it is a policy gate, not
    a language model call, and it needs to be explainable in an audit trail.
    """

    lowered = justification.lower()
    if any(signal in lowered for signal in WEAK_JUSTIFICATION_SIGNALS):
        return False
    return len(justification.split()) >= MIN_JUSTIFICATION_WORDS


def evaluate(ticket: ITTicket) -> tuple[PolicyDecision, str]:
    """Returns the policy decision and a written reason for it.

    The reason is not an afterthought, it is what makes the auto-approved
    path defensible later. Every outcome, automated or escalated, carries
    one.
    """

    if ticket.ticket_type is TicketType.PASSWORD_RESET:
        return (
            PolicyDecision.AUTO_APPROVE,
            "Password resets are auto-approved by policy and always logged.",
        )

    if ticket.ticket_type is TicketType.SOFTWARE_INSTALL:
        name = (ticket.software_name or "").strip().lower()
        if name in APPROVED_SOFTWARE_CATALOG:
            return (
                PolicyDecision.AUTO_APPROVE,
                f"{ticket.software_name} is on the approved software catalog.",
            )
        if _justification_is_specific(ticket.justification):
            return (
                PolicyDecision.AUTO_APPROVE_WITH_JUSTIFICATION,
                f"{ticket.software_name} is off the approved catalog, but the "
                f'justification ties it to a specific work task: "{ticket.justification}"',
            )
        return (
            PolicyDecision.ESCALATE,
            f"{ticket.software_name} is off the approved catalog and the "
            "justification does not tie it to a specific work task.",
        )

    if ticket.ticket_type is TicketType.ACCESS_REQUEST:
        system = (ticket.system_requested or "").strip().lower()
        if system in HIGH_SENSITIVITY_SYSTEMS:
            return (
                PolicyDecision.ESCALATE,
                f"{ticket.system_requested} is a high-sensitivity system, every "
                "request routes to a human regardless of justification.",
            )
        allowed_roles = STANDARD_ACCESS_ALLOWLIST.get(system)
        if allowed_roles and ticket.requester_role in allowed_roles:
            return (
                PolicyDecision.AUTO_APPROVE,
                f"{ticket.requester_role} requesting {ticket.system_requested} "
                "matches the standard access allowlist.",
            )
        return (
            PolicyDecision.ESCALATE,
            f"{ticket.system_requested} is not on the standard allowlist for "
            f"{ticket.requester_role}, so this needs a human to confirm it.",
        )

    raise ValueError(f"Unhandled ticket type: {ticket.ticket_type}")
