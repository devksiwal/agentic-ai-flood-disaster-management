
from app.agents.route_planning import assess_route


def test_missing_route_data_is_not_declared_safe():
    result = assess_route(
        origin="Patna, Bihar",
        destination="Rescue Centre A",
    )

    assert result.status == "insufficient_data"
    assert result.route_available is False
    assert result.safety_status == "unknown"
    assert "road_network_route" in result.missing_data
    assert "current_flood_hazard_data" in result.missing_data
    assert "current_road_closure_data" in result.missing_data
    assert result.requires_human_review is True


def test_missing_origin_and_destination_are_reported():
    result = assess_route(
        origin=None,
        destination=None,
    )

    assert "origin" in result.missing_data
    assert "destination" in result.missing_data
    assert result.status == "insufficient_data"
    assert result.requires_human_review is True


def test_available_data_does_not_certify_route_as_safe():
    result = assess_route(
        origin="Patna, Bihar",
        destination="Rescue Centre A",
        road_route_available=True,
        flood_hazard_data_available=True,
        road_closure_data_available=True,
    )

    assert result.status == "requires_review"
    assert result.route_available is True
    assert result.safety_status == "not_certified_safe"
    assert result.requires_human_review is True
