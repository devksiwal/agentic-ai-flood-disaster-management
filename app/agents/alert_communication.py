
from dataclasses import dataclass, field


@dataclass
class AlertDraft:
    status: str
    incident_type: str
    priority_level: str
    priority_score: int
    location: str | None
    people_affected: int | None
    message: str
    missing_fields: list[str] = field(default_factory=list)
    requires_human_approval: bool = True
    sent: bool = False


def create_alert(
    incident_type: str,
    priority_level: str,
    priority_score: int,
    location: str | None,
    people_affected: int | None,
) -> AlertDraft:
    """
    Prepare an emergency alert for human review.

    This function does not send messages or contact emergency services.
    """

    missing_fields = []

    if not location or not location.strip():
        missing_fields.append("location")

    if people_affected is None:
        missing_fields.append("people_affected")

    if incident_type in {"unclassified", "multiple_or_ambiguous"}:
        missing_fields.append("confirmed_incident_type")

    if missing_fields:
        status = "requires_clarification"
    else:
        status = "pending_human_approval"

    message = (
        f"FLOOD DISASTER MANAGEMENT ALERT\n"
        f"Incident type: {incident_type}\n"
        f"Priority: {priority_level} ({priority_score}/100)\n"
        f"Location: {location or 'Unknown - confirmation required'}\n"
        f"People affected: "
        f"{people_affected if people_affected is not None else 'Unknown'}\n"
        f"Review status: {status}\n"
        f"NOTIFICATION NOT SENT - human review required."
    )

    return AlertDraft(
        status=status,
        incident_type=incident_type,
        priority_level=priority_level,
        priority_score=priority_score,
        location=location,
        people_affected=people_affected,
        message=message,
        missing_fields=missing_fields,
        requires_human_approval=True,
        sent=False,
    )
