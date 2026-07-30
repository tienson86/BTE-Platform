"""Pytest fixtures for Registry infrastructure tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from services.registry_loader import RegistryLoader


def _valid_record(
    registry_id: str,
    object_id: str,
    *,
    namespace: str = "knowledge",
    status: str = "draft",
    uri: str | None = None,
    deps: list[str] | None = None,
    domain: str = "five_elements",
    category: str = "basic",
    object_type: str = "knowledge_asset",
) -> dict[str, Any]:
    return {
        "identity": {
            "registry_id": registry_id,
            "object_id": object_id,
            "namespace": namespace,
        },
        "metadata": {
            "version": "1.0.0",
            "status": status,
            "owner": "Knowledge Team",
            "created_date": "2026-07-30",
            "updated_date": "2026-07-30",
        },
        "object": {
            "canonical_name": object_id.lower(),
            "object_type": object_type,
            "uri": uri or f"bte://knowledge/{object_id}",
            "path": f"knowledge/knowledge_canon/{object_id}.md",
            "checksum": "",
        },
        "classification": {
            "domain": domain,
            "category": category,
            "tags": ["test"],
        },
        "dependencies": deps or [],
        "validation": {
            "schema_valid": True,
            "dependency_valid": True,
            "checksum_valid": True,
        },
        "governance": {
            "reviewer": "Reviewer",
            "approval_status": "pending",
            "next_review": "",
        },
        "traceability": {
            "trace_id": "TRACE-000001",
            "audit_id": "AUD-000001",
        },
        "revision_history": [
            {
                "version": "1.0.0",
                "date": "2026-07-30",
                "summary": "initial",
            }
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


@pytest.fixture
def registry_root(tmp_path: Path, project_root: Path) -> Path:
    """Create a minimal registry tree with schemas and one catalog."""
    root = tmp_path / "registry"
    schema_src = (
        project_root
        / "knowledge"
        / "registry"
        / "schemas"
        / "registry_record.schema.json"
    )
    container_src = (
        project_root
        / "knowledge"
        / "registry"
        / "schemas"
        / "registry_container.schema.json"
    )
    schemas = root / "schemas"
    schemas.mkdir(parents=True)
    schemas.joinpath("registry_record.schema.json").write_text(
        schema_src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    schemas.joinpath("registry_container.schema.json").write_text(
        container_src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    _write_json(
        root / "global_registry" / "namespace_registry.json",
        {
            "version": "1.0.0",
            "records": [
                {"namespace": "knowledge", "prefix": "KREG"},
                {"namespace": "rule", "prefix": "RREG"},
            ],
        },
    )
    _write_json(
        root / "global_registry" / "object_type_registry.json",
        {
            "version": "1.0.0",
            "records": [
                {"object_type": "knowledge_asset", "namespace": "knowledge"},
                {"object_type": "rule", "namespace": "rule"},
            ],
        },
    )
    _write_json(
        root / "global_registry" / "registry_index.json",
        {
            "version": "1.0.0",
            "index_name": "registry_index",
            "entries": [
                {
                    "registry_name": "knowledge_registry",
                    "prefix": "KREG",
                    "path": "knowledge_registry/knowledge_registry.json",
                    "status": "framework",
                },
                {
                    "registry_name": "rule_registry",
                    "prefix": "RREG",
                    "path": "rule_registry/rule_registry.json",
                    "status": "framework",
                },
            ],
        },
    )
    _write_json(
        root / "global_registry" / "registry_statistics.json",
        {
            "version": "1.0.0",
            "generated_at": "",
            "statistics": {
                "total_records": 0,
                "by_registry": {},
                "by_status": {},
                "by_namespace": {},
            },
        },
    )
    _write_json(
        root / "knowledge_registry" / "knowledge_registry.json",
        {
            "version": "1.0.0",
            "registry_name": "knowledge_registry",
            "registry_prefix": "KREG",
            "description": "test knowledge",
            "schema": "../schemas/registry_record.schema.json",
            "records": [
                _valid_record("KREG-000001", "KNO-000001", status="published"),
                _valid_record(
                    "KREG-000002",
                    "KNO-000002",
                    status="draft",
                    deps=["KREG-000001"],
                    domain="patterns",
                    category="special",
                ),
            ],
        },
    )
    _write_json(
        root / "rule_registry" / "rule_registry.json",
        {
            "version": "1.0.0",
            "registry_name": "rule_registry",
            "registry_prefix": "RREG",
            "description": "test rules",
            "schema": "../schemas/registry_record.schema.json",
            "records": [
                _valid_record(
                    "RREG-000001",
                    "RUL-000001",
                    namespace="rule",
                    status="registered",
                    uri="bte://rule/RUL-000001",
                    deps=["KREG-000001"],
                    object_type="rule",
                ),
            ],
        },
    )
    _write_json(
        root / "samples" / "empty_registry_record.json",
        {
            "identity": {"registry_id": "", "object_id": "", "namespace": ""},
            "metadata": {
                "version": "1.0.0",
                "status": "draft",
                "owner": "",
                "created_date": "",
                "updated_date": "",
            },
            "object": {
                "canonical_name": "",
                "object_type": "",
                "uri": "",
                "path": "",
                "checksum": "",
            },
            "classification": {"domain": "", "category": "", "tags": []},
            "dependencies": [],
            "validation": {
                "schema_valid": False,
                "dependency_valid": False,
                "checksum_valid": False,
            },
            "governance": {
                "reviewer": "",
                "approval_status": "",
                "next_review": "",
            },
            "traceability": {"trace_id": "", "audit_id": ""},
            "revision_history": [],
        },
    )
    return root


@pytest.fixture
def loader(registry_root: Path) -> RegistryLoader:
    """Registry loader bound to the temporary registry root."""
    return RegistryLoader(registry_root=registry_root)
