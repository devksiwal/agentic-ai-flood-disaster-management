
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_message: Mapped[str] = mapped_column(Text)
    original_language: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
    translated_message: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    emergency_type: Mapped[str] = mapped_column(
        String(100), default="unclassified"
    )
    location_text: Mapped[str | None] = mapped_column(
        String(300), nullable=True
    )
    latitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    longitude: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    people_affected: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    priority_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default="received"
    )
    requires_review: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    events: Mapped[list["SystemEvent"]] = relationship(
        back_populates="incident"
    )



class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    resource_type: Mapped[str] = mapped_column(String(80))
    capabilities: Mapped[str] = mapped_column(
        Text, default="general_rescue"
    )
    capacity: Mapped[int] = mapped_column(Integer, default=1)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="available"
    )



class SystemEvent(Base):
    __tablename__ = "system_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100))
    details: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    incident_id: Mapped[int | None] = mapped_column(
        ForeignKey("incidents.id"), nullable=True
    )

    incident: Mapped[Incident | None] = relationship(
        back_populates="events"
    )
