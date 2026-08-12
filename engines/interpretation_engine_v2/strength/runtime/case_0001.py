"""Build PublishedStrengthFacts from calibration evidence."""

from __future__ import annotations

import json
from pathlib import Path

from engines.interpretation_engine_v2.strength.contracts.models import (
    EvidenceState,
    PublishedStrengthFacts,
)


def default_case_0001_path() -> Path:
    """Return default CASE-0001 calibration JSON path."""
    return (
        Path(__file__).resolve().parents[4]
        / "knowledge"
        / "pilot"
        / "replay"
        / "root_cause"
        / "strength_calibration"
        / "evidence"
        / "CASE-0001.json"
    )


def load_case_0001_facts(path: Path | None = None) -> PublishedStrengthFacts:
    """Load CASE-0001 published Strength facts."""
    source = path or default_case_0001_path()
    payload = json.loads(source.read_text(encoding="utf-8"))
    pipeline = payload["pipeline"]
    contract = pipeline["published_contract"]
    context = pipeline["context_fields"]

    root_level = context.get("root_level", "")
    drain_count = int(context.get("drain_count", 0) or 0)
    drain_type = context.get("drain_type")

    facts: dict[str, EvidenceState] = {
        "classification": EvidenceState.AVAILABLE,
        "season": EvidenceState.AVAILABLE,
        "root": EvidenceState.AVAILABLE,
        "support": EvidenceState.AVAILABLE,
        "control": EvidenceState.AVAILABLE,
        "special": EvidenceState.AVAILABLE,
        "combination": EvidenceState.NOT_APPLICABLE,
        "hidden_stems": EvidenceState.MISSING,
        "luck_interaction": EvidenceState.MISSING,
    }

    if "Thông căn 1 chi" in root_level:
        facts["root_thin"] = EvidenceState.AVAILABLE
    else:
        facts["root_thin"] = EvidenceState.MISSING

    if drain_count == 0 and drain_type is None:
        facts["drain"] = EvidenceState.INACTIVE
        facts["drain_active"] = EvidenceState.INACTIVE
    elif drain_count > 0:
        facts["drain"] = EvidenceState.AVAILABLE
        facts["drain_active"] = EvidenceState.AVAILABLE
    else:
        facts["drain"] = EvidenceState.MISSING

    forbidden_flags = {
        "drain_inactive": facts["drain"] == EvidenceState.INACTIVE,
        "root_thin": facts.get("root_thin") == EvidenceState.AVAILABLE,
        "root_deep_required": facts.get("root_thin") == EvidenceState.AVAILABLE,
        "luck_missing": facts["luck_interaction"] == EvidenceState.MISSING,
        "special_is_not_override": True,
    }

    return PublishedStrengthFacts(
        case_id=payload.get("case_id", "CASE-0001"),
        class_id=contract["strength_level"],
        strength_score=float(contract["strength_score"]),
        facts=facts,
        polarities={
            "season": "support",
            "root": "support",
            "root_thin": "support",
            "support": "support",
            "control": "weaken",
            "special": "support",
            "drain": "inactive",
        },
        forbidden_flags=forbidden_flags,
        interpretation_confidence=72,
        confidence_band="high",
        alternative_primary="strong",
        alternative_runner_up="balanced",
        alternative_shares={"balanced": 0.28},
        conflicts=["C1"],
    )
