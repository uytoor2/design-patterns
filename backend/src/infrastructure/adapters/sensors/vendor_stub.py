from datetime import datetime, timezone
from domain.devices.entity import Device
from domain.sensors.ports import SensorPort
from domain.sensors.reading import Reading


class VendorStubSensorAdapter(SensorPort):
    def read(self, device: Device) -> Reading:
        vendor_raw_data = {"sensor_val_raw": 420, "scale_factor": 0.001, "u": "VWC"}
        normalized_value = round(vendor_raw_data["sensor_val_raw"] * vendor_raw_data["scale_factor"], 4)

        return Reading(
            device_id=device.id,
            value=normalized_value,
            unit=vendor_raw_data["u"].lower(),
            source="vendor",
            recorded_at=datetime.now(timezone.utc),
        )