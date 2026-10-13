from uuid import UUID
from domain.automation.context import LocationAutomationContext, ZoneContext
from domain.automation.strategy import get_strategy
from application.automation.dto import EvaluationResponseDto, ZoneRecommendationDto
from infrastructure.persistence.automation_repository import AutomationRepository


class AutomationService:
    def __init__(self, repo: AutomationRepository) -> None:
        self._repo = repo

    def set_strategy(self, location_id: UUID, strategy_key: str) -> None:
        loc = self._repo.get_location(location_id)
        if not loc:
            raise ValueError(f"Location {location_id} not found.")
        
        # Validates key before persisting
        get_strategy(strategy_key)
        self._repo.upsert_strategy(location_id, strategy_key)

    def evaluate(self, location_id: UUID) -> EvaluationResponseDto:
        loc = self._repo.get_location(location_id)
        if not loc:
            raise ValueError(f"Location {location_id} not found.")

        strategy_key = self._repo.get_strategy_key(location_id)
        strategy = get_strategy(strategy_key)

        zones = self._repo.get_zones_for_location(location_id)
        zone_contexts: list[ZoneContext] = []

        for z in zones:
            moisture = self._repo.get_latest_moisture_for_zone(z.id)
            zone_contexts.append(
                ZoneContext(
                    zone_id=z.id,
                    zone_name=z.name,
                    threshold_low=float(z.moisture_threshold_low),
                    threshold_high=float(z.moisture_threshold_high),
                    latest_moisture=moisture,
                )
            )

        context = LocationAutomationContext(
            location_id=location_id,
            zones=tuple(zone_contexts),
        )

        recommendation = strategy.decide(context)

        return EvaluationResponseDto(
            location_id=location_id,
            strategy_key=strategy_key,
            action=recommendation.overall_action,
            reason=recommendation.summary_reason,
            zone_details=[
                ZoneRecommendationDto(
                    zone_id=zr.zone_id,
                    zone_name=zr.zone_name,
                    action=zr.action,
                    reason=zr.reason,
                )
                for zr in recommendation.zone_recommendations
            ],
        )