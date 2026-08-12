"""CASE-0001 runtime fixture using ProductionEngineRunner."""

from __future__ import annotations

from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Source
from engines.report_engine.contracts.report_input_v1 import ReportProfileV1

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest

CASE_0001_CANONICAL = {
    "case_id": "CASE-0001",
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "timezone": "Asia/Bangkok",
    "profile": ReportProfileV1(
        full_name="Nguyễn Tiến Sơn",
        gender="male",
        birth_date="1987-01-21",
        birth_time="04:30",
        birth_place="Hà Tây, Việt Nam",
        timezone="Asia/Bangkok",
    ),
    "expected_pillars": {
        "year": "Bính Dần",
        "month": "Tân Sửu",
        "day": "Canh Ngọ",
        "hour": "Mậu Dần",
    },
}


def build_case_0001_source() -> ReportInputV1Source:
    """Run production engines for CASE-0001 canonical birth data."""
    birth = CASE_0001_CANONICAL
    request = ProductionRequest(
        case_id=birth["case_id"],
        year=birth["year"],
        month=birth["month"],
        day=birth["day"],
        hour=birth["hour"],
        minute=birth["minute"],
        gender=birth["gender"],
        timezone=birth["timezone"],
        full_name=birth["profile"].full_name,
        birth_place=birth["profile"].birth_place,
    )
    output = ProductionEngineRunner().run(request)
    source = output.report_source
    source.profile = birth["profile"]
    return source
