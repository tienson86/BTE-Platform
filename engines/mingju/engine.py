"""MingJuDecisionEngine — canonical MC-01 runtime owner."""

from __future__ import annotations

from engines.mingju.achievement import evaluate_achievement
from engines.mingju.career import evaluate_career
from engines.mingju.compatibility import evaluate_climate_compatibility, evaluate_useful_god_compatibility
from engines.mingju.composer import compose_mingju_decision
from engines.mingju.damage import evaluate_damage
from engines.mingju.enums import AnalysisState, MingJuDecisionStatus
from engines.mingju.evidence import RecordBook
from engines.mingju.exceptions import MingJuVersionError
from engines.mingju.grade import evaluate_grade
from engines.mingju.integrity import evaluate_integrity
from engines.mingju.models import MingJuContext, MingJuDecisionResult
from engines.mingju.pattern import resolve_pattern
from engines.mingju.pattern_strength import evaluate_pattern_strength
from engines.mingju.purity import evaluate_purity
from engines.mingju.rescue import evaluate_rescue
from engines.mingju.serialization import clamp_confidence, compute_content_hash
from engines.mingju.support import evaluate_support
from engines.mingju.validators import validate_context, validate_result
from engines.mingju.versions import RULESET_VERSION, SCHEMA_CONTEXT, SCHEMA_DECISION
from engines.mingju.views import to_pack07_snapshot
from engines.mingju.wealth import evaluate_wealth


class MingJuDecisionEngine:
    """Canonical owner of Mệnh Cục structural synthesis."""

    def analyze(
        self,
        context: MingJuContext,
        *,
        ruleset_version: str | None = None,
    ) -> MingJuDecisionResult:
        """Run the frozen MC-01 pipeline and publish one MingJuDecisionResult."""
        validate_context(context)
        if ruleset_version and ruleset_version != RULESET_VERSION:
            raise MingJuVersionError(f"unsupported ruleset: {ruleset_version}")
        book = RecordBook()
        pattern = resolve_pattern(context, book)
        purity = evaluate_purity(context, pattern, book)
        pattern_strength = evaluate_pattern_strength(context, pattern, book)
        support = evaluate_support(context, pattern, book)
        damage = evaluate_damage(context, pattern, book)
        rescue = evaluate_rescue(context, damage, book)
        useful_god = evaluate_useful_god_compatibility(context, pattern, book)
        climate = evaluate_climate_compatibility(context, pattern, book)
        integrity = evaluate_integrity(
            context,
            purity,
            pattern_strength,
            support,
            damage,
            rescue,
            useful_god,
            climate,
            book,
        )
        grade = evaluate_grade(integrity, book)
        achievement = evaluate_achievement(context, pattern, integrity, grade, book)
        wealth = evaluate_wealth(context, integrity, book)
        career = evaluate_career(achievement, wealth, book)
        status = MingJuDecisionStatus.COMPLETE.value
        if pattern.state != AnalysisState.RESOLVED.value:
            status = MingJuDecisionStatus.INSUFFICIENT_EVIDENCE.value
        elif integrity.state == "unresolved" or grade.state != AnalysisState.RESOLVED.value:
            status = MingJuDecisionStatus.UNRESOLVED.value
        elif not context.hour_present:
            status = MingJuDecisionStatus.PARTIAL.value
        confidences = [
            pattern.confidence,
            purity.confidence,
            pattern_strength.confidence,
            integrity.confidence,
            grade.confidence,
        ]
        result = MingJuDecisionResult(
            analysis_id=context.analysis_id,
            chart_id=context.chart_id,
            schema_version=SCHEMA_DECISION,
            ruleset_version=RULESET_VERSION,
            context_schema_version=SCHEMA_CONTEXT,
            status=status,
            confidence=clamp_confidence(min((value for value in confidences if value > 0), default=0.0)),
            pattern=pattern,
            purity=purity,
            pattern_strength=pattern_strength,
            support=support,
            damage=damage,
            rescue=rescue,
            useful_god_compatibility=useful_god,
            climate_compatibility=climate,
            integrity=integrity,
            grade=grade,
            achievement=achievement,
            wealth=wealth,
            career=career,
            warnings=tuple(book.warnings),
            evidence=tuple(book.evidence),
            traces=tuple(book.traces),
            source_versions=dict(context.source_versions),
        )
        result.decision = compose_mingju_decision(result)
        result.trace_ids = tuple(item.trace_id for item in result.traces)
        snapshot = to_pack07_snapshot(result)
        snapshot.pop("content_hash", None)
        snapshot.pop("result_id", None)
        result.content_hash = compute_content_hash(snapshot)
        if context.analysis_id:
            result.result_id = f"mc01:{context.analysis_id}"
        else:
            result.result_id = f"mc01:{context.chart_id}:{result.content_hash[:16]}" if context.chart_id else (
                f"mc01:{result.content_hash[:16]}"
            )
        validate_result(result, context)
        return result
