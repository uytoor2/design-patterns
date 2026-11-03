from uuid import UUID
from sqlalchemy.orm import Session
from infrastructure.persistence.models import ActuatorStateRow, DeviceRow


class ActuatorStateRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_state(self, device_id: UUID) -> str:
        row = (
            self._db.query(ActuatorStateRow)
            .filter(ActuatorStateRow.device_id == device_id)
            .first()
        )
        if not row:
            # Auto-seed if device exists and is an actuator
            device = self._db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
            if not device or device.role != "actuator":
                raise ValueError(f"Device {device_id} is not an actuator.")
            row = ActuatorStateRow(device_id=device_id, state="idle")
            self._db.add(row)
            self._db.commit()
            self._db.refresh(row)
        return row.state

    def save_state(self, device_id: UUID, new_state: str) -> None:
        row = (
            self._db.query(ActuatorStateRow)
            .filter(ActuatorStateRow.device_id == device_id)
            .first()
        )
        if not row:
            row = ActuatorStateRow(device_id=device_id, state=new_state)
            self._db.add(row)
        else:
            row.state = new_state
        self._db.commit()