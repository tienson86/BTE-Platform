"""Presentation/template validation for Date Selection render trees.

Does not repeat P6-01 analytical validation.
"""

from __future__ import annotations

import json
import re
from typing import Any

from engines.date_selection_report.exceptions import DateSelectionReportTemplateError
from engines.date_selection_report.rendering.labels import (
    FORBIDDEN_PUBLIC_TERMS,
    LABELS,
    POSITIVE_GROUP_ORDER,
)
from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree
from engines.date_selection_report.rendering.tokens import (
    DAY_PRESENTATION_ORDER,
    PERSON_FIELD_ORDER,
    SECTION_ORDER,
)
from engines.date_selection_report.templates.package import (
    REQUIRED_PLACEHOLDERS,
    load_date_selection_template_package,
)

_PLACEHOLDER_PATTERN = re.compile(r"\{\{[^}]+\}\}")


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        found: list[str] = []
        for item in value.values():
            found.extend(_walk_strings(item))
        return found
    if isinstance(value, (list, tuple)):
        found: list[str] = []
        for item in value:
            found.extend(_walk_strings(item))
        return found
    return []


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise DateSelectionReportTemplateError(message)


def validate_render_tree(tree: DateSelectionRenderTree) -> None:
    """Abort when required presentation nodes or placeholders are missing."""
    _require(tree.section_order == SECTION_ORDER, "invalid section order")
    _require(tree.header.section_id == "header", "missing header")
    _require(tree.person.section_id == "person", "missing person")
    _require(tree.search_period.section_id == "search_period", "missing search_period")
    _require(tree.guidance.section_id == "guidance", "missing guidance")
    _require(tree.footer.section_id == "footer", "missing footer")
    _require(bool(tree.header.title), "missing header title")
    _require(tree.header.title == LABELS["report_title"], "invalid header title")
    _require(bool(tree.recommendations_title), "missing recommendations title")
    _require(
        tree.recommendations_title == LABELS["section_recommendations"],
        "invalid recommendations title",
    )
    _validate_person(tree)
    _validate_search(tree)
    _validate_recommendations(tree)
    _validate_guidance(tree)
    _validate_footer(tree)
    _validate_placeholders_resolved(tree)
    _validate_forbidden_terms(tree)
    load_date_selection_template_package()


def _validate_person(tree: DateSelectionRenderTree) -> None:
    keys = tuple(row.key for row in tree.person.rows)
    _require(keys == PERSON_FIELD_ORDER, "person field order mismatch")
    for row in tree.person.rows:
        _require(bool(row.label and row.value), f"missing person.{row.key}")


def _validate_search(tree: DateSelectionRenderTree) -> None:
    search = tree.search_period
    _require(bool(search.month_display), "missing search_period.display")
    _require(bool(search.recommendation_count), "missing recommendation count")


def _validate_recommendations(tree: DateSelectionRenderTree) -> None:
    if not tree.recommendations:
        _require(tree.empty_state is not None, "missing empty-state node")
        _require(bool(tree.empty_state.message), "missing empty-state message")
        return
    _require(tree.empty_state is None, "empty-state must not accompany recommendations")
    for node in tree.recommendations:
        _require(
            node.presentation_field_keys() == DAY_PRESENTATION_ORDER,
            "recommendation day field order mismatch",
        )
        _require(bool(node.date_header.solar_date), "missing solar_date")
        _require(bool(node.date_header.lunar_date), "missing lunar_date")
        _require(bool(node.date_header.day_result), "missing day_result")
        _require(node.pagination.keep_together is True, "recommendation must keep_together")
        _require(
            node.pagination.do_not_split == ("date_header", "day_information"),
            "date header must stay with day information",
        )
        _require(bool(node.compatible_hours.rows), "missing compatible hours")
        for row in node.compatible_hours.rows:
            _require(bool(row.branch and row.time_range and row.cung_display), "incomplete hour")
            _require("hour_result" not in row.to_dict(), "hour_result is forbidden")
        _validate_positive_groups(node.positive_times.groups)


def _validate_positive_groups(groups: tuple[Any, ...]) -> None:
    labels = tuple(group.label for group in groups)
    allowed = set(POSITIVE_GROUP_ORDER)
    _require(all(label in allowed for label in labels), "disallowed positive class")
    expected = tuple(name for name in POSITIVE_GROUP_ORDER if name in labels)
    _require(labels == expected, "positive group order mismatch")
    for group in groups:
        _require(bool(group.items), "empty positive group must be omitted")


def _validate_guidance(tree: DateSelectionRenderTree) -> None:
    _require(bool(tree.guidance.items), "missing guidance items")
    _require(tree.guidance.title == LABELS["section_guidance"], "invalid guidance title")


def _validate_footer(tree: DateSelectionRenderTree) -> None:
    _require(bool(tree.footer.generator), "missing footer generator")
    _require(bool(tree.footer.report_version), "missing footer report_version")


def _validate_placeholders_resolved(tree: DateSelectionRenderTree) -> None:
    payload = tree.to_dict()
    text = json.dumps(payload, ensure_ascii=False)
    leftover = _PLACEHOLDER_PATTERN.findall(text)
    _require(not leftover, f"unresolved placeholders: {leftover}")
    _require(bool(REQUIRED_PLACEHOLDERS), "template placeholders missing")
    person_values = {row.key: row.value for row in tree.person.rows}
    _require(bool(person_values.get("full_name")), "unresolved {{person.full_name}}")
    if tree.recommendations:
        first = tree.recommendations[0]
        _require(bool(first.date_header.day_result), "unresolved {{recommendation.day_result}}")
        _require(
            bool(first.day_information.rows[2].value),
            "unresolved {{recommendation.day_ganzhi}}",
        )
        _require(bool(first.compatible_hours.rows[0].branch), "unresolved {{hour.branch}}")


def _validate_forbidden_terms(tree: DateSelectionRenderTree) -> None:
    blob = " ".join(_walk_strings(tree.to_dict()))
    for term in FORBIDDEN_PUBLIC_TERMS:
        _require(term not in blob, f"forbidden public term: {term}")
