
from dataclasses import dataclass, field


@dataclass
class RouteAssessment:
    status: str
    origin: str | None
    destination: str | None
    route_available: bool
    safety_status: str
    missing_data: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    requires_human_review: bool = True


def assess_route(
    origin: str | None,
    destination: str | None,
    road_route_available: bool = False,
    flood_hazard_data_available: bool = False,
    road_closure_data_available: bool = False,
) -> RouteAssessment:
    """
    Assess whether enough information exists to evaluate a rescue route.

    This baseline does not calculate routes or certify road safety.
    Human review is always required.
    """
    missing_data = []
    warnings = []

    if not origin or not origin.strip():
        missing_data.append("origin")

    if not destination or not destination.strip():
        missing_data.append("destination")

    if not road_route_available:
        missing_data.append("road_network_route")

    if not flood_hazard_data_available:
        missing_data.append("current_flood_hazard_data")

    if not road_closure_data_available:
        missing_data.append("current_road_closure_data")

    if missing_data:
        status = "insufficient_data"
        safety_status = "unknown"
        route_available = False
        warnings.append(
            "Route safety cannot be determined from the available data."
        )
    else:
        status = "requires_review"
        safety_status = "not_certified_safe"
        route_available = True
        warnings.append(
            "A route is available for assessment, but its safety "
            "has not been independently verified."
        )

    return RouteAssessment(
        status=status,
        origin=origin,
        destination=destination,
        route_available=route_available,
        safety_status=safety_status,
        missing_data=missing_data,
        warnings=warnings,
        requires_human_review=True,
    )
