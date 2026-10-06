from datetime import datetime, timezone
from uuid import UUID, uuid4

from infrastructure.persistence.base import Base
from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, text, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
class ReadingRow(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    device_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    value: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False)  # "simulation" | "mqtt" | "vendor"
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    device: Mapped["DeviceRow"] = relationship("DeviceRow")

    __table_args__ = (
        Index("ix_sensor_readings_device_recorded_at", "device_id", text("recorded_at DESC")),
    )

class LocationRow(Base):
    __tablename__ = "locations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    zones: Mapped[list["ZoneRow"]] = relationship(
        "ZoneRow", back_populates="location", cascade="all, delete-orphan"
    )


class ZoneRow(Base):
    __tablename__ = "zones"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    location_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("locations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    moisture_threshold_low: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    moisture_threshold_high: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    schedule: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    location: Mapped["LocationRow"] = relationship("LocationRow", back_populates="zones")

    __table_args__ = (
        Index("ix_zones_location_id", "location_id"),
    )


# Update existing DeviceRow
class DeviceRow(Base):
    __tablename__ = "devices"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    device_type: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="sensor")
    device_family: Mapped[str] = mapped_column(String(32), nullable=False, default="simulation")
    display_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    default_config: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    zone_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("zones.id", ondelete="SET NULL"), nullable=True
    )
    location_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True
    )

    # Phase 5 Additions
    sampling_interval_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="300"
    )
    tracking_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="true"
    )
    location_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )