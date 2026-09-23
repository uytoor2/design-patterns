from sqlalchemy.orm import Session
from domain.devices.entity import Device
from domain.sensors.entity import Sensor
from infrastructure.persistence.models import DeviceRow
from application.devices.mappers import row_to_device, device_to_row


class DeviceRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    # --- Phase 3 Generalized Device Methods ---
    def save_device(self, device: Device) -> Device:
        row = device_to_row(device)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row_to_device(row)

    def save_devices(self, devices: list[Device]) -> list[Device]:
        rows = [device_to_row(d) for d in devices]
        self._db.add_all(rows)
        self._db.commit()
        for row in rows:
            self._db.refresh(row)
        return [row_to_device(row) for row in rows]

    def list_devices(
        self,
        *,
        device_family: str | None = None,
        role: str | None = None,
    ) -> list[Device]:
        query = self._db.query(DeviceRow)
        if device_family:
            query = query.filter(DeviceRow.device_family == device_family)
        if role:
            query = query.filter(DeviceRow.role == role)
        rows = query.all()
        return [row_to_device(r) for r in rows]

    # --- Sensor-Specific Wrapper Methods (for SensorService compatibility) ---
    def save_sensor(self, sensor: Sensor) -> Sensor:
        row = DeviceRow(
            device_type=sensor.device_type,
            role="sensor",
            display_name=sensor.display_name,
            default_config=sensor.default_config,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)

        return Sensor(
            id=row.id,
            device_type=row.device_type,
            display_name=row.display_name,
            default_config=row.default_config,
        )

    def list_sensors(self) -> list[Sensor]:
        rows = (
            self._db.query(DeviceRow)
            .filter(DeviceRow.role == "sensor")
            .order_by(DeviceRow.created_at.desc())
            .all()
        )

        return [
            Sensor(
                id=row.id,
                device_type=row.device_type,
                display_name=row.display_name,
                default_config=row.default_config,
            )
            for row in rows
        ]