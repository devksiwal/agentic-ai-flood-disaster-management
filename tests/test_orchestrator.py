
from app.orchestration.orchestrator import process_incident


def test_workflow_processes_flood_rescue():
    resources = [
        {
            "id": 1,
            "name": "Test Boat",
            "resource_type": "boat",
            "capabilities": "water_rescue",
            "capacity": 5,
            "available": True,
            "status": "available",
        }
    ]

    result = process_incident(
        message="Flood water is entering our house. Three people need rescue.",
        location_text="Patna, Bihar",
        people_affected=3,
        resources=resources,
    )

    assert result.emergency_detection["emergency_type"] == "flood_rescue"
    assert result.priority_assessment["score"] == 45
    assert result.resource_recommendation["status"] == "candidates_found"
    assert len(result.resource_recommendation["candidates"]) > 0
    assert result.resource_recommendation["requires_human_approval"] is True
    assert "EMERGENCY_DETECTION_COMPLETED" in result.workflow_events
    assert "PRIORITY_ASSESSMENT_COMPLETED" in result.workflow_events
    assert "RESOURCE_RECOMMENDATION_GENERATED" in result.workflow_events


def test_unknown_message_holds_resource_recommendation():
    result = process_incident(
        message="Please help us.",
        location_text=None,
        people_affected=None,
        resources=[],
    )

    assert result.emergency_detection["emergency_type"] == "unclassified"
    assert result.resource_recommendation["status"] == "requires_clarification"
    assert result.resource_recommendation["candidates"] == []
    assert result.resource_recommendation["requires_human_approval"] is True
    assert "RESOURCE_ALLOCATION_HELD" in result.workflow_events
    assert "RESOURCE_RECOMMENDATION_GENERATED" not in result.workflow_events
    assert result.route_assessment["safety_status"] == "unknown"
    assert result.route_assessment["requires_human_review"] is True
