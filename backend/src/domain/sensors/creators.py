from abc import ABC, abstractmethod

from domain.sensors.entity import Sensor


class SensorCreator(ABC):
    @abstractmethod
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        """Create a sensor with the creator's specific defaults."""


class MoistureSensorCreator(SensorCreator):
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        return Sensor(
            id=None,
            device_type="moisture_sensor",
            display_name=display_name or "Soil moisture sensor",
            default_config={
                "unit": "vwc",
                "threshold": 0.30,
                "sampling_interval_seconds": 300,
            },
        )


class LightSensorCreator(SensorCreator):
    def create_sensor(self, display_name: str | None = None) -> Sensor:
        return Sensor(
            id=None,
            device_type="light_sensor",
            display_name=display_name or "Greenhouse light sensor",
            default_config={
                "unit": "lux",
                "sampling_interval_seconds": 60,
            },
        )


def get_creator(sensor_type: str) -> SensorCreator:
    creators: dict[str, SensorCreator] = {
        "moisture": MoistureSensorCreator(),
        "light": LightSensorCreator(),
    }

    try:
        return creators[sensor_type]
    except KeyError as error:
        raise ValueError(f"Unsupported sensor type: {sensor_type}") from error