from uuid import UUID
from sqlalchemy.orm import Session

from application.overview.dto import (
    LocationOverviewDto,
    LocationSummaryDto,
    DeviceCountsDto,
    OverviewZoneDto,
    OverviewDeviceDto,
    OverviewReadingDto,
    RecommendationSummaryDto,
)
from infrastructure.persistence.overview_repository import OverviewRepository
from infrastructure.persistence.automation_repository import AutomationRepository
from application.automation.service import AutomationService


class LocationOverviewFacade:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = OverviewRepository(db)

    def get_overview(self, location_id: UUID) -> LocationOverviewDto:
        loc_data = self._repo.get_location_with_zones(location_id)
        if not loc_data:
            raise ValueError(f"Location {location_id} not found")

        location_row, zone_rows = loc_data

        # 1. Fetch assigned devices
        assigned_devices = self._repo.get_assigned_devices(location_id)

        # 2. Compute assigned device counts by role
        sensor_count = sum(1 for d in assigned_devices if d.role == "sensor")
        actuator_count = sum(1 for d in assigned_devices if d.role == "actuator")
        device_counts = DeviceCountsDto(sensor=sensor_count, actuator=actuator_count)

        # 3. Group devices by zone_id
        devices_by_zone: dict[UUID, list[OverviewDeviceDto]] = {}
        assigned_device_ids = [d.id for d in assigned_devices]

        for d in assigned_devices:
            if d.zone_id not in devices_by_zone:
                devices_by_zone[d.zone_id] = []
            devices_by_zone[d.zone_id].append(
                OverviewDeviceDto(
                    id=d.id,
                    device_type=d.device_type,
                    role=d.role,
                    display_name=d.display_name,
                )
            )

        # 4. Fetch latest readings for all assigned devices
        latest_readings_map = self._repo.get_latest_readings_for_devices(assigned_device_ids)

        # Map device details (tracking, interval) for reading summaries
        device_map = {d.id: d for d in assigned_devices}

        # 5. Assemble Zone DTOs (including empty zones)
        zone_dtos: list[OverviewZoneDto] = []
        for zone in zone_rows:
            zone_devices = devices_by_zone.get(zone.id, [])
            zone_readings: list[OverviewReadingDto] = []

            for dev in zone_devices:
                if dev.id in latest_readings_map:
                    r_row = latest_readings_map[dev.id]
                    dev_entity = device_map[dev.id]
                    zone_readings.append(
                        OverviewReadingDto(
                            device_id=r_row.device_id,
                            value=float(r_row.value),
                            unit=r_row.unit,
                            recorded_at=r_row.recorded_at,
                            tracking_enabled=dev_entity.tracking_enabled,
                            sampling_interval_seconds=dev_entity.sampling_interval_seconds,
                        )
                    )

            zone_dtos.append(
                OverviewZoneDto(
                    id=zone.id,
                    name=zone.name,
                    moisture_threshold_low=float(zone.moisture_threshold_low),
                    moisture_threshold_high=float(zone.moisture_threshold_high),
                    devices=zone_devices,
                    latest_readings=zone_readings,
                )
            )

        # 6. Saved Strategy & Dynamic Recommendation Evaluation
        strategy_key = self._repo.get_saved_strategy_key(location_id)
        last_recommendation: RecommendationSummaryDto | None = None

        if strategy_key:
            auto_repo = AutomationRepository(self._db)
            auto_service = AutomationService(auto_repo)
            eval_res = auto_service.evaluate(location_id)
            last_recommendation = RecommendationSummaryDto(
                action=eval_res.action,
                reason=eval_res.reason,
            )

        return LocationOverviewDto(
            location=LocationSummaryDto(id=location_row.id, name=location_row.name),
            device_counts=device_counts,
            zones=zone_dtos,
            strategy_key=strategy_key,
            last_recommendation=last_recommendation,
        )