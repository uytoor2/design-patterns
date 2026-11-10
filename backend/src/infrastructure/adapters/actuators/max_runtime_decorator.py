from datetime import datetime, timezone, timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from domain.actuators.ports import ActuatorPort
from infrastructure.persistence.models import ActuatorStateRow


class MaxRunTimeExceededError(ValueError):
    """Raised when an actuator has been running longer than the allowed duration."""
    pass


class MaxRunTimeActuatorDecorator(ActuatorPort):
    def __init__(self, inner: ActuatorPort, db: Session, max_minutes: int = 30) -> None:
        self._inner = inner
        self._db = db
        self._max_minutes = max_minutes

    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        state_row = (
            self._db.query(ActuatorStateRow)
            .filter(ActuatorStateRow.device_id == device_id)
            .first()
        )

        if state_row and state_row.state == "running":
            now = datetime.now(timezone.utc)
            updated_at = state_row.updated_at
            if updated_at.tzinfo is None:
                updated_at = updated_at.replace(tzinfo=timezone.utc)

            elapsed = now - updated_at
            if elapsed >= timedelta(minutes=self._max_minutes):
                raise MaxRunTimeExceededError("Max run time exceeded")

        # Pass call to inner adapter if policy check passes
        self._inner.apply(device_id, command, payload)