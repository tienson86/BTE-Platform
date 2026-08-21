"""G2-05 history snapshot probe. Copies stored analysis; no engine writes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT))

from applications.api.services.customer_export import (  # noqa: E402
    build_customer_export_filename,
    prepare_customer_report_input,
)
from applications.api.services.orchestrator import OrchestratorService  # noqa: E402
from applications.api.services.result_identity import stamp_customer_result_identity  # noqa: E402

from _g2_01_binding_probe import CASES, FROZEN, fingerprint  # noqa: E402

OUT = ROOT / "G2_05_HISTORY_PROBE.json"


def main() -> int:
    orch = OrchestratorService()
    rows: list[dict[str, object]] = []
    mismatch = 0
    frozen = json.loads(FROZEN.read_text(encoding="utf-8")) if FROZEN.is_file() else {}
    for index, spec in enumerate(CASES):
        name = str(spec["name"])
        kwargs = {key: value for key, value in spec.items() if key != "name"}
        live = stamp_customer_result_identity(orch.analyze(**kwargs), f"g2-05-{index}")
        stored = json.loads(json.dumps(live))
        live_fp = fingerprint(name, live)
        stored_fp = fingerprint(name, stored)
        report = prepare_customer_report_input(
            analysis_id=f"g2-05-{index}",
            source="history",
            data=stored,
            birth_input=spec,
        )
        filename = build_customer_export_filename(report, "pdf")
        analytical_match = live_fp == stored_fp
        if not analytical_match:
            mismatch += 1
        rows.append(
            {
                "name": name,
                "analysis_id": stored.get("analysis_id"),
                "created_at": (stored.get("result_meta") or {}).get("created_at"),
                "customer_contract": (stored.get("useful_god_source") or {}).get("contract"),
                "live": live_fp,
                "stored": stored_fp,
                "export_filename": filename,
                "export_case_id": report.metadata.case_id,
                "match": "MATCH" if analytical_match else "DIFF",
                "frozen_present": name in frozen,
            }
        )
    payload = {
        "mismatch_count": mismatch,
        "rows": rows,
        "policy": "History stores the Analyze snapshot. Opening it must not re-run engines.",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"G2-05 probe {len(rows)}/10 stored, mismatch_count {mismatch}")
    return 0 if mismatch == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
