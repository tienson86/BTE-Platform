"""Unit tests for Knowledge validators."""

from __future__ import annotations

import json
from pathlib import Path

from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.knowledge_validator import KnowledgeValidator


def test_validate_all_ok(loader: KnowledgeLoader) -> None:
    result = KnowledgeValidator(loader).validate_all()
    assert result.ok, [issue.message for issue in result.errors]
    assert result.records_checked == 2
    assert result.schemas_checked >= 20


def test_duplicate_id(loader: KnowledgeLoader, canon_root: Path) -> None:
    path = canon_root / "01_five_elements" / "dup.json"
    payload = json.loads(
        (canon_root / "01_five_elements" / "wood.json").read_text(encoding="utf-8")
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader.clear_cache()
    result = KnowledgeValidator(loader).validate_all(check_schema=False)
    assert any(issue.code == "duplicate_knowledge_id" for issue in result.errors)


def test_broken_relationship(loader: KnowledgeLoader, canon_root: Path) -> None:
    path = canon_root / "01_five_elements" / "wood.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["relationships"]["depends_on"] = [
        {"knowledge_id": "KNO-999999", "relationship_type": "depends_on"}
    ]
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader.clear_cache()
    result = KnowledgeValidator(loader).validate_all(check_schema=False)
    assert any(issue.code == "broken_relationship" for issue in result.errors)


def test_missing_official_references(
    loader: KnowledgeLoader,
    canon_root: Path,
) -> None:
    path = canon_root / "01_five_elements" / "fire.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["references"] = []
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader.clear_cache()
    result = KnowledgeValidator(loader).validate_all(check_schema=False)
    assert any(issue.code == "missing_references" for issue in result.errors)


def test_domain_mismatch(loader: KnowledgeLoader, canon_root: Path) -> None:
    path = canon_root / "01_five_elements" / "wood.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["classification"]["domain"] = "ten_gods"
    path.write_text(json.dumps(payload), encoding="utf-8")
    loader.clear_cache()
    result = KnowledgeValidator(loader).validate_all(check_schema=False)
    assert any(issue.code == "domain_mismatch" for issue in result.errors)


def test_real_scaffold_foundation(
    project_root: Path,
) -> None:
    loader = KnowledgeLoader(project_root=project_root)
    result = KnowledgeValidator(loader).validate_all()
    assert result.ok
    assert result.records_checked == 0
    assert result.schemas_checked >= 20
