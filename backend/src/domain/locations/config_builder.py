from domain.locations.entity import Location, LocationConfig, Zone
from domain.locations.errors import ConfigurationError


class LocationConfigBuilder:
    def __init__(self) -> None:
        self._name: str | None = None
        self._zones: list[Zone] = []

    def with_location_name(self, name: str) -> "LocationConfigBuilder":
        self._name = name.strip() if name else ""
        return self

    def add_zone(
        self,
        name: str,
        moisture_threshold_low: float,
        moisture_threshold_high: float,
        schedule: dict | None = None,
    ) -> "LocationConfigBuilder":
        zone = Zone(
            name=name.strip() if name else "",
            moisture_threshold_low=float(moisture_threshold_low),
            moisture_threshold_high=float(moisture_threshold_high),
            schedule=schedule or {},
        )
        self._zones.append(zone)
        return self

    def build(self) -> LocationConfig:
        if not self._name:
            raise ConfigurationError("Location name is required and cannot be empty.")
        
        if not self._zones:
            raise ConfigurationError("At least one zone is required in the location configuration.")

        seen_zone_names: set[str] = set()

        for zone in self._zones:
            if not zone.name:
                raise ConfigurationError("Zone name cannot be empty.")
            
            if zone.name in seen_zone_names:
                raise ConfigurationError(f"Duplicate zone name '{zone.name}' within location.")
            seen_zone_names.add(zone.name)

            if not (0.0 <= zone.moisture_threshold_low <= 1.0) or not (0.0 <= zone.moisture_threshold_high <= 1.0):
                raise ConfigurationError(
                    f"Moisture thresholds for zone '{zone.name}' must be between 0.0 and 1.0."
                )

            if zone.moisture_threshold_low >= zone.moisture_threshold_high:
                raise ConfigurationError(
                    f"Low threshold ({zone.moisture_threshold_low}) must be strictly less than high threshold ({zone.moisture_threshold_high}) in zone '{zone.name}'."
                )

        location = Location(name=self._name, zones=tuple(self._zones))
        return LocationConfig(location=location)