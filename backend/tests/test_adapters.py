from datetime import datetime, timedelta, timezone
from uuid import uuid4
from domain.devices.entity import Device
from infrastructure.adapters.sensors.simulation import SimulationSensorAdapter
from infrastructure.adapters.sensors.vendor_stub import VendorStubSensorAdapter
from infrastructure.adapters.sensors.mqtt import MqttSensorAdapter


def test_simulation_adapter_range():
    dev = Device(
        id=uuid4(),
        device_type="moisture_sensor",
        role="sensor",
        device_family="simulation",
        display_name="Test Moisture",
        default_config={},
    )
    adapter = SimulationSensorAdapter()
    reading = adapter.read(dev)

    assert reading.source == "simulation"
    assert reading.unit == "vwc"
    assert 0.20 <= reading.value <= 0.60


def test_vendor_stub_adapter_translation():
    dev = Device(
        id=uuid4(),
        device_type="moisture_sensor",
        role="sensor",
        device_family="edge",
        display_name="Vendor Sensor",
        default_config={"protocol": "vendor_stub"},
    )
    adapter = VendorStubSensorAdapter()
    reading = adapter.read(dev)

    assert reading.source == "vendor"
    assert reading.value == 0.420
    assert reading.unit == "vwc"


def test_mqtt_adapter_translation():
    dev = Device(
        id=uuid4(),
        device_type="moisture_sensor",
        role="sensor",
        device_family="edge",
        display_name="MQTT Sensor",
        default_config={"protocol": "mqtt"},
    )
    payload = {"value": 0.45, "unit": "vwc"}
    adapter = MqttSensorAdapter()
    reading = adapter.translate(dev, payload)

    assert reading.source == "mqtt"
    assert reading.value == 0.45
    assert reading.unit == "vwc"