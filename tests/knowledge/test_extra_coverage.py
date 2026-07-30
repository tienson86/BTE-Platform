"""Extra coverage for Knowledge infrastructure edge paths."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.knowledge.exceptions import KnowledgeLoadError, KnowledgeSchemaError
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.record_loader import RecordLoader
from services.knowledge.reference_validator import ReferenceValidator
from services.knowledge.relationship_validator import RelationshipValidator
from services.knowledge.schema_loader import SchemaLoader


def test_schema_loader_missing(schema_root: Path) -> None:
    with pytest.raises(KnowledgeLoadError):
        SchemaLoader(schema_root).load_schema("nope.schema.json")


def test_schema_for_unknown_domain(schema_root: Path) -> None:
    with pytest.raises(KnowledgeSchemaError):
        SchemaLoader(schema_root).schema_for_domain("99_unknown")


def test_invalid_record_json(canon_root: Path) -> None:
    bad = canon_root / "01_five_elements" / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(KnowledgeLoadError):
        RecordLoader(canon_root).load_record(bad)


def test_reference_and_relationship_edge_cases(loader: KnowledgeLoader) -> None:
    records = loader.load_records()
    wood = next(item for item in records if item.knowledge_id == "KNO-000001")
    wood.data["references"] = [
        {"reference_id": "REF-1", "title": "A"},
        {"reference_id": "REF-1", "title": "B"},
        "bad",
    ]
    wood.data["relationships"]["related_to"] = "bad"
    ref_issues = ReferenceValidator().validate(records)
    rel_issues = RelationshipValidator().validate(records)
    assert any(issue.code == "duplicate_reference_id" for issue in ref_issues)
    assert any(issue.code == "invalid_reference_item" for issue in ref_issues)
    assert any(issue.code == "invalid_relationship_value" for issue in rel_issues)


def test_loader_from_defaults(project_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(project_root)
    loader = KnowledgeLoader()
    assert loader.stats().schema_count >= 20


def test_circular_depends(loader: KnowledgeLoader, canon_root: Path) -> None:
    wood = canon_root / "01_five_elements" / "wood.json"
    fire = canon_root / "01_five_elements" / "fire.json"
    w = json.loads(wood.read_text(encoding="utf-8"))
    f = json.loads(fire.read_text(encoding="utf-8"))
    w["relationships"]["depends_on"] = [
        {"knowledge_id": "KNO-000002", "relationship_type": "depends_on"}
    ]
    f["relationships"]["depends_on"] = [
        {"knowledge_id": "KNO-000001", "relationship_type": "depends_on"}
    ]
    wood.write_text(json.dumps(w), encoding="utf-8")
    fire.write_text(json.dumps(f), encoding="utf-8")
    loader.clear_cache()
    issues = RelationshipValidator().validate(loader.load_records())
    assert any(issue.code == "circular_relationship" for issue in issues)
