from abc import ABC, abstractmethod
from domain.actuators.errors import IllegalTransitionError


class ActuatorState(ABC):
    name: str

    @abstractmethod
    def allowed_transitions(self) -> set[str]:
        pass

    @abstractmethod
    def allowed_commands(self) -> list[str]:
        pass

    def transition_to(self, target_name: str) -> "ActuatorState":
        if target_name not in self.allowed_transitions():
            raise IllegalTransitionError(
                f"Cannot transition from state '{self.name}' to '{target_name}'."
            )
        return get_state_object(target_name)


class IdleState(ActuatorState):
    name = "idle"

    def allowed_transitions(self) -> set[str]:
        return {"running", "maintenance", "error", "off"}

    def allowed_commands(self) -> list[str]:
        return ["start_pump", "enter_maintenance", "power_off"]


class RunningState(ActuatorState):
    name = "running"

    def allowed_transitions(self) -> set[str]:
        return {"idle", "error"}

    def allowed_commands(self) -> list[str]:
        return ["stop_pump", "emergency_stop"]


class OffState(ActuatorState):
    name = "off"

    def allowed_transitions(self) -> set[str]:
        return {"idle", "maintenance", "error"}

    def allowed_commands(self) -> list[str]:
        return ["power_on"]


class MaintenanceState(ActuatorState):
    name = "maintenance"

    def allowed_transitions(self) -> set[str]:
        return {"idle", "error", "off"}

    def allowed_commands(self) -> list[str]:
        return ["exit_maintenance", "run_diagnostics"]


class ErrorState(ActuatorState):
    name = "error"

    def allowed_transitions(self) -> set[str]:
        return {"idle", "maintenance"}

    def allowed_commands(self) -> list[str]:
        return ["reset_error", "enter_maintenance"]


STATE_MAP: dict[str, ActuatorState] = {
    IdleState.name: IdleState(),
    RunningState.name: RunningState(),
    OffState.name: OffState(),
    MaintenanceState.name: MaintenanceState(),
    ErrorState.name: ErrorState(),
}


def get_state_object(state_name: str) -> ActuatorState:
    if state_name not in STATE_MAP:
        raise ValueError(f"Unknown state '{state_name}'. Valid states: {list(STATE_MAP.keys())}")
    return STATE_MAP[state_name]