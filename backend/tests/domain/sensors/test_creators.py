import pytest

from domain.sensors.creators import (
    LightSensorCreator,
    MoistureSensorCreator,
    get_creator,
)


def test_moisture_creator_defaults() -> None:
    sensor = MoistureSensorCreator().create_sensor()

    assert sensor.id is None
    assert sensor.device_type == "moisture_sensor"
    assert sensor.display_name == "Soil moisture sensor"
    assert sensor.default_config["unit"] == "vwc"
    assert "threshold" in sensor.default_config
    assert sensor.default_config["sampling_interval_seconds"] == 300


def test_light_creator_defaults() -> None:
    sensor = LightSensorCreator().create_sensor()

    assert sensor.id is None
    assert sensor.device_type == "light_sensor"
    assert sensor.display_name == "Greenhouse light sensor"
    assert sensor.default_config["unit"] == "lux"
    assert sensor.default_config["sampling_interval_seconds"] == 60
    assert "threshold" not in sensor.default_config


def test_creators_have_distinct_configurations() -> None:
    moisture_sensor = MoistureSensorCreator().create_sensor()
    light_sensor = LightSensorCreator().create_sensor()

    assert moisture_sensor.default_config != light_sensor.default_config
    assert moisture_sensor.default_config["unit"] != light_sensor.default_config["unit"]


def test_creator_keeps_custom_display_name() -> None:
    sensor = LightSensorCreator().create_sensor(display_name="North roof light")

    assert sensor.display_name == "North roof light"


@pytest.mark.parametrize(
    ("sensor_type", "expected_creator"),
    [
        ("moisture", MoistureSensorCreator),
        ("light", LightSensorCreator),
    ],
)
def test_creator_registry_returns_correct_creator(
    sensor_type: str,
    expected_creator: type[MoistureSensorCreator | LightSensorCreator],
) -> None:
    creator = get_creator(sensor_type)

    assert isinstance(creator, expected_creator)


def test_creator_registry_rejects_unknown_sensor_type() -> None:
    with pytest.raises(ValueError, match="Unsupported sensor type"):
        get_creator("temperature")