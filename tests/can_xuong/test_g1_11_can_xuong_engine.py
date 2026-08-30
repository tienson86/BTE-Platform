"""G1-11 Cân Xương engine lookup and analyze wiring."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.can_xuong_engine import CanXuongEngine
from engines.can_xuong_engine.calculator import format_display_weight
from engines.identity.assemble import bone_weight_identity_from_payload

from applications.api.services.orchestrator import OrchestratorService


def test_lookup_binh_ngo_year_weight() -> None:
    """Bính Ngọ year row is 13 chỉ in the canonical table."""
    engine = CanXuongEngine()
    result = engine.calculate(
        year_ganzhi="Bính Ngọ",
        lunar_month=1,
        lunar_day=1,
        hour_branch="Dần",
    )
    assert result.year_chi == 13
    assert result.hour_chi == 7
    assert result.month_chi == 6
    assert result.day_chi == 5
    assert result.total_weight == 13 + 6 + 5 + 7
    assert result.display_weight == format_display_weight(result.total_weight)[2]
    assert result.classification
    assert result.summary
    assert result.version == "G1-11"


def test_display_weight_splits_liang_chi() -> None:
    """47 chỉ displays as 4 lượng 7 chỉ."""
    liang, chi, display = format_display_weight(47)
    assert liang == 4
    assert chi == 7
    assert display == "4 lượng 7 chỉ"


def test_identity_copies_display_weight() -> None:
    """Identity bone_weight.weight prefers canonical display_weight."""
    copied = bone_weight_identity_from_payload(
        {
            "display_weight": "4 lượng 7 chỉ",
            "classification": "Thượng cách",
            "rating": "Khá",
            "summary": "Tài lộc khá · hậu vận thuận",
        }
    )
    assert copied.weight == "4 lượng 7 chỉ"
    assert copied.classification == "Thượng cách"


def test_analyze_1966_publishes_can_xuong() -> None:
    """Live 1966 inputs produce analysis.can_xuong from the engine, not dashes."""
    calendar = CalendarEngine().build(1966, 9, 24, 4, 15, gender="male")
    bazi = BaziEngine().build(calendar, gender="male")
    engine = CanXuongEngine()
    expected = engine.calculate_from_calendar_bazi(calendar, bazi)
    payload = OrchestratorService().analyze(
        year=1966,
        month=9,
        day=24,
        hour=4,
        minute=15,
        gender="male",
    )
    published = payload.get("can_xuong") or {}
    assert published.get("display_weight") == expected.display_weight
    assert published.get("classification") == expected.classification
    assert published.get("version") == "G1-11"
    identity = (payload.get("identity") or {}).get("bone_weight") or {}
    assert identity.get("weight") == expected.display_weight
    assert identity.get("classification") == expected.classification
    assert expected.display_weight
    assert "—" not in expected.display_weight
