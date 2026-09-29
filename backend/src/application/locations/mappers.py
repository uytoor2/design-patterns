from infrastructure.persistence.models import LocationRow, ZoneRow
from application.locations.dto import LocationConfigDto, LocationResponseDto, ZoneResponseDto


def location_config_to_dto(location_row: LocationRow, zone_rows: list[ZoneRow]) -> LocationConfigDto:
    return LocationConfigDto(
        location=LocationResponseDto(
            id=location_row.id,
            name=location_row.name,
        ),
        zones=[
            ZoneResponseDto(
                id=z.id,
                location_id=z.location_id,
                name=z.name,
                moisture_threshold_low=float(z.moisture_threshold_low),
                moisture_threshold_high=float(z.moisture_threshold_high),
                schedule=z.schedule,
            )
            for z in zone_rows
        ],
    )