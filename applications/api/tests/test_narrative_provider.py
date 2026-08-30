"""N-REL-01 Narrative provider flag and dual-store attach."""

from __future__ import annotations

from applications.api.services.narrative_v2_shadow import attach_narrative_v2_shadow
from applications.customer_portal.config import PortalSettings, _narrative_provider
from engines.narrative_v2.presentation import PRESENTATION_VERSION


def test_provider_flag_defaults_to_v2(monkeypatch: object) -> None:
    monkeypatch.delenv("NARRATIVE_PROVIDER", raising=False)
    assert _narrative_provider() == "v2"
    settings = PortalSettings()
    assert settings.narrative_provider == "v2"


def test_provider_flag_rollback_is_pack05(monkeypatch: object) -> None:
    monkeypatch.setenv("NARRATIVE_PROVIDER", "pack05")
    assert _narrative_provider() == "pack05"


def test_provider_flag_allows_auto(monkeypatch: object) -> None:
    monkeypatch.setenv("NARRATIVE_PROVIDER", "auto")
    assert _narrative_provider() == "auto"


def test_invalid_provider_falls_back_to_v2(monkeypatch: object) -> None:
    monkeypatch.setenv("NARRATIVE_PROVIDER", "retired")
    assert _narrative_provider() == "v2"


def test_attach_records_duration_and_version_without_replacing_pack05() -> None:
    envelope = attach_narrative_v2_shadow({"source": "canonical_analysis_placeholder"})
    assert envelope["status"] == "ok"
    assert envelope["replaces_pack05"] is False
    assert envelope["presentation_version"] == PRESENTATION_VERSION
    assert isinstance(envelope["runtime_ms"], int)
    assert envelope["runtime_ms"] >= 0
    assert envelope["presentation"]["metadata"]["version"] == PRESENTATION_VERSION
    assert envelope["error"] is None


def test_attach_failure_is_isolated(monkeypatch: object) -> None:
    monkeypatch.setattr(
        "applications.api.services.narrative_v2_shadow.NarrativeRuntime.run",
        lambda self, canonical: (_ for _ in ()).throw(RuntimeError("v2 exploded")),
    )
    envelope = attach_narrative_v2_shadow({"source": "canonical_analysis_placeholder"})
    assert envelope["status"] == "error"
    assert envelope["presentation"] is None
    assert envelope["replaces_pack05"] is False
    assert envelope["error"] == "shadow_runtime_failed"
    assert envelope["runtime_ms"] >= 0
