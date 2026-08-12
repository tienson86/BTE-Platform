"""CASE-0001 Ten Gods runtime adapter."""

from __future__ import annotations

from engines.ten_gods_engine.engine import TenGodsEngine
from engines.ten_gods_engine.models import TenGodsResult

CASE_0001_PILLARS = {
    "year": {"stem": "Bính", "branch": "Dần"},
    "month": {"stem": "Tân", "branch": "Sửu"},
    "day": {"stem": "Canh", "branch": "Ngọ"},
    "hour": {"stem": "Mậu", "branch": "Dần"},
}


def run_case_0001() -> TenGodsResult:
    """Run Ten Gods Core Engine for canonical CASE-0001."""
    engine = TenGodsEngine()
    return engine.calculate(
        day_master="Canh",
        pillars=CASE_0001_PILLARS,
        case_id="CASE-0001",
    )
