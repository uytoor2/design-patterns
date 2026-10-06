import logging
from uuid import UUID
from domain.actuators.ports import ActuatorPort

logger = logging.getLogger(__name__)


class SimulationActuatorAdapter(ActuatorPort):
    def __init__(self) -> None:
        self.execution_log: list[dict] = []

    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        record = {"device_id": str(device_id), "command": command, "payload": payload}
        self.execution_log.append(record)
        logger.info(f"[SIMULATION ACTUATOR] Command '{command}' executed on device {device_id}: {payload}")