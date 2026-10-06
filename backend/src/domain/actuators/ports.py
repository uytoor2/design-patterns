from abc import ABC, abstractmethod
from uuid import UUID


class ActuatorPort(ABC):
    @abstractmethod
    def apply(self, device_id: UUID, command: str, payload: dict) -> None:
        """Executes a command on the target actuator."""
        pass