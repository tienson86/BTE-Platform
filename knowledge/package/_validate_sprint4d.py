"""Validate Sprint 4D knowledge/package specification suite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
UNITS = {
    "Pack",
    "Module",
    "Section",
    "Knowledge Record",
    "Release",
    "Version",
    "Compatibility",
}


def main() -> int:
    errors: list[str] = []
    if ROOT.name != "package":
        errors.append(f"WRONG_FOLDER {ROOT.name}")

    files = [
        "README.md",
        "pack.schema.json",
        "module.schema.json",
        "pack_registry.json",
        "module_registry.json",
        "package_layout.json",
        "package_lifecycle.json",
        "examples/pack_01_example.json",
        "examples/module_01_example.json",
    ]
    data: dict[str, object] = {}
    for name in files:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"MISSING {name}")
            print(f"MISSING {name}")
            continue
        if name.endswith(".json"):
            data[name] = json.loads(path.read_text(encoding="utf-8"))
            print(f"PARSE_OK {name}")
        else:
            data[name] = path.read_text(encoding="utf-8")
            print(f"EXISTS_OK {name}")

    pack_schema = data["pack.schema.json"]
    module_schema = data["module.schema.json"]
    assert isinstance(pack_schema, dict) and isinstance(module_schema, dict)
    Draft202012Validator.check_schema(pack_schema)
    Draft202012Validator.check_schema(module_schema)
    print("SCHEMA_OK pack.schema.json")
    print("SCHEMA_OK module.schema.json")

    pack_v = Draft202012Validator(pack_schema)
    mod_v = Draft202012Validator(module_schema)

    pack_reg = data["pack_registry.json"]
    assert isinstance(pack_reg, dict)
    for pack in pack_reg.get("packs", []):
        errs = sorted(pack_v.iter_errors(pack), key=lambda e: list(e.path))
        if errs:
            for err in errs:
                errors.append(
                    f"PACK_REG_FAIL {pack.get('pack_id')} {list(err.path)}: {err.message}"
                )
        else:
            print(f"PACK_REG_OK {pack.get('pack_id')}")

    mod_reg = data["module_registry.json"]
    assert isinstance(mod_reg, dict)
    for mod in mod_reg.get("modules", []):
        errs = sorted(mod_v.iter_errors(mod), key=lambda e: list(e.path))
        if errs:
            for err in errs:
                errors.append(
                    f"MOD_REG_FAIL {mod.get('module_id')} {list(err.path)}: {err.message}"
                )
        else:
            print(f"MOD_REG_OK {mod.get('module_id')}")

    pack_ex = data["examples/pack_01_example.json"]
    mod_ex = data["examples/module_01_example.json"]
    assert isinstance(pack_ex, dict) and isinstance(mod_ex, dict)
    for label, validator, inst in [
        ("pack_example", pack_v, pack_ex["instance"]),
        ("module_example", mod_v, mod_ex["instance"]),
    ]:
        errs = sorted(validator.iter_errors(inst), key=lambda e: list(e.path))
        if errs:
            for err in errs:
                errors.append(f"{label} {list(err.path)}: {err.message}")
        else:
            print(f"INSTANCE_OK {label}")

    layout = data["package_layout.json"]
    assert isinstance(layout, dict)
    units = {h.get("unit") for h in layout.get("hierarchy", [])}
    if units != UNITS:
        errors.append(f"LAYOUT_UNITS fail {sorted(units)}")
    else:
        print("LAYOUT_UNITS_OK")

    life = data["package_lifecycle.json"]
    assert isinstance(life, dict)
    states = [s.get("state") for s in life.get("states", [])]
    if "released" not in states or "planned" not in states:
        errors.append("LIFECYCLE_STATES incomplete")
    else:
        print("LIFECYCLE_OK")

    readme = str(data.get("README.md", ""))
    for unit in UNITS:
        if unit not in readme:
            errors.append(f"README_MISSING {unit}")
    if not any(e.startswith("README_MISSING") for e in errors):
        print("README_OK")

    # Cross-check: every pack.module_id exists in module registry
    mod_ids = {m["module_id"] for m in mod_reg.get("modules", [])}
    for pack in pack_reg.get("packs", []):
        if pack["module_id"] not in mod_ids:
            errors.append(f"ORPHAN_PACK_MODULE {pack['pack_id']}")
    if not any(e.startswith("ORPHAN") for e in errors):
        print("PACK_MODULE_LINK_OK")

    if errors:
        for err in errors:
            print(err)
        print(f"RESULT FAIL ({len(errors)})")
        return 1
    print("RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
