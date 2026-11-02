
from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    resource_type: str = Field(min_length=1, max_length=80)
    capabilities: str = Field(
        default="general_rescue", max_length=500
    )
    capacity: int = Field(default=1, ge=1, le=100000)
    available: bool = True
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    status: str = Field(default="available", max_length=50)


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    resource_type: str
    capabilities: str
    capacity: int
    available: bool
    latitude: float | None
    longitude: float | None
    status: str
