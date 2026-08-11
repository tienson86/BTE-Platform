"""Replay runner for synthetic Strength stress cases (PILOT-1G)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context

from .adapter import build_synthetic_bazi_chart, context_snapshot_ascii
from .compare import classify_match

ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT / "datasets"
RESULTS_DIR = ROOT / "results"


def load_case(case_id: str | Path) -> dict[str, Any]:
    """Load one synthetic case JSON by id or path."""
    if isinstance(case_id, Path):
        path = case_id
    else:
        path = DATASETS_DIR / f"{case_id}.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def list_case_ids() -> list[str]:
    """Return sorted SYN-STR case ids present in datasets/."""
    ids = sorted(p.stem for p in DATASETS_DIR.glob("SYN-STR-*.json"))
    return ids


def _weighted_buckets_raw(result: Any) -> dict[str, float]:
    """Recover raw bucket totals from published component scores when possible."""
    # Published component scores are already /scale; evidence extraction in
    # prior pilots stored raw buckets. Reconstruct via metadata when present.
    meta = getattr(result, "metadata", None) or {}
    scoring = ((meta.get("trace") or {}).get("scoring") or {})
    raw_total = scoring.get("raw_total")
    # Prefer reconstructing from analysis is not available; use published scores * 100.
    profile = {
        "season": float(result.season_score or 0.0) * 100.0,
        "root": float(result.root_score or 0.0) * 100.0,
        "support": float(result.support_score or 0.0) * 100.0,
        "drain": float(result.drain_score or 0.0) * 100.0,
        "control": float(result.control_score or 0.0) * 100.0,
        "combination": 0.0,
        "special": 0.0,
    }
    # Approximate special as residual so profile sum ~= raw_total when known.
    if raw_total is not None:
        residual = float(raw_total) - sum(profile.values())
        profile["special"] = residual
    return profile


def replay_case(
    case: dict[str, Any],
    *,
    engine: StrengthEngine | None = None,
) -> dict[str, Any]:
    """Run Strength Engine on one synthetic pillar case."""
    engine = engine or StrengthEngine(database_path="database/12_strength")
    case_id = str(case["case_id"])
    pillars = case["pillars"]
    day_master = case.get("day_master")

    chart = build_synthetic_bazi_chart(pillars, day_master_ascii=day_master)
    context = build_strength_context(chart, calendar=None)
    result = engine.calculate(context)

    profile = _weighted_buckets_raw(result)
    runtime_score = float(result.strength_score or 0.0)
    runtime_band = str(result.strength_level or "unknown").lower()
    synthetic_expected = str(case.get("synthetic_expected_taxonomy") or "").lower()

    comparison = classify_match(
        synthetic_expected_taxonomy=synthetic_expected,
        runtime_v1_band=runtime_band,
        runtime_score=runtime_score,
        runtime_profile=profile,
    )

    meta = getattr(result, "metadata", None) or {}
    scoring = ((meta.get("trace") or {}).get("scoring") or {})

    return {
        "case_id": case_id,
        "dataset_type": case.get("dataset_type"),
        "calibration_eligible": case.get("calibration_eligible", False),
        "golden_eligible": case.get("golden_eligible", False),
        "synthetic_pillars": case.get("synthetic_pillars", True),
        "calendar_verified": case.get("calendar_verified", False),
        "day_master": case.get("day_master"),
        "pillars": pillars,
        "synthetic_expected_taxonomy": synthetic_expected,
        "evidence_profile": case.get("evidence_profile"),
        "stress_purpose": case.get("stress_purpose"),
        "runtime": {
            "success": bool(result.success),
            "score": runtime_score,
            "raw_total": scoring.get("raw_total"),
            "v1_band": runtime_band,
            "v1_label": result.reasoning,
            "confidence": float(result.confidence or 0.0),
            "matched_rules": list(result.matched_rules or []),
            "profile": profile,
            "component_scores": {
                "season_score": float(result.season_score or 0.0),
                "root_score": float(result.root_score or 0.0),
                "support_score": float(result.support_score or 0.0),
                "drain_score": float(result.drain_score or 0.0),
                "control_score": float(result.control_score or 0.0),
            },
            "context": context_snapshot_ascii(context),
            "error": result.error,
            "level_rule": scoring.get("level_rule"),
        },
        "comparison": comparison,
        "notes": [
            "SYNTHETIC stress case only; not calibration evidence.",
            "Mismatch is diagnostic; not automatically a production bug.",
        ],
    }


def replay_all(*, write_results: bool = True) -> list[dict[str, Any]]:
    """Replay every SYN-STR case under datasets/."""
    engine = StrengthEngine(database_path="database/12_strength")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []
    for case_id in list_case_ids():
        case = load_case(case_id)
        result = replay_case(case, engine=engine)
        outputs.append(result)
        if write_results:
            out_path = RESULTS_DIR / f"{case_id}.json"
            with out_path.open("w", encoding="utf-8") as handle:
                json.dump(result, handle, ensure_ascii=True, indent=2)
                handle.write("\n")
    return outputs


def main() -> None:
    """CLI entry: replay all synthetic cases and write results/."""
    results = replay_all(write_results=True)
    matches = sum(1 for r in results if r["comparison"]["exact_synthetic_match"])
    print(f"replayed={len(results)} exact_matches={matches} mismatches={len(results) - matches}")


if __name__ == "__main__":
    main()
