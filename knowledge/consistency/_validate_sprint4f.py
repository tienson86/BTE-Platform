"""Validate Sprint 4F knowledge/consistency specification suite."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMENSIONS = {
    "canonical_definition_uniqueness",
    "terminology_consistency",
    "ontology_consistency",
    "relationship_consistency",
    "cross_references",
    "dependency_integrity",
    "duplicate_definitions",
    "contradictions",
}
FILES = [
    "README.md",
    "consistency_rules.json",
    "cross_record_validation.json",
    "terminology_consistency.json",
    "ontology_consistency.json",
    "relationship_consistency.json",
    "canonical_definition_rules.json",
    "CONSISTENCY_REPORT.md",
    "examples/consistency_findings_example.json",
]


def main() -> int:
    errors: list[str] = []
    if ROOT.name != "consistency":
        errors.append(f"WRONG_FOLDER {ROOT.name}")

    data: dict[str, object] = {}
    for name in FILES:
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

    rules = data.get("consistency_rules.json")
    assert isinstance(rules, dict)
    dims = set(rules.get("dimensions", []))
    if dims != DIMENSIONS:
        errors.append(f"DIMS fail {sorted(dims)}")
    else:
        print("DIMENSIONS_OK")
    rule_dims = {r.get("dimension") for r in rules.get("rules", [])}
    if rule_dims != DIMENSIONS:
        errors.append(f"RULE_DIM_COVERAGE fail {sorted(rule_dims)}")
    else:
        print("RULE_DIM_COVERAGE_OK")
    if len(rules.get("rules", [])) < 15:
        errors.append("CON_RULES_LT_15")
    else:
        print(f"CON_RULES_OK {len(rules['rules'])}")

    example = data.get("examples/consistency_findings_example.json")
    assert isinstance(example, dict)
    summary = example.get("summary", {})
    if set(summary.get("dimensions_covered", [])) != DIMENSIONS:
        errors.append("EXAMPLE_DIMS fail")
    else:
        print("EXAMPLE_DIMS_OK")
    if summary.get("errors") != 0:
        errors.append("EXAMPLE_ERRORS_NONZERO")
    else:
        print("EXAMPLE_ERRORS_OK")
    if summary.get("result") != "PASS_WITH_WARNINGS":
        errors.append("EXAMPLE_RESULT fail")
    else:
        print("EXAMPLE_RESULT_OK")

    report = str(data.get("CONSISTENCY_REPORT.md", ""))
    for needle in [
        "PASS",
        "Canonical Definition",
        "Terminology",
        "Ontology",
        "Relationship",
        "Cross reference",
        "Dependency",
        "Duplicate",
        "Contradiction",
    ]:
        if needle.lower() not in report.lower():
            errors.append(f"REPORT_MISSING {needle}")
    if "Overall Sprint 4F validation: PASS" not in report:
        errors.append("REPORT_PASS_LINE missing")
    if not any(e.startswith("REPORT_") for e in errors):
        print("REPORT_OK")

    readme = str(data.get("README.md", ""))
    for f in FILES[1:]:
        base = Path(f).name
        if base not in readme:
            errors.append(f"README_MISSING {base}")
    if not any(e.startswith("README_MISSING") for e in errors):
        print("README_OK")

    # ontology lists match expected sizes
    ont = data.get("ontology_consistency.json")
    assert isinstance(ont, dict)
    if len(ont.get("allowed_node_types", [])) != 8:
        errors.append("NODE_TYPES_NE_8")
    if len(ont.get("allowed_edge_types", [])) != 8:
        errors.append("EDGE_TYPES_NE_8")
    if not any(e.endswith("_NE_8") for e in errors):
        print("ONTOLOGY_ENUMS_OK")

    if errors:
        for err in errors:
            print(err)
        print(f"RESULT FAIL ({len(errors)})")
        return 1
    print("RESULT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
