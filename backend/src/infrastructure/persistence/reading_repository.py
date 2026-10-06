from uuid import UUID
from sqlalchemy.orm import Session
from domain.sensors.reading import Reading
from infrastructure.persistence.models import ReadingRow


class ReadingRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert(self, reading: Reading) -> ReadingRow:
        row = ReadingRow(
            device_id=reading.device_id,
            value=reading.value,
            unit=reading.unit,
            source=reading.source,
            recorded_at=reading.recorded_at,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return row

    def list_for_device(self, device_id: UUID, limit: int = 20) -> list[ReadingRow]:
        return (
            self._db.query(ReadingRow)
            .filter(ReadingRow.device_id == device_id)
            .order_by(ReadingRow.recorded_at.desc())
            .limit(limit)
            .all()
        )