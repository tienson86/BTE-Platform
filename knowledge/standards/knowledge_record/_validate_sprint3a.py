"""Validate Sprint 3A knowledge_record schemas (Draft 2020-12)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent


def main() -> int:
    errors: list[str] = []
    schemas: dict[str, dict] = {}

    for path in sorted(ROOT.glob("*.schema.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.name] = data
        try:
            Draft202012Validator.check_schema(data)
            print(f"SCHEMA_OK {path.name}")
        except Exception as exc:  # noqa: BLE001 - report all schema failures
            msg = f"SCHEMA_FAIL {path.name}: {exc}"
            errors.append(msg)
            print(msg)

    resources: list[tuple[str, Resource]] = []
    for name, data in schemas.items():
        uri = data.get("$id", name)
        resource = Resource.from_contents(data)
        resources.append((uri, resource))
        resources.append((name, resource))

    registry = Registry().with_resources(resources)
    master = schemas["knowledge_record.schema.json"]
    instance = json.loads(
        (ROOT / "examples" / "kr_infrastructure_example.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(master, registry=registry)
    instance_errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if instance_errors:
        for err in instance_errors:
            msg = f"INSTANCE_FAIL path={list(err.path)}: {err.message}"
            errors.append(msg)
            print(msg)
    else:
        print("INSTANCE_OK examples/kr_infrastructure_example.json")

    validation_cfg = json.loads(
        (ROOT / "knowledge_record_validation.json").read_text(encoding="utf-8")
    )
    assert validation_cfg["draft"] == "2020-12"
    print("VALIDATION_CONFIG_OK")

    if errors:
        print(f"RESULT FAIL ({len(errors)})")
        return 1
    print("RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
