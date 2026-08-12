"""CASE-0002 validation subject — Hoàng Thị Thu Phương (generalization failure)."""

from __future__ import annotations

from applications.production.models import ProductionRequest

CASE_0002_REQUEST = ProductionRequest(
    case_id="CASE-0002",
    year=1997,
    month=7,
    day=1,
    hour=14,
    minute=24,
    gender="female",
    timezone="Asia/Ho_Chi_Minh",
    full_name="Hoàng Thị Thu Phương",
    birth_place="Quảng Ninh, Việt Nam",
    export_pdf=False,
)

# Infrastructure-only synthetic — not CASE-0002 commercial subject.
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
