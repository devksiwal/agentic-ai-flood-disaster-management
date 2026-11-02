
from app.agents.alert_communication import create_alert


def test_complete_incident_creates_alert_for_approval():
    alert = create_alert(
        incident_type="flood_rescue",
        priority_level="moderate",
        priority_score=45,
        location="Patna, Bihar",
        people_affected=3,
    )

    assert alert.status == "pending_human_approval"
    assert alert.incident_type == "flood_rescue"
    assert alert.priority_score == 45
    assert alert.missing_fields == []
    assert alert.requires_human_approval is True
    assert alert.sent is False
    assert "Patna, Bihar" in alert.message
    assert "People affected: 3" in alert.message


def test_missing_location_requires_clarification():
    alert = create_alert(
        incident_type="flood_rescue",
        priority_level="high",
        priority_score=60,
        location=None,
        people_affected=3,
    )

    assert alert.status == "requires_clarification"
    assert "location" in alert.missing_fields
    assert alert.requires_human_approval is True
    assert alert.sent is False


def test_unclassified_incident_requires_clarification():
    alert = create_alert(
        incident_type="unclassified",
        priority_level="low",
        priority_score=20,
        location=None,
        people_affected=None,
    )

    assert alert.status == "requires_clarification"
    assert "confirmed_incident_type" in alert.missing_fields
    assert "location" in alert.missing_fields
    assert "people_affected" in alert.missing_fields
    assert alert.requires_human_approval is True
    assert alert.sent is False
