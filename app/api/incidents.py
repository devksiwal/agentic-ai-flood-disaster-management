
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agents.emergency_detection import detect_emergency
from app.database.connection import SessionLocal
from app.database.models import Incident, Resource, SystemEvent
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.agents.rescue_priority import calculate_priority
from app.agents.resource_allocation import recommend_resources
from app.orchestration.orchestrator import process_incident

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(
    payload: IncidentCreate,
    db: Session = Depends(get_db),
):
    incident = Incident(
        **payload.model_dump(),
        status="received",
        requires_review=True,
    )
    db.add(incident)
    db.flush()

    db.add(
        SystemEvent(
            event_type="SOS_RECEIVED",
            incident_id=incident.id,
            details=json.dumps({"source": "text_api"}),
        )
    )

    db.commit()
    db.refresh(incident)
    return incident


@router.get("", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.id.desc()).all()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.post("/{incident_id}/assess")
def assess_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    message = incident.translated_message or incident.original_message

    result = detect_emergency(
        message=message,
        location_text=incident.location_text,
        people_affected=incident.people_affected,
    )

    incident.emergency_type = result.emergency_type
    incident.requires_review = result.requires_review
    incident.status = "assessed"

    details = {
        "emergency_type": result.emergency_type,
        "confidence": result.confidence,
        "evidence": result.evidence,
        "missing_fields": result.missing_fields,
        "requires_review": result.requires_review,
        "method": "keyword_rules_v1",
    }

    db.add(
        SystemEvent(
            event_type="INCIDENT_ASSESSED",
            incident_id=incident.id,
            details=json.dumps(details),
        )
    )

    db.commit()
    db.refresh(incident)

    return {
        "incident_id": incident.id,
        **details,
        "status": incident.status,
    }

@router.post("/{incident_id}/prioritize")
def prioritize_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    message = incident.translated_message or incident.original_message

    result = calculate_priority(
        message=message,
        emergency_type=incident.emergency_type,
        people_affected=incident.people_affected,
        location_text=incident.location_text,
    )

    incident.priority_score = result.score
    incident.requires_review = (
        incident.requires_review or result.requires_review
    )

    details = {
        "score": result.score,
        "level": result.level,
        "factors": result.factors,
        "missing_fields": result.missing_fields,
        "requires_review": result.requires_review,
        "method": "rule_based_priority_v1",
    }

    db.add(
        SystemEvent(
            event_type="INCIDENT_PRIORITIZED",
            incident_id=incident.id,
            details=json.dumps(details),
        )
    )

    db.commit()
    db.refresh(incident)

    return {
        "incident_id": incident.id,
        **details,
    }


@router.post("/{incident_id}/allocate")
def allocate_resources(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    resources = db.query(Resource).all()

    resource_records = [
        {
            "id": resource.id,
            "name": resource.name,
            "resource_type": resource.resource_type,
            "capabilities": resource.capabilities,
            "capacity": resource.capacity,
            "available": resource.available,
            "status": resource.status,
        }
        for resource in resources
    ]

    result = process_incident(
        message=incident.original_message,
        location_text=incident.location_text,
        people_affected=incident.people_affected,
        resources=resource_records,
    )

    response = {
    "incident_id": incident.id,
    "emergency_detection": result.emergency_detection,
    "priority_assessment": result.priority_assessment,
    "resource_recommendation": result.resource_recommendation,
    "route_assessment": result.route_assessment,
    "workflow_events": result.workflow_events,
    "requires_human_approval": True,
}

    db.add(
        SystemEvent(
            event_type="ORCHESTRATED_INCIDENT_ASSESSMENT",
            incident_id=incident.id,
            details=json.dumps(response),
        )
    )

    db.commit()

    return response
