"""G1-07 ShenSha canonical identity, formula, and evidence."""

from __future__ import annotations

from applications.api.services.bazi_truth import build_bazi_view
from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.shensha.catalog import (
    ALIAS_TIAN_DE,
    ALIAS_TIAN_YI,
    ALIAS_YUE_DE,
    ID_HONG_LUAN,
    ID_TIAN_DE,
    ID_TIAN_XI,
    ID_TIAN_YI,
    ID_YUE_DE,
    NAME_HONG_LUAN,
    NAME_TIAN_DE,
    NAME_TIAN_XI,
    NAME_TIAN_YI,
    NAME_YUE_DE,
    PUBLISHED_NAMES,
)
from engines.bazi_engine.shensha.service import ShenShaService
from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    ReportInputV1Source,
)
from applications.api.models.analysis_result import AnalysisResult


def _service() -> ShenShaService:
    return ShenShaService()


def _match(result, star_id: str):
    return next((item for item in result.matches if item.id == star_id), None)


def test_calculate_is_projection_of_evaluate() -> None:
    """Legacy names come from structured matches, not a second detector."""
    service = _service()
    kwargs = {
        "day_master": "Canh",
        "year_branch": "Dần",
        "month_branch": "Sửu",
        "day_branch": "Ngọ",
        "hour_branch": "Dần",
        "stems": ["Bính", "Tân", "Canh", "Mậu"],
        "branches": ["Dần", "Sửu", "Ngọ", "Dần"],
    }
    result = service.evaluate(**kwargs)
    assert service.calculate(**kwargs) == result.canonical_names()


def test_thien_at_alias_not_double_published() -> None:
    """Thiên Ất is an alias of Thiên Ất Quý Nhân."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Tý",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Hợi",
        stems=["Giáp", "Ất", "Canh", "Bính"],
        branches=["Tý", "Sửu", "Ngọ", "Hợi"],
    )
    names = result.canonical_names()
    assert NAME_TIAN_YI in names
    assert ALIAS_TIAN_YI not in names
    assert names.count(NAME_TIAN_YI) == 1
    match = _match(result, ID_TIAN_YI)
    assert match is not None
    assert ALIAS_TIAN_YI in match.aliases
    assert match.source_type == "day_stem"
    assert match.source_value == "Canh"
    assert match.target_value == "Sửu"
    assert match.pillar == "month"


def test_thien_duc_alias_not_double_published() -> None:
    """Thiên Đức is an alias of Thiên Đức Quý Nhân."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Tý",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Hợi",
        stems=["Giáp", "Ất", "Canh", "Bính"],
        branches=["Tý", "Sửu", "Ngọ", "Hợi"],
    )
    names = result.canonical_names()
    assert NAME_TIAN_DE in names
    assert ALIAS_TIAN_DE not in names
    match = _match(result, ID_TIAN_DE)
    assert match is not None
    assert match.source_type == "month_branch"
    assert match.source_value == "Sửu"
    assert match.target_value == "Canh"
    assert match.pillar == "day"
    assert match.location == "stem"


def test_nguyet_duc_alias_not_double_published() -> None:
    """Nguyệt Đức is an alias of Nguyệt Đức Quý Nhân."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Tý",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Hợi",
        stems=["Giáp", "Ất", "Canh", "Bính"],
        branches=["Tý", "Sửu", "Ngọ", "Hợi"],
    )
    names = result.canonical_names()
    assert NAME_YUE_DE in names
    assert ALIAS_YUE_DE not in names
    match = _match(result, ID_YUE_DE)
    assert match is not None
    assert match.source_type == "month_branch"
    assert match.target_value == "Canh"


def test_hong_luan_independent_dan_suu() -> None:
    """Niên chi Dần → Hồng Loan target Sửu, without Thiên Hỷ."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Dần",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Dần",
        stems=["Bính", "Tân", "Canh", "Mậu"],
        branches=["Dần", "Sửu", "Ngọ", "Dần"],
    )
    assert _match(result, ID_HONG_LUAN) is not None
    assert _match(result, ID_TIAN_XI) is None
    hong = _match(result, ID_HONG_LUAN)
    assert hong.source_type == "year_branch"
    assert hong.source_value == "Dần"
    assert hong.target_value == "Sửu"
    assert hong.pillar == "month"


def test_thien_hy_independent_dan_mui() -> None:
    """Niên chi Dần → Thiên Hỷ target Mùi, without false Hồng Loan."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Dần",
        month_branch="Tý",
        day_branch="Ngọ",
        hour_branch="Mùi",
        stems=["Bính", "Tân", "Canh", "Mậu"],
        branches=["Dần", "Tý", "Ngọ", "Mùi"],
    )
    assert _match(result, ID_TIAN_XI) is not None
    assert _match(result, ID_HONG_LUAN) is None
    hy = _match(result, ID_TIAN_XI)
    assert hy.source_value == "Dần"
    assert hy.target_value == "Mùi"
    assert hy.pillar == "hour"


def test_dan_suu_without_mui_has_no_false_thien_hy() -> None:
    """Dần + Sửu without Mùi does not publish Thiên Hỷ."""
    result = _service().evaluate(
        day_master="Giáp",
        year_branch="Dần",
        month_branch="Sửu",
        day_branch="Tý",
        hour_branch="Hợi",
        stems=["Giáp", "Ất", "Bính", "Đinh"],
        branches=["Dần", "Sửu", "Tý", "Hợi"],
    )
    names = result.canonical_names()
    assert NAME_HONG_LUAN in names
    assert NAME_TIAN_XI not in names


def test_multiple_occurrences_preserved() -> None:
    """Same canonical ID at Year and Hour keeps both positions."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Sửu",
        month_branch="Tý",
        day_branch="Ngọ",
        hour_branch="Sửu",
        stems=["Giáp", "Ất", "Canh", "Bính"],
        branches=["Sửu", "Tý", "Ngọ", "Sửu"],
    )
    match = _match(result, ID_TIAN_YI)
    assert match is not None
    assert len(match.occurrences) == 2
    assert {item.pillar for item in match.occurrences} == {"year", "hour"}
    assert result.canonical_names().count(NAME_TIAN_YI) == 1
    assert "trụ Năm" in match.presence_label
    assert "trụ Giờ" in match.presence_label


def test_alias_same_id_is_one_logical_star() -> None:
    """Canonical ID + alias must not become two published stars."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Tý",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Hợi",
        stems=["Giáp", "Ất", "Canh", "Bính"],
        branches=["Tý", "Sửu", "Ngọ", "Hợi"],
    )
    ids = [item.id for item in result.matches]
    assert ids.count(ID_TIAN_YI) == 1
    assert ids.count(ID_TIAN_DE) == 1
    assert ids.count(ID_YUE_DE) == 1


def test_every_published_item_has_provenance() -> None:
    """Every match stores source, target, and at least one location."""
    result = _service().evaluate(
        day_master="Canh",
        year_branch="Dần",
        month_branch="Sửu",
        day_branch="Ngọ",
        hour_branch="Dần",
        stems=["Bính", "Tân", "Canh", "Mậu"],
        branches=["Dần", "Sửu", "Ngọ", "Dần"],
    )
    assert result.matches
    for match in result.matches:
        assert match.id
        assert match.canonical_name in PUBLISHED_NAMES
        assert match.source_type
        assert match.source_value
        assert match.target_value
        assert match.occurrences
        assert match.pillar
        assert match.location
        assert match.rule_source
        assert match.evidence_text
        assert "gặp" in match.evidence_text
        assert match.canonical_name not in (ALIAS_TIAN_YI, ALIAS_TIAN_DE, ALIAS_YUE_DE)


def test_case_0001_live_canonical_list() -> None:
    """Live CASE-0001: alias pairs collapse; Thiên Hỷ absent without Mùi."""
    chart = BaziEngine().build(1987, 1, 21, 4, 30)
    names = chart.shensha
    assert ALIAS_TIAN_YI not in names
    assert ALIAS_TIAN_DE not in names
    assert ALIAS_YUE_DE not in names
    assert NAME_TIAN_YI in names
    assert NAME_HONG_LUAN in names
    assert NAME_TIAN_DE in names
    assert NAME_YUE_DE in names
    assert NAME_TIAN_XI not in names
    result = chart.shensha_result
    assert result is not None
    tian_yi = _match(result, ID_TIAN_YI)
    hong = _match(result, ID_HONG_LUAN)
    tian_de = _match(result, ID_TIAN_DE)
    yue_de = _match(result, ID_YUE_DE)
    assert tian_yi is not None
    assert tian_yi.source_value == "Canh"
    assert tian_yi.target_value == "Sửu"
    assert tian_yi.pillar == "month"
    assert hong is not None
    assert hong.source_value == "Dần"
    assert hong.target_value == "Sửu"
    assert hong.pillar == "month"
    assert tian_de is not None
    assert tian_de.source_value == "Sửu"
    assert tian_de.target_value == "Canh"
    assert tian_de.pillar == "day"
    assert yue_de is not None
    assert yue_de.target_value == "Canh"


def test_portal_report_same_canonical_result() -> None:
    """API view names and Report items copy the same engine matches."""
    chart = BaziEngine().build(1987, 1, 21, 4, 30)
    view = build_bazi_view(chart)
    assert view.published_shensha_names() == chart.shensha
    assert [item.canonical_name for item in view.shensha_matches] == chart.shensha
    report = ReportInputV1Adapter().build(
        ReportInputV1Source(analysis=AnalysisResult(bazi=view), case_id="CASE-0001")
    )
    report_names = [item.name for item in report.shensha]
    assert report_names == chart.shensha
    for item in report.shensha:
        assert item.evidence
        assert item.evidence != item.name
        assert item.presence_label.startswith("Có")
        assert item.source_value
        assert item.target_value
        assert item.occurrences


def test_khong_vong_not_in_production_catalog() -> None:
    """Không Vong is not a production natal ShenSha in V1.0."""
    chart = BaziEngine().build(1987, 1, 21, 4, 30)
    assert "Không Vong" not in chart.shensha
    assert "Không Vong" not in PUBLISHED_NAMES
