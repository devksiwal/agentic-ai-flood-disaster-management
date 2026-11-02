
from dataclasses import dataclass, field

from app.agents.emergency_detection import detect_emergency
from app.agents.rescue_priority import calculate_priority
from app.agents.resource_allocation import recommend_resources
from app.agents.route_planning import assess_route
from app.agents.alert_communication import create_alert

@dataclass
class WorkflowResult:
    alert_draft: dict
    emergency_detection: dict
    priority_assessment: dict
    resource_recommendation: dict
    route_assessment: dict
    workflow_events: list[str] = field(default_factory=list)


def process_incident(
    message: str,
    location_text: str | None,
    people_affected: int | None,
    resources: list[dict],
) -> WorkflowResult:
    events = ["INCIDENT_RECEIVED"]

    detection = detect_emergency(
        message=message,
        location_text=location_text,
        people_affected=people_affected,
    )
    events.append("EMERGENCY_DETECTION_COMPLETED")

    priority = calculate_priority(
        message=message,
        emergency_type=detection.emergency_type,
        people_affected=people_affected,
        location_text=location_text,
    )
    events.append("PRIORITY_ASSESSMENT_COMPLETED")
    # The reported incident location is not a verified rescue destination.
    # Assess route-data availability without claiming the route is safe.
    route_assessment = assess_route(
        origin=location_text,
        destination=None,
    )
    events.append("ROUTE_ASSESSMENT_COMPLETED")
    alert = create_alert(
        incident_type=detection.emergency_type,
        priority_level=priority.level,
        priority_score=priority.score,
        location=location_text,
        people_affected=people_affected,
    )
    events.append("ALERT_DRAFT_CREATED")

    # Do not recommend resources automatically for an
    # unclassified incident. Ask for clarification instead.
    if detection.emergency_type in {
        "unclassified",
        "multiple_or_ambiguous",
    }:
        allocation = {
            "status": "requires_clarification",
            "candidates": [],
            "rejection_reasons": [],
            "requires_human_approval": True,
        }
        events.append("RESOURCE_ALLOCATION_HELD")
    else:
        result = recommend_resources(
            emergency_type=detection.emergency_type,
            people_affected=people_affected,
            resources=resources,
        )
        allocation = {
            "status": result.status,
            "candidates": result.candidates,
            "rejection_reasons": result.rejection_reasons,
            "requires_human_approval": True,
        }
        events.append("RESOURCE_RECOMMENDATION_GENERATED")

    return WorkflowResult(
        emergency_detection={
            "emergency_type": detection.emergency_type,
            "confidence": detection.confidence,
            "evidence": detection.evidence,
            "missing_fields": detection.missing_fields,
            "requires_review": detection.requires_review,
        },
        priority_assessment={
            "score": priority.score,
            "level": priority.level,
            "factors": priority.factors,
            "missing_fields": priority.missing_fields,
            "requires_review": priority.requires_review,
        },
        resource_recommendation=allocation,
        route_assessment={
            "status": route_assessment.status,
            "origin": route_assessment.origin,
            "destination": route_assessment.destination,
            "route_available": route_assessment.route_available,
            "safety_status": route_assessment.safety_status,
            "missing_data": route_assessment.missing_data,
            "warnings": route_assessment.warnings,
            "requires_human_review": route_assessment.requires_human_review,
        },
        alert_draft={
            "status": alert.status,
            "incident_type": alert.incident_type,
            "priority_level": alert.priority_level,
            "priority_score": alert.priority_score,
            "location": alert.location,
            "people_affected": alert.people_affected,
            "message": alert.message,
            "missing_fields": alert.missing_fields,
            "requires_human_approval": alert.requires_human_approval,
            "sent": alert.sent,
        },
        workflow_events=events,

    )
    