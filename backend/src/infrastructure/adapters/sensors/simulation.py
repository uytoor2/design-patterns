import random
from datetime import datetime, timezone
from domain.devices.entity import Device
from domain.sensors.ports import SensorPort
from domain.sensors.reading import Reading


class SimulationSensorAdapter(SensorPort):
    def read(self, device: Device) -> Reading:
        now = datetime.now(timezone.utc)
        if "moisture" in device.device_type.lower():
            value = round(random.uniform(0.20, 0.60), 4)
            unit = "vwc"
        elif "light" in device.device_type.lower():
            value = round(random.uniform(200.0, 2000.0), 2)
            unit = "lux"
        else:
            value = round(random.uniform(0.0, 100.0), 2)
            unit = "pct"

        return Reading(
            device_id=device.id,
            value=value,
            unit=unit,
            source="simulation",
            recorded_at=now,
        )