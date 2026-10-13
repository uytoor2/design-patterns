from uuid import UUID
from pydantic import BaseModel


class SetStrategyRequestDto(BaseModel):
    strategy_key: str


class ZoneRecommendationDto(BaseModel):
    zone_id: str
    zone_name: str
    action: str
    reason: str


class EvaluationResponseDto(BaseModel):
    location_id: UUID
    strategy_key: str
    action: str
    reason: str
    zone_details: list[ZoneRecommendationDto]