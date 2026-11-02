
from app.agents.rescue_priority import calculate_priority


def test_rising_water_and_trapped_people_increase_priority():
    result = calculate_priority(
        message="Rising water. We are trapped on the roof.",
        emergency_type="trapped_people",
        people_affected=3,
        location_text="Patna, Bihar",
    )

    assert result.score == 70
    assert result.level == "critical"
    assert result.requires_review is False


def test_missing_location_requires_review():
    result = calculate_priority(
        message="Flood water is entering our house.",
        emergency_type="flood_rescue",
        people_affected=2,
        location_text=None,
    )

    assert result.score == 45
    
    assert "location" in result.missing_fields  
    assert result.requires_review is True


def test_unknown_emergency_requires_review():
    result = calculate_priority(
        message="Please help us.",
        emergency_type="unclassified",
        people_affected=None,
        location_text=None,
    )

    assert result.level == "low"
    assert result.requires_review is True
    assert result.score == 20
