"""CASE-0002 readiness placeholder — infrastructure only, no interpretation."""

from __future__ import annotations

from applications.production.models import ProductionRequest

SYNTHETIC_REQUEST_B = ProductionRequest(
    case_id="",
    year=1992,
    month=8,
    day=3,
    hour=14,
    minute=45,
    gender="female",
    timezone="Asia/Bangkok",
    full_name="Synthetic Readiness Subject",
    birth_place="Hà Nội, Việt Nam",
    export_pdf=False,
)
