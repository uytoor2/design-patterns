import pytest
from sqlalchemy.orm import Session
from infrastructure.db import get_db


@pytest.fixture
def db_session() -> Session:
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()