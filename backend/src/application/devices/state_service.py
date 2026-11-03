from uuid import UUID
from sqlalchemy.orm import Session
from domain.actuators.context import ActuatorContext
from infrastructure.persistence.actuator_state_repository import ActuatorStateRepository


class ActuatorStateService:
    def __init__(self, db: Session) -> None:
        self._repo = ActuatorStateRepository(db)

    def get_context(self, device_id: UUID) -> ActuatorContext:
        current_state = self._repo.get_state(device_id)
        return ActuatorContext.create(device_id, current_state)

    def transition_state(self, device_id: UUID, target_state: str) -> ActuatorContext:
        context = self.get_context(device_id)
        context.transition(target_state)  # Domain guards check here
        self._repo.save_state(device_id, context.current_state_name)
        return context