from datetime import datetime, timezone
from sqlalchemy.orm import Session
from domain.devices.entity import Device
from infrastructure.adapters.sensors.simulation import SimulationSensorAdapter
from infrastructure.persistence.models import DeviceRow, ReadingRow
from infrastructure.persistence.reading_repository import ReadingRepository
from domain.sensors.reading import Reading

class SimulationSampler:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = ReadingRepository(db)
        self._sim_adapter = SimulationSensorAdapter()

    def run_once(self, now: datetime | None = None) -> int:
        if now is None:
            now = datetime.now(timezone.utc)

        # Query devices configured for simulation and with tracking_enabled = True
        devices = (
            self._db.query(DeviceRow)
            .filter(
                DeviceRow.role == "sensor",
                DeviceRow.tracking_enabled.is_(True),
            )
            .all()
        )

        sampled_count = 0
        for dev in devices:
            # Skip MQTT/external protocol devices in periodic sampler
            if dev.default_config.get("protocol") == "mqtt":
                continue

            # Check latest recorded reading
            last_reading = (
                self._db.query(ReadingRow)
                .filter(ReadingRow.device_id == dev.id)
                .order_by(ReadingRow.recorded_at.desc())
                .first()
            )

            should_sample = False
            if last_reading is None:
                should_sample = True
            else:
                elapsed_seconds = (now - last_reading.recorded_at).total_seconds()
                if elapsed_seconds >= dev.sampling_interval_seconds:
                    should_sample = True

            if should_sample:
                domain_device = Device(
                    id=dev.id,
                    device_type=dev.device_type,
                    role=dev.role,
                    device_family=dev.device_family,
                    display_name=dev.display_name or "",
                    default_config=dev.default_config,
                )
                reading = self._sim_adapter.read(domain_device)
                # Override timestamp to current evaluation time
                reading = Reading(
                    device_id=reading.device_id,
                    value=reading.value,
                    unit=reading.unit,
                    source=reading.source,
                    recorded_at=now,
                )
                self._repo.insert(reading)
                sampled_count += 1

        return sampled_count