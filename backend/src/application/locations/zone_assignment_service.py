from uuid import UUID
from sqlalchemy.orm import Session
from infrastructure.persistence.models import DeviceRow, ZoneRow


class ZoneAssignmentService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def assign_device(self, device_id: UUID, zone_id: UUID | None) -> bool:
        device = self._db.query(DeviceRow).filter(DeviceRow.id == device_id).first()
        if not device:
            return False

        if zone_id is None:
            device.zone_id = None
            device.location_id = None
        else:
            zone = self._db.query(ZoneRow).filter(ZoneRow.id == zone_id).first()
            if not zone:
                return False
            device.zone_id = zone.id
            device.location_id = zone.location_id  # Copies location_id from zone

        self._db.commit()
        return True