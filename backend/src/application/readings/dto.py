from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ReadingDto(BaseModel):
    device_id: UUID
    value: float
    unit: str
    source: str
    recorded_at: datetime


class UpdateSamplingRequestDto(BaseModel):
    sampling_interval_seconds: int = Field(..., ge=5)
    tracking_enabled: bool