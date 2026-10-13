from abc import ABC, abstractmethod
from domain.automation.context import LocationAutomationContext
from domain.automation.recommendation import Recommendation, ZoneRecommendation


class AutomationStrategy(ABC):
    key: str

    @abstractmethod
    def decide(self, context: LocationAutomationContext) -> Recommendation:
        """Evaluates location context and returns an irrigation recommendation."""
        pass


class ConservativeMoistureStrategy(AutomationStrategy):
    key = "conservative"

    def decide(self, context: LocationAutomationContext) -> Recommendation:
        zone_recs: list[ZoneRecommendation] = []
        any_irrigate = False

        for zone in context.zones:
            if zone.latest_moisture is None:
                zone_recs.append(
                    ZoneRecommendation(
                        zone_id=str(zone.zone_id),
                        zone_name=zone.zone_name,
                        action="wait",
                        reason="No moisture sensor in this zone.",
                    )
                )
                continue

            # Conservative Rule: Only irrigate if moisture falls strictly below threshold_low
            if zone.latest_moisture < zone.threshold_low:
                any_irrigate = True
                action = "irrigate"
                reason = f"Moisture ({zone.latest_moisture:.2f}) is below low threshold ({zone.threshold_low:.2f})."
            else:
                action = "wait"
                reason = f"Moisture ({zone.latest_moisture:.2f}) is safe (>= low threshold {zone.threshold_low:.2f})."

            zone_recs.append(
                ZoneRecommendation(
                    zone_id=str(zone.zone_id),
                    zone_name=zone.zone_name,
                    action=action,
                    reason=reason,
                )
            )

        overall_action = "irrigate" if any_irrigate else "wait"
        summary = (
            "One or more zones require irrigation (Conservative Policy)."
            if any_irrigate
            else "All zones have sufficient moisture (Conservative Policy)."
        )

        return Recommendation(
            overall_action=overall_action,
            summary_reason=summary,
            zone_recommendations=tuple(zone_recs),
        )


class AggressiveMoistureStrategy(AutomationStrategy):
    key = "aggressive"

    def decide(self, context: LocationAutomationContext) -> Recommendation:
        zone_recs: list[ZoneRecommendation] = []
        any_irrigate = False

        for zone in context.zones:
            if zone.latest_moisture is None:
                zone_recs.append(
                    ZoneRecommendation(
                        zone_id=str(zone.zone_id),
                        zone_name=zone.zone_name,
                        action="wait",
                        reason="No moisture sensor in this zone.",
                    )
                )
                continue

            # Aggressive Rule: Irrigate if moisture falls below midpoint of (threshold_low, threshold_high)
            midpoint = (zone.threshold_low + zone.threshold_high) / 2.0
            if zone.latest_moisture < midpoint:
                any_irrigate = True
                action = "irrigate"
                reason = f"Moisture ({zone.latest_moisture:.2f}) is below aggressive target midpoint ({midpoint:.2f})."
            else:
                action = "wait"
                reason = f"Moisture ({zone.latest_moisture:.2f}) is above target midpoint ({midpoint:.2f})."

            zone_recs.append(
                ZoneRecommendation(
                    zone_id=str(zone.zone_id),
                    zone_name=zone.zone_name,
                    action=action,
                    reason=reason,
                )
            )

        overall_action = "irrigate" if any_irrigate else "wait"
        summary = (
            "Proactive irrigation recommended (Aggressive Policy)."
            if any_irrigate
            else "Moisture levels optimal across all zones (Aggressive Policy)."
        )

        return Recommendation(
            overall_action=overall_action,
            summary_reason=summary,
            zone_recommendations=tuple(zone_recs),
        )


STRATEGIES: dict[str, AutomationStrategy] = {
    ConservativeMoistureStrategy.key: ConservativeMoistureStrategy(),
    AggressiveMoistureStrategy.key: AggressiveMoistureStrategy(),
}


def get_strategy(key: str) -> AutomationStrategy:
    if key not in STRATEGIES:
        valid_keys = ", ".join(STRATEGIES.keys())
        raise ValueError(f"Unknown strategy_key '{key}'. Valid choices: {valid_keys}")
    return STRATEGIES[key]