from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure.persistence.db import get_db
from infrastructure.persistence.automation_repository import AutomationRepository
from application.automation.service import AutomationService
from application.automation.dto import SetStrategyRequestDto, EvaluationResponseDto

router = APIRouter(prefix="/api/locations", tags=["automation"])


@router.put("/{location_id}/automation", status_code=status.HTTP_200_OK)
def set_location_strategy(
    location_id: UUID, dto: SetStrategyRequestDto, db: Session = Depends(get_db)
):
    repo = AutomationRepository(db)
    service = AutomationService(repo)
    try:
        service.set_strategy(location_id, dto.strategy_key)
        return {"message": f"Strategy updated to '{dto.strategy_key}'"}
    except ValueError as err:
        if "not found" in str(err).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post("/{location_id}/automation/evaluate", response_model=EvaluationResponseDto)
def evaluate_location_automation(location_id: UUID, db: Session = Depends(get_db)):
    repo = AutomationRepository(db)
    service = AutomationService(repo)
    try:
        return service.evaluate(location_id)
    except ValueError as err:
        if "not found" in str(err).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))