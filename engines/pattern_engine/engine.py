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
            cach_cuc=pattern_display_label(
                data.get("pattern"),
                data.get("description"),
            ),
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
