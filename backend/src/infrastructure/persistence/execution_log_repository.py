from uuid import UUID
from sqlalchemy.orm import Session
from infrastructure.persistence.models import ActuatorExecutionLogRow


class ExecutionLogRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create_log(
        self,
        device_id: UUID,
        success: bool,
        policy_applied: list[str],
        message: str | None = None,
    ) -> ActuatorExecutionLogRow:
        log_row = ActuatorExecutionLogRow(
            device_id=device_id,
            success=success,
            policy_applied=policy_applied,
            message=message,
        )
        self._db.add(log_row)
        self._db.commit()
        self._db.refresh(log_row)
        return log_row

    def list_executions(self, limit: int = 20) -> list[ActuatorExecutionLogRow]:
        return (
            self._db.query(ActuatorExecutionLogRow)
            .order_by(ActuatorExecutionLogRow.created_at.desc())
            .limit(limit)
            .all()
        )