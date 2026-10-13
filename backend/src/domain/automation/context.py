from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ZoneContext:
    zone_id: UUID
    zone_name: str
    threshold_low: float
    threshold_high: float
    latest_moisture: float | None = None


@dataclass(frozen=True)
class LocationAutomationContext:
    location_id: UUID
    zones: tuple[ZoneContext, ...]