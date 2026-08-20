"""Customer result identity / contract metadata. Presentation only — not an engine."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

CUSTOMER_USEFUL_GOD_CONTRACT = "analysis_result.UsefulGodView@1.5"
GATE_CORE_FREEZE = "G1"
MONTH_PILLAR_STANDARD = "BTE-MONTH-PILLAR-LUNAR-V1.0"
RELEASE_LABEL = "BTE V1.0 — Gate 1 Core Engine"


def stamp_customer_result_identity(
    payload: dict[str, Any],
    request_id: str | None,
) -> dict[str, Any]:
    """Attach canonical analysis ID and contract metadata to Analyze `data`.

    Does not change engine calculations. Copies the HTTP request_id so Portal
    ResultStore does not invent a second customer identity.
    """
    stamped = dict(payload)
    analysis_id = str(request_id or "").strip()
    if analysis_id:
        stamped["analysis_id"] = analysis_id
        stamped["request_id"] = analysis_id
    source = dict(stamped.get("useful_god_source") or {})
    contract = str(source.get("contract") or CUSTOMER_USEFUL_GOD_CONTRACT)
    source["contract"] = contract
    stamped["useful_god_source"] = source
    stamped["result_meta"] = {
        "analysis_id": analysis_id or None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "customer_contract": contract,
        "gate_core_freeze": GATE_CORE_FREEZE,
        "month_pillar_standard": MONTH_PILLAR_STANDARD,
        "release_label": RELEASE_LABEL,
    }
    narrative = stamped.get("narrative_result")
    if isinstance(narrative, dict) and analysis_id:
        narrative = dict(narrative)
        if not str(narrative.get("run_id") or "").strip():
            narrative["run_id"] = analysis_id
        stamped["narrative_result"] = narrative
    return stamped
