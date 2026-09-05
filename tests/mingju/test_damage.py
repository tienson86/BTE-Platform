"""MC-01 Damage: co-presence is not confirmation."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from tests.mingju.conftest import context_from, hidden, visible


def test_copresence_of_hurting_officer_does_not_confirm_damage() -> None:
    result = analyze_mingju(
        context_from(
            pattern={
                "success": True,
                "pattern": "chinh_quan",
                "cach_cuc": "Chính Quan",
                "month_main_qi_ten_god": "Chính Quan",
                "day_master": "Canh",
            },
            ten_gods={
                "visible": [visible("month", "zheng_guan", "Chính Quan")],
                "hidden": [hidden("year", "shang_guan", "Thương Quan", "tertiary")],
            },
        )
    )
    types = {item.damage_type for item in result.damage.findings}
    assert "hurting_officer_attacks_officer" not in types


def test_material_hurting_officer_confirms_damage() -> None:
    result = analyze_mingju(
        context_from(
            pattern={
                "success": True,
                "pattern": "chinh_quan",
                "cach_cuc": "Chính Quan",
                "month_main_qi_ten_god": "Chính Quan",
                "day_master": "Canh",
            },
            ten_gods={
                "visible": [
                    visible("month", "zheng_guan", "Chính Quan"),
                    visible("hour", "shang_guan", "Thương Quan"),
                    visible("year", "shang_guan", "Thương Quan"),
                ],
                "hidden": [],
            },
        )
    )
    confirmed = [item for item in result.damage.findings if item.damage_type == "hurting_officer_attacks_officer"]
    assert confirmed
    item = confirmed[0]
    assert item.damage_id.startswith("DMG-MC-")
    assert item.source == "shang_guan"
    assert item.target == "zheng_guan"
    assert item.evidence_ids
    assert item.trace_ids
    assert 0 < item.confidence <= 1


def test_each_confirmed_damage_has_required_fields() -> None:
    result = analyze_mingju(
        context_from(
            pattern={
                "success": True,
                "pattern": "chinh_quan",
                "cach_cuc": "Chính Quan",
                "month_main_qi_ten_god": "Chính Quan",
            },
            ten_gods={
                "visible": [
                    visible("month", "zheng_guan", "Chính Quan"),
                    visible("hour", "shang_guan", "Thương Quan"),
                ],
                "hidden": [],
            },
        )
    )
    for item in result.damage.findings:
        assert item.damage_id
        assert item.target
        assert item.source
        assert item.severity
        assert item.evidence_ids
        assert item.trace_ids
        assert item.confidence > 0
