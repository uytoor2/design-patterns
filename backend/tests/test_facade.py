import pytest
from uuid import uuid4
from sqlalchemy.orm import Session

from infrastructure.persistence.models import LocationRow, ZoneRow, DeviceRow, ReadingRow, AutomationRuleRow
from application.overview.facade import LocationOverviewFacade


def test_overview_returns_strategy_and_readings(db_session: Session):
    # 1. Seed Location and 2 Zones
    loc = LocationRow(name="Lab Site A")
    db_session.add(loc)
    db_session.flush()

    zone1 = ZoneRow(
        location_id=loc.id,
        name="Bench 1",
        moisture_threshold_low=0.2,
        moisture_threshold_high=0.45,
    )
    zone2 = ZoneRow(
        location_id=loc.id,
        name="Bench 2 (Empty)",
        moisture_threshold_low=0.3,
        moisture_threshold_high=0.6,
    )
    db_session.add_all([zone1, zone2])
    db_session.flush()

    # 2. Seed Assigned Sensor in Zone 1
    sensor = DeviceRow(
        device_type="moisture_sensor",
        role="sensor",
        display_name="Bench Moisture",
        location_id=loc.id,
        zone_id=zone1.id,
        sampling_interval_seconds=300,
        tracking_enabled=True,
    )
    # Seed Unassigned Device (Must be excluded from overview counts)
    unassigned_dev = DeviceRow(
        device_type="light_sensor",
        role="sensor",
        display_name="Unassigned Light",
        location_id=None,
        zone_id=None,
    )
    db_session.add_all([sensor, unassigned_dev])
    db_session.flush()

    # 3. Seed Reading for Assigned Sensor
    reading = ReadingRow(
        device_id=sensor.id,
        value=0.31,
        unit="vwc",
        source="simulation",
    )
    db_session.add(reading)
    db_session.commit()

    facade = LocationOverviewFacade(db_session)

    # 4. Test state BEFORE strategy is saved
    overview_before = facade.get_overview(loc.id)
    assert overview_before.location.name == "Lab Site A"
    assert overview_before.device_counts.sensor == 1
    assert overview_before.device_counts.actuator == 0
    assert len(overview_before.zones) == 2
    assert overview_before.strategy_key is None
    assert overview_before.last_recommendation is None

    # Check reading properties copied from device
    z1_dto = next(z for z in overview_before.zones if z.id == zone1.id)
    assert len(z1_dto.latest_readings) == 1
    assert z1_dto.latest_readings[0].value == 0.31
    assert z1_dto.latest_readings[0].tracking_enabled is True
    assert z1_dto.latest_readings[0].sampling_interval_seconds == 300

    # Check empty zone
    z2_dto = next(z for z in overview_before.zones if z.id == zone2.id)
    assert len(z2_dto.devices) == 0
    assert len(z2_dto.latest_readings) == 0

    # 5. Save strategy and verify recommendation evaluation
    rule = AutomationRuleRow(location_id=loc.id, strategy_key="conservative")
    db_session.add(rule)
    db_session.commit()

    overview_after = facade.get_overview(loc.id)
    assert overview_after.strategy_key == "conservative"
    assert overview_after.last_recommendation is not None
    assert overview_after.last_recommendation.action in ["irrigate", "wait"]


def test_overview_missing_location_raises_error(db_session: Session):
    facade = LocationOverviewFacade(db_session)
    with pytest.raises(ValueError, match="not found"):
        facade.get_overview(uuid4())