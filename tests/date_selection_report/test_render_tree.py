"""B, H, K, M, O. Render tree structure and immutability."""

from __future__ import annotations

from dataclasses import replace

import pytest

from engines.date_selection_report.exceptions import DateSelectionReportValidationError
from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.builders import EmptyRecommendationsSectionBuilder
from engines.date_selection_report.rendering.labels import (
    EMPTY_STATE_DORMANT,
    EMPTY_STATE_MESSAGE,
    FORBIDDEN_PUBLIC_TERMS,
    LABELS,
)
from engines.date_selection_report.rendering.tree import (
    build_render_tree,
    create_render_context,
)
from engines.date_selection_report.validators import validate_report_model


def test_render_tree_section_order(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    assert tree.section_order == (
        "header",
        "person",
        "search_period",
        "recommendations",
        "guidance",
        "footer",
    )
    payload = tree.to_dict()
    assert list(payload)[:4] == ["header", "person", "search_period", "recommendations"]


def test_header_and_footer(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    assert tree.header.title == "BÁO CÁO CHỌN NGÀY TỐT"
    assert tree.header.subtitle == "BTE Platform"
    assert tree.footer.generator == "BTE Platform"
    assert tree.footer.product == "Báo cáo chọn ngày tốt"
    assert tree.footer.report_version == "1.0"


def test_vietnamese_labels_present(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    blob = str(tree.to_dict())
    required = (
        "BÁO CÁO CHỌN NGÀY TỐT",
        "THÔNG TIN NGƯỜI XEM",
        "THÔNG TIN TÌM NGÀY TỐT",
        "CÁC NGÀY ĐỀ XUẤT",
        "Giờ phù hợp Nhóm Trạch của bạn",
        "Các thời điểm đẹp",
        "HƯỚNG DẪN THAM KHẢO",
    )
    for label in required:
        assert label in blob
    assert LABELS["section_recommendations"] == "CÁC NGÀY ĐỀ XUẤT"


def test_no_ket_qua_gio_or_english_algorithm_terms(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    blob = str(tree.to_dict())
    for term in FORBIDDEN_PUBLIC_TERMS:
        assert term not in blob


def test_report_model_unchanged_after_tree_build(
    presentation_model: DateSelectionReportModel,
) -> None:
    before = presentation_model.to_dict()
    tree = build_render_tree(create_render_context(presentation_model))
    after = presentation_model.to_dict()
    assert before == after
    assert tree.recommendations[0].rank == 1
    assert presentation_model.recommendations[0].cung == "Cấn"
    assert presentation_model.recommendations[0].cung_element == "Thổ"


def test_empty_state_is_dormant_under_p6_01(
    presentation_model: DateSelectionReportModel,
) -> None:
    empty = replace(presentation_model, recommendations=())
    with pytest.raises(DateSelectionReportValidationError, match="missing recommendations"):
        validate_report_model(empty)
    assert EMPTY_STATE_DORMANT is True
    node = EmptyRecommendationsSectionBuilder().build()
    assert node.message == EMPTY_STATE_MESSAGE
    assert node.message == "Không tìm thấy ngày phù hợp trong khoảng thời gian đã chọn."
