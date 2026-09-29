from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.persistence.db import get_db
from infrastructure.persistence.location_repository import LocationRepository
from application.locations.config_service import LocationConfigService
from application.locations.zone_assignment_service import ZoneAssignmentService
from application.locations.dto import (
    BuildLocationConfigRequestDto,
    LocationConfigDto,
    LocationResponseDto,
    AssignZoneRequestDto,
)
from domain.locations.errors import ConfigurationError

router = APIRouter(prefix="/api/locations", tags=["locations"])


@router.post("/config", response_model=LocationConfigDto, status_code=status.HTTP_201_CREATED)
def create_location_config(
    dto: BuildLocationConfigRequestDto, db: Session = Depends(get_db)
):
    repo = LocationRepository(db)
    service = LocationConfigService(repo)
    try:
        return service.build_and_save(dto)
    except ConfigurationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get("", response_model=list[LocationResponseDto])
def list_locations(db: Session = Depends(get_db)):
    repo = LocationRepository(db)
    rows = repo.list_locations()
    return [LocationResponseDto(id=r.id, name=r.name) for r in rows]


@router.get("/{location_id}/config", response_model=LocationConfigDto)
def get_location_config(location_id: UUID, db: Session = Depends(get_db)):
    repo = LocationRepository(db)
    service = LocationConfigService(repo)
    config = service.get_config(location_id)
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return config


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: UUID, db: Session = Depends(get_db)):
    repo = LocationRepository(db)
    if not repo.delete_location(location_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")


# Device Zone Assignment Endpoint
device_router = APIRouter(prefix="/api/devices", tags=["devices"])

@device_router.patch("/{device_id}/zone", status_code=status.HTTP_200_OK)
def assign_device_zone(
    device_id: UUID, dto: AssignZoneRequestDto, db: Session = Depends(get_db)
):
    service = ZoneAssignmentService(db)
    success = service.assign_device(device_id, dto.zone_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device or Zone not found")
    return {"message": "Assignment updated successfully"}