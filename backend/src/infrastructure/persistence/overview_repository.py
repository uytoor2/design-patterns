from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session

from infrastructure.persistence.models import LocationRow, ZoneRow, DeviceRow, ReadingRow, AutomationRuleRow


class OverviewRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_location_with_zones(self, location_id: UUID) -> tuple[LocationRow, list[ZoneRow]] | None:
        location = self._db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not location:
            return None
        zones = self._db.query(ZoneRow).filter(ZoneRow.location_id == location_id).all()
        return location, zones

    def get_assigned_devices(self, location_id: UUID) -> list[DeviceRow]:
        # A device is assigned only when location_id is set and zone_id is NOT NULL
        return (
            self._db.query(DeviceRow)
            .filter(
                DeviceRow.location_id == location_id,
                DeviceRow.zone_id.isnot(None),
            )
            .all()
        )

    def get_latest_readings_for_devices(self, device_ids: list[UUID]) -> dict[UUID, ReadingRow]:
        if not device_ids:
            return {}

        # Subquery to identify the latest recorded_at timestamp per device_id
        subq = (
            self._db.query(
                ReadingRow.device_id,
                func.max(ReadingRow.recorded_at).label("max_recorded_at"),
            )
            .filter(ReadingRow.device_id.in_(device_ids))
            .group_by(ReadingRow.device_id)
            .subquery()
        )

        rows = (
            self._db.query(ReadingRow)
            .join(
                subq,
                (ReadingRow.device_id == subq.c.device_id)
                & (ReadingRow.recorded_at == subq.c.max_recorded_at),
            )
            .all()
        )

        return {r.device_id: r for r in rows}

    def get_saved_strategy_key(self, location_id: UUID) -> str | None:
        rule = (
            self._db.query(AutomationRuleRow)
            .filter(AutomationRuleRow.location_id == location_id)
            .first()
        )
        return rule.strategy_key if rule else None