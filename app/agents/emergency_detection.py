
from dataclasses import dataclass


@dataclass
class DetectionResult:
    emergency_type: str
    confidence: float
    evidence: list[str]
    missing_fields: list[str]
    requires_review: bool


def detect_emergency(
    message: str,
    location_text: str | None = None,
    people_affected: int | None = None,
) -> DetectionResult:
    """
    Rule-based emergency classification baseline.
    This is not a trained AI model.
    """
    text = message.casefold()
    evidence: list[str] = []

    categories = {
        "flood_rescue": [
            "flood", "floodwater", "water entering",
            "rising water", "drowning", "river overflow",
        ],
        "trapped_people": [
            "trapped", "stranded", "stuck on roof",
            "cannot escape", "cannot get out",
        ],
        "medical_emergency": [
            "injured", "unconscious", "bleeding",
            "medical emergency", "cannot breathe",
        ],
        "evacuation": [
            "evacuate", "evacuation", "need shelter",
            "leave our home", "relocation",
        ],
        "missing_person": [
            "missing person", "cannot find", "lost child",
            "missing family member",
        ],
    }

    matches = []

    for category, keywords in categories.items():
        found = [word for word in keywords if word in text]
        if found:
            matches.append(category)
            evidence.extend(found)

    # Do not silently choose between conflicting categories.
    if len(matches) == 1:
        emergency_type = matches[0]
        confidence = 0.80
    elif len(matches) > 1:
        emergency_type = "multiple_or_ambiguous"
        confidence = 0.50
    else:
        emergency_type = "unclassified"
        confidence = 0.20

    missing_fields = []

    if not location_text or not location_text.strip():
        missing_fields.append("location")

    if people_affected is None:
        missing_fields.append("people_affected")

    requires_review = (
        emergency_type in {"unclassified", "multiple_or_ambiguous"}
        or bool(missing_fields)
    )

    return DetectionResult(
        emergency_type=emergency_type,
        confidence=confidence,
        evidence=evidence,
        missing_fields=missing_fields,
        requires_review=requires_review,
    )
    