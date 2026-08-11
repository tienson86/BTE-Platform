"""Schema integrity tests for PILOT-1K."""

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
    "STRENGTH_OUTPUT_ENVELOPE.md",
    "STRENGTH_SCORE_OUTPUT.md",
    "STRENGTH_CONTRIBUTION_OUTPUT.md",
    "STRENGTH_SEASONAL_OUTPUT.md",
    "STRENGTH_ROOT_OUTPUT.md",
    "STRENGTH_SUPPORT_OUTPUT.md",
    "STRENGTH_PRESSURE_OUTPUT.md",
    "STRENGTH_DRAIN_OUTPUT.md",
    "STRENGTH_STRUCTURAL_OUTPUT.md",
    "STRENGTH_FOLLOW_PATTERN_OUTPUT.md",
    "STRENGTH_TEMPERATURE_OUTPUT.md",
    "STRENGTH_CONFLICT_OUTPUT.md",
    "STRENGTH_PROVENANCE_OUTPUT.md",
    "STRENGTH_COMPLETENESS_OUTPUT.md",
    "UNKNOWN_AND_MISSING_DATA_POLICY.md",
    "REQUIRED_OPTIONAL_RESERVED_MATRIX.md",
    "MINIMUM_STRENGTH_OUTPUT_CONTRACT.md",
    "V1_OUTPUT_GAP_ANALYSIS.md",
    "PROFILE_COMPATIBILITY.md",
    "SCORE_PROFILE_BOUNDARY.md",
    "FUTURE_ENGINE_COMPATIBILITY.md",
    "IMPLEMENTATION_GUARDRAILS.md",
    "PILOT_1K_SUMMARY.md",
]

SCHEMA_FILES = [
    "strength_output_envelope.schema.json",
    "strength_score_output.schema.json",
    "strength_evidence_output.schema.json",
    "strength_root_output.schema.json",
    "strength_structural_output.schema.json",
    "strength_conflict_output.schema.json",
    "strength_provenance_output.schema.json",
    "strength_completeness_output.schema.json",
]

HAN = re.compile(r"[\u3400-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]")


def _registry():
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError:
        pytest.skip("jsonschema/referencing not installed")

    store = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in SCHEMAS.glob("*.json")}
    resources = []
    for name, schema in store.items():
        resources.append((name, Resource.from_contents(schema, default_specification=DRAFT202012)))
        sid = schema.get("$id")
        if sid:
            resources.append((sid, Resource.from_contents(schema, default_specification=DRAFT202012)))
    return store, Registry().with_resources(resources), Draft202012Validator


def test_required_docs() -> None:
    for name in REQUIRED_MD:
        assert (ROOT / name).exists(), name


def test_schemas_parse() -> None:
    for name in SCHEMA_FILES:
        data = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
        assert data["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_examples_validate() -> None:
    store, registry, Draft202012Validator = _registry()
    mapping = {
        "minimum_output.json": "strength_output_envelope.schema.json",
        "saturated_score_output.json": "strength_output_envelope.schema.json",
        "partial_output.json": "strength_output_envelope.schema.json",
        "unknown_output.json": "strength_output_envelope.schema.json",
        "root_output.json": "strength_root_output.schema.json",
        "structural_output.json": "strength_structural_output.schema.json",
    }
    for fname, sname in mapping.items():
        instance = json.loads((EXAMPLES / fname).read_text(encoding="utf-8"))
        validator = Draft202012Validator(store[sname], registry=registry)
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        assert not errors, f"{fname}: {errors[0].message}"


def test_no_han_in_json() -> None:
    for folder in (SCHEMAS, EXAMPLES, ROOT / "reports", VALIDATION):
        for path in folder.glob("*.json"):
            assert HAN.search(path.read_text(encoding="utf-8")) is None, path.name


def test_summary() -> None:
    text = (ROOT / "PILOT_1K_SUMMARY.md").read_text(encoding="utf-8")
    assert "MINIMUM_CONTRACT_DEFINED: YES" in text
    assert "TAXONOMY_V2_IMPLEMENTED: NO" in text
    assert "Final Decision:\nDESIGN_COMPLETE" in text
