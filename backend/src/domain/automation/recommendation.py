from dataclasses import dataclass


@dataclass(frozen=True)
class ZoneRecommendation:
    zone_id: str
    zone_name: str
    action: str  # "irrigate" | "wait"
    reason: str


@dataclass(frozen=True)
class Recommendation:
    overall_action: str  # "irrigate" | "wait"
    summary_reason: str
    zone_recommendations: tuple[ZoneRecommendation, ...]