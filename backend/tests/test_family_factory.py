import pytest
from domain.devices.family_factory import (
    EdgeHardwareFactory,
    SimulationDeviceFactory,
    get_family_factory,
)


def test_simulation_factory_returns_four_devices():
    factory = SimulationDeviceFactory()
    devices = factory.create_device_set()
    
    assert len(devices) == 4
    roles = [d.role for d in devices]
    assert roles.count("sensor") == 2
    assert roles.count("actuator") == 2
    assert all(d.device_family == "simulation" for d in devices)


def test_edge_factory_differs_from_simulation():
    sim_factory = SimulationDeviceFactory()
    edge_factory = EdgeHardwareFactory()
    
    sim_devices = sim_factory.create_device_set()
    edge_devices = edge_factory.create_device_set()
    
    assert len(sim_devices) == 4
    assert len(edge_devices) == 4
    assert sim_devices[0].default_config["protocol"] != edge_devices[0].default_config["protocol"]


def test_get_family_factory_invalid_family():
    with pytest.raises(ValueError, match="Unknown device family"):
        get_family_factory("quantum")