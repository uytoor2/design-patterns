from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ActuatorExecutionLogDto(BaseModel):
    id: UUID
    device_id: UUID
    success: bool
    policy_applied: list[str]
    message: str | None = None
    created_at: datetime


class ApplyCommandRequestDto(BaseModel):
    command: str
    payload: dict = {}