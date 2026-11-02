
from app.agents.resource_allocation import recommend_resources


def test_matching_available_resource_is_recommended():
    resources = [
        {
            "id": 1,
            "name": "Rescue Boat A",
            "resource_type": "boat",
            "capabilities": "water_rescue, evacuation",
            "capacity": 5,
            "available": True,
            "status": "available",
        }
    ]

    result = recommend_resources("flood_rescue", 3, resources)

    assert result.status == "candidates_found"
    assert result.candidates[0]["resource_id"] == 1
    assert result.requires_human_approval is True


def test_unavailable_resource_is_rejected():
    resources = [
        {
            "id": 2,
            "name": "Boat B",
            "resource_type": "boat",
            "capabilities": "water_rescue",
            "capacity": 10,
            "available": False,
            "status": "unavailable",
        }
    ]

    result = recommend_resources("flood_rescue", 2, resources)

    assert result.status == "no_feasible_resource"
    assert len(result.candidates) == 0


def test_insufficient_capacity_is_rejected():
    resources = [
        {
            "id": 3,
            "name": "Medical Unit",
            "resource_type": "medical",
            "capabilities": "medical",
            "capacity": 2,
            "available": True,
            "status": "available",
        }
    ]

    result = recommend_resources("medical_emergency", 5, resources)

    assert result.status == "no_feasible_resource"
    assert result.rejection_reasons[0]["reason"] == "Insufficient capacity."
