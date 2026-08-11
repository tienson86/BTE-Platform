"""Schema integrity tests for PILOT-1I design package."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
VALIDATION = ROOT / "validation"

REQUIRED_MD = [
    "README.md",
    "STRENGTH_EVIDENCE_SCHEMA.md",
    "STRENGTH_EVIDENCE_VOCABULARY.md",
    "STRENGTH_PROFILE_SCHEMA.md",
    "STRENGTH_PROFILE_CONTRACT.md",
    "STRENGTH_CONFIDENCE_SCHEMA.md",
    "STRENGTH_PROVENANCE_MODEL.md",
    "STRENGTH_COMPLETENESS_MODEL.md",
    "STRENGTH_CONFLICT_MODEL.md",
    "STRENGTH_SCORE_REFERENCE.md",
    "STRENGTH_SATURATION_METADATA.md",
    "STRENGTH_ROOTING_MODEL.md",
    "STRENGTH_SUPPORT_MODEL.md",
    "STRENGTH_PRESSURE_MODEL.md",
    "STRENGTH_DRAIN_MODEL.md",
    "STRENGTH_SEASONAL_MODEL.md",
    "STRENGTH_STRUCTURAL_MODEL.md",
    "STRENGTH_TEMPERATURE_MODEL.md",
    "STRENGTH_EXPERT_COMPATIBILITY.md",
    "STRENGTH_SYNTHETIC_COMPATIBILITY.md",
    "V1_PROFILE_COMPATIBILITY.md",
    "PROFILE_TAXONOMY_BOUNDARY.md",
    "INFORMATION_LOSS_MODEL.md",
    "DESIGN_EXAMPLES.md",
    "IMPLEMENTATION_GUARDRAILS.md",
    "PILOT_1I_SUMMARY.md",
]

SCHEMA_FILES = [
    "strength_evidence.schema.json",
    "strength_profile.schema.json",
    "strength_confidence.schema.json",
    "strength_conflict.schema.json",
    "strength_completeness.schema.json",
    "strength_provenance.schema.json",
]

HAN_OR_CJK = re.compile(r"[\u3400-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")


def _load_schema_store() -> dict[str, dict]:
    store = {}
    for name in SCHEMA_FILES:
        store[name] = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return store


def _validator_for(schema_name: str):
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError:
        pytest.skip("jsonschema/referencing not installed")

    store = _load_schema_store()
    resources = []
    for name, schema in store.items():
        resources.append((name, Resource.from_contents(schema, default_specification=DRAFT202012)))
        # also register by $id if present
        schema_id = schema.get("$id")
        if schema_id:
            resources.append((schema_id, Resource.from_contents(schema, default_specification=DRAFT202012)))
    registry = Registry().with_resources(resources)
    return Draft202012Validator(store[schema_name], registry=registry)


def test_required_markdown_present() -> None:
    for name in REQUIRED_MD:
        assert (ROOT / name).exists(), name


def test_schemas_present_and_parse() -> None:
    for name in SCHEMA_FILES:
        data = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert "schema_version" in json.dumps(data) or "const" in json.dumps(data.get("properties", {}).get("schema_version", {}))


def test_examples_validate_against_profile_schema() -> None:
    validator = _validator_for("strength_profile.schema.json")
    for path in sorted(EXAMPLES.glob("*.json")):
        instance = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
        assert not errors, f"{path.name}: {[e.message for e in errors[:5]]}"


def test_no_han_in_machine_json() -> None:
    for folder in (SCHEMAS, EXAMPLES, ROOT / "reports", VALIDATION):
        for path in folder.glob("*.json"):
            text = path.read_text(encoding="utf-8")
            assert HAN_OR_CJK.search(text) is None, path.name


def test_summary_status_block() -> None:
    text = (ROOT / "PILOT_1I_SUMMARY.md").read_text(encoding="utf-8")
    assert "EVIDENCE_SCHEMA_DESIGNED: YES" in text
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "T1_T6_FROZEN: NO" in text
    assert "Final Decision:\nDESIGN_COMPLETE" in text


def test_validation_json() -> None:
    data = json.loads((VALIDATION / "VALIDATION.json").read_text(encoding="utf-8"))
    assert data["final_decision"] == "DESIGN_COMPLETE"
    assert data["taxonomy_v2_implemented"] is False
    assert data["production_code_changed"] is False
