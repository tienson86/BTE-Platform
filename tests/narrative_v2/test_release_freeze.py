"""N-REL-04 Release Freeze tests. No new Runtime or Presentation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.certification.certification_result import (
    CERTIFICATION_VERSION,
    STATUS_CERTIFIED,
)
from engines.narrative_v2.export import PresentationExportLayer, presentation_from_mapping
from engines.narrative_v2.golden import GOLDEN_SCHEMA_VERSION, GoldenDataset
from engines.narrative_v2.golden.golden_case import STATUS_FROZEN
from engines.narrative_v2.language.language_asset_status import SENTENCE_LIBRARY_VERSION
from engines.narrative_v2.presentation.presentation_status import (
    NARRATIVE_VERSION,
    PRESENTATION_VERSION,
)
from engines.narrative_v2.release import (
    FREEZE_STATUS_FROZEN,
    FROZEN_SURFACES,
    HEALTH_FAIL,
    HEALTH_PASS,
    NARRATIVE_PRODUCTION_OFF,
    NARRATIVE_PRODUCTION_ON,
    NEXT_VERSION,
    PACK05_STATUS_ARCHIVED,
    RELEASE_VERSION,
    ReleaseFreeze,
    ReleaseFreezeError,
    ReleaseHistory,
    ReleaseMonitor,
    build_v1_manifest,
    evaluate_alerts,
    resolve_production_provider,
)
from engines.narrative_v2.runtime.narrative_runtime import RUNTIME_VERSION

REPO = Path(__file__).resolve().parents[2]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
CERT = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"
PORTAL_PROVIDER = (
    REPO / "applications" / "customer_portal" / "src" / "resultState" / "narrativeProvider.ts"
)


def _presentation() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def test_v1_manifest_records_official_versions() -> None:
    manifest = build_v1_manifest(release_date="2026-08-30T00:00:00+00:00")
    assert manifest.release_version == RELEASE_VERSION == "1.0"
    assert manifest.narrative_version == NARRATIVE_VERSION
    assert manifest.presentation_version == PRESENTATION_VERSION == "bte.presentation.v2.1"
    assert manifest.language_asset_version == SENTENCE_LIBRARY_VERSION
    assert manifest.golden_version == GOLDEN_SCHEMA_VERSION
    assert manifest.certification_version == CERTIFICATION_VERSION
    assert manifest.runtime_version == RUNTIME_VERSION
    assert manifest.pack05_status == PACK05_STATUS_ARCHIVED
    assert manifest.freeze_status == FREEZE_STATUS_FROZEN
    assert manifest.metadata["narrative_v2_production"] == NARRATIVE_PRODUCTION_ON
    assert manifest.metadata["pack05_production"] == NARRATIVE_PRODUCTION_OFF
    assert manifest.metadata["next_version_required"] == NEXT_VERSION
    assert tuple(manifest.metadata["frozen_surfaces"]) == FROZEN_SURFACES


def test_freeze_is_write_once(tmp_path: Path) -> None:
    freeze = ReleaseFreeze(tmp_path / "release_manifest_v1.json")
    first = freeze.write(build_v1_manifest(release_date="2026-08-30T00:00:00+00:00"))
    assert freeze.is_frozen() is True
    assert freeze.load().release_version == "1.0"
    with pytest.raises(ReleaseFreezeError):
        freeze.write(first)


def test_pack05_archived_production_is_v2() -> None:
    manifest = build_v1_manifest()
    assert manifest.pack05_status == "archived"
    assert resolve_production_provider("pack05") == "v2"
    source = PORTAL_PROVIDER.read_text(encoding="utf-8")
    assert 'NARRATIVE_PROVIDERS = ["v2"]' in source


def test_golden_case0001_is_release_baseline() -> None:
    golden = GoldenDataset()
    case = golden.get("CASE-0001")
    assert case is not None
    assert case.status == STATUS_FROZEN
    assert case.version == 1
    payload = _presentation()
    compared = golden.compare(case_id="CASE-0001", presentation=payload)
    assert compared["matched"] is True


def test_certification_case0001_is_certified_append_only() -> None:
    history = CertificationHistory(CERT)
    assert history.current_status("CASE-0001") == STATUS_CERTIFIED
    rows = history.list_for("CASE-0001")
    assert len(rows) >= 2
    assert rows[-1]["status"] == STATUS_CERTIFIED
    assert rows[-1]["certification_version"] == CERTIFICATION_VERSION
    original = CERT.read_text(encoding="utf-8")
    loaded = history.list_for("CASE-0001")
    assert json.dumps(loaded, ensure_ascii=False) in original or len(loaded) == len(rows)


def test_final_health_has_no_critical_alerts(tmp_path: Path) -> None:
    monitor = ReleaseMonitor(
        history=ReleaseHistory(tmp_path / "release_history.json"),
        certification=CertificationHistory(CERT),
    )
    snapshot = monitor.observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="v2",
        portal_selected="v2",
        case_id="CASE-0001",
    )
    assert snapshot.health.overall() == HEALTH_PASS
    assert snapshot.health.runtime_status == HEALTH_PASS
    assert snapshot.health.presentation_status == HEALTH_PASS
    assert snapshot.health.portal_status == HEALTH_PASS
    assert snapshot.health.export_status == HEALTH_PASS
    assert snapshot.health.golden_status == HEALTH_PASS
    assert snapshot.health.certification_status == HEALTH_PASS
    alerts = evaluate_alerts(snapshot.health)
    assert all(item.level != HEALTH_FAIL for item in alerts)
    assert snapshot.health.fallback_count == 0


def test_json_export_equals_presentation() -> None:
    payload = _presentation()
    exported = PresentationExportLayer().export_json(presentation_from_mapping(payload))
    assert exported.payload["metadata"]["version"] == PRESENTATION_VERSION
    assert exported.payload["interpretation"]["consulting_flow"]


def test_freeze_does_not_add_runtime_or_builder() -> None:
    freeze_src = (
        REPO / "engines" / "narrative_v2" / "release" / "release_freeze.py"
    ).read_text(encoding="utf-8")
    assert "NarrativeRuntime" not in freeze_src
    assert "PresentationBuilder" not in freeze_src
    assert "new Builder" not in freeze_src
