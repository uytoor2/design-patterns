from uuid import UUID
from domain.actuators.ports import ActuatorPort


class SimulationActuatorAdapter(ActuatorPort):
    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        # Core physical / simulated hardware invocation
        print(f"[SIMULATION ADAPTER] Executed '{command}' on device {device_id} with {payload}")