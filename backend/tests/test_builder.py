import pytest
from domain.locations.config_builder import LocationConfigBuilder
from domain.locations.errors import ConfigurationError


def test_build_success():
    builder = LocationConfigBuilder()
    config = (
        builder.with_location_name("Greenhouse Alpha")
        .add_zone("Zone 1", moisture_threshold_low=0.2, moisture_threshold_high=0.6)
        .build()
    )
    assert config.location.name == "Greenhouse Alpha"
    assert len(config.location.zones) == 1
    assert config.location.zones[0].name == "Zone 1"


def test_build_requires_name():
    builder = LocationConfigBuilder()
    builder.add_zone("Zone 1", 0.2, 0.6)
    with pytest.raises(ConfigurationError, match="Location name is required"):
        builder.build()


def test_build_requires_zones():
    builder = LocationConfigBuilder()
    builder.with_location_name("Empty Site")
    with pytest.raises(ConfigurationError, match="At least one zone is required"):
        builder.build()


def test_build_rejects_invalid_thresholds():
    builder = LocationConfigBuilder()
    builder.with_location_name("Site B")
    builder.add_zone("Zone Invalid", moisture_threshold_low=0.7, moisture_threshold_high=0.3)
    with pytest.raises(ConfigurationError, match="Low threshold .* must be strictly less than high threshold"):
        builder.build()