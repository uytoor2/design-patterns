from uuid import uuid4
from domain.automation.context import LocationAutomationContext, ZoneContext
from domain.automation.strategy import (
    ConservativeMoistureStrategy,
    AggressiveMoistureStrategy,
    get_strategy,
)


def test_conservative_waits_when_above_low_threshold():
    ctx = LocationAutomationContext(
        location_id=uuid4(),
        zones=(
            ZoneContext(
                zone_id=uuid4(),
                zone_name="Bench 1",
                threshold_low=0.25,
                threshold_high=0.55,
                latest_moisture=0.35,  # Midpoint: conservative waits
            ),
        ),
    )
    strategy = ConservativeMoistureStrategy()
    rec = strategy.decide(ctx)
    assert rec.overall_action == "wait"


def test_aggressive_irrigates_at_same_moisture():
    ctx = LocationAutomationContext(
        location_id=uuid4(),
        zones=(
            ZoneContext(
                zone_id=uuid4(),
                zone_name="Bench 1",
                threshold_low=0.25,
                threshold_high=0.55,
                latest_moisture=0.35,  # Below midpoint (0.40): aggressive irrigates
            ),
        ),
    )
    strategy = AggressiveMoistureStrategy()
    rec = strategy.decide(ctx)
    assert rec.overall_action == "irrigate"


def test_unknown_strategy_key_raises_error():
    import pytest
    with pytest.raises(ValueError, match="Unknown strategy_key"):
        get_strategy("invalid_key")