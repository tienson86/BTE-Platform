"""CK-01B Consulting Knowledge catalog tests. Catalog only. No matching runtime."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.consulting_knowledge import (
    CATALOG_ID,
    CATALOG_VERSION,
    CONSULTING_DOMAINS,
    CONSULTING_KNOWLEDGE_CATALOG,
    KNOWLEDGE_UNIT_FIELDS,
    ConsultingKnowledgeError,
    catalog_by_domain,
    consulting_knowledge_contract,
    get_catalog_unit,
    load_consulting_knowledge_catalog,
)

PACKAGE = Path(__file__).resolve().parents[2] / "engines" / "consulting_knowledge"
CATALOG_FILES = (PACKAGE / "catalog.py", PACKAGE / "loader.py")


def test_catalog_contract_is_store_only() -> None:
    """CK-01B freezes a catalog id. Matching runtime stays off."""
    contract = consulting_knowledge_contract()
    assert contract["catalog_id"] == CATALOG_ID
    assert contract["catalog_version"] == CATALOG_VERSION
    assert contract["matching_runtime"] is False
    assert contract["runtime"] is False
    assert contract["engine"] is False
    assert contract["llm"] is False


def test_catalog_covers_every_frozen_domain() -> None:
    """Every consulting domain has stored units. Order is domain order."""
    grouped = catalog_by_domain()
    assert tuple(grouped.keys()) == CONSULTING_DOMAINS
    for domain in CONSULTING_DOMAINS:
        assert grouped[domain], f"missing units for {domain}"
        assert all(unit.domain == domain for unit in grouped[domain])


def test_catalog_units_have_required_fields() -> None:
    """Each stored unit carries condition, scope, meaning, wording, actions, references."""
    units = load_consulting_knowledge_catalog()
    assert units == CONSULTING_KNOWLEDGE_CATALOG
    for unit in units:
        payload = unit.to_dict()
        for field in KNOWLEDGE_UNIT_FIELDS:
            assert payload[field], f"{unit.unit_id} missing {field}"
        assert unit.status == "complete"
        assert unit.customer_wording
        assert unit.recommended_actions
        assert unit.references
        assert unit.condition
        assert unit.applicable_scope.get("domain") == unit.domain


def test_catalog_unit_ids_are_unique_and_stable() -> None:
    """unit_id is the catalog key. Duplicate ids are invalid."""
    units = load_consulting_knowledge_catalog()
    ids = [unit.unit_id for unit in units]
    assert ids == [
        "ck-career-001",
        "ck-career-002",
        "ck-finance-001",
        "ck-finance-002",
        "ck-relationship-001",
        "ck-relationship-002",
        "ck-health-001",
        "ck-health-002",
        "ck-leadership-001",
        "ck-leadership-002",
        "ck-management-001",
        "ck-management-002",
        "ck-communication-001",
        "ck-communication-002",
        "ck-business-001",
        "ck-business-002",
        "ck-personality-001",
        "ck-personality-002",
        "ck-action-001",
        "ck-action-002",
        "ck-action-003",
        "ck-action-004",
    ]
    assert len(ids) == len(set(ids))
    assert get_catalog_unit("ck-career-001").domain == "career"
    with pytest.raises(ConsultingKnowledgeError):
        get_catalog_unit("ck-missing")


def test_catalog_load_is_deterministic() -> None:
    """Same catalog load returns the same ordered units."""
    first = load_consulting_knowledge_catalog()
    second = load_consulting_knowledge_catalog()
    assert [unit.unit_id for unit in first] == [unit.unit_id for unit in second]
    assert first[0].customer_wording == ("Ưu tiên dựng khung việc trước khi mở rộng.",)


def test_action_library_is_referenced_not_invented() -> None:
    """Domain units may point at action_library ids. They do not generate new actions."""
    actions = catalog_by_domain()["action_library"]
    action_ids = {unit.unit_id for unit in actions}
    assert action_ids == {
        "ck-action-001",
        "ck-action-002",
        "ck-action-003",
        "ck-action-004",
    }
    career = get_catalog_unit("ck-career-001")
    assert "consulting_knowledge.action_library.ck-action-001" in career.references
    assert career.recommended_actions == get_catalog_unit("ck-action-001").recommended_actions


def test_catalog_does_not_run_matching() -> None:
    """CK-01B is catalog only. Loader and catalog store must not match signals."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in CATALOG_FILES)
    assert "match_consulting_knowledge" not in joined
    assert "project_signals" not in joined
    assert "from engines.consulting_knowledge.matching" not in joined
    assert "def calculate(" not in joined
    assert "openai" not in joined.lower()
    assert "compose" not in joined.lower()


def test_catalog_does_not_import_engines_or_delivery() -> None:
    """Catalog store stays off Calendar, Identity runtime, Narrative, and Report."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in CATALOG_FILES)
    assert "from engines.calendar" not in joined
    assert "from engines.bazi" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.narrative_framework" not in joined
    assert "from engines.report_engine" not in joined
    assert "customer_portal" not in joined
