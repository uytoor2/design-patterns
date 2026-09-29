from uuid import UUID
from domain.locations.config_builder import LocationConfigBuilder
from application.locations.dto import BuildLocationConfigRequestDto, LocationConfigDto
from application.locations.mappers import location_config_to_dto
from infrastructure.persistence.location_repository import LocationRepository


class LocationConfigService:
    def __init__(self, repo: LocationRepository) -> None:
        self._repo = repo

    def build_and_save(self, request: BuildLocationConfigRequestDto) -> LocationConfigDto:
        builder = LocationConfigBuilder().with_location_name(request.location_name)
        for z in request.zones:
            builder.add_zone(
                name=z.name,
                moisture_threshold_low=z.moisture_threshold_low,
                moisture_threshold_high=z.moisture_threshold_high,
                schedule=z.schedule,
            )
        
        config = builder.build()
        loc_row, zone_rows = self._repo.save_config(config)
        return location_config_to_dto(loc_row, zone_rows)

    def get_config(self, location_id: UUID) -> LocationConfigDto | None:
        res = self._repo.get_config(location_id)
        if not res:
            return None
        return location_config_to_dto(res[0], res[1])