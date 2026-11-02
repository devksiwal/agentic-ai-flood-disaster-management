
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IncidentCreate(BaseModel):
    original_message: str = Field(min_length=3, max_length=5000)
    original_language: str | None = Field(default=None, max_length=20)
    translated_message: str | None = Field(default=None, max_length=5000)
    emergency_type: str = Field(default="unclassified", max_length=100)
    location_text: str | None = Field(default=None, max_length=300)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    people_affected: int | None = Field(default=None, ge=1, le=100000)


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_message: str
    original_language: str | None
    translated_message: str | None
    emergency_type: str
    location_text: str | None
    latitude: float | None
    longitude: float | None
    people_affected: int | None
    priority_score: float | None
    status: str
    requires_review: bool
    created_at: datetime
