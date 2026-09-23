from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Literal

from application.devices.dto import DeviceDto
from application.devices.mappers import device_to_dto
from application.devices.family_service import DeviceFamilyService
from infrastructure.persistence.device_repository import DeviceRepository
from infrastructure.db import get_db

router = APIRouter(prefix="/api/devices", tags=["devices"])


def get_device_service(db: Session = Depends(get_db)) -> DeviceFamilyService:
    repo = DeviceRepository(db)
    return DeviceFamilyService(repo)


@router.post(
    "/provision",
    status_code=status.HTTP_201_CREATED,
    response_model=list[DeviceDto],
)
def provision_family(
    family: Literal["simulation", "edge"] = Query(..., description="Device family to provision"),
    service: DeviceFamilyService = Depends(get_device_service),
):
    try:
        devices = service.provision_family(family)
        return [device_to_dto(d) for d in devices]
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("", response_model=list[DeviceDto])
def list_devices(
    family: str | None = Query(None, alias="family"),
    role: str | None = Query(None, alias="role"),
    service: DeviceFamilyService = Depends(get_device_service),
):
    devices = service.list_devices(family=family, role=role)
    return [device_to_dto(d) for d in devices]