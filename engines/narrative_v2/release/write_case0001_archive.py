"""Write N-REL-03 CASE-0001 Pack05 archive artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from applications.api.services.narrative_production_export import export_production_json
from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.release import (
    EXPORT_SOURCE_V2,
    PACK05_CONTRACT,
    load_pack05_archive,
    resolve_production_provider,
    select_export_source,
)

OUT = REPO / "implementation" / "narrative_release" / "n_rel_03"


def _analyze_case0001() -> dict:
    request = CASE_0001_REQUEST
    return OrchestratorService().analyze(
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )


def main() -> None:
    """Verify CASE-0001 production V2, historical Pack05, comparison."""
    OUT.mkdir(parents=True, exist_ok=True)
    payload = _analyze_case0001()
    archive = load_pack05_archive(payload)
    production_provider = resolve_production_provider("pack05")
    export_source = select_export_source(payload, legacy=False)
    exported = export_production_json(payload)
    consulting = ""
    presentation = payload.get("narrative_v2_shadow", {}).get("presentation") or {}
    interpretation = presentation.get("interpretation") if isinstance(presentation, dict) else {}
    if isinstance(interpretation, dict):
        consulting = str(interpretation.get("consulting_flow") or "")
    comparison_pass = (
        archive.available
        and archive.contract == PACK05_CONTRACT
        and production_provider == "v2"
        and export_source == EXPORT_SOURCE_V2
        and bool(consulting)
        and exported.get("interpretation", {}).get("consulting_flow") == consulting
        and payload.get("narrative_v2_shadow", {}).get("replaces_pack05") is False
    )
    record = {
        "case_id": "CASE-0001",
        "production_provider": production_provider,
        "pack05_available": archive.available,
        "pack05_read_only": archive.read_only,
        "pack05_contract": archive.contract,
        "export_source": export_source,
        "replaces_pack05": payload.get("narrative_v2_shadow", {}).get("replaces_pack05"),
        "consulting_flow_present": bool(consulting),
        "comparison": "PASS" if comparison_pass else "FAIL",
    }
    (OUT / "case0001_archive.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "case0001_archive.md").write_text(_markdown(record, comparison_pass), encoding="utf-8")
    if not comparison_pass:
        raise SystemExit("CASE-0001 archive comparison FAIL")


def _markdown(record: dict, comparison_pass: bool) -> str:
    status = "PASS" if comparison_pass else "FAIL"
    return f"""# CASE-0001 Archive

Sprint: N-REL-03

Status: {status}

---

## Production

Provider: `{record["production_provider"]}`

Pack05 cannot be selected.

Narrative V2 is the only production provider.

---

## Historical Pack05

Available: `{record["pack05_available"]}`

Read only: `{record["pack05_read_only"]}`

Contract: `{record["pack05_contract"]}`

`replaces_pack05`: `{record["replaces_pack05"]}`

Pack05 was not deleted, overwritten, or migrated.

---

## Comparison

Studio / archive comparison: **{record["comparison"]}**

Export source: `{record["export_source"]}`

Consulting flow present: `{record["consulting_flow_present"]}`

Production renders Narrative V2.

Historical Pack05 remains in ResultStore / analyze payload.

---

## Rollback

Production rollback to Pack05 is removed.

Archive access remains via `PACK05_LEGACY`.
"""


if __name__ == "__main__":
    main()
