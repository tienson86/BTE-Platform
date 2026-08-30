"""Write N-REL-04 CASE-0001 freeze artifacts and V1.0 manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.export import PresentationExportLayer
from engines.narrative_v2.golden import GoldenDataset
from engines.narrative_v2.presentation import NarrativeV2Presentation, serialize_customer
from engines.narrative_v2.release import (
    HEALTH_FAIL,
    HEALTH_PASS,
    RELEASE_VERSION,
    ReleaseFreeze,
    ReleaseFreezeError,
    ReleaseHistory,
    ReleaseMonitor,
    build_v1_manifest,
    evaluate_alerts,
    resolve_production_provider,
)
from engines.narrative_v2.runtime import NarrativeRuntime

OUT = REPO / "implementation" / "narrative_release" / "n_rel_04"
CANONICAL = REPO / "implementation" / "narrative_release" / "release_manifest_v1.json"
CERT = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"


def _run_case0001() -> tuple[NarrativeV2Presentation, dict]:
    request = CASE_0001_REQUEST
    canonical = OrchestratorService().run_stage(
        "luck",
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )
    result = NarrativeRuntime().run(canonical)
    if not isinstance(result.presentation, NarrativeV2Presentation):
        raise RuntimeError("presentation_unavailable")
    return result.presentation, serialize_customer(result.presentation)


def _write_freeze() -> dict:
    freeze = ReleaseFreeze(CANONICAL)
    manifest = build_v1_manifest()
    try:
        recorded = freeze.write(manifest)
    except ReleaseFreezeError:
        recorded = freeze.load()
    return recorded.to_record()


def main() -> None:
    """Freeze V1.0 and verify CASE-0001 production baseline."""
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = _write_freeze()
    (OUT / "release_manifest_v1.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    history = ReleaseHistory(OUT / "release_history.json")
    if history.path.exists():
        history.path.unlink()
    monitor = ReleaseMonitor(
        history=history,
        certification=CertificationHistory(CERT),
    )
    presentation, payload = _run_case0001()
    snapshot = monitor.observe(
        presentation=presentation,
        runtime_ok=True,
        provider="v2",
        portal_selected=resolve_production_provider("pack05"),
        case_id="CASE-0001",
    )
    layer = PresentationExportLayer()
    json_export = layer.export_json(presentation)
    pdf = layer.export_pdf(presentation, OUT / "case0001.pdf")
    docx = layer.export_docx(presentation, OUT / "case0001.docx")
    golden = GoldenDataset().compare(case_id="CASE-0001", presentation=payload)
    cert_status = CertificationHistory(CERT).current_status("CASE-0001")
    alerts = evaluate_alerts(snapshot.health)
    critical = [item.to_record() for item in alerts if item.level == HEALTH_FAIL]
    checks = {
        "runtime": snapshot.health.runtime_status,
        "presentation": snapshot.health.presentation_status,
        "portal": snapshot.health.portal_status,
        "pdf": HEALTH_PASS if pdf.path and Path(pdf.path).is_file() else HEALTH_FAIL,
        "docx": HEALTH_PASS if docx.path and Path(docx.path).is_file() else HEALTH_FAIL,
        "json": HEALTH_PASS if json_export.payload.get("metadata") else HEALTH_FAIL,
        "golden": HEALTH_PASS if golden.get("matched") else HEALTH_FAIL,
        "certification": snapshot.health.certification_status,
        "monitoring": snapshot.health.overall(),
        "no_critical_alerts": HEALTH_PASS if not critical else HEALTH_FAIL,
    }
    all_pass = all(value == HEALTH_PASS for value in checks.values())
    health_record = snapshot.health.to_record()
    (OUT / "release_health_final.json").write_text(
        json.dumps(health_record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "case0001_final.json").write_text(
        json.dumps(
            {
                "case_id": "CASE-0001",
                "release_version": RELEASE_VERSION,
                "checks": checks,
                "certification_status": cert_status,
                "golden_matched": golden.get("matched"),
                "critical_alerts": critical,
                "overall": "PASS" if all_pass else "FAIL",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (OUT / "release_summary.md").write_text(_summary(manifest, checks, all_pass), encoding="utf-8")
    (OUT / "freeze_report.md").write_text(_freeze_report(manifest, checks, all_pass), encoding="utf-8")
    if not all_pass:
        raise SystemExit("CASE-0001 final verification FAIL")


def _summary(manifest: dict, checks: dict, all_pass: bool) -> str:
    status = "PASS" if all_pass else "FAIL"
    return f"""# Narrative V2 V1.0 Release Summary

Status: {status}

Release version: `{manifest["release_version"]}`

Presentation: `{manifest["presentation_version"]}`

Pack05: `{manifest["pack05_status"]}` (production OFF)

Narrative V2: production ON

Freeze: `{manifest["freeze_status"]}`

Next version required: `1.1`

## CASE-0001

| Surface | Status |
| --- | --- |
| Runtime | {checks["runtime"]} |
| Presentation | {checks["presentation"]} |
| Portal | {checks["portal"]} |
| PDF | {checks["pdf"]} |
| DOCX | {checks["docx"]} |
| JSON | {checks["json"]} |
| Golden | {checks["golden"]} |
| Certification | {checks["certification"]} |
| Monitoring | {checks["monitoring"]} |
| Critical alerts | {checks["no_critical_alerts"]} |
"""


def _freeze_report(manifest: dict, checks: dict, all_pass: bool) -> str:
    status = "FROZEN" if all_pass else "FAIL"
    surfaces = "\n".join(f"- {item}" for item in manifest["metadata"]["frozen_surfaces"])
    return f"""# Freeze Report

Sprint: N-REL-04

Status: {status}

Official release: Narrative V2 Version {manifest["release_version"]}

Presentation: {manifest["presentation_version"]}

Pack05: Legacy Archive, read only, production OFF

## Frozen surfaces

{surfaces}

## Rules

After Freeze:

- No Runtime edits
- No Presentation edits
- No Language Asset edits
- No Export edits
- No Release edits

Changes require Version 1.1.

## Specification freeze

- `knowledge/narrative_v2/` frozen
- `implementation/narrative_v2/` archived
- `implementation/narrative_release/` archived

Golden Dataset CASE-0001 v1 is the release baseline.

Certification history remains append-only.

EPIC Narrative V2 Release is closed.
"""


if __name__ == "__main__":
    main()
