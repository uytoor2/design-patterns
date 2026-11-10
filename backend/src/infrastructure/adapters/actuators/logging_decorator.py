from uuid import UUID
from domain.actuators.ports import ActuatorPort
from infrastructure.adapters.actuators.max_runtime_decorator import MaxRunTimeExceededError
from infrastructure.persistence.execution_log_repository import ExecutionLogRepository


class LoggingActuatorDecorator(ActuatorPort):
    def __init__(self, inner: ActuatorPort, repo: ExecutionLogRepository) -> None:
        self._inner = inner
        self._repo = repo

    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        policy_applied: list[str] = []
        try:
            # Delegate to inner stack
            self._inner.apply(device_id, command, payload)
            policy_applied.append("logging")
            self._repo.create_log(
                device_id=device_id,
                success=True,
                policy_applied=policy_applied,
                message=None,
            )
        except MaxRunTimeExceededError as err:
            policy_applied.extend(["maxRunTime", "logging"])
            self._repo.create_log(
                device_id=device_id,
                success=False,
                policy_applied=policy_applied,
                message=str(err),
            )
            raise err
        except Exception as err:
            policy_applied.append("logging")
            self._repo.create_log(
                device_id=device_id,
                success=False,
                policy_applied=policy_applied,
                message=str(err),
            )
            raise err