from abc import ABC, abstractmethod
from domain.devices.entity import Device


class DeviceFamilyFactory(ABC):
    @property
    @abstractmethod
    def family_key(self) -> str:
        """Returns the identifier simulation or edge etc."""
        pass

    @abstractmethod
    def create_device_set(self) -> list[Device]:
        """Creates and returns device."""
        pass


class SimulationDeviceFactory(DeviceFamilyFactory):
    @property
    def family_key(self) -> str:
        return "simulation"

    def create_device_set(self) -> list[Device]:
        return [
            Device(
                id=None,
                device_type="moisture_sensor",
                role="sensor",
                device_family="simulation",
                display_name="Simulated Moisture Sensor",
                default_config={
                    "sampling_interval_seconds": 300,
                    "unit": "vwc",
                    "protocol": "sim",
                },
            ),
            Device(
                id=None,
                device_type="light_sensor",
                role="sensor",
                device_family="simulation",
                display_name="Simulated Light Sensor",
                default_config={
                    "sampling_interval_seconds": 300,
                    "unit": "lux",
                    "protocol": "sim",
                },
            ),
            Device(
                id=None,
                device_type="water_pump",
                role="actuator",
                device_family="simulation",
                display_name="Simulated Water Pump",
                default_config={
                    "protocol": "sim",
                    "flow_rate_lpm": 1.5,
                },
            ),
            Device(
                id=None,
                device_type="grow_light",
                role="actuator",
                device_family="simulation",
                display_name="Simulated Grow Light",
                default_config={
                    "protocol": "sim",
                    "power_watts": 100,
                },
            ),
        ]


class EdgeHardwareFactory(DeviceFamilyFactory):
    @property
    def family_key(self) -> str:
        return "edge"

    def create_device_set(self) -> list[Device]:
        return [
            Device(
                id=None,
                device_type="moisture_sensor",
                role="sensor",
                device_family="edge",
                display_name="Edge GPIO Moisture Sensor",
                default_config={
                    "sampling_interval_seconds": 60,
                    "unit": "vwc",
                    "protocol": "gpio-stub",
                    "pin": 17,
                },
            ),
            Device(
                id=None,
                device_type="light_sensor",
                role="sensor",
                device_family="edge",
                display_name="Edge I2C Light Sensor",
                default_config={
                    "sampling_interval_seconds": 60,
                    "unit": "lux",
                    "protocol": "i2c-stub",
                    "address": "0x23",
                },
            ),
            Device(
                id=None,
                device_type="water_pump",
                role="actuator",
                device_family="edge",
                display_name="Edge Relay Water Pump",
                default_config={
                    "protocol": "gpio-relay",
                    "pin": 22,
                },
            ),
            Device(
                id=None,
                device_type="grow_light",
                role="actuator",
                device_family="edge",
                display_name="Edge Relay Grow Light",
                default_config={
                    "protocol": "gpio-relay",
                    "pin": 23,
                },
            ),
        ]


def get_family_factory(family: str) -> DeviceFamilyFactory:
    factories: dict[str, DeviceFamilyFactory] = {
        "simulation": SimulationDeviceFactory(),
        "edge": EdgeHardwareFactory(),
    }
    if family not in factories:
        raise ValueError(f"Unknown device family: '{family}'. Supported families: {list(factories.keys())}")
    return factories[family]