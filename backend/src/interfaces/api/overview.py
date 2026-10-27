from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.persistence.db import get_db
from application.overview.facade import LocationOverviewFacade
from application.overview.dto import LocationOverviewDto

router = APIRouter(prefix="/api/locations", tags=["overview"])


@router.get("/{location_id}/overview", response_model=LocationOverviewDto, status_code=status.HTTP_200_OK)
def get_location_overview(location_id: UUID, db: Session = Depends(get_db)):
    facade = LocationOverviewFacade(db)
    try:
        return facade.get_overview(location_id)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))