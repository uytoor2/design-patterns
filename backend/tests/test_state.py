import pytest
from uuid import uuid4
from domain.actuators.context import ActuatorContext
from domain.actuators.errors import IllegalTransitionError


def test_idle_to_running_allowed():
    ctx = ActuatorContext.create(device_id=uuid4(), current_state_name="idle")
    assert ctx.current_state_name == "idle"
    assert "start_pump" in ctx.allowed_commands

    ctx.transition("running")
    assert ctx.current_state_name == "running"
    assert "stop_pump" in ctx.allowed_commands


def test_running_to_maintenance_rejected():
    ctx = ActuatorContext.create(device_id=uuid4(), current_state_name="running")
    with pytest.raises(IllegalTransitionError, match="Cannot transition from state 'running' to 'maintenance'"):
        ctx.transition("maintenance")


def test_error_state_recovery():
    ctx = ActuatorContext.create(device_id=uuid4(), current_state_name="error")
    ctx.transition("idle")
    assert ctx.current_state_name == "idle"