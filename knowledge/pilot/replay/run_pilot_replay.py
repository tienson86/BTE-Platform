"""
BTE Pilot Replay — CASE-0001 → CASE-0009

Canonical harness: applications.api.services.orchestrator.OrchestratorService
Does NOT modify engines/knowledge/pipelines/API/UI.
Does NOT overwrite expert_expected with actual_result.
"""

from __future__ import annotations

import json
import traceback
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from applications.api.services.orchestrator import OrchestratorService
from applications.api.utils.serializers import to_jsonable
from applications.api.utils.pillars import pillar_text

ROOT = Path(__file__).resolve().parents[3]
REPLAY_DIR = Path(__file__).resolve().parent
RESULTS_DIR = REPLAY_DIR / "results"
SNAPSHOTS_DIR = REPLAY_DIR / "snapshots"
FIXTURES_DIR = REPLAY_DIR / "fixtures"
CASES_DIR = REPLAY_DIR / "cases"

FOLLOW_MARKERS = (
    "Tòng Tài",
    "Tòng Quan",
    "Tòng Sát",
    "Tòng Nhi",
    "Tòng Ấn",
    "Tòng Vượng",
    "Tòng Thế",
    "Tòng Cường",
)

# Expert expected strength bands vs engine 3-level taxonomy.
STRENGTH_MATCH: dict[str, dict[str, Any]] = {
    "Thân trung bình / thiên nhược": {
        "preferred_levels": ["balanced"],
        "near_levels": ["weak"],
        "preferred_reasoning_substrings": ["trung", "nhược", "cân bằng"],
    },
    "Thân rất vượng": {
        "preferred_levels": ["strong"],
        "near_levels": [],
        "preferred_reasoning_substrings": ["vượng"],
        "granularity_gap": "engine has no very_strong band",
    },
    "Thân hơi nhược": {
        "preferred_levels": ["weak", "balanced"],
        "near_levels": [],
        "preferred_reasoning_substrings": ["nhược", "trung"],
        "boundary": True,
    },
    "Thân vượng": {
        "preferred_levels": ["strong"],
        "near_levels": [],
        "preferred_reasoning_substrings": ["vượng"],
    },
    "Thân trung bình thiên vượng": {
        "preferred_levels": ["balanced"],
        "near_levels": ["strong"],
        "preferred_reasoning_substrings": ["trung", "vượng", "cân bằng"],
    },
    "Thân trung bình thiên nhược": {
        "preferred_levels": ["balanced"],
        "near_levels": ["weak"],
        "preferred_reasoning_substrings": ["trung", "nhược", "cân bằng"],
    },
}


CASES: list[dict[str, Any]] = [
    {
        "case_id": "CASE-0001",
        "case_type": "expert",
        "subject": {"full_name": "Nguyễn Tiến Sơn", "gender": "male"},
        "birth": {
            "year": 1987,
            "month": 1,
            "day": 21,
            "hour": 4,
            "minute": 30,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hà Nội, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân trung bình / thiên nhược",
            "four_pillars": {
                "year": "Bính Dần",
                "month": "Tân Sửu",
                "day": "Canh Ngọ",
                "hour": "Mậu Dần",
            },
        },
        "external_expected": None,
        "notes": [],
        "runnable": True,
    },
    {
        "case_id": "CASE-0002",
        "case_type": "expert",
        "subject": {"full_name": "Đinh Thành Trung", "gender": "male"},
        "birth": {
            "year": 1977,
            "month": 2,
            "day": 18,
            "hour": 6,
            "minute": 30,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hải Phòng, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân rất vượng",
            "four_pillars": {
                "year": "Đinh Tỵ",
                "month": "Nhâm Dần",
                "day": "Bính Ngọ",
                "hour": "Tân Mão",
            },
        },
        "external_expected": None,
        "notes": [],
        "runnable": True,
    },
    {
        "case_id": "CASE-0003",
        "case_type": "expert_boundary",
        "subject": {"full_name": "Nguyễn Tiến Khang", "gender": "male"},
        "birth": {
            "year": 2015,
            "month": 8,
            "day": 14,
            "hour": 7,
            "minute": 20,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hà Nội, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân hơi nhược",
            "four_pillars": {
                "year": "Ất Mùi",
                "month": "Giáp Thân",
                "day": "Nhâm Tuất",
                "hour": "Giáp Thìn",
            },
        },
        "external_expected": None,
        "notes": ["Boundary case — do not force engine toward expected."],
        "runnable": True,
        "force_boundary": True,
    },
    {
        "case_id": "CASE-0004",
        "case_type": "expert",
        "subject": {"full_name": "Nguyễn Tiến Minh", "gender": "male"},
        "birth": {
            "year": 2013,
            "month": 8,
            "day": 20,
            "hour": 13,
            "minute": 40,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hà Nội, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân vượng",
            "four_pillars": {
                "year": "Quý Tỵ",
                "month": "Canh Thân",
                "day": "Mậu Ngọ",
                "hour": "Kỷ Mùi",
            },
        },
        "external_expected": None,
        "notes": [],
        "runnable": True,
    },
    {
        "case_id": "CASE-0005",
        "case_type": "expert",
        "subject": {
            "full_name": "Lương Ngọc Huỳnh",
            "gender": None,
            "gender_status": "unspecified",
        },
        "birth": {
            "year": 1966,
            "month": 9,
            "day": 24,
            "hour": 4,
            "minute": 15,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hà Nội, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân trung bình thiên vượng",
            "four_pillars": {
                "year": "Bính Ngọ",
                "month": "Đinh Dậu",
                "day": "Bính Tuất",
                "hour": "Canh Dần",
            },
        },
        "external_expected": None,
        "notes": [
            "Gender unspecified — schema allows None; do not invent gender.",
        ],
        "runnable": True,
    },
    {
        "case_id": "CASE-0006",
        "case_type": "expert",
        "subject": {"full_name": "Nguyễn Thị Hương Mai", "gender": "female"},
        "birth": {
            "year": 1988,
            "month": 6,
            "day": 7,
            "hour": 20,
            "minute": 45,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Hải Phòng, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân trung bình thiên nhược",
            "four_pillars": {
                "year": "Mậu Thìn",
                "month": "Đinh Tỵ",
                "day": "Quý Tỵ",
                "hour": "Nhâm Tuất",
            },
        },
        "external_expected": None,
        "notes": [],
        "runnable": True,
    },
    {
        "case_id": "CASE-0007",
        "case_type": "expert",
        "subject": {"full_name": "Vũ Thị Thanh Tuyền", "gender": "female"},
        "birth": {
            "year": 1984,
            "month": 7,
            "day": 13,
            "hour": 21,
            "minute": 1,
            "timezone": "Asia/Ho_Chi_Minh",
            "location": "Quảng Ninh, Việt Nam",
        },
        "expert_expected": {
            "strength": "Thân vượng",
            "four_pillars": {
                "year": "Giáp Tý",
                "month": "Tân Mùi",
                "day": "Mậu Thân",
                "hour": "Quý Hợi",
            },
        },
        "external_expected": None,
        "notes": [],
        "runnable": True,
    },
    {
        "case_id": "CASE-0008",
        "case_type": "reference",
        "subject": {"full_name": None, "gender": None},
        "birth": None,
        "pillars_only": {
            "year": "Quý Dậu",
            "month": "Giáp Tý",
            "day": "Mậu Tý",
            "hour": "Nhâm Tý",
            "day_master": "Mậu Thổ",
        },
        "expert_expected": None,
        "external_expected": {
            "classification": "Follow Wealth / Tòng Tài",
            "classification_type": "REFERENCE_ONLY",
            "note": "External reference is not absolute ground truth.",
        },
        "notes": [
            "No birth datetime provided. OrchestratorService.analyze requires "
            "solar birth datetime. Cannot invent datetime for replay.",
        ],
        "runnable": False,
        "block_reason": "MISSING_BIRTH_DATETIME",
    },
    {
        "case_id": "CASE-0009",
        "case_type": "reference_transformation",
        "subject": {"full_name": None, "gender": None},
        "birth": None,
        "pillars_only": None,
        "expert_expected": None,
        "external_expected": {
            "intent": "Combination detected vs Transformation detected",
            "classification_type": "REFERENCE_ONLY",
        },
        "notes": [
            "No reliable birth/pillar source for a transformation reference case "
            "was found in Pilot fixtures, QC2 scenarios (slug-only), or repo search. "
            "Do not fabricate CASE-0009 input.",
        ],
        "runnable": False,
        "block_reason": "BLOCKED_REFERENCE_DATA",
    },
]


def _pillar_label(pillar: dict[str, Any] | None) -> str:
    if not isinstance(pillar, dict):
        return pillar_text(pillar) if pillar is not None else ""
    stem = str(pillar.get("stem") or "").strip()
    branch = str(pillar.get("branch") or "").strip()
    return f"{stem} {branch}".strip()


def _actual_pillars(payload: dict[str, Any]) -> dict[str, str]:
    bazi = payload.get("bazi") or {}
    return {
        "year": _pillar_label(bazi.get("year_pillar")),
        "month": _pillar_label(bazi.get("month_pillar")),
        "day": _pillar_label(bazi.get("day_pillar")),
        "hour": _pillar_label(bazi.get("hour_pillar")),
    }


def _normalize_pillar(text: str) -> str:
    return " ".join(str(text or "").replace("/", " ").split())


def _compare_pillars(
    expected: dict[str, str] | None,
    actual: dict[str, str],
) -> dict[str, Any]:
    if not expected:
        return {"status": "N/A", "matches": {}, "all_match": False}
    matches = {
        key: _normalize_pillar(expected.get(key, "")) == _normalize_pillar(actual.get(key, ""))
        for key in ("year", "month", "day", "hour")
    }
    return {
        "status": "PASS" if all(matches.values()) else "DISCREPANCY",
        "matches": matches,
        "all_match": all(matches.values()),
        "expected": expected,
        "actual": actual,
    }


def _extract_follow(pattern: dict[str, Any]) -> dict[str, Any]:
    tong = str(pattern.get("tong_cach") or "").strip()
    follow_type = str(pattern.get("follow_type") or "").strip()
    detected = None
    for marker in FOLLOW_MARKERS:
        if tong == marker or follow_type == marker:
            detected = marker
            break
    return {
        "follow_detected": detected is not None,
        "follow_pattern_type": detected,
        "tong_cach_raw": tong,
        "follow_type_raw": follow_type or None,
        "note": (
            "tong_cach equals main pattern label — not a follow detection"
            if tong and detected is None
            else None
        ),
    }


def _extract_transform(payload: dict[str, Any]) -> dict[str, Any]:
    # Production Orchestrator public payload does not expose transformation_*.
    # Probe known slots without inventing values.
    candidates: list[Any] = []
    for key in (
        "transformation_detected",
        "transformation_score",
        "transformation_type",
        "transformation",
    ):
        if key in payload:
            candidates.append({key: payload.get(key)})
    pattern = payload.get("pattern") or {}
    for key in (
        "transformation_detected",
        "transformation_score",
        "hoa",
        "hoa_khi",
    ):
        if key in pattern:
            candidates.append({f"pattern.{key}": pattern.get(key)})
    return {
        "transformation_detected": None,
        "transformation_score": None,
        "producer_present": False,
        "probed_slots": candidates,
        "status": "NOT_PRODUCED",
        "note": (
            "No transformation_* fields on OrchestratorService public payload; "
            "combination≠transformation per package contracts."
        ),
    }


def _compare_strength(
    expert_label: str | None,
    strength: dict[str, Any],
    *,
    force_boundary: bool = False,
) -> dict[str, Any]:
    level = str(strength.get("strength_level") or "")
    reasoning = str(strength.get("reasoning") or "")
    score = strength.get("strength_score")
    if not expert_label:
        return {
            "status": "N/A",
            "expert_expected": None,
            "actual_level": level,
            "actual_reasoning": reasoning,
            "actual_score": score,
        }
    spec = STRENGTH_MATCH.get(expert_label, {})
    preferred = list(spec.get("preferred_levels") or [])
    near = list(spec.get("near_levels") or [])
    boundary = bool(spec.get("boundary") or force_boundary)

    if level in preferred:
        # Exact band match — still flag granularity gaps for "rất vượng".
        if spec.get("granularity_gap") and expert_label != reasoning:
            status = "DISCREPANCY"
            detail = (
                f"Engine band '{level}' / reasoning '{reasoning}' is coarser than "
                f"expert '{expert_label}' ({spec['granularity_gap']})."
            )
        else:
            # Also require reasoning not contradict preferred direction when possible.
            status = "PASS"
            detail = "Strength level matches preferred engine band for expert label."
            if expert_label.startswith("Thân trung bình") and level == "balanced":
                status = "DISCREPANCY"
                detail = (
                    "Engine only emits balanced/strong/weak; expert asks for "
                    f"directional bias '{expert_label}' which engine cannot express."
                )
    elif level in near:
        status = "DISCREPANCY"
        detail = (
            f"Near-band match: actual '{level}' vs preferred {preferred} "
            f"for expert '{expert_label}'."
        )
    else:
        status = "DISCREPANCY"
        detail = (
            f"Strength mismatch: expert '{expert_label}' → preferred {preferred}; "
            f"actual level='{level}' reasoning='{reasoning}' score={score}."
        )

    if boundary:
        # Boundary cases are never forced PASS even if band coincides.
        if status == "PASS":
            status = "BOUNDARY"
            detail = (
                "Boundary case: actual landed in preferred band, but expert label "
                "is intentionally soft — do not treat as golden PASS."
            )
        else:
            status = "BOUNDARY"
            detail = (
                "Boundary case: actual diverges from soft expert expectation; "
                "do not force engine. " + detail
            )

    return {
        "status": status,
        "expert_expected": expert_label,
        "actual_level": level,
        "actual_reasoning": reasoning,
        "actual_score": score,
        "preferred_levels": preferred,
        "detail": detail,
        "granularity_gap": spec.get("granularity_gap"),
    }


def _stage_status(
    *,
    executed: bool,
    ok: bool | None = None,
    blocked_reason: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    if blocked_reason:
        return {"status": "BLOCKED", "reason": blocked_reason, "note": note}
    if not executed:
        return {"status": "NOT_RUN", "note": note}
    if ok is True:
        return {"status": "PASS", "note": note}
    if ok is False:
        return {"status": "DISCREPANCY", "note": note}
    return {"status": "EXECUTED", "note": note}


def _first_divergence(trace: dict[str, Any]) -> str | None:
    order = [
        "input",
        "validation",
        "calendar_bazi",
        "strength",
        "follow",
        "transform",
        "decision",
        "luck",
        "interpretation",
        "report",
    ]
    for key in order:
        item = trace.get(key) or {}
        status = str(item.get("status") or "")
        if status in {"DISCREPANCY", "BOUNDARY", "BLOCKED", "FAIL", "NOT_PRODUCED"}:
            if status == "NOT_PRODUCED" and key == "transform":
                # Transform absence is systemic; only call it first divergence
                # when case specifically requires transform evaluation.
                continue
            if status == "BLOCKED" and key in {"decision", "luck"}:
                continue
            return key
    return None


def _strip_rendered(payload: dict[str, Any]) -> dict[str, Any]:
    """Keep canonical JSON; drop bulky rendered prose bodies from snapshot."""
    out = deepcopy(payload)
    report = out.get("report")
    if isinstance(report, dict):
        out["report"] = {
            "title": report.get("title"),
            "section_count": report.get("section_count"),
            "markdown_present": bool(report.get("markdown")),
            "html_present": bool(report.get("html")),
            "markdown_chars": len(str(report.get("markdown") or "")),
            "html_chars": len(str(report.get("html") or "")),
        }
    narrative = out.get("narrative")
    if isinstance(narrative, dict):
        # Keep structure keys only when huge.
        slim = {k: narrative.get(k) for k in narrative if k not in {"html", "markdown", "body"}}
        out["narrative"] = slim
    interpretation = out.get("interpretation")
    if isinstance(interpretation, dict):
        sections = interpretation.get("sections") or []
        out["interpretation"] = {
            "section_count": len(sections),
            "confidence": interpretation.get("confidence"),
            "section_ids": [
                (s.get("id") if isinstance(s, dict) else None) for s in sections
            ],
            "sections_summary": [
                {
                    "id": s.get("id"),
                    "title": s.get("title"),
                    "body_chars": len(str(s.get("body") or "")),
                }
                for s in sections
                if isinstance(s, dict)
            ],
        }
    return out


def _run_case(case: dict[str, Any], orch: OrchestratorService) -> dict[str, Any]:
    case_id = case["case_id"]
    now = datetime.now(timezone.utc).isoformat()
    result: dict[str, Any] = {
        "case_id": case_id,
        "case_type": case["case_type"],
        "run": {
            "date": now,
            "entrypoint": "applications.api.services.orchestrator.OrchestratorService.analyze",
            "engine_or_knowledge_modified": False,
            "architecture_freeze": "AF-1 unchanged",
        },
        "input": {
            "subject": case.get("subject"),
            "birth": case.get("birth"),
            "pillars_only": case.get("pillars_only"),
        },
        "expected": {
            "expert_expected": case.get("expert_expected"),
            "external_expected": case.get("external_expected"),
        },
        "actual": None,
        "comparison": {},
        "verdict": "BLOCKED",
        "trace": {},
        "audit": {
            "notes": list(case.get("notes") or []),
            "freeze_compliance": True,
        },
        "diagnostics": {},
    }

    if not case.get("runnable"):
        reason = case.get("block_reason") or "BLOCKED"
        result["verdict"] = "BLOCKED" if case_id != "CASE-0008" else "REFERENCE_ONLY"
        if case_id == "CASE-0008":
            result["verdict"] = "REFERENCE_ONLY"
        if reason == "BLOCKED_REFERENCE_DATA":
            result["verdict"] = "BLOCKED"
        result["trace"] = {
            "input": _stage_status(
                executed=False,
                blocked_reason=reason,
                note="; ".join(case.get("notes") or []),
            ),
            "validation": _stage_status(executed=False, blocked_reason=reason),
            "calendar_bazi": _stage_status(executed=False, blocked_reason=reason),
            "strength": _stage_status(executed=False, blocked_reason=reason),
            "follow": _stage_status(executed=False, blocked_reason=reason),
            "transform": _stage_status(executed=False, blocked_reason=reason),
            "decision": _stage_status(
                executed=False,
                blocked_reason="DECISION_ENGINE_NOT_IN_ORCHESTRATOR",
                note="DecisionEngine is not imported/called by OrchestratorService.",
            ),
            "luck": _stage_status(
                executed=False,
                blocked_reason=reason,
                note="Luck runs internally on full analyze but is stripped from public payload.",
            ),
            "interpretation": _stage_status(executed=False, blocked_reason=reason),
            "report": _stage_status(executed=False, blocked_reason=reason),
        }
        result["diagnostics"]["block_reason"] = reason
        result["comparison"]["first_divergence"] = "input"
        return result

    birth = case["birth"]
    gender = (case.get("subject") or {}).get("gender")
    try:
        payload = orch.analyze(
            year=int(birth["year"]),
            month=int(birth["month"]),
            day=int(birth["day"]),
            hour=int(birth["hour"]),
            minute=int(birth["minute"]),
            gender=gender,
            timezone=str(birth.get("timezone") or "Asia/Ho_Chi_Minh"),
        )
        payload = to_jsonable(payload)
    except Exception as exc:  # noqa: BLE001 — record real runtime failure
        result["verdict"] = "BLOCKED"
        result["diagnostics"]["exception"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        result["trace"] = {
            "input": _stage_status(executed=True, ok=True),
            "validation": _stage_status(
                executed=True,
                ok=False,
                blocked_reason="RUNTIME_EXCEPTION",
                note=str(exc),
            ),
        }
        result["comparison"]["first_divergence"] = "validation"
        return result

    slim = _strip_rendered(payload)
    pillars = _actual_pillars(payload)
    strength = payload.get("strength") or {}
    pattern = payload.get("pattern") or {}
    score = payload.get("score") or {}
    temperature = payload.get("temperature") or {}
    useful_god = payload.get("useful_god") or {}
    interpretation = slim.get("interpretation") or {}
    report = slim.get("report") or {}

    expert = case.get("expert_expected") or {}
    pillar_cmp = _compare_pillars(expert.get("four_pillars"), pillars)
    strength_cmp = _compare_strength(
        expert.get("strength"),
        strength if isinstance(strength, dict) else {},
        force_boundary=bool(case.get("force_boundary")),
    )
    follow = _extract_follow(pattern if isinstance(pattern, dict) else {})
    transform = _extract_transform(payload)

    # Decision: not wired in orchestrator.
    decision_status = _stage_status(
        executed=False,
        blocked_reason="DECISION_ENGINE_NOT_IN_ORCHESTRATOR",
        note="No DecisionEngine call in applications.api.services.orchestrator.",
    )

    # Luck: executed inside analyze, stripped from public contract.
    luck_status = _stage_status(
        executed=True,
        ok=None,
        note=(
            "LuckEngine.build runs inside OrchestratorService.analyze (Stage 7) "
            "but key 'luck' is removed by _finalize_public_payload / "
            "_INTERNAL_PAYLOAD_KEYS. Public coverage = NOT_EXPOSED."
        ),
    )
    luck_status["status"] = "INTERNAL_ONLY"

    interp_ran = int(interpretation.get("section_count") or 0) > 0
    report_ran = bool(report.get("markdown_present") or report.get("html_present"))

    # Score anomaly flag (observed total_score==0 on smoke run).
    score_total = score.get("total_score") if isinstance(score, dict) else None
    score_anomaly = score_total == 0 or score_total == 0.0

    # No expert_expected for interpretation/report prose → EXECUTED, never PASS.
    interpretation_status = {
        "status": "EXECUTED" if interp_ran else "DISCREPANCY",
        "note": (
            f"sections={interpretation.get('section_count')}; "
            "no expert_expected for interpretation prose — not scored PASS."
        ),
    }
    report_status = {
        "status": "EXECUTED" if report_ran else "DISCREPANCY",
        "note": (
            f"section_count={report.get('section_count')} "
            f"markdown={report.get('markdown_present')} "
            f"html={report.get('html_present')}; "
            "no expert_expected for report content — not scored PASS."
        ),
    }

    trace = {
        "input": _stage_status(executed=True, ok=True),
        "validation": _stage_status(executed=True, ok=True),
        "calendar_bazi": _stage_status(
            executed=True,
            ok=pillar_cmp["all_match"],
            note="Pillars checked against expert/user-confirmed four pillars.",
        ),
        "strength": {
            "status": strength_cmp["status"],
            "detail": strength_cmp.get("detail"),
            "actual_level": strength_cmp.get("actual_level"),
            "actual_reasoning": strength_cmp.get("actual_reasoning"),
            "actual_score": strength_cmp.get("actual_score"),
            "expert_expected": strength_cmp.get("expert_expected"),
        },
        "follow": {
            "status": (
                "EXECUTED"
                if follow["follow_detected"]
                else "EXECUTED_NEGATIVE"
            ),
            **follow,
            "note": (
                "REFERENCE_ONLY external follow not compared as absolute truth"
                if case["case_type"] == "reference"
                else follow.get("note")
            ),
        },
        "transform": transform,
        "decision": decision_status,
        "luck": luck_status,
        "interpretation": interpretation_status,
        "report": report_status,
        "score_surface": {
            "status": "ANOMALY" if score_anomaly else "EXECUTED",
            "total_score": score_total,
            "grade": score.get("grade") if isinstance(score, dict) else None,
            "note": (
                "Public score.total_score is 0 / empty grade — report as observed, "
                "do not patch engine."
                if score_anomaly
                else None
            ),
        },
        "temperature": {
            "status": "EXECUTED",
            "temperature_level": (
                temperature.get("temperature_level")
                if isinstance(temperature, dict)
                else None
            ),
            "temperature_score": (
                temperature.get("temperature_score")
                if isinstance(temperature, dict)
                else None
            ),
            "reasoning": (
                temperature.get("reasoning") if isinstance(temperature, dict) else None
            ),
        },
        "useful_god": {
            "status": "EXECUTED",
            "useful_god": (
                useful_god.get("useful_god") if isinstance(useful_god, dict) else None
            ),
            "confidence": (
                useful_god.get("confidence") if isinstance(useful_god, dict) else None
            ),
        },
        "pipeline": payload.get("pipeline"),
    }

    # Verdict policy
    if case.get("force_boundary") or strength_cmp["status"] == "BOUNDARY":
        verdict = "BOUNDARY"
    elif not pillar_cmp["all_match"]:
        verdict = "DISCREPANCY"
    elif strength_cmp["status"] == "DISCREPANCY":
        verdict = "DISCREPANCY"
    elif strength_cmp["status"] == "PASS" and pillar_cmp["all_match"]:
        # Full PASS only if pillars + strength match and no forced boundary.
        verdict = "PASS"
    else:
        verdict = "DISCREPANCY"

    first = _first_divergence(trace)
    if first is None and verdict == "PASS":
        first = None
    elif first is None and verdict != "PASS":
        first = "strength"

    result["actual"] = {
        "pipeline": payload.get("pipeline"),
        "calendar": slim.get("calendar"),
        "bazi": {
            "pillars": pillars,
            "day_master": (payload.get("bazi") or {}).get("day_master"),
            "day_master_element": (payload.get("bazi") or {}).get("day_master_element"),
            "day_master_yin_yang": (payload.get("bazi") or {}).get(
                "day_master_yin_yang"
            ),
            "gender": (payload.get("bazi") or {}).get("gender"),
            "ten_gods": (payload.get("bazi") or {}).get("ten_gods"),
            "shensha_count": len((payload.get("bazi") or {}).get("shensha") or []),
        },
        "strength": strength,
        "temperature": {
            k: temperature.get(k)
            for k in (
                "temperature_level",
                "temperature_score",
                "warm_score",
                "cold_score",
                "dry_score",
                "humid_score",
                "reasoning",
                "matched_rules",
            )
            if isinstance(temperature, dict)
        },
        "pattern": pattern,
        "follow": follow,
        "transform": transform,
        "useful_god": useful_god,
        "score": score,
        "interpretation": interpretation,
        "report": report,
        "sources": {
            k: payload.get(k)
            for k in payload
            if k.endswith("_source")
        },
    }
    result["comparison"] = {
        "pillars": pillar_cmp,
        "strength": strength_cmp,
        "follow": follow,
        "transform": transform,
        "first_divergence": first,
    }
    result["trace"] = trace
    result["verdict"] = verdict
    result["diagnostics"] = {
        "score_anomaly": score_anomaly,
        "public_luck_exposed": "luck" in payload,
        "decision_wired": False,
        "transformation_produced": False,
        "portal": {
            "status": "BLOCKED",
            "reason": (
                "Portal/DOM live replay not started in this Pilot Replay run."
            ),
        },
    }
    result["_snapshot_payload"] = slim
    return result


def _matrix_cell(trace: dict[str, Any], key: str) -> str:
    item = trace.get(key) or {}
    status = str(item.get("status") or "—")
    # Matrix must not claim PASS for fixture-only / non-evaluated layers.
    if status in {"EXECUTED", "EXECUTED_NEGATIVE", "INTERNAL_ONLY", "ANOMALY"}:
        return status
    if status == "NOT_PRODUCED":
        return "NOT_PRODUCED"
    return status


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, default=str)
        fh.write("\n")


def _case_md(result: dict[str, Any]) -> str:
    case_id = result["case_id"]
    expected = result.get("expected") or {}
    expert = expected.get("expert_expected") or {}
    external = expected.get("external_expected")
    actual = result.get("actual") or {}
    comparison = result.get("comparison") or {}
    trace = result.get("trace") or {}
    lines = [
        f"# {case_id}",
        "",
        f"**Verdict:** {result.get('verdict')}",
        f"**Case type:** {result.get('case_type')}",
        "",
        "## Input",
        "",
        "```json",
        json.dumps(result.get("input"), ensure_ascii=False, indent=2),
        "```",
        "",
        "## Expected",
        "",
        "### expert_expected",
        "",
        "```json",
        json.dumps(expert, ensure_ascii=False, indent=2),
        "```",
        "",
        "### external_expected",
        "",
        "```json",
        json.dumps(external, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Actual (summary)",
        "",
        "```json",
        json.dumps(
            {
                "pipeline": (actual or {}).get("pipeline"),
                "pillars": ((actual or {}).get("bazi") or {}).get("pillars"),
                "strength": (actual or {}).get("strength"),
                "pattern": (actual or {}).get("pattern"),
                "follow": (actual or {}).get("follow"),
                "transform": (actual or {}).get("transform"),
                "score": (actual or {}).get("score"),
                "interpretation": (actual or {}).get("interpretation"),
                "report": (actual or {}).get("report"),
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        "```",
        "",
        "## Comparison",
        "",
        "```json",
        json.dumps(comparison, ensure_ascii=False, indent=2, default=str),
        "```",
        "",
        "## Trace",
        "",
        "```json",
        json.dumps(trace, ensure_ascii=False, indent=2, default=str),
        "```",
        "",
        "## First divergence",
        "",
        f"`{comparison.get('first_divergence')}`",
        "",
        "## Audit",
        "",
        "```json",
        json.dumps(result.get("audit"), ensure_ascii=False, indent=2),
        "```",
        "",
        "## Diagnostics",
        "",
        "```json",
        json.dumps(result.get("diagnostics"), ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    CASES_DIR.mkdir(parents=True, exist_ok=True)

    # Persist fixtures (inputs/expected only — never overwrite with actual).
    for case in CASES:
        _write_json(FIXTURES_DIR / f"{case['case_id']}.input.json", {
            "case_id": case["case_id"],
            "case_type": case["case_type"],
            "subject": case.get("subject"),
            "birth": case.get("birth"),
            "pillars_only": case.get("pillars_only"),
            "notes": case.get("notes"),
            "runnable": case.get("runnable"),
            "block_reason": case.get("block_reason"),
        })
        _write_json(FIXTURES_DIR / f"{case['case_id']}.expected.json", {
            "case_id": case["case_id"],
            "expert_expected": case.get("expert_expected"),
            "external_expected": case.get("external_expected"),
        })

    orch = OrchestratorService()
    results: list[dict[str, Any]] = []
    for case in CASES:
        print(f"REPLAY {case['case_id']} ...")
        result = _run_case(case, orch)
        snapshot_payload = result.pop("_snapshot_payload", None)
        results.append(result)
        _write_json(RESULTS_DIR / f"{case['case_id']}.json", result)
        _write_json(
            SNAPSHOTS_DIR / f"{case['case_id']}.json",
            {
                "case_id": case["case_id"],
                "verdict": result.get("verdict"),
                "canonical_outputs": snapshot_payload,
                "contracts": {
                    "entrypoint": result["run"]["entrypoint"],
                    "public_pipeline": [
                        "calendar",
                        "bazi",
                        "pattern",
                        "score",
                        "interpretation",
                        "report",
                        "narrative",
                    ],
                    "sources": (result.get("actual") or {}).get("sources"),
                },
                "trace": result.get("trace"),
                "audit": result.get("audit"),
                "diagnostics": result.get("diagnostics"),
            },
        )
        (CASES_DIR / f"{case['case_id']}.md").write_text(
            _case_md(result), encoding="utf-8"
        )
        print(f"  -> {result.get('verdict')} first={((result.get('comparison') or {}).get('first_divergence'))}")

    # Aggregate matrix
    matrix_rows = []
    for r in results:
        trace = r.get("trace") or {}
        strength_status = (trace.get("strength") or {}).get("status") or "—"
        follow_status = _matrix_cell(trace, "follow")
        transform_status = _matrix_cell(trace, "transform")
        decision_status = _matrix_cell(trace, "decision")
        luck_status = _matrix_cell(trace, "luck")
        interp_status = _matrix_cell(trace, "interpretation")
        report_status = _matrix_cell(trace, "report")
        # Strength column: only PASS when strength comparison truly passed.
        if strength_status == "PASS":
            strength_col = "PASS"
        elif strength_status in {"DISCREPANCY", "BOUNDARY", "BLOCKED"}:
            strength_col = strength_status
        else:
            strength_col = strength_status
        matrix_rows.append(
            {
                "case": r["case_id"],
                "type": r["case_type"],
                "strength": strength_col,
                "follow": follow_status,
                "transform": transform_status,
                "decision": decision_status,
                "luck": luck_status,
                "interpretation": interp_status,
                "report": report_status,
                "verdict": r.get("verdict"),
                "first_divergence": (r.get("comparison") or {}).get("first_divergence"),
            }
        )

    summary = {
        "run_date": datetime.now(timezone.utc).isoformat(),
        "entrypoint": "applications.api.services.orchestrator.OrchestratorService.analyze",
        "cases_total": len(results),
        "verdicts": {
            "PASS": sum(1 for r in results if r.get("verdict") == "PASS"),
            "DISCREPANCY": sum(1 for r in results if r.get("verdict") == "DISCREPANCY"),
            "BOUNDARY": sum(1 for r in results if r.get("verdict") == "BOUNDARY"),
            "BLOCKED": sum(1 for r in results if r.get("verdict") == "BLOCKED"),
            "REFERENCE_ONLY": sum(
                1 for r in results if r.get("verdict") == "REFERENCE_ONLY"
            ),
        },
        "matrix": matrix_rows,
        "runtime_coverage": {
            "input": True,
            "calendar": True,
            "bazi": True,
            "strength": True,
            "temperature": True,
            "pattern": True,
            "useful_god": True,
            "score": True,
            "luck_public": False,
            "luck_internal": True,
            "decision": False,
            "transformation": False,
            "interpretation": True,
            "report": True,
            "narrative": True,
            "portal_dom": False,
        },
        "engine_pipeline_package_api_ui_modified": False,
    }
    _write_json(RESULTS_DIR / "summary.json", summary)
    _write_json(RESULTS_DIR / "matrix.json", matrix_rows)
    print(json.dumps(summary["verdicts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
