"""N. Template / presentation validation."""

from __future__ import annotations

from dataclasses import replace

import pytest

from engines.date_selection_report.exceptions import DateSelectionReportTemplateError
from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.tree import build_render_tree, create_render_context
from engines.date_selection_report.templates.package import (
    SECTION_TEMPLATES,
    load_date_selection_template_package,
)
from engines.date_selection_report.templates.validation import validate_render_tree
from engines.report_engine.models.foundation_models import PlaceholderModel


def test_template_package_reuses_pack05_placeholders() -> None:
    package = load_date_selection_template_package()
    assert package.template_id == "date_selection_report"
    assert package.theme_id == "bte.report.theme.v1"
    assert package.section_ids == (
        "header",
        "person",
        "search_period",
        "recommendations",
        "guidance",
        "footer",
    )
    assert "recommendation" in SECTION_TEMPLATES
    assert "compatible_hours" in SECTION_TEMPLATES
    assert "positive_times" in SECTION_TEMPLATES
    assert all(isinstance(item, PlaceholderModel) for item in package.placeholders)
    ids = {item.placeholder_id for item in package.placeholders}
    assert "person.full_name" in ids
    assert "recommendation.day_result" in ids
    assert "hour.branch" in ids


def test_valid_tree_passes_template_validation(
    presentation_model: DateSelectionReportModel,
) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    validate_render_tree(tree)


def test_unresolved_placeholder_fails(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    broken_search = replace(tree.search_period, explanation="{{person.full_name}}")
    broken = replace(tree, search_period=broken_search)
    with pytest.raises(DateSelectionReportTemplateError, match="unresolved placeholders"):
        validate_render_tree(broken)


def test_disallowed_positive_class_fails(presentation_model: DateSelectionReportModel) -> None:
    tree = build_render_tree(create_render_context(presentation_model))
    rec = tree.recommendations[0]
    groups = rec.positive_times.groups
    bad_group = replace(groups[0], label="Lưu Liên")
    bad_positive = replace(rec.positive_times, groups=(bad_group, *groups[1:]))
    bad_rec = replace(rec, positive_times=bad_positive)
    broken = replace(tree, recommendations=(bad_rec,))
    with pytest.raises(DateSelectionReportTemplateError, match="disallowed positive class"):
        validate_render_tree(broken)
