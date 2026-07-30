"""Unit tests for Knowledge Console validators, diff, and service."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.knowledge_console.api.diff import build_diff
from applications.knowledge_console.api.services import (
    KnowledgeEditorService,
    ValidationError,
    WorkflowError,
)
from applications.knowledge_console.api.store import AssetStore
from applications.knowledge_console.api.validators import validate_asset_payload


def test_validate_rule_requires_fields() -> None:
    issues = validate_asset_payload(
        asset_type="rule",
        title="x",
        content={"rule_id": "", "condition": "a", "action": "b"},
    )
    codes = {issue.code for issue in issues}
    assert "rule_missing_id" in codes


def test_validate_sentence_warning_on_unbalanced_placeholder() -> None:
    issues = validate_asset_payload(
        asset_type="sentence",
        title="Intro",
        content={
            "sentence_id": "s1",
            "template": "Hello {day_master",
        },
    )
    warnings = [i for i in issues if i.severity == "warning"]
    assert any(i.code == "sentence_unbalanced_placeholder" for i in warnings)


def test_validate_phrase_and_terminology_ok() -> None:
    phrase_issues = validate_asset_payload(
        asset_type="phrase",
        title="Open",
        content={"phrase_id": "p1", "text": "Hello"},
    )
    term_issues = validate_asset_payload(
        asset_type="terminology",
        title="Term",
        content={
            "term_id": "t1",
            "display_name": "Name",
            "domain": "pattern",
        },
    )
    assert not any(i.severity == "error" for i in phrase_issues)
    assert not any(i.severity == "error" for i in term_issues)


def test_build_diff_detects_add_and_remove() -> None:
    result = build_diff(
        asset_id="a1",
        from_version="0.1.0",
        to_version="0.1.1",
        from_content={"text": "one\ntwo"},
        to_content={"text": "one\nthree"},
    )
    kinds = {line.kind for line in result.lines}
    assert "add" in kinds
    assert "remove" in kinds


def test_service_create_rejects_invalid(tmp_path: Path) -> None:
    service = KnowledgeEditorService(AssetStore(tmp_path / "data"))
    with pytest.raises(ValidationError):
        service.create_asset(
            asset_type="rule",
            title="Bad",
            content={"rule_id": "r1"},
        )


def test_service_workflow_and_preview(tmp_path: Path) -> None:
    service = KnowledgeEditorService(AssetStore(tmp_path / "data"))
    created = service.create_asset(
        asset_type="phrase",
        title="Greeting",
        content={"phrase_id": "G1", "text": "Xin chào", "type": "opening"},
    )
    asset_id = created["asset_id"]
    preview = service.preview(asset_id)
    assert "Xin chào" in preview["preview_text"]

    validation = service.validate(asset_id)
    assert validation["valid"] is True

    submitted = service.transition(asset_id, action="submit", actor="editor")
    assert submitted["status"] == "review"

    with pytest.raises(WorkflowError):
        service.update_asset(asset_id, title="Nope")

    approved = service.transition(asset_id, action="approve", actor="reviewer")
    assert approved["status"] == "approved"

    released = service.transition(asset_id, action="release", actor="publisher")
    assert released["status"] == "released"
    assert len(released["versions"]) >= 2
    assert len(released["history"]) >= 3


def test_service_diff_and_history(tmp_path: Path) -> None:
    service = KnowledgeEditorService(AssetStore(tmp_path / "data"))
    created = service.create_asset(
        asset_type="sentence",
        title="Tpl",
        content={"sentence_id": "s1", "template": "A {x}"},
    )
    asset_id = created["asset_id"]
    updated = service.update_asset(
        asset_id,
        content={"sentence_id": "s1", "template": "B {x}"},
        note="Rewrite",
    )
    assert updated["version"] == "0.1.1"
    diff = service.diff(asset_id, from_version="0.1.0")
    assert diff["from_version"] == "0.1.0"
    assert any(line["kind"] != "equal" for line in diff["lines"])
    history = service.history(asset_id)
    assert history[0]["action"] == "updated"
