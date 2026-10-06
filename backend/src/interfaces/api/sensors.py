from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.readings.dto import ReadingDto, UpdateSamplingRequestDto
from application.readings.service import ReadingIngest
from application.sensors.service import SensorService
from infrastructure.db import get_db
from infrastructure.persistence.device_repository import DeviceRepository
from infrastructure.persistence.models import DeviceRow
from infrastructure.persistence.reading_repository import ReadingRepository

router = APIRouter(prefix="/api", tags=["sensors"])


# ==========================================
# Phase 2/3 Existing Routes (Keep intact!)
# ==========================================

class CreateSensorRequest(BaseModel):
    type: str
    display_name: str | None = None


class SensorResponse(BaseModel):
    id: UUID
    device_type: str
    display_name: str | None
    default_config: dict[str, Any]


def get_sensor_service(
    db: Session = Depends(get_db),
) -> SensorService:
    return SensorService(DeviceRepository(db))


@router.get("/sensors", response_model=list[SensorResponse])
def list_sensors(
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorResponse]:
    sensors = service.list_sensors()
    return [
        SensorResponse(
            id=sensor.id,
            device_type=sensor.device_type,
            display_name=sensor.display_name,
            default_config=sensor.default_config,
        )
        for sensor in sensors
    ]


@router.post(
    "/sensors",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sensor(
    payload: CreateSensorRequest,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    try:
        sensor = service.create_sensor(
            sensor_type=payload.type,
            display_name=payload.display_name,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    return SensorResponse(
        id=sensor.id,
        device_type=sensor.device_type,
        display_name=sensor.display_name,
        default_config=sensor.default_config,
    )


# ==========================================
# Phase 5 New Routes (Telemetry & Sampling)
# ==========================================

@router.post(
    "/sensors/{device_id}/read",
    response_model=ReadingDto,
    status_code=status.HTTP_201_CREATED,
)
def trigger_sensor_read(device_id: UUID, db: Session = Depends(get_db)):
    ingest = ReadingIngest(db)
    try:
        return ingest.take_reading(device_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.get("/sensors/{device_id}/readings", response_model=list[ReadingDto])
def list_sensor_readings(
    device_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    repo = ReadingRepository(db)
    rows = repo.list_for_device(device_id, limit=limit)
    return [
        ReadingDto(
            device_id=r.device_id,
            value=float(r.value),
            unit=r.unit,
            source=r.source,
            recorded_at=r.recorded_at,
        )
        for r in rows
    ]


@router.patch("/devices/{device_id}/sampling", status_code=status.HTTP_200_OK)
def update_device_sampling(
    device_id: UUID,
    dto: UpdateSamplingRequestDto,
    db: Session = Depends(get_db),
):
    if dto.sampling_interval_seconds < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="sampling_interval_seconds must be at least 5 seconds",
        )

    dev = db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    dev.sampling_interval_seconds = dto.sampling_interval_seconds
    dev.tracking_enabled = dto.tracking_enabled
    db.commit()

    return {"message": "Sampling parameters updated successfully"}