"""Baseline comparison primitives."""

from __future__ import annotations

from typing import Any


def _as_map(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {
        str(item.get(key)): item
        for item in items
        if isinstance(item, dict) and item.get(key) is not None
    }


def compare_mappings(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Compare two keyed dictionaries and classify added/removed/changed."""
    old_keys = set(old)
    new_keys = set(new)
    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    changed = sorted(
        key
        for key in sorted(old_keys & new_keys)
        if old[key] != new[key]
    )
    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged_count": len(old_keys & new_keys) - len(changed),
    }


def compare_registry_snapshots(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Detect registry inventory changes between baselines."""
    old_map = _as_map(old.get("registries", []), "registry_id")
    new_map = _as_map(new.get("registries", []), "registry_id")
    base = compare_mappings(old_map, new_map)
    detail = []
    for registry_id in base["changed"]:
        detail.append(
            {
                "registry_id": registry_id,
                "old_record_count": old_map[registry_id].get("record_count"),
                "new_record_count": new_map[registry_id].get("record_count"),
                "old_checksum": old_map[registry_id].get("checksum"),
                "new_checksum": new_map[registry_id].get("checksum"),
            }
        )
    return {**base, "changed_detail": detail}


def compare_ontology_snapshots(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Detect ontology class and type changes."""
    old_classes = _as_map(old.get("ontology_classes", []), "id")
    new_classes = _as_map(new.get("ontology_classes", []), "id")
    return {
        "classes": compare_mappings(old_classes, new_classes),
        "statistics_old": old.get("ontology_statistics", {}),
        "statistics_new": new.get("ontology_statistics", {}),
    }


def compare_dependency_snapshots(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Detect dependency graph changes."""
    old_edges = {
        item.get("edge_id"): item
        for item in old.get("academic_dependency_graph", {}).get("edges", [])
    }
    new_edges = {
        item.get("edge_id"): item
        for item in new.get("academic_dependency_graph", {}).get("edges", [])
    }
    return {
        "academic_edges": compare_mappings(old_edges, new_edges),
        "topological_order_changed": old.get("topological_order")
        != new.get("topological_order"),
        "load_order_changed": old.get("load_order") != new.get("load_order"),
        "cycles_old": old.get("cycle_detection", {}),
        "cycles_new": new.get("cycle_detection", {}),
    }


def compare_compiler_snapshots(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Detect compiler contract and pipeline changes."""
    old_contracts = {
        item.get("contract_id"): item for item in old.get("contracts", [])
    }
    new_contracts = {
        item.get("contract_id"): item for item in new.get("contracts", [])
    }
    return {
        "contracts": compare_mappings(old_contracts, new_contracts),
        "pipeline_changed": old.get("pipeline") != new.get("pipeline"),
        "stage_order_old": old.get("pipeline", {}).get("stage_order", []),
        "stage_order_new": new.get("pipeline", {}).get("stage_order", []),
    }


def compare_validation_snapshots(
    old: dict[str, Any],
    new: dict[str, Any],
) -> dict[str, Any]:
    """Detect validation rule changes."""
    old_rules = {
        item.get("code"): item for item in old.get("validation_rules", [])
    }
    new_rules = {
        item.get("code"): item for item in new.get("validation_rules", [])
    }
    return {
        "rules": compare_mappings(old_rules, new_rules),
        "coverage_old": old.get("coverage", {}),
        "coverage_new": new.get("coverage", {}),
    }
