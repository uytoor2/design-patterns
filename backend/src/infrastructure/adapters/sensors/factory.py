from domain.devices.entity import Device
from domain.sensors.ports import SensorPort
from infrastructure.adapters.sensors.simulation import SimulationSensorAdapter
from infrastructure.adapters.sensors.vendor_stub import VendorStubSensorAdapter


def get_sensor_adapter(device: Device) -> SensorPort:
    protocol = device.default_config.get("protocol", "simulation")
    if protocol == "vendor_stub":
        return VendorStubSensorAdapter()
    return SimulationSensorAdapter()