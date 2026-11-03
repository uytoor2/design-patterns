from pydantic import BaseModel
from uuid import UUID


class DeviceDto(BaseModel):
    id: UUID
    device_type: str
    role: str
    device_family: str
    display_name: str
    default_config: dict

    class Config:
        from_attributes = True

class DeviceDetailDto(BaseModel):
    id: UUID
    device_type: str
    role: str
    device_family: str
    display_name: str | None = None
    state: str | None = None
    allowed_commands: list[str] = []


class TransitionRequestDto(BaseModel):
    target: str