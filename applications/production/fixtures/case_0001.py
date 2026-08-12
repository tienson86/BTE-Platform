"""CASE-0001 golden commercial regression fixture — reference only."""

from __future__ import annotations

from applications.production.models import ProductionRequest

CASE_0001_REQUEST = ProductionRequest(
    case_id="CASE-0001",
    year=1987,
    month=1,
    day=21,
    hour=4,
    minute=30,
    gender="male",
    timezone="Asia/Bangkok",
    full_name="Nguyễn Tiến Sơn",
    birth_place="Hà Tây, Việt Nam",
)

CASE_0001_EXPECTED_PILLARS = {
    "year": "Bính Dần",
    "month": "Tân Sửu",
    "day": "Canh Ngọ",
    "hour": "Mậu Dần",
}

CASE_0001_EXPECTED_STRENGTH = {
    "strength_level": "strong",
    "strength_score": 0.87,
}
