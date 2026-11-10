from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from infrastructure.db import get_db
from application.actuators.service import ActuatorExecutionService
from application.actuators.dto import ActuatorExecutionLogDto, ApplyCommandRequestDto
from infrastructure.adapters.actuators.max_runtime_decorator import MaxRunTimeExceededError

router = APIRouter(prefix="/api/actuators", tags=["actuators"])


@router.get("/executions", response_model=list[ActuatorExecutionLogDto], status_code=status.HTTP_200_OK)
def list_actuator_executions(
    limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)
):
    service = ActuatorExecutionService(db)
    return service.get_recent_executions(limit=limit)


@router.post("/{device_id}/apply", status_code=status.HTTP_200_OK)
def apply_actuator_command(
    device_id: UUID, dto: ApplyCommandRequestDto, db: Session = Depends(get_db)
):
    service = ActuatorExecutionService(db)
    try:
        service.apply_command(device_id, dto.command, dto.payload)
        return {"message": f"Command '{dto.command}' executed successfully."}
    except MaxRunTimeExceededError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))