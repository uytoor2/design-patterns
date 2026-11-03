from dataclasses import dataclass
from uuid import UUID
from domain.actuators.state import ActuatorState, get_state_object


@dataclass
class ActuatorContext:
    device_id: UUID
    _state: ActuatorState

    @property
    def current_state_name(self) -> str:
        return self._state.name

    @property
    def allowed_commands(self) -> list[str]:
        return self._state.allowed_commands()

    def transition(self, target_state_name: str) -> None:
        self._state = self._state.transition_to(target_state_name)

    @classmethod
    def create(cls, device_id: UUID, current_state_name: str = "idle") -> "ActuatorContext":
        state_obj = get_state_object(current_state_name)
        return cls(device_id=device_id, _state=state_obj)