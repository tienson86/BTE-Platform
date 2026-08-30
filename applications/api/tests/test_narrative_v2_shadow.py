"""Narrative V2 Portal shadow tests (N-IMP-10)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from applications.api.services.narrative_v2_shadow import attach_narrative_v2_shadow
from applications.api.services.orchestrator import OrchestratorService
from engines.narrative_engine import NarrativeEngine
from engines.narrative_v2.presentation import PRESENTATION_VERSION

FORBIDDEN = (
    "engines.calendar_engine",
    "engines.bazi_engine",
    "engines.score_engine",
)


def test_ps11_pack05_remains_on_analyze_payload(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        "applications.api.services.orchestrator._attach_narrative_v2_shadow",
        lambda _payload: {
            "status": "ok",
            "portal_connection": "true_shadow",
            "replaces_pack05": False,
            "presentation": {"metadata": {"version": PRESENTATION_VERSION}},
            "error": None,
        },
    )
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
    )
    assert payload["narrative_result"]["contract"] == "pack05_narrative_result_v1"
    assert payload["narrative_v2_shadow"]["replaces_pack05"] is False
    assert payload["narrative_v2_shadow"] is not payload["narrative_result"]


def test_ps12_v2_failure_does_not_break_analyze(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        "applications.api.services.narrative_v2_shadow.NarrativeRuntime.run",
        lambda self, canonical: (_ for _ in ()).throw(RuntimeError("v2 exploded")),
    )
    envelope = attach_narrative_v2_shadow({"source": "canonical_analysis_placeholder"})
    assert envelope["status"] == "error"
    assert envelope["presentation"] is None
    assert envelope["error"] == "shadow_runtime_failed"
    monkeypatch.setattr(
        "applications.api.services.orchestrator._attach_narrative_v2_shadow",
        lambda _payload: envelope,
    )
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
    )
    assert payload["narrative_result"]["contract"] == "pack05_narrative_result_v1"
    assert payload["narrative_v2_shadow"]["status"] == "error"


def test_ps15_store_layers_are_independent(monkeypatch: Any) -> None:
    monkeypatch.setattr(
        "applications.api.services.orchestrator._attach_narrative_v2_shadow",
        lambda _payload: {
            "status": "error",
            "presentation": None,
            "error": "shadow_runtime_failed",
            "replaces_pack05": False,
            "portal_connection": "true_shadow",
        },
    )
    payload = OrchestratorService().analyze(
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
    )
    pack05 = payload["narrative_result"]
    shadow = payload["narrative_v2_shadow"]
    assert pack05.get("sections")
    assert shadow["presentation"] is None
    assert pack05.get("contract") == "pack05_narrative_result_v1"


def test_runtime_portal_connection_is_true_shadow() -> None:
    from engines.narrative_v2.runtime import NarrativeRuntime

    result = NarrativeRuntime().run({"source": "canonical_analysis_placeholder"})
    assert result.runtime_metadata["portal_connected"] is False
    assert result.runtime_metadata["portal_connection"] == "true_shadow"
    assert result.runtime_metadata["replaces_pack05"] is False
    source = Path("applications/api/services/narrative_v2_shadow.py").read_text(encoding="utf-8")
    for name in FORBIDDEN:
        assert name not in source
    engine = Path("engines/narrative_engine/engine.py").read_text(encoding="utf-8")
    assert "class NarrativeEngine" in engine


def test_ps17_pdf_docx_untouched() -> None:
    assert NarrativeEngine is not None
    export = Path("applications/api/routes/export.py").read_text(encoding="utf-8")
    assert "narrative_v2" not in export


def test_shadow_presentation_from_case_0001_luck() -> None:
    canonical = OrchestratorService().run_stage(
        "luck",
        year=1987,
        month=1,
        day=21,
        hour=4,
        minute=30,
        gender="male",
        timezone="Asia/Bangkok",
    )
    envelope = attach_narrative_v2_shadow(canonical)
    assert envelope["status"] == "ok"
    presentation = envelope["presentation"]
    assert presentation["metadata"]["version"] == PRESENTATION_VERSION
    assert presentation["interpretation"]["consulting_flow"]
    assert presentation["commercial"] is None

