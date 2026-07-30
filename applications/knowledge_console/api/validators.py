"""Validation rules for Knowledge Console assets."""

from __future__ import annotations

from typing import Any

from applications.knowledge_console.api.models import (
    ASSET_TYPES,
    KnowledgeAsset,
    ValidationIssue,
)


def validate_asset_payload(
    *,
    asset_type: str,
    title: str,
    content: dict[str, Any],
) -> list[ValidationIssue]:
    """Validate create/update payload before persistence."""
    issues: list[ValidationIssue] = []
    if asset_type not in ASSET_TYPES:
        issues.append(
            ValidationIssue(
                code="invalid_asset_type",
                severity="error",
                message=f"Unsupported asset_type: {asset_type}",
                path="asset_type",
            )
        )
    if not title or not title.strip():
        issues.append(
            ValidationIssue(
                code="missing_title",
                severity="error",
                message="title is required",
                path="title",
            )
        )
    if not isinstance(content, dict):
        issues.append(
            ValidationIssue(
                code="invalid_content",
                severity="error",
                message="content must be an object",
                path="content",
            )
        )
        return issues

    if asset_type == "rule":
        issues.extend(_validate_rule(content))
    elif asset_type == "sentence":
        issues.extend(_validate_sentence(content))
    elif asset_type == "phrase":
        issues.extend(_validate_phrase(content))
    elif asset_type == "terminology":
        issues.extend(_validate_terminology(content))
    return issues


def validate_asset(asset: KnowledgeAsset) -> list[ValidationIssue]:
    """Validate a persisted asset."""
    return validate_asset_payload(
        asset_type=asset.asset_type,
        title=asset.title,
        content=asset.content,
    )


def _require_str(
    content: dict[str, Any],
    key: str,
    *,
    code: str,
) -> list[ValidationIssue]:
    value = content.get(key)
    if not isinstance(value, str) or not value.strip():
        return [
            ValidationIssue(
                code=code,
                severity="error",
                message=f"content.{key} is required",
                path=f"content.{key}",
            )
        ]
    return []


def _validate_rule(content: dict[str, Any]) -> list[ValidationIssue]:
    issues = _require_str(content, "rule_id", code="rule_missing_id")
    issues.extend(_require_str(content, "condition", code="rule_missing_condition"))
    issues.extend(_require_str(content, "action", code="rule_missing_action"))
    priority = content.get("priority")
    if priority is not None and not isinstance(priority, int):
        issues.append(
            ValidationIssue(
                code="rule_invalid_priority",
                severity="error",
                message="content.priority must be an integer",
                path="content.priority",
            )
        )
    return issues


def _validate_sentence(content: dict[str, Any]) -> list[ValidationIssue]:
    issues = _require_str(content, "sentence_id", code="sentence_missing_id")
    issues.extend(_require_str(content, "template", code="sentence_missing_template"))
    template = content.get("template")
    if isinstance(template, str) and "{" in template and "}" not in template:
        issues.append(
            ValidationIssue(
                code="sentence_unbalanced_placeholder",
                severity="warning",
                message="template may contain unbalanced placeholder braces",
                path="content.template",
            )
        )
    return issues


def _validate_phrase(content: dict[str, Any]) -> list[ValidationIssue]:
    issues = _require_str(content, "phrase_id", code="phrase_missing_id")
    issues.extend(_require_str(content, "text", code="phrase_missing_text"))
    phrase_type = content.get("type")
    if phrase_type is not None and not isinstance(phrase_type, str):
        issues.append(
            ValidationIssue(
                code="phrase_invalid_type",
                severity="error",
                message="content.type must be a string",
                path="content.type",
            )
        )
    return issues


def _validate_terminology(content: dict[str, Any]) -> list[ValidationIssue]:
    issues = _require_str(content, "term_id", code="term_missing_id")
    issues.extend(
        _require_str(content, "display_name", code="term_missing_display_name")
    )
    issues.extend(_require_str(content, "domain", code="term_missing_domain"))
    return issues
