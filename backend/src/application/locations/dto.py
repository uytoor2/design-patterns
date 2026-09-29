from uuid import UUID
from pydantic import BaseModel, Field


class ZoneCreateDto(BaseModel):
    name: str
    moisture_threshold_low: float = Field(..., ge=0.0, le=1.0)
    moisture_threshold_high: float = Field(..., ge=0.0, le=1.0)
    schedule: dict = Field(default_factory=dict)


class BuildLocationConfigRequestDto(BaseModel):
    location_name: str
    zones: list[ZoneCreateDto]


class ZoneResponseDto(BaseModel):
    id: UUID
    location_id: UUID
    name: str
    moisture_threshold_low: float
    moisture_threshold_high: float
    schedule: dict


class LocationResponseDto(BaseModel):
    id: UUID
    name: str


class LocationConfigDto(BaseModel):
    location: LocationResponseDto
    zones: list[ZoneResponseDto]


class AssignZoneRequestDto(BaseModel):
    zone_id: UUID | None = None