"""Fixtures for Knowledge infrastructure tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from services.knowledge.knowledge_loader import KnowledgeLoader


def _record(
    knowledge_id: str,
    *,
    domain: str = "five_elements",
    category: str = "element",
    status: str = "draft",
    deps: list[dict[str, str]] | None = None,
    refs: list[dict[str, str]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "identity": {
            "knowledge_id": knowledge_id,
            "canonical_name": knowledge_id.lower(),
            "chinese": "测",
            "pinyin": "ce",
            "english_name": knowledge_id,
        },
        "classification": {
            "domain": domain,
            "category": category,
        },
        "definition": "Structural placeholder definition used only for infrastructure tests.",
        "characteristics": {"nature": "test"},
        "relationships": {
            "depends_on": deps or [],
        },
        "references": refs
        or [{"reference_id": "REF-000001", "title": "Test Source"}],
        "metadata": {
            "version": "1.0.0",
            "status": status,
            "schema_version": "1.0.0",
        },
        "validation": {
            "schema_valid": True,
            "reference_valid": True,
            "relationship_valid": True,
            "integrity_valid": True,
        },
        "revision_history": [
            {
                "version": "1.0.0",
                "date": "2026-07-30",
                "summary": "test fixture",
            }
        ],
    }
    if extra:
        payload.update(extra)
    return payload


@pytest.fixture
def schema_root(project_root: Path) -> Path:
    """Point at the real foundation schemas."""
    return project_root / "knowledge" / "schema"


@pytest.fixture
def canon_root(tmp_path: Path) -> Path:
    """Temporary canon with two valid five_element records."""
    domain = tmp_path / "01_five_elements"
    domain.mkdir(parents=True)
    wood = _record(
        "KNO-000001",
        extra={
            "identity": {
                "knowledge_id": "KNO-000001",
                "canonical_name": "Wood",
                "chinese": "木",
                "pinyin": "mu",
                "english_name": "Wood",
            },
            "correspondences": {"season": "spring", "direction": "east"},
            "relationships": {
                "depends_on": [],
                "generates": {
                    "knowledge_id": "KNO-000002",
                    "relationship_type": "generates",
                },
            },
        },
    )
    fire = _record(
        "KNO-000002",
        status="official",
        deps=[
            {
                "knowledge_id": "KNO-000001",
                "relationship_type": "depends_on",
            }
        ],
        extra={
            "identity": {
                "knowledge_id": "KNO-000002",
                "canonical_name": "Fire",
                "chinese": "火",
                "pinyin": "huo",
                "english_name": "Fire",
            },
            "correspondences": {"season": "summer", "direction": "south"},
        },
    )
    (domain / "wood.json").write_text(
        json.dumps(wood, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (domain / "fire.json").write_text(
        json.dumps(fire, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    # Pointer schema file should be ignored by record loader.
    (domain / "five_element.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$ref": "ignored-by-record-loader",
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


@pytest.fixture
def loader(project_root: Path, canon_root: Path, schema_root: Path) -> KnowledgeLoader:
    """Knowledge loader bound to temp canon + real schemas."""
    return KnowledgeLoader(
        project_root=project_root,
        canon_root=canon_root,
        schema_root=schema_root,
    )
