"""
Pattern Engine.

Điểm vào chính của Pattern Engine — sole producer of PatternResult
and the published RuleContext attached to PatternResult.rule_context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

from .context import PatternContext
from .labels import pattern_display_label
from .override_eligibility import classify_pattern_override
from .rule_context_bridge import (
    build_rule_context,
    enrich_result_from_rule_context,
)
from .service import PatternService


# Repo root: engines/pattern_engine/engine.py → parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[2]

# Canonical Pattern Rule Database (WP1)
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "14_pattern")


@dataclass(slots=True)
class PatternResult:
    """Authoritative pattern recognition result for the production pipeline."""

    success: bool = True
    pattern: Optional[str] = None
    score: float = 0.0
    priority: int = 0
    matched_rules: List[str] = field(default_factory=list)
    error: Optional[str] = None
    description: Optional[str] = None
    cach_cuc: str = ""
    follow_type: Optional[str] = None
    # Decision-pipeline fields (Phase 3B)
    candidate_patterns: List[str] = field(default_factory=list)
    validated_patterns: List[str] = field(default_factory=list)
    final_pattern: Optional[str] = None
    secondary_patterns: List[str] = field(default_factory=list)
    confidence: float = 0.0
    reason: Optional[str] = None
    # Metadata published only when Pattern Engine already computed them.
    pattern_rank: Optional[int] = None
    pattern_quality: Optional[str] = None
    combination_status: Optional[str] = None
    clash_status: Optional[str] = None
    success_reason: Optional[str] = None
    failure_reason: Optional[str] = None
    than: str = ""
    than_vuong_nhuoc: str = ""
    tong_cach: str = ""
    dung_than: str = ""
    hy_than: str = ""
    ky_than: str = ""
    dieu_hau: str = ""
    winning_rule_id: str = ""
    evidence_compact: str = ""
    month_branch: str = ""
    month_main_qi: str = ""
    month_main_qi_ten_god: str = ""
    month_hidden_stems: List[str] = field(default_factory=list)
    day_master: str = ""
    penetration_exact: bool | None = None
    penetration_related: List[dict[str, Any]] = field(default_factory=list)
    fallback_used: bool = False
    ug_override_eligible: bool = False
    qualification_level: int | None = None
    detected_special_pattern: str | None = None
    rule_context: dict[str, Any] = field(default_factory=dict)

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize PatternView fields for API / Portal (no internal fields)."""
        label = self.cach_cuc or pattern_display_label(self.pattern, self.description)
        payload: dict[str, Any] = {
            "success": self.success,
            "pattern": self.pattern or "",
            "cach_cuc": label,
            "score": float(self.score or 0.0),
            "priority": int(self.priority or 0),
        }
        if self.than:
            payload["than"] = self.than
        if self.than_vuong_nhuoc:
            payload["than_vuong_nhuoc"] = self.than_vuong_nhuoc
        if self.tong_cach:
            payload["tong_cach"] = self.tong_cach
        if self.dung_than:
            payload["dung_than"] = self.dung_than
        if self.hy_than:
            payload["hy_than"] = self.hy_than
        if self.ky_than:
            payload["ky_than"] = self.ky_than
        if self.dieu_hau:
            payload["dieu_hau"] = self.dieu_hau
        if self.winning_rule_id:
            payload["winning_rule_id"] = self.winning_rule_id
        if self.evidence_compact:
            payload["evidence_compact"] = self.evidence_compact
        if self.month_branch:
            payload["month_branch"] = self.month_branch
        if self.month_main_qi:
            payload["month_main_qi"] = self.month_main_qi
        if self.month_main_qi_ten_god:
            payload["month_main_qi_ten_god"] = self.month_main_qi_ten_god
        if self.month_hidden_stems:
            payload["month_hidden_stems"] = list(self.month_hidden_stems)
        if self.day_master:
            payload["day_master"] = self.day_master
        if self.penetration_exact is not None:
            payload["penetration_exact"] = bool(self.penetration_exact)
        if self.penetration_related:
            payload["penetration_related"] = list(self.penetration_related)
        if self.candidate_patterns:
            payload["candidate_patterns"] = list(self.candidate_patterns)
        payload["fallback_used"] = bool(self.fallback_used)
        payload["ug_override_eligible"] = bool(self.ug_override_eligible)
        if self.qualification_level is not None:
            payload["qualification_level"] = int(self.qualification_level)
        if self.detected_special_pattern:
            payload["detected_special_pattern"] = self.detected_special_pattern
        # Optional metadata — omit when unset (no fabricated defaults).
        if self.follow_type:
            payload["follow_type"] = self.follow_type
        if self.success_reason:
            payload["success_reason"] = self.success_reason
        if self.failure_reason:
            payload["failure_reason"] = self.failure_reason
        if self.pattern_rank is not None:
            payload["pattern_rank"] = int(self.pattern_rank)
        if self.pattern_quality:
            payload["pattern_quality"] = self.pattern_quality
        if self.combination_status:
            payload["combination_status"] = self.combination_status
        if self.clash_status:
            payload["clash_status"] = self.clash_status
        return payload


class PatternEngine:

    def __init__(
        self,
        database_path: str | None = None,
    ):

        self.database_path = database_path or DEFAULT_DATABASE_PATH

        self.service = PatternService(
            self.database_path
        )

    def calculate(
        self,
        context: PatternContext,
    ) -> PatternResult:

        data = self.service.analyze(
            context
        )

        result = PatternResult(
            success=data.get(
                "success",
                False
            ),
            pattern=data.get(
                "pattern"
            ),
            score=float(data.get(
                "score",
                0
            ) or 0),
            priority=int(data.get(
                "priority",
                0
            ) or 0),
            matched_rules=list(data.get(
                "matched_rules",
                []
            ) or []),
            error=data.get(
                "error"
            ),
            description=data.get("description"),
            follow_type=data.get("follow_type") or None,
            candidate_patterns=list(data.get("candidate_patterns") or []),
            validated_patterns=list(data.get("validated_patterns") or []),
            final_pattern=data.get("final_pattern") or data.get("pattern"),
            secondary_patterns=list(data.get("secondary_patterns") or []),
            confidence=float(data.get("confidence", 0) or 0),
            reason=data.get("reason"),
            # Publish existing calculator signals only — never invent ranks/quality.
            pattern_rank=data.get("pattern_rank"),
            pattern_quality=data.get("pattern_quality"),
            combination_status=data.get("combination_status"),
            clash_status=data.get("clash_status"),
            success_reason=(
                data.get("success_reason")
                or data.get("reason")
                or (data.get("description") if data.get("success") else None)
            ),
            failure_reason=(
                data.get("failure_reason") or data.get("error")
            ),
            winning_rule_id=str(data.get("winning_rule_id") or ""),
            evidence_compact=str(data.get("evidence_compact") or ""),
            month_branch=str(data.get("month_branch") or ""),
            month_main_qi=str(data.get("month_main_qi") or ""),
            month_main_qi_ten_god=str(data.get("month_main_qi_ten_god") or ""),
            month_hidden_stems=[
                str(item) for item in (data.get("month_hidden_stems") or [])
            ],
            day_master=str(data.get("day_master") or ""),
            penetration_exact=(
                bool(data["penetration_exact"])
                if data.get("penetration_exact") is not None
                else None
            ),
            penetration_related=list(data.get("penetration_related") or []),
            fallback_used=bool(data.get("fallback_used")),
            ug_override_eligible=bool(data.get("ug_override_eligible")),
            qualification_level=(
                int(data["qualification_level"])
                if data.get("qualification_level") is not None
                else None
            ),
            detected_special_pattern=data.get("detected_special_pattern") or None,
        )
        override = classify_pattern_override(result.pattern, result.follow_type)
        result.ug_override_eligible = override.ug_override_eligible
        result.qualification_level = override.qualification_level
        result.detected_special_pattern = override.detected_special_pattern
        result.cach_cuc = pattern_display_label(
            result.pattern,
            result.description,
            ug_override_eligible=override.ug_override_eligible,
        )

        # Pattern Engine is the sole RuleContext producer.
        self._publish_rule_context(result, context)
        return result

    def _publish_rule_context(
        self,
        result: PatternResult,
        context: PatternContext,
    ) -> None:
        """
        Attach RuleContext to PatternResult for Score / Interpretation.

        Uses calendar / bazi (and optional strength / temperature hints) already
        present on PatternContext — does not invent upstream engine results.
        """
        calendar = getattr(context, "calendar", None)
        bazi = getattr(context, "bazi", None)
        if calendar is None and bazi is None:
            return

        strength_payload = None
        if getattr(context, "strength_level", None):
            strength_payload = {
                "level": context.strength_level,
                "score": float(getattr(context, "strength_score", 0.0) or 0.0),
            }
        temperature_payload = None
        if getattr(context, "temperature_type", None):
            temperature_payload = {"status": context.temperature_type}

        published = build_rule_context(
            calendar=calendar,
            bazi=bazi,
            pattern=result,
            strength=strength_payload,
            temperature=temperature_payload,
            shensha=getattr(context, "shensha", None),
        )
        # Keep RuleContext wire-clean for Score / Interpretation consumers.
        published.pop("_unified_context", None)
        enrich_result_from_rule_context(result, published)

    def clear_cache(self):

        self.service.clear_cache()
