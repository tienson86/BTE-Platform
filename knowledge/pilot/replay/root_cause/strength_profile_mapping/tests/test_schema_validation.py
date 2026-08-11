"""Schema validation tests for mapped profiles."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
EXAMPLES = ROOT / "examples"
MAPPED_SCHEMA = ROOT / "schemas" / "mapped_profile.schema.json"
DESIGN_SCHEMAS = ROOT.parents[0] / "strength_profile_design" / "schemas"


def _profile_validator():
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError:
        pytest.skip("jsonschema/referencing not installed")

    store = {p.name: json.loads(p.read_text(encoding="utf-8")) for p in DESIGN_SCHEMAS.glob("*.json")}
    resources = []
    for name, schema in store.items():
        resources.append((name, Resource.from_contents(schema, default_specification=DRAFT202012)))
        schema_id = schema.get("$id")
        if schema_id:
            resources.append(
                (schema_id, Resource.from_contents(schema, default_specification=DRAFT202012))
            )
    registry = Registry().with_resources(resources)
    return Draft202012Validator(store["strength_profile.schema.json"], registry=registry)


def _envelope_validator():
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        pytest.skip("jsonschema not installed")
    schema = json.loads(MAPPED_SCHEMA.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_all_results_validate_profile_and_envelope() -> None:
    pval = _profile_validator()
    eval_ = _envelope_validator()
    for path in sorted(RESULTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        eval_.validate(data)
        errors = sorted(pval.iter_errors(data["profile"]), key=lambda e: list(e.path))
        assert not errors, f"{path.name}: {errors[0].message}"


def test_examples_validate() -> None:
    pval = _profile_validator()
    eval_ = _envelope_validator()
    for path in EXAMPLES.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        eval_.validate(data)
        errors = sorted(pval.iter_errors(data["profile"]), key=lambda e: list(e.path))
        assert not errors, path.name
