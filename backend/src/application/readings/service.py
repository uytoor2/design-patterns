from uuid import UUID
from sqlalchemy.orm import Session
from domain.devices.entity import Device
from domain.sensors.reading import Reading
from application.readings.dto import ReadingDto
from infrastructure.adapters.sensors.factory import get_sensor_adapter
from infrastructure.persistence.models import DeviceRow
from infrastructure.persistence.reading_repository import ReadingRepository


class ReadingIngest:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = ReadingRepository(db)

    def take_reading(self, device_id: UUID) -> ReadingDto:
        dev_row = self._db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not dev_row:
            raise ValueError(f"Device {device_id} not found")

        domain_device = Device(
            id=dev_row.id,
            device_type=dev_row.device_type,
            role=dev_row.role,
            device_family=dev_row.device_family,
            display_name=dev_row.display_name or "",
            default_config=dev_row.default_config,
        )

        adapter = get_sensor_adapter(domain_device)
        reading = adapter.read(domain_device)
        row = self._repo.insert(reading)

        return ReadingDto(
            device_id=row.device_id,
            value=float(row.value),
            unit=row.unit,
            source=row.source,
            recorded_at=row.recorded_at,
        )

    def record(self, reading: Reading) -> ReadingDto:
        row = self._repo.insert(reading)
        return ReadingDto(
            device_id=row.device_id,
            value=float(row.value),
            unit=row.unit,
            source=row.source,
            recorded_at=row.recorded_at,
        )