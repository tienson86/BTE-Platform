"""CK-01D commercial consulting composer tests. Composer consumes matched units."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from engines.commercial_composer import (
    CommercialComposerInput,
    compose_commercial_consulting,
    stable_unique,
)
from engines.consulting_knowledge import (
    CONSULTING_KNOWLEDGE_CATALOG,
    get_catalog_unit,
    load_consulting_knowledge_catalog,
)
from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.contracts.report_input_v1 import ReportInputV1

COMPOSER_DIR = Path(__file__).resolve().parents[2] / "engines" / "commercial_composer"
CONSULTING_COMPOSE = COMPOSER_DIR / "consulting_compose.py"
CONSULTING_MODELS = COMPOSER_DIR / "consulting_models.py"


def _career_units():
    return (
        get_catalog_unit("ck-career-001"),
        get_catalog_unit("ck-career-002"),
    )


def test_d1_composer_accepts_matched_units() -> None:
    """Valid matched units produce a CommercialComposerResult."""
    result = compose_commercial_consulting(
        CommercialComposerInput(matched_units=(get_catalog_unit("ck-career-001"),))
    )
    assert result.status == "complete"
    assert len(result.sections) == 1
    assert result.sections[0].domain == "career"
    assert result.sections[0].title == "Sự nghiệp"
    assert "Ưu tiên dựng khung việc" in result.sections[0].summary


def test_d2_domain_grouping() -> None:
    """Several units in one domain become one commercial section."""
    result = compose_commercial_consulting(matched_units=_career_units())
    assert len(result.sections) == 1
    section = result.sections[0]
    assert section.domain == "career"
    assert section.source_unit_ids == ("ck-career-001", "ck-career-002")


def test_d3_deterministic_order() -> None:
    """Compose repeatedly with the same matched set. Results stay identical."""
    payload = CommercialComposerInput(
        matched_units=(
            get_catalog_unit("ck-career-001"),
            get_catalog_unit("ck-finance-001"),
        )
    )
    first = compose_commercial_consulting(payload)
    second = compose_commercial_consulting(payload)
    assert first.to_dict() == second.to_dict()
    assert tuple(section.domain for section in first.sections) == ("career", "finance")


def test_d4_stable_deduplication() -> None:
    """Exact duplicate actions and references collapse to first occurrence."""
    first = get_catalog_unit("ck-career-001")
    duplicate = replace(
        get_catalog_unit("ck-career-002"),
        recommended_actions=first.recommended_actions,
        references=first.references,
    )
    result = compose_commercial_consulting(matched_units=(first, duplicate))
    section = result.sections[0]
    assert section.recommendations == first.recommended_actions
    assert section.references == first.references
    assert stable_unique(("a", "a", "b", "a")) == ("a", "b")


def test_d5_traceability() -> None:
    """Every published section cites non-empty source_unit_ids."""
    result = compose_commercial_consulting(
        matched_units=(
            get_catalog_unit("ck-career-001"),
            get_catalog_unit("ck-leadership-001"),
        )
    )
    assert result.sections
    for section in result.sections:
        assert section.source_unit_ids
        payload = section.to_dict()
        assert payload["source_unit_ids"]
        assert "condition" not in payload


def test_d6_unmatched_knowledge_is_empty() -> None:
    """No matched units produce an empty result. No invented advice."""
    result = compose_commercial_consulting(CommercialComposerInput(matched_units=()))
    assert result.status == "insufficient"
    assert result.sections == ()
    assert result.to_dict()["sections"] == []


def test_d7_composer_does_not_rematch() -> None:
    """Composer source does not call the matcher."""
    joined = CONSULTING_COMPOSE.read_text(encoding="utf-8") + CONSULTING_MODELS.read_text(
        encoding="utf-8"
    )
    assert "match_consulting_knowledge" not in joined
    assert "match_published_knowledge" not in joined
    assert "project_signals" not in joined
    assert "load_consulting_knowledge_catalog" not in joined
    compose_commercial_consulting(matched_units=(get_catalog_unit("ck-career-001"),))


def test_d8_compose_does_not_mutate_catalog() -> None:
    """Compose leaves frozen catalog units unchanged."""
    before = tuple(
        (unit.unit_id, unit.customer_wording, unit.recommended_actions)
        for unit in CONSULTING_KNOWLEDGE_CATALOG
    )
    compose_commercial_consulting(matched_units=load_consulting_knowledge_catalog()[:2])
    after = tuple(
        (unit.unit_id, unit.customer_wording, unit.recommended_actions)
        for unit in CONSULTING_KNOWLEDGE_CATALOG
    )
    assert before == after
    assert CONSULTING_KNOWLEDGE_CATALOG[0].unit_id == "ck-career-001"


def test_d9_report_adapter_accepts_composer_result() -> None:
    """CommercialComposerResult is copied onto ReportInputV1 without rendering HTML."""
    result = compose_commercial_consulting(
        matched_units=(get_catalog_unit("ck-career-001"),)
    )
    report_input = ReportInputV1(commercial_consulting=result.to_dict())
    payload = report_input.to_dict()
    assert payload["commercial_consulting"]["sections"][0]["source_unit_ids"] == [
        "ck-career-001"
    ]
    omitted = ReportInputV1()
    assert "commercial_consulting" not in omitted.to_dict()

    class _Source:
        commercial_consulting = result.to_dict()

    copied = ReportInputV1Adapter._copy_commercial_consulting(_Source())  # type: ignore[arg-type]
    assert copied == result.to_dict()
