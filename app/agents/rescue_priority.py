
from dataclasses import dataclass


@dataclass
class PriorityResult:
    score: int
    level: str
    factors: list[dict[str, object]]
    missing_fields: list[str]
    requires_review: bool


def calculate_priority(
    message: str,
    emergency_type: str,
    people_affected: int | None,
    location_text: str | None,
) -> PriorityResult:
    """
    Transparent rule-based priority baseline.
    Not a clinically validated triage model.
    """
    text = message.casefold()
    score = 20
    factors: list[dict[str, object]] = [
        {
            "factor": "baseline",
            "points": 20,
            "reason": "Incident received; urgency requires assessment.",
        }
    ]

    def add_factor(name: str, points: int, reason: str) -> None:
        nonlocal score
        score += points
        factors.append(
            {"factor": name, "points": points, "reason": reason}
        )

    if emergency_type == "medical_emergency" or any(
        term in text
        for term in (
            "unconscious",
            "cannot breathe",
            "severe bleeding",
            "critical injury",
        )
    ):
        add_factor(
            "medical_danger",
            25,
            "Medical danger indicator reported.",
        )

    if emergency_type == "trapped_people" or any(
        term in text
        for term in (
            "trapped",
            "stranded",
            "stuck on roof",
            "cannot escape",
        )
    ):
        add_factor(
            "trapped_people",
            25,
            "People reported trapped or unable to escape.",
        )

    if any(
        term in text
        for term in (
    "rising water",
    "water entering",
    "water is entering",
    "water is rising",
    "flood water is entering",
    "drowning",
    "river overflow",
)
    ):
        add_factor(
            "immediate_flood_threat",
            20,
            "Immediate flood-threat indicator reported.",
        )

    if people_affected is not None:
        if people_affected >= 10:
            add_factor(
                "people_affected",
                15,
                "Ten or more people reported affected.",
            )
        elif people_affected >= 4:
            add_factor(
                "people_affected",
                10,
                "Four to nine people reported affected.",
            )
        elif people_affected >= 1:
            add_factor(
                "people_affected",
                5,
                "One to three people reported affected.",
            )

    missing_fields = []

    if not location_text or not location_text.strip():
        missing_fields.append("location")

    if people_affected is None:
        missing_fields.append("people_affected")

    score = min(score, 100)

    if score >= 70:
        level = "critical"
    elif score >= 50:
        level = "high"
    elif score >= 30:
        level = "moderate"
    else:
        level = "low"

    requires_review = (
        bool(missing_fields)
        or emergency_type in {
            "unclassified",
            "multiple_or_ambiguous",
        }
    )

    return PriorityResult(
        score=score,
        level=level,
        factors=factors,
        missing_fields=missing_fields,
        requires_review=requires_review,
    )
