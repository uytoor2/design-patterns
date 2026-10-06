from abc import ABC, abstractmethod
from domain.devices.entity import Device
from domain.sensors.reading import Reading


class SensorPort(ABC):
    @abstractmethod
    def read(self, device: Device) -> Reading:
        """Reads or generates a normalized Reading for the given device."""
        pass