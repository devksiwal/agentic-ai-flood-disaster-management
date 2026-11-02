
from app.agents.emergency_detection import detect_emergency


def test_flood_rescue_is_detected():
    result = detect_emergency(
        message="Flood water is entering our house. Three people need rescue.",
        location_text="Patna, Bihar",
        people_affected=3,
    )

    assert result.emergency_type == "flood_rescue"
    assert result.requires_review is False
    assert "flood" in result.evidence


def test_missing_location_requires_review():
    result = detect_emergency(
        message="We are trapped in flood water.",
        location_text=None,
        people_affected=2,
    )

    assert "location" in result.missing_fields
    assert result.requires_review is True


def test_unknown_message_is_flagged():
    result = detect_emergency(
        message="Please help us.",
        location_text="Patna, Bihar",
        people_affected=2,
    )

    assert result.emergency_type == "unclassified"
    assert result.requires_review is True


def test_ambiguous_message_is_flagged():
    result = detect_emergency(
        message="Flood water is rising and an injured person is bleeding.",
        location_text="Patna, Bihar",
        people_affected=2,
    )

    assert result.emergency_type == "multiple_or_ambiguous"
    assert result.requires_review is True
