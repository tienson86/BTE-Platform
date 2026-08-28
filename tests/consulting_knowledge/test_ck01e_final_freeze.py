"""CK-01E Commercial Knowledge V1 freeze tests. Contract lock only. No rendering."""

from __future__ import annotations

from pathlib import Path

from engines.commercial_composer import (
    compose_commercial_consulting,
    compose_commercial_narrative,
)
from engines.consulting_knowledge import (
    CANONICAL_COMPOSER,
    CATALOG_ID,
    CK01_FROZEN,
    COMMERCIAL_KNOWLEDGE_ID,
    CONSULTING_DOMAINS,
    CONSULTING_KNOWLEDGE_CATALOG,
    FROZEN_CATALOG_UNIT_IDS,
    INT03_EDITORIAL_COMPOSER,
    RUNTIME_PATH,
    SECTION_OUTPUT_FIELDS,
    commercial_knowledge_freeze,
    load_consulting_knowledge_catalog,
)
from engines.report_engine.contracts.report_input_v1 import ReportInputV1

ROOT = Path(__file__).resolve().parents[2]
COMPOSER_DIR = ROOT / "engines" / "commercial_composer"


def test_commercial_knowledge_v1_is_frozen() -> None:
    """CK-01E locks the approved commercial knowledge contract."""
    freeze = commercial_knowledge_freeze()
    assert freeze["contract_id"] == COMMERCIAL_KNOWLEDGE_ID
    assert freeze["frozen"] is True
    assert CK01_FROZEN is True
    assert freeze["catalog_id"] == CATALOG_ID
    assert freeze["canonical_composer"] == CANONICAL_COMPOSER == "compose_commercial_consulting"
    assert freeze["int03_editorial_composer"] == INT03_EDITORIAL_COMPOSER
    assert freeze["canonical_matcher"] == "match_published_knowledge"
    assert freeze["runtime_path"] == list(RUNTIME_PATH)
    assert freeze["rendering"] == {"html": False, "pdf": False, "docx": False, "ui": False}
    assert freeze["llm"] is False
    assert freeze["recalculates"] is False
    assert freeze["engine"] is False


def test_frozen_catalog_ids_and_domains() -> None:
    """Catalog content and domain order stay on the freeze list."""
    units = load_consulting_knowledge_catalog()
    assert tuple(unit.unit_id for unit in units) == FROZEN_CATALOG_UNIT_IDS
    assert len(FROZEN_CATALOG_UNIT_IDS) == 22
    assert CONSULTING_DOMAINS == (
        "career",
        "finance",
        "relationship",
        "health",
        "leadership",
        "management",
        "communication",
        "business",
        "personality",
        "action_library",
    )
    assert CONSULTING_KNOWLEDGE_CATALOG[0].unit_id == "ck-career-001"


def test_two_composer_paths_remain_separate() -> None:
    """CK-01 consulting composer is not the INT-03 editorial composer."""
    assert compose_commercial_consulting is not compose_commercial_narrative
    assert CANONICAL_COMPOSER != INT03_EDITORIAL_COMPOSER
    compose_src = (COMPOSER_DIR / "consulting_compose.py").read_text(encoding="utf-8")
    narrative_src = (COMPOSER_DIR / "compose.py").read_text(encoding="utf-8")
    assert "def compose_commercial_consulting(" in compose_src
    assert "def compose_commercial_narrative(" in narrative_src
    assert "match_published_knowledge" not in compose_src
    assert "match_consulting_knowledge" not in compose_src


def test_section_output_fields_are_frozen() -> None:
    """Customer sections keep the freeze field set. No raw conditions."""
    assert SECTION_OUTPUT_FIELDS == (
        "domain",
        "title",
        "summary",
        "meaning",
        "recommendations",
        "references",
        "source_unit_ids",
    )
    from engines.commercial_composer.consulting_models import CommercialConsultingSection

    section = CommercialConsultingSection(
        domain="career",
        title="Sự nghiệp",
        summary="stored",
        meaning=("meaning",),
        recommendations=("action",),
        references=("ref",),
        source_unit_ids=("ck-career-001",),
    )
    payload = section.to_dict()
    assert tuple(payload) == SECTION_OUTPUT_FIELDS
    assert "condition" not in payload


def test_report_field_stays_optional() -> None:
    """commercial_consulting stays omitted from ReportInputV1 when unset."""
    assert "commercial_consulting" not in ReportInputV1().to_dict()


def test_publisher_calls_matcher_then_composer() -> None:
    """Orchestration layer owns matching. Composer remains a consumer."""
    publisher = (
        ROOT / "applications" / "api" / "services" / "consulting_commercial_publish.py"
    ).read_text(encoding="utf-8")
    body = publisher.split("def publish_commercial_consulting", 1)[1]
    matcher_at = body.index("match_published_knowledge")
    composer_at = body.index("compose_commercial_consulting")
    assert matcher_at < composer_at
    orchestrator = (ROOT / "applications" / "api" / "services" / "orchestrator.py").read_text(
        encoding="utf-8"
    )
    assert "publish_commercial_consulting" in orchestrator
    assert "payload[\"commercial_consulting\"]" in orchestrator


def test_freeze_module_does_not_import_engines_or_renderers() -> None:
    """Freeze surface is contract only."""
    freeze_src = (ROOT / "engines" / "consulting_knowledge" / "freeze.py").read_text(
        encoding="utf-8"
    )
    assert "from engines.calendar" not in freeze_src
    assert "from engines.bazi" not in freeze_src
    assert "from engines.report_engine" not in freeze_src
    assert "from engines.commercial_composer" not in freeze_src
    assert "def calculate(" not in freeze_src
    assert "openai" not in freeze_src.lower()
