#!/usr/bin/env python3
"""Validate Knowledge Schema Foundation (Draft 2020-12) with python-jsonschema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load_schemas() -> dict[str, Any]:
    """Load all schema documents keyed by $id and by filename."""
    store: dict[str, Any] = {}
    for path in sorted(ROOT.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema_id = str(schema.get("$id", path.name))
        store[schema_id] = schema
        store[path.name] = schema
        store[str(path.as_uri())] = schema
    return store


def detect_cycles(store: dict[str, Any]) -> list[str]:
    """Detect circular $ref chains across local schema files."""
    graph: dict[str, set[str]] = {}

    def walk(node: Any, current: str) -> None:
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and not ref.startswith("#"):
                target = ref.split("#", 1)[0]
                graph.setdefault(current, set()).add(target)
            for value in node.values():
                walk(value, current)
        elif isinstance(node, list):
            for item in node:
                walk(item, current)

    for path in ROOT.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        walk(schema, path.name)

    cycles: list[str] = []

    def dfs(node: str, stack: list[str]) -> None:
        if node in stack:
            cycles.append(" -> ".join(stack + [node]))
            return
        for nxt in sorted(graph.get(node, set())):
            dfs(nxt, stack + [node])

    for start in sorted(graph):
        dfs(start, [])
    return sorted(set(cycles))


def main() -> int:
    """Validate meta-schema compliance and sample instance checks."""
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
        from referencing import Registry, Resource
        from referencing.jsonschema import DRAFT202012
    except ImportError as exc:
        print(f"FAIL: missing dependency: {exc}")
        return 1

    store = load_schemas()
    resources = []
    for key, schema in store.items():
        if key.endswith(".schema.json") and "://" not in key and not key.startswith("file:"):
            # Prefer $id registration
            continue
        resources.append((key, Resource.from_contents(schema, default_specification=DRAFT202012)))

    # Register by $id and by bare filename for relative refs.
    registry = Registry()
    for path in sorted(ROOT.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        schema_id = str(schema["$id"])
        registry = registry.with_resource(schema_id, resource)
        registry = registry.with_resource(path.name, resource)

    errors: list[str] = []
    cycles = detect_cycles(store)
    if cycles:
        errors.extend(f"circular reference: {item}" for item in cycles)

    for path in sorted(ROOT.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"{path.name}: invalid Draft 2020-12 schema: {exc}")
            continue

        try:
            validator = Draft202012Validator(schema, registry=registry)
            # Structural compile/resolve check via empty aspirational instance handling
            list(validator.iter_errors({}))
        except Exception as exc:  # noqa: BLE001 - collect resolver failures
            errors.append(f"{path.name}: resolver/runtime error: {exc}")

    # Positive instance check against base + five_element
    sample = {
        "identity": {
            "knowledge_id": "KNO-000001",
            "canonical_name": "Wood",
            "chinese": "木",
            "pinyin": "mu",
            "english_name": "Wood",
        },
        "classification": {
            "domain": "five_elements",
            "category": "element",
        },
        "definition": "Structural placeholder definition for schema validation only.",
        "characteristics": {"nature": "growth"},
        "relationships": {},
        "references": [{"reference_id": "REF-000001", "title": "Placeholder Source"}],
        "metadata": {"version": "1.0.0", "status": "draft", "schema_version": "1.0.0"},
        "validation": {
            "schema_valid": True,
            "reference_valid": True,
            "relationship_valid": True,
            "integrity_valid": True,
        },
        "revision_history": [
            {"version": "1.0.0", "date": "2026-07-30", "summary": "schema foundation sample"}
        ],
        "correspondences": {"season": "spring", "direction": "east"},
    }
    five = json.loads((ROOT / "five_element.schema.json").read_text(encoding="utf-8"))
    five_validator = Draft202012Validator(five, registry=registry)
    sample_errors = sorted(five_validator.iter_errors(sample), key=lambda e: e.path)
    if sample_errors:
        for err in sample_errors:
            errors.append(f"five_element sample: {err.message}")

    if errors:
        print("SCHEMA VALIDATION FAILED")
        for item in errors:
            print(f" - {item}")
        return 1

    print("SCHEMA VALIDATION PASSED")
    print(f"schemas_checked={len(list(ROOT.glob('*.schema.json')))}")
    print("circular_references=0")
    print("draft=2020-12")
    print("engine=python-jsonschema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
