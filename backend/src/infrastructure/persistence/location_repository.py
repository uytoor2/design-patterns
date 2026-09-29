from uuid import UUID
from sqlalchemy.orm import Session
from infrastructure.persistence.models import LocationRow, ZoneRow, DeviceRow
from domain.locations.entity import LocationConfig


class LocationRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def save_config(self, config: LocationConfig) -> tuple[LocationRow, list[ZoneRow]]:
        location_row = LocationRow(name=config.location.name)
        self._db.add(location_row)
        self._db.flush()  # Generates location_row.id

        zone_rows = []
        for zone in config.location.zones:
            z_row = ZoneRow(
                location_id=location_row.id,
                name=zone.name,
                moisture_threshold_low=zone.moisture_threshold_low,
                moisture_threshold_high=zone.moisture_threshold_high,
                schedule=zone.schedule,
            )
            zone_rows.append(z_row)
            self._db.add(z_row)

        self._db.commit()
        self._db.refresh(location_row)
        for z in zone_rows:
            self._db.refresh(z)

        return location_row, zone_rows

    def list_locations(self) -> list[LocationRow]:
        return self._db.query(LocationRow).order_by(LocationRow.created_at.desc()).all()

    def get_config(self, location_id: UUID) -> tuple[LocationRow, list[ZoneRow]] | None:
        loc = self._db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc:
            return None
        zones = self._db.query(ZoneRow).filter(ZoneRow.location_id == location_id).all()
        return loc, zones

    def delete_location(self, location_id: UUID) -> bool:
        loc = self._db.query(LocationRow).filter(LocationRow.id == location_id).first()
        if not loc:
            return False
        
        # Clear device location_id and zone_id before cascade delete
        self._db.query(DeviceRow).filter(DeviceRow.location_id == location_id).update(
            {DeviceRow.zone_id: None, DeviceRow.location_id: None}, synchronize_session=False
        )
        
        self._db.delete(loc)
        self._db.commit()
        return True