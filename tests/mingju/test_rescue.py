"""MC-01 Rescue must target registered Damage."""

from __future__ import annotations

from engines.mingju import analyze_mingju
from engines.mingju.exceptions import MingJuValidationError
from engines.mingju.models import RescueFinding
from engines.mingju.validators import validate_result
from tests.mingju.conftest import context_from, visible


def test_no_orphan_rescue_without_damage() -> None:
    result = analyze_mingju(context_from())
    if not result.damage.findings:
        assert result.rescue.findings == ()


def test_rescue_references_existing_damage() -> None:
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
                    visible("year", "zheng_yin", "Chính Ấn"),
                ],
                "hidden": [],
            },
        )
    )
    if result.damage.findings and result.rescue.findings:
        damage_ids = {item.damage_id for item in result.damage.findings}
        for item in result.rescue.findings:
            assert item.target_damage_ids
            assert set(item.target_damage_ids) <= damage_ids
            assert item.evidence_ids


def test_validator_rejects_orphan_rescue() -> None:
    result = analyze_mingju(context_from())
    result.rescue.findings = (
        RescueFinding(
            rescue_id="RSC-MC-999",
            rescue_type="seal_controls_hurting_officer",
            source="resource",
            target_damage_ids=("DMG-MC-missing",),
            strength="moderate",
            evidence_ids=("E-MC-001",),
        ),
    )
    try:
        validate_result(result, context_from())
        raise AssertionError("orphan rescue must fail closed")
    except MingJuValidationError:
        pass
