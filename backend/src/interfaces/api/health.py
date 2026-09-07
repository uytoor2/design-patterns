from fastapi import APIRouter

from infrastructure.db import check_database

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health():
    db_ok = check_database()
    return {
        "status": "ok" if db_ok else "degraded",
        "db": "ok" if db_ok else "fail",
    }