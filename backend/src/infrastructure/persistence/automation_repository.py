from uuid import UUID
from sqlalchemy.orm import Session
from infrastructure.persistence.models import AutomationRuleRow, LocationRow, ZoneRow, DeviceRow, ReadingRow


class AutomationRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def upsert_strategy(self, location_id: UUID, strategy_key: str) -> AutomationRuleRow:
        rule = (
            self._db.query(AutomationRuleRow)
            .filter(AutomationRuleRow.location_id == location_id)
            .first()
        )
        if not rule:
            rule = AutomationRuleRow(location_id=location_id, strategy_key=strategy_key)
            self._db.add(rule)
        else:
            rule.strategy_key = strategy_key

        self._db.commit()
        self._db.refresh(rule)
        return rule

    def get_strategy_key(self, location_id: UUID) -> str:
        rule = (
            self._db.query(AutomationRuleRow)
            .filter(AutomationRuleRow.location_id == location_id)
            .first()
        )
        return rule.strategy_key if rule else "conservative"

    def get_location(self, location_id: UUID) -> LocationRow | None:
        return self._db.query(LocationRow).filter(LocationRow.id == location_id).first()

    def get_zones_for_location(self, location_id: UUID) -> list[ZoneRow]:
        return self._db.query(ZoneRow).filter(ZoneRow.location_id == location_id).all()

    def get_latest_moisture_for_zone(self, zone_id: UUID) -> float | None:
        # Finds moisture sensors assigned to zone_id
        sensor = (
            self._db.query(DeviceRow)
            .filter(
                DeviceRow.zone_id == zone_id,
                DeviceRow.role == "sensor",
                DeviceRow.device_type.ilike("%moisture%"),
            )
            .first()
        )
        if not sensor:
            return None

        latest_reading = (
            self._db.query(ReadingRow)
            .filter(ReadingRow.device_id == sensor.id)
            .order_by(ReadingRow.recorded_at.desc())
            .first()
        )
        return float(latest_reading.value) if latest_reading else None