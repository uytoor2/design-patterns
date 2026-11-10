from uuid import UUID
from sqlalchemy.orm import Session

from domain.actuators.ports import ActuatorPort
from infrastructure.adapters.actuators.simulation import SimulationActuatorAdapter
from infrastructure.adapters.actuators.max_runtime_decorator import MaxRunTimeActuatorDecorator
from infrastructure.adapters.actuators.logging_decorator import LoggingActuatorDecorator
from infrastructure.persistence.execution_log_repository import ExecutionLogRepository
from application.actuators.dto import ActuatorExecutionLogDto


class ActuatorExecutionService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = ExecutionLogRepository(db)

    def _build_decorated_port(self) -> ActuatorPort:
        # 1. Innermost: Core simulation adapter
        core_adapter = SimulationActuatorAdapter()
        # 2. Middle: Max run-time policy guard
        max_runtime_decorator = MaxRunTimeActuatorDecorator(inner=core_adapter, db=self._db, max_minutes=30)
        # 3. Outermost: Logging decorator
        logging_decorator = LoggingActuatorDecorator(inner=max_runtime_decorator, repo=self._repo)
        return logging_decorator

    def apply_command(self, device_id: UUID, command: str, payload: dict) -> None:
        port = self._build_decorated_port()
        port.apply(device_id, command, payload)

    def get_recent_executions(self, limit: int = 20) -> list[ActuatorExecutionLogDto]:
        rows = self._repo.list_executions(limit=limit)
        return [
            ActuatorExecutionLogDto(
                id=r.id,
                device_id=r.device_id,
                success=r.success,
                policy_applied=r.policy_applied,
                message=r.message,
                created_at=r.created_at,
            )
            for r in rows
        ]