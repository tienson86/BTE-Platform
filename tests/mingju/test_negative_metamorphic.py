"""Negative and metamorphic MC-01 tests."""

from __future__ import annotations

from engines.mingju import analyze_mingju, build_mingju_context
from engines.mingju.exceptions import MingJuValidationError, MingJuVersionError
from engines.mingju.validators import validate_context, validate_result
from tests.mingju.conftest import context_from, hidden, visible


def test_unsupported_context_schema_fails_closed() -> None:
    context = context_from()
    context.schema_version = "bte.unknown.v9"
    try:
        validate_context(context)
        raise AssertionError("unsupported schema must fail")
    except MingJuVersionError:
        pass


def test_analysis_id_mismatch_fails_closed() -> None:
    result = analyze_mingju(context_from())
    other = context_from()
    other.analysis_id = "an-other"
    try:
        validate_result(result, other)
        raise AssertionError("analysis_id mismatch must fail")
    except MingJuValidationError:
        pass


def test_grade_without_integrity_fails_closed() -> None:
    result = analyze_mingju(context_from())
    result.integrity.state = "unresolved"
    result.integrity.score = None
    try:
        validate_result(result, context_from())
        raise AssertionError("grade without integrity must fail")
    except MingJuValidationError:
        pass


def test_hidden_residual_noise_does_not_create_damage() -> None:
    baseline = analyze_mingju(context_from())
    noisy = analyze_mingju(
        context_from(
            ten_gods={
                "visible": [
                    visible("month", "zheng_yin", "Chính Ấn", "Ất"),
                    visible("hour", "zheng_yin", "Chính Ấn", "Đinh"),
                ],
                "hidden": [
                    hidden("month", "zheng_yin", "Chính Ấn", "primary"),
                    hidden("year", "shang_guan", "Thương Quan", "tertiary"),
                    hidden("day", "qi_sha", "Thất Sát", "tertiary"),
                ],
            }
        )
    )
    assert {item.damage_type for item in baseline.damage.findings} == {
        item.damage_type for item in noisy.damage.findings
    }


def test_same_input_same_result() -> None:
    first = analyze_mingju(context_from())
    second = analyze_mingju(context_from())
    assert first.content_hash == second.content_hash
    assert first.grade.grade == second.grade.grade
    assert first.purity.score == second.purity.score
    assert first.result_id == second.result_id


def test_build_mingju_context_does_not_decide() -> None:
    context = build_mingju_context(payload={"pattern": {"cach_cuc": "Chính Ấn"}})
    assert context.pattern_label == "Chính Ấn"
    assert context.schema_version == "bte.mingju.context.v1"
