"""Validation snapshot generator."""

from __future__ import annotations

from collections import Counter
from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext


def generate_validation_snapshot(
    context: BuildContext,
    validation: dict[str, Any],
) -> dict[str, Any]:
    """Generate validation snapshot covering stages, rules, and coverage."""
    rules = validation.get("rules", [])
    severity_counter = Counter(
        str(rule.get("severity", "UNKNOWN")).upper() for rule in rules
    )
    validators = validation.get("validators", [])
    stages = validation.get("stages", [])

    covered_validators = [v for v in validators if v.get("rule_count", 0) > 0]
    coverage = {
        "validator_coverage_ratio": (
            round(len(covered_validators) / len(validators), 4)
            if validators
            else 1.0
        ),
        "validators_with_rules": len(covered_validators),
        "validators_total": len(validators),
        "rules_with_severity": sum(
            1 for rule in rules if rule.get("severity")
        ),
        "rules_total": len(rules),
    }

    return {
        "artifact": "validation_snapshot",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "validation_stages": stages,
        "validation_rules": [
            {
                "code": rule.get("code") or rule.get("rule_id"),
                "title": rule.get("title") or rule.get("statement", "")[:80],
                "severity": str(rule.get("severity", "")).upper(),
                "source_file": rule.get("source_file", ""),
            }
            for rule in rules
        ],
        "validators": validators,
        "coverage": coverage,
        "statistics": {
            **validation.get("statistics", {}),
            "severity_distribution": dict(sorted(severity_counter.items())),
        },
        "severity": {
            "levels": validation.get("severity_levels", []),
            "distribution": dict(sorted(severity_counter.items())),
        },
    }
