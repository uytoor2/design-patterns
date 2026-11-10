from datetime import datetime, timezone, timedelta
from uuid import uuid4
import pytest
from sqlalchemy.orm import Session

from infrastructure.persistence.models import DeviceRow, ActuatorStateRow
from infrastructure.adapters.actuators.simulation import SimulationActuatorAdapter
from infrastructure.adapters.actuators.max_runtime_decorator import (
    MaxRunTimeActuatorDecorator,
    MaxRunTimeExceededError,
)
from infrastructure.adapters.actuators.logging_decorator import LoggingActuatorDecorator
from infrastructure.persistence.execution_log_repository import ExecutionLogRepository
from infrastructure.db import get_db


def test_max_runtime_does_not_call_inner():
    db = next(get_db())
    try:
        # Seed actuator device
        device = DeviceRow(
            device_type="water_pump",
            role="actuator",
            display_name="Main Pump",
        )
        db.add(device)
        db.flush()

        # Seed running state updated 35 minutes ago
        past_time = datetime.now(timezone.utc) - timedelta(minutes=35)
        state_row = ActuatorStateRow(
            device_id=device.id,
            state="running",
            updated_at=past_time,
        )
        db.add(state_row)
        db.commit()

        class MockInnerAdapter(SimulationActuatorAdapter):
            def __init__(self):
                self.called = False

            def apply(self, device_id, command, payload):
                self.called = True

        mock_inner = MockInnerAdapter()
        decorator = MaxRunTimeActuatorDecorator(inner=mock_inner, db=db, max_minutes=30)

        with pytest.raises(MaxRunTimeExceededError):
            decorator.apply(device.id, "pulse", {})

        # Verify inner adapter was NOT called
        assert mock_inner.called is False
    finally:
        db.close()


def test_failed_policy_writes_execution_row():
    db = next(get_db())
    try:
        device = DeviceRow(
            device_type="water_pump",
            role="actuator",
            display_name="Main Pump 2",
        )
        db.add(device)
        db.flush()

        past_time = datetime.now(timezone.utc) - timedelta(minutes=40)
        state_row = ActuatorStateRow(
            device_id=device.id,
            state="running",
            updated_at=past_time,
        )
        db.add(state_row)
        db.commit()

        repo = ExecutionLogRepository(db)
        core_adapter = SimulationActuatorAdapter()
        max_runtime_dec = MaxRunTimeActuatorDecorator(inner=core_adapter, db=db, max_minutes=30)
        stack = LoggingActuatorDecorator(inner=max_runtime_dec, repo=repo)

        with pytest.raises(MaxRunTimeExceededError):
            stack.apply(device.id, "pulse", {})

        # Assert log row written with success=False and policies
        logs = repo.list_executions(limit=1)
        assert len(logs) == 1
        assert logs[0].device_id == device.id
        assert logs[0].success is False
        assert "maxRunTime" in logs[0].policy_applied
        assert "logging" in logs[0].policy_applied
        assert logs[0].message == "Max run time exceeded"
    finally:
        db.close()