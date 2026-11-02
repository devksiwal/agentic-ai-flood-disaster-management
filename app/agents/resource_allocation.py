
from dataclasses import dataclass


@dataclass
class AllocationResult:
    status: str
    candidates: list[dict]
    rejection_reasons: list[dict]
    requires_human_approval: bool = True


def recommend_resources(
    emergency_type: str,
    people_affected: int | None,
    resources: list[dict],
) -> AllocationResult:
    """
    Filter resources using availability, status, capability,
    and capacity. This creates recommendations, not dispatches.
    """
    required_capability = {
        "flood_rescue": "water_rescue",
        "trapped_people": "water_rescue",
        "medical_emergency": "medical",
        "evacuation": "evacuation",
        "missing_person": "search_rescue",
    }.get(emergency_type, "general_rescue")

    required_capacity = max(people_affected or 1, 1)
    candidates = []
    rejection_reasons = []

    for resource in resources:
        resource_id = resource.get("id")
        capabilities = {
            item.strip().casefold()
            for item in resource.get("capabilities", "").split(",")
            if item.strip()
        }

        if (
            not resource.get("available", False)
            or resource.get("status") != "available"
        ):
            rejection_reasons.append({
                "resource_id": resource_id,
                "reason": "Resource is unavailable.",
            })
            continue

        if required_capability not in capabilities:
            rejection_reasons.append({
                "resource_id": resource_id,
                "reason": f"Missing capability: {required_capability}.",
            })
            continue

        if resource.get("capacity", 0) < required_capacity:
            rejection_reasons.append({
                "resource_id": resource_id,
                "reason": "Insufficient capacity.",
            })
            continue

        candidates.append({
            "resource_id": resource_id,
            "name": resource.get("name"),
            "resource_type": resource.get("resource_type"),
            "capacity": resource.get("capacity"),
            "matched_capability": required_capability,
        })

    return AllocationResult(
        status="candidates_found" if candidates else "no_feasible_resource",
        candidates=candidates,
        rejection_reasons=rejection_reasons,
    )
