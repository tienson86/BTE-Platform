"""Pack 07 stage validators. Guard contracts; do not reason."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

from engines.detailed_interpretation_engine.constants import (
    FORBIDDEN_OWNED_TRUTH_KEYS,
    MC01_GRADE_MISSING_CODE,
    MC01_HASH_MISMATCH_CODE,
    MC01_HASH_MISSING_CODE,
    MC01_LINEAGE_MISMATCH_CODE,
    MC01_NOT_BOUND_CODE,
    MC01_NOT_BOUND_MESSAGE,
    MC01_OWNERSHIP_DAMAGE_CODE,
    MC01_OWNERSHIP_RESCUE_CODE,
    MC01_PATTERN_MISSING_CODE,
    MC01_SNAPSHOT_HASH_CODE,
    PUBLISHED_DOMAIN_IDS,
    SCHEMA_CONTEXT,
    SCHEMA_EVIDENCE_PRIORITY,
    SCHEMA_LUCK_ACTIVATION,
    SCHEMA_RUNTIME_CONTRACT,
    SCHEMA_SHEN_SHA,
    SCHEMA_SHEN_SHA_ECOSYSTEM,
    SCHEMA_TEN_GOD_COMBINATIONS,
    SCHEMA_TEN_GODS,
    SCHEMA_TEN_GODS_BALANCE,
    TEMPORAL_LAYER_PARENT,
)
from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.context_layers import (
    CanonicalAnalysisContext,
    DomainContext,
    EvidenceContext,
    NarrativeContext,
    OptimizationContext,
    TemporalContext,
)
from engines.detailed_interpretation_engine.enums import (
    ActivationState,
    CombinationState,
    DomainState,
    EvaluationStatus,
    IssueSeverity,
    PriorityTier,
    ShenShaClusterState,
    ShenShaInterpretationState,
    ShenShaModifierState,
    TemporalLayer,
    ValidationStatus,
)
from engines.detailed_interpretation_engine.exceptions import DetailedInterpretationValidationError
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult, DomainSection
from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    DOMAIN_DRIVER_IDS,
    FORBIDDEN_AUTHORITY_DRIVER_IDS,
    FORBIDDEN_VITALITY_DRIVER_IDS,
    FORBIDDEN_WEALTH_DRIVER_IDS,
    GRAPH_RELATIONS,
    KNOWN_DOMAIN_IDS,
    MAIN_DOMAIN_IDS,
    MAJOR_DAMAGE_TYPES,
    SHEN_SHA_SOURCE_KINDS as DOMAIN_SHEN_SHA_KINDS,
)
from engines.detailed_interpretation_engine.domain_interpretation.labels import DAMAGE_LABELS, DRIVER_LABELS
from engines.detailed_interpretation_engine.luck_activation.constants import (
    ACTIVATION_DRIVER_IDS,
    ACTIVATION_TYPES,
    KNOWN_ACTIVATION_IDS,
    MAIN_ACTIVATION_IDS,
)
from engines.detailed_interpretation_engine.luck_activation.models import (
    ACTIVATION_GRAPH_RELATIONS,
    DomainActivationResult,
)
from engines.detailed_interpretation_engine.luck_interaction.validation import (
    validate_luck_interaction_result,
)
from engines.detailed_interpretation_engine.temporal import LuckActivationResult
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult
from engines.detailed_interpretation_engine.evidence_priority.constants import (
    SHEN_SHA_SOURCE_KINDS,
    SHEN_SHA_TIER_CEILING,
    TIER_INDEX,
)
from engines.detailed_interpretation_engine.mc01 import snapshot_hash_matches
from engines.detailed_interpretation_engine.runtime import (
    CanonicalAPIModel,
    CanonicalConsultingModel,
    CanonicalExportModel,
    CanonicalRuntimeResult,
)
from engines.detailed_interpretation_engine.schema_registry import registered_schema_ids
from engines.detailed_interpretation_engine.serialization import (
    compute_content_hash,
    serialize_runtime_result,
    to_jsonable,
)
from engines.detailed_interpretation_engine.shen_sha.constants import (
    APPLIED_MODIFIERS,
    CANONICAL_CLUSTER_IDS,
    KNOWN_STAR_IDS,
)
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import (
    FAMILY_MEMBERS,
    V1_COMBINATION_IDS,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodCombinationCollection,
)
from engines.detailed_interpretation_engine.ten_gods.constants import (
    CANONICAL_TEN_GOD_IDS,
    FORBIDDEN_ALIAS_IDS,
)
from engines.detailed_interpretation_engine.ten_gods.ecosystem.constants import FAMILY_GODS
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import TenGodEcosystemResult
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult, result_from_issues


EVALUATED_STATUSES: frozenset[EvaluationStatus] = frozenset(
    {
        EvaluationStatus.RESOLVED,
        EvaluationStatus.PARTIALLY_RESOLVED,
        EvaluationStatus.CONFLICTING_EVIDENCE,
        EvaluationStatus.INSUFFICIENT_EVIDENCE,
    }
)
_LAYER_VALUES: frozenset[str] = frozenset(item.value for item in TemporalLayer)
_OWNER_CODES: dict[str, str] = {
    "pattern": "P7V-OWNERSHIP-PATTERN",
    "grade": "P7V-OWNERSHIP-GRADE",
    "integrity": "P7V-OWNERSHIP-INTEGRITY",
    "achievement": "P7V-OWNERSHIP-ACHIEVEMENT",
    "wealth_profile": "P7V-OWNERSHIP-WEALTH-PROFILE",
    "career_profile": "P7V-OWNERSHIP-CAREER-PROFILE",
}


@dataclass(slots=True)
class _Bag:
    """Mutable issue collector for one validator pass."""

    validator: str
    analysis_id: str
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(
        self,
        code: str,
        severity: IssueSeverity,
        layer: str,
        message: str,
        *,
        field: str = "",
        expected: str = "",
        actual: str = "",
        trace_id: str = "",
    ) -> None:
        """Record one issue with validator, analysis_id, and trace."""
        self.issues.append(
            ValidationIssue(
                code=code,
                severity=severity,
                layer=layer,
                field=field,
                message=message,
                expected=expected,
                actual=actual,
                trace_id=trace_id or f"p7v-{uuid4().hex[:12]}",
                validator=self.validator,
                analysis_id=self.analysis_id,
            )
        )

    def finish(self) -> ValidationResult:
        """Fold collected issues."""
        return result_from_issues(self.issues, analysis_id=self.analysis_id)


def _supported_schema(version: str) -> bool:
    if not version:
        return False
    if version in registered_schema_ids():
        return True
    prefix = version.rsplit(".", 1)[0]
    return any(item.startswith(prefix) for item in registered_schema_ids())


def _require_analysis_id(bag: _Bag, analysis_id: str, layer: str) -> None:
    if not (analysis_id or "").strip():
        bag.add(
            "P7V-CTX-ANALYSIS-ID-MISSING",
            IssueSeverity.CRITICAL,
            layer,
            "analysis_id is required",
            field="analysis_id",
            expected="non-empty analysis_id",
            actual=analysis_id,
        )


def _match_id(
    bag: _Bag,
    expected: str,
    actual: str,
    layer: str,
    field: str,
    code: str = "P7V-CTX-ANALYSIS-ID-MISMATCH",
) -> None:
    if actual and expected and actual != expected:
        bag.add(
            code,
            IssueSeverity.CRITICAL,
            layer,
            "analysis_id mismatch",
            field=field,
            expected=expected,
            actual=actual,
        )


def _check_schema(bag: _Bag, version: str, layer: str, field: str = "schema_version") -> None:
    if not _supported_schema(version):
        bag.add(
            "P7V-VERSION-UNSUPPORTED",
            IssueSeverity.CRITICAL,
            layer,
            "unsupported schema version",
            field=field,
            expected="registered Pack 07 schema id",
            actual=version,
        )


def validate_interpretation_context(context: InterpretationContext) -> ValidationResult:
    """Validate identity-only InterpretationContext. No interpretation."""
    bag = _Bag("validate_interpretation_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "interpretation")
    _match_id(bag, context.analysis_id, context.chart_identity.analysis_id, "interpretation", "chart_identity.analysis_id")
    _check_schema(bag, context.schema_version or SCHEMA_CONTEXT, "interpretation")
    _check_schema(bag, context.versions.contract_version, "interpretation", "versions.contract_version")
    if not context.chart_identity.analysis_id and not context.chart_identity.birth_civil:
        bag.add(
            "P7V-CTX-CALENDAR-IDENTITY",
            IssueSeverity.WARNING,
            "interpretation",
            "calendar identity is empty",
            field="chart_identity",
        )
    if not context.mc01.mingju_result_id:
        bag.add(
            MC01_NOT_BOUND_CODE,
            IssueSeverity.WARNING,
            "interpretation",
            MC01_NOT_BOUND_MESSAGE,
            field="mc01",
            expected="bound Mc01Reference",
            actual="not_bound",
        )
        return bag.finish()
    if not context.mc01.content_hash:
        bag.add(
            MC01_HASH_MISSING_CODE,
            IssueSeverity.CRITICAL,
            "interpretation",
            "bound MC-01 reference requires content_hash",
            field="mc01.content_hash",
        )
    if not context.pattern_ref:
        bag.add(
            MC01_PATTERN_MISSING_CODE,
            IssueSeverity.CRITICAL,
            "interpretation",
            "bound MC-01 reference requires Pattern",
            field="pattern_ref",
        )
    if not context.grade_ref:
        bag.add(
            MC01_GRADE_MISSING_CODE,
            IssueSeverity.CRITICAL,
            "interpretation",
            "bound MC-01 reference requires Grade",
            field="grade_ref",
        )
    if context.analysis_id and context.mc01.mingju_result_id.startswith("mc01:"):
        lineage = context.mc01.mingju_result_id[5:]
        if lineage != context.analysis_id and not lineage.startswith(f"{context.chart_id}:"):
            bag.add(
                MC01_LINEAGE_MISMATCH_CODE,
                IssueSeverity.CRITICAL,
                "interpretation",
                "MC-01 lineage does not match analysis_id",
                field="mc01.mingju_result_id",
                expected=f"mc01:{context.analysis_id}",
                actual=context.mc01.mingju_result_id,
            )
    if context.mingju_content_hash and context.mc01.content_hash:
        if context.mingju_content_hash != context.mc01.content_hash:
            bag.add(
                MC01_HASH_MISMATCH_CODE,
                IssueSeverity.CRITICAL,
                "interpretation",
                "MC-01 content_hash mismatch",
                field="mc01.content_hash",
                expected=context.mingju_content_hash,
                actual=context.mc01.content_hash,
            )
    return bag.finish()


def validate_evidence_context(context: EvidenceContext) -> ValidationResult:
    """Empty not_evaluated evidence is valid. Evaluated without sources is not."""
    bag = _Bag("validate_evidence_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "evidence")
    _check_schema(bag, context.schema_version, "evidence")
    evaluated = context.status in EVALUATED_STATUSES or context.evidence.status in EVALUATED_STATUSES
    if evaluated and not (context.evidence.evidence_ids or context.evidence.trace_ids):
        bag.add(
            "P7V-EVIDENCE-EVALUATED-EMPTY",
            IssueSeverity.ERROR,
            "evidence",
            "evaluated evidence requires source refs",
            field="evidence.evidence_ids",
            expected="evidence_ids or trace_ids",
            actual="empty",
        )
    return bag.finish()


def validate_domain_context(context: DomainContext) -> ValidationResult:
    """Six natal shells may be empty not_evaluated. Evaluated needs sources."""
    bag = _Bag("validate_domain_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "domain")
    _check_schema(bag, context.schema_version, "domain")
    for natal in (
        context.authority.natal,
        context.career.natal,
        context.wealth.natal,
        context.relationship.natal,
        context.legacy.natal,
        context.vitality.natal,
    ):
        if natal.domain_id not in PUBLISHED_DOMAIN_IDS:
            bag.add(
                "P7V-CTX-REF-SHAPE",
                IssueSeverity.ERROR,
                "domain",
                "unknown domain shell id",
                field="domain_id",
                actual=natal.domain_id,
            )
        evaluated = natal.state not in (DomainState.NOT_EVALUATED, DomainState.UNRESOLVED)
        if evaluated and not natal.supporting_evidence_ids and not natal.trace_ids and not natal.evidence_ids:
            bag.add(
                "P7V-DOMAIN-EVALUATED-EMPTY",
                IssueSeverity.ERROR,
                "domain",
                "evaluated domain shell requires source refs",
                field=f"{natal.domain_id}.supporting_evidence_ids",
            )
        if natal.driver_source.lower().startswith("shen_sha") or "shen_sha" in natal.driver_source:
            bag.add(
                "P7V-DOMAIN-SHEN-SHA-DRIVER",
                IssueSeverity.CRITICAL,
                "domain",
                "Shen Sha cannot be Domain Driver",
                field=f"{natal.domain_id}.driver_source",
                actual=natal.driver_source,
            )
    return bag.finish()


def validate_temporal_context(context: TemporalContext) -> ValidationResult:
    """Validate layer enum and parent relation. No activation."""
    bag = _Bag("validate_temporal_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "temporal")
    _check_schema(bag, context.schema_version, "temporal")
    activation = context.temporal
    for layer in activation.requested_layers + activation.evaluated_layers:
        if layer and layer not in _LAYER_VALUES:
            bag.add(
                "P7V-TEMPORAL-LAYER",
                IssueSeverity.ERROR,
                "temporal",
                "unknown temporal layer",
                field="requested_layers",
                expected="luck_cycle|annual|monthly|daily|hourly",
                actual=layer,
            )
    if "hourly" in activation.requested_layers and "hourly" not in activation.evaluated_layers:
        bag.add(
            "P7V-TEMPORAL-LAYER",
            IssueSeverity.WARNING,
            "temporal",
            "hourly layer not evaluated",
            field="evaluated_layers",
        )
    if "monthly" in activation.requested_layers and "monthly" not in activation.evaluated_layers:
        bag.add(
            "P7V-TEMPORAL-LAYER",
            IssueSeverity.WARNING,
            "temporal",
            "optional monthly layer not evaluated",
            field="evaluated_layers",
        )
    if activation.active_layer in TEMPORAL_LAYER_PARENT:
        expected_parent = TEMPORAL_LAYER_PARENT[activation.active_layer]
        if activation.parent_layer and activation.parent_layer != expected_parent:
            bag.add(
                "P7V-TEMPORAL-PARENT",
                IssueSeverity.ERROR,
                "temporal",
                "parent-child layer relation is invalid",
                field="parent_layer",
                expected=expected_parent,
                actual=activation.parent_layer,
            )
    return bag.finish()


def validate_optimization_context(context: OptimizationContext) -> ValidationResult:
    """not_evaluated is valid. Actions without a supporting result fail."""
    bag = _Bag("validate_optimization_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "optimization")
    _check_schema(bag, context.schema_version, "optimization")
    inputs = context.inputs
    if inputs.actions and (inputs.state is EvaluationStatus.NOT_EVALUATED or not inputs.evidence_ids):
        bag.add(
            "P7V-OPTIMIZATION-ACTION-NO-RESULT",
            IssueSeverity.ERROR,
            "optimization",
            "optimization actions require a supporting result",
            field="inputs.actions",
        )
    for domain_id in inputs.domain_plans:
        if domain_id not in PUBLISHED_DOMAIN_IDS:
            bag.add(
                "P7V-CTX-REF-SHAPE",
                IssueSeverity.ERROR,
                "optimization",
                "action references unknown domain",
                field="inputs.domain_plans",
                actual=domain_id,
            )
    return bag.finish()


def validate_narrative_context(context: NarrativeContext) -> ValidationResult:
    """not_evaluated is valid. Nodes must not invent unknown evidence."""
    bag = _Bag("validate_narrative_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "narrative")
    _check_schema(bag, context.schema_version, "narrative")
    known = set(context.inputs.result.trace)
    evaluated = context.inputs.result.status in EVALUATED_STATUSES
    for node in context.inputs.graph.nodes:
        for evidence_id in node.evidence_ids:
            if known and evidence_id not in known:
                bag.add(
                    "P7V-NARRATIVE-UNKNOWN-EVIDENCE",
                    IssueSeverity.ERROR,
                    "narrative",
                    "narrative node references unknown evidence IDs",
                    field="graph.nodes.evidence_ids",
                    actual=evidence_id,
                )
        if evaluated and not node.evidence_ids:
            bag.add(
                "P7V-NARRATIVE-UNKNOWN-EVIDENCE",
                IssueSeverity.ERROR,
                "narrative",
                "evaluated narrative claims require source refs",
                field="graph.nodes",
            )
    return bag.finish()


def _payload_for_stable_hash(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Match factory hashing: created_at excluded, content_hash not part of digest."""
    clone = to_jsonable(payload)
    if not isinstance(clone, dict):
        return {}
    meta = clone.get("metadata")
    if isinstance(meta, dict):
        meta["content_hash"] = ""
    return clone


def _scan_owned_truth(bag: _Bag, payload: Mapping[str, Any], layer: str) -> None:
    for key in FORBIDDEN_OWNED_TRUTH_KEYS:
        if key not in payload or payload.get(key) in (None, "", {}, []):
            continue
        bag.add(
            _OWNER_CODES.get(key, "P7V-RUNTIME-LAYER-OWNERSHIP"),
            IssueSeverity.CRITICAL,
            layer,
            "Pack 07 must not publish this upstream truth as owned",
            field=key,
            expected="reference only",
            actual="owned payload present",
        )


def _collect_ids(items: Any, field_name: str) -> set[str]:
    found: set[str] = set()
    if not isinstance(items, (list, tuple)):
        return found
    for item in items:
        if not isinstance(item, Mapping):
            continue
        for token in item.get(field_name) or ():
            text = str(token).strip()
            if text:
                found.add(text)
    return found


def _allowed_structural_ids(runtime: CanonicalRuntimeResult, field_name: str) -> set[str]:
    snapshot = runtime.mc01_snapshot
    payload: Mapping[str, Any] = {}
    if isinstance(snapshot, Mapping):
        payload = snapshot
    elif snapshot:
        try:
            loaded = json.loads(snapshot)
        except (TypeError, ValueError):
            loaded = {}
        if isinstance(loaded, Mapping):
            payload = loaded
    allowed = {str(item).strip() for item in payload.get(field_name) or () if str(item).strip()}
    return allowed


def validate_canonical_runtime(
    result: CanonicalRuntimeResult | Mapping[str, Any],
) -> ValidationResult:
    """Validate CanonicalRuntimeResult: one analysis_id, versions, ownership."""
    payload = result if isinstance(result, Mapping) else serialize_runtime_result(result)
    if not isinstance(payload, Mapping):
        bag = _Bag("validate_canonical_runtime", "")
        bag.add(
            "P7V-RUNTIME-ROOT",
            IssueSeverity.CRITICAL,
            "runtime",
            "invalid runtime root",
            field="CanonicalRuntimeResult",
        )
        return bag.finish()
    runtime = (
        result
        if isinstance(result, CanonicalRuntimeResult)
        else CanonicalRuntimeResult.from_dict(payload)
    )
    analysis_id = runtime.analysis_id
    bag = _Bag("validate_canonical_runtime", analysis_id)
    _require_analysis_id(bag, analysis_id, "runtime")
    _match_id(
        bag, analysis_id, runtime.identity.analysis_id, "runtime", "identity.analysis_id",
        "P7V-RUNTIME-ANALYSIS-ID",
    )
    _match_id(
        bag, analysis_id, runtime.metadata.analysis_id, "runtime", "metadata.analysis_id",
        "P7V-RUNTIME-ANALYSIS-ID",
    )
    _check_schema(
        bag,
        runtime.metadata.contract_version or SCHEMA_RUNTIME_CONTRACT,
        "runtime",
        "contract_version",
    )
    _check_schema(bag, runtime.metadata.schema_version, "runtime", "schema_version")
    _scan_owned_truth(bag, payload, "runtime")
    interpretation = payload.get("interpretation")
    if isinstance(interpretation, Mapping):
        _scan_owned_truth(bag, interpretation, "interpretation")
    domains = payload.get("domains")
    if isinstance(domains, Mapping):
        _scan_owned_truth(bag, domains, "domains")
    if runtime.mc01.mingju_result_id and runtime.mc01.content_hash:
        if runtime.mc01_snapshot and not snapshot_hash_matches(
            runtime.mc01_snapshot, runtime.mc01.content_hash
        ):
            bag.add(
                MC01_SNAPSHOT_HASH_CODE,
                IssueSeverity.CRITICAL,
                "runtime",
                "MC-01 snapshot hash does not match content_hash",
                field="mc01_snapshot",
                expected=runtime.mc01.content_hash,
            )
        allowed_damage = _allowed_structural_ids(runtime, "damage_ids")
        allowed_rescue = _allowed_structural_ids(runtime, "rescue_ids")
        ten_gods = payload.get("interpretation")
        natal_items = ()
        combo_items = ()
        if isinstance(ten_gods, Mapping):
            shell = ten_gods.get("ten_gods")
            if isinstance(shell, Mapping):
                natal = shell.get("natal")
                combos = shell.get("combinations")
                if isinstance(natal, Mapping):
                    natal_items = natal.get("items") or ()
                if isinstance(combos, Mapping):
                    combo_items = combos.get("items") or ()
        claimed_damage = _collect_ids(natal_items, "damage_ids") | _collect_ids(combo_items, "damage_ids")
        claimed_rescue = _collect_ids(natal_items, "rescue_ids") | _collect_ids(combo_items, "rescue_ids")
        invented_damage = claimed_damage - allowed_damage
        invented_rescue = claimed_rescue - allowed_rescue
        if invented_damage:
            bag.add(
                MC01_OWNERSHIP_DAMAGE_CODE,
                IssueSeverity.CRITICAL,
                "interpretation",
                "Pack 07 must not create Damage IDs",
                field="damage_ids",
                expected="MC-01 damage refs only",
                actual=",".join(sorted(invented_damage)),
            )
        if invented_rescue:
            bag.add(
                MC01_OWNERSHIP_RESCUE_CODE,
                IssueSeverity.CRITICAL,
                "interpretation",
                "Pack 07 must not create Rescue IDs",
                field="rescue_ids",
                expected="MC-01 rescue refs only",
                actual=",".join(sorted(invented_rescue)),
            )
    expected_hash = compute_content_hash(_payload_for_stable_hash(payload))
    actual_hash = runtime.metadata.content_hash
    if actual_hash and actual_hash != expected_hash:
        bag.add(
            "P7V-RUNTIME-HASH",
            IssueSeverity.ERROR,
            "runtime",
            "content_hash is not stable for canonical payload",
            field="metadata.content_hash",
            expected=expected_hash,
            actual=actual_hash,
        )
    return bag.finish()


def validate_export_projection(
    model: CanonicalExportModel,
    result: CanonicalRuntimeResult,
) -> ValidationResult:
    """Export projection must share analysis_id and not create a second truth."""
    bag = _Bag("validate_export_projection", result.analysis_id)
    _require_analysis_id(bag, model.analysis_id, "export")
    _match_id(
        bag, result.analysis_id, model.analysis_id, "export", "analysis_id",
        "P7V-PROJECTION-ANALYSIS-ID",
    )
    return bag.finish()


def validate_api_projection(model: CanonicalAPIModel, result: CanonicalRuntimeResult) -> ValidationResult:
    """API projection must wrap the same CanonicalRuntimeResult."""
    bag = _Bag("validate_api_projection", result.analysis_id)
    _require_analysis_id(bag, model.analysis_id, "api")
    _match_id(
        bag, result.analysis_id, model.analysis_id, "api", "analysis_id",
        "P7V-PROJECTION-ANALYSIS-ID",
    )
    _match_id(
        bag, result.analysis_id, model.contract.analysis_id, "api", "contract.analysis_id",
        "P7V-PROJECTION-ANALYSIS-ID",
    )
    left = model.contract.metadata.content_hash
    right = result.metadata.content_hash
    if left and right and left != right:
        bag.add(
            "P7V-PROJECTION-SECOND-TRUTH",
            IssueSeverity.CRITICAL,
            "api",
            "API projection must not create a second truth",
            field="contract.metadata.content_hash",
            expected=right,
            actual=left,
        )
    return bag.finish()


def validate_consulting_projection(
    model: CanonicalConsultingModel,
    result: CanonicalRuntimeResult,
) -> ValidationResult:
    """Consulting projection must share analysis_id."""
    bag = _Bag("validate_consulting_projection", result.analysis_id)
    _require_analysis_id(bag, model.analysis_id, "consulting")
    _match_id(
        bag, result.analysis_id, model.analysis_id, "consulting", "analysis_id",
        "P7V-PROJECTION-ANALYSIS-ID",
    )
    return bag.finish()


def validate_ten_gods_collection(collection: TenGodInterpretationCollection) -> ValidationResult:
    """Validate natal Ten God collection. No identity-only conclusions."""
    bag = _Bag("validate_ten_gods_collection", collection.analysis_id)
    if collection.state is EvaluationStatus.NOT_EVALUATED and not collection.items:
        return bag.finish()
    _check_schema(bag, collection.schema_version or SCHEMA_TEN_GODS, "ten_gods")
    ids = tuple(item.ten_god_id for item in collection.items)
    if len(collection.items) != len(CANONICAL_TEN_GOD_IDS):
        bag.add(
            "P7V-TG-COUNT",
            IssueSeverity.CRITICAL,
            "ten_gods",
            "collection must include all 10 Ten Gods",
            field="items",
            expected=str(len(CANONICAL_TEN_GOD_IDS)),
            actual=str(len(collection.items)),
        )
    if any(god_id in FORBIDDEN_ALIAS_IDS for god_id in ids):
        bag.add(
            "P7V-TG-ALIAS",
            IssueSeverity.CRITICAL,
            "ten_gods",
            "Thiên Quan is not a separate Ten God identity",
            field="ten_god_id",
            expected="qi_sha",
            actual="thien_quan",
        )
    missing = [god_id for god_id in CANONICAL_TEN_GOD_IDS if god_id not in ids]
    if missing:
        bag.add(
            "P7V-TG-MISSING",
            IssueSeverity.ERROR,
            "ten_gods",
            "canonical Ten God missing from collection",
            field="items",
            expected=",".join(CANONICAL_TEN_GOD_IDS),
            actual=",".join(missing),
        )
    for item in collection.items:
        if item.state not in {EvaluationStatus.UNRESOLVED, EvaluationStatus.NOT_EVALUATED}:
            if not item.trace_ids:
                bag.add(
                    "P7V-TG-TRACE",
                    IssueSeverity.ERROR,
                    "ten_gods",
                    "material Ten God result requires trace",
                    field=item.ten_god_id,
                )
    return bag.finish()


_KNOWN_SUBJECTS: frozenset[str] = frozenset(
    CANONICAL_TEN_GOD_IDS
    + ("day_master",)
    + tuple(FAMILY_MEMBERS)
    + tuple(FAMILY_GODS)
)


def validate_ten_god_combinations(
    collection: TenGodCombinationCollection,
    *,
    natal: TenGodInterpretationCollection | None = None,
) -> ValidationResult:
    """Validate combination analysis_id, participants, and chain refs."""
    bag = _Bag("validate_ten_god_combinations", collection.analysis_id)
    if collection.state is EvaluationStatus.NOT_EVALUATED and not collection.items:
        return bag.finish()
    _check_schema(bag, collection.schema_version or SCHEMA_TEN_GOD_COMBINATIONS, "ten_god_combinations")
    natal_ids = {item.ten_god_id for item in natal.items} if natal is not None else set(CANONICAL_TEN_GOD_IDS)
    known_ids = natal_ids | {"day_master"} | set(FAMILY_MEMBERS) | set(FAMILY_GODS)
    combo_ids = {item.combination_id for item in collection.items}
    for item in collection.items:
        if item.combination_id and item.combination_id not in V1_COMBINATION_IDS:
            bag.add(
                "P7V-COMB-UNKNOWN-ID",
                IssueSeverity.ERROR,
                "ten_god_combinations",
                "unknown combination id",
                field="combination_id",
                actual=item.combination_id,
            )
        if item.state not in {CombinationState.INACTIVE, CombinationState.UNRESOLVED}:
            if not item.trace_ids:
                bag.add(
                    "P7V-COMB-TRACE",
                    IssueSeverity.ERROR,
                    "ten_god_combinations",
                    "material combination requires trace",
                    field=item.combination_id,
                )
        for participant in item.participants:
            if participant.ten_god_id and participant.ten_god_id not in known_ids:
                bag.add(
                    "P7V-COMB-PARTICIPANT",
                    IssueSeverity.CRITICAL,
                    "ten_god_combinations",
                    "participant does not exist in natal Ten Gods",
                    field=item.combination_id,
                    actual=participant.ten_god_id,
                )
        for node in item.chain.nodes:
            if node and node not in known_ids:
                bag.add(
                    "P7V-COMB-CHAIN-REF",
                    IssueSeverity.CRITICAL,
                    "ten_god_combinations",
                    "chain node is not a known Ten God or family",
                    field=item.combination_id,
                    actual=node,
                )
        if item.source_combination_id and item.source_combination_id not in combo_ids:
            bag.add(
                "P7V-COMB-CHAIN-REF",
                IssueSeverity.CRITICAL,
                "ten_god_combinations",
                "source_combination_id is unknown",
                field=item.combination_id,
                actual=item.source_combination_id,
            )
    return bag.finish()


def validate_ten_god_ecosystem(
    result: TenGodEcosystemResult,
    *,
    natal: TenGodInterpretationCollection | None = None,
    combinations: TenGodCombinationCollection | None = None,
) -> ValidationResult:
    """Validate ecosystem refs, driver basis, and bottleneck chain membership."""
    bag = _Bag("validate_ten_god_ecosystem", result.analysis_id)
    if result.state is EvaluationStatus.NOT_EVALUATED and not result.trace_ids:
        return bag.finish()
    _check_schema(bag, result.schema_version or SCHEMA_TEN_GODS_BALANCE, "ten_gods_ecosystem")
    forbidden_basis = {"count", "occurrence_count", "frequency", "raw_count"}
    if any(token in forbidden_basis for token in result.driver.basis):
        bag.add(
            "P7V-ECO-DRIVER-COUNT",
            IssueSeverity.CRITICAL,
            "ten_gods_ecosystem",
            "driver must not be derived from raw frequency",
            field="driver.basis",
            actual=",".join(result.driver.basis),
        )
    active_chain_ids: set[str] = set()
    if combinations is not None:
        active_chain_ids = {
            item.chain.chain_id
            for item in combinations.items
            if item.state
            in {
                CombinationState.CONFIRMED,
                CombinationState.CONDITIONAL,
                CombinationState.WEAK,
            }
            and item.chain.chain_id
        }
        known_chains = {item.chain.chain_id for item in combinations.items if item.chain.chain_id}
        for chain_id in (
            result.bottleneck.source_chain_ids
            + result.support.source_chain_ids
            + result.blocked.source_chain_ids
        ):
            if chain_id and chain_id not in known_chains:
                bag.add(
                    "P7V-ECO-CHAIN-REF",
                    IssueSeverity.CRITICAL,
                    "ten_gods_ecosystem",
                    "ecosystem references unknown combination chain",
                    field="source_chain_ids",
                    actual=chain_id,
                )
    if result.bottleneck.state in EVALUATED_STATUSES:
        if not result.bottleneck.source_chain_ids:
            bag.add(
                "P7V-ECO-BOTTLENECK-CHAIN",
                IssueSeverity.CRITICAL,
                "ten_gods_ecosystem",
                "bottleneck must belong to an active chain",
                field="bottleneck.source_chain_ids",
            )
        elif combinations is not None and not set(result.bottleneck.source_chain_ids) & active_chain_ids:
            bag.add(
                "P7V-ECO-BOTTLENECK-CHAIN",
                IssueSeverity.CRITICAL,
                "ten_gods_ecosystem",
                "bottleneck must belong to an active chain",
                field="bottleneck.source_chain_ids",
                actual=",".join(result.bottleneck.source_chain_ids),
            )
    natal_ids = {item.ten_god_id for item in natal.items} if natal is not None else set(CANONICAL_TEN_GOD_IDS)
    for assignment in (
        result.driver,
        result.support,
        result.suppressed,
        result.blocked,
        result.excessive,
        result.deficient,
        result.missing,
        result.bottleneck,
        result.balancer,
    ) + result.neutral:
        if assignment.subject and assignment.subject not in natal_ids | _KNOWN_SUBJECTS:
            bag.add(
                "P7V-ECO-SUBJECT",
                IssueSeverity.CRITICAL,
                "ten_gods_ecosystem",
                "ecosystem subject is not a known Ten God or family",
                field=assignment.role.value,
                actual=assignment.subject,
            )
    return bag.finish()


def validate_shen_sha_collection(collection: ShenShaInterpretationCollection) -> ValidationResult:
    """Validate known star IDs, traces, and no structural ownership."""
    bag = _Bag("validate_shen_sha_collection", collection.analysis_id)
    if collection.state is EvaluationStatus.NOT_EVALUATED and not collection.items:
        return bag.finish()
    _check_schema(bag, collection.schema_version or SCHEMA_SHEN_SHA, "shen_sha")
    _match_id(
        bag,
        collection.analysis_id,
        collection.analysis_id,
        "shen_sha",
        "analysis_id",
        "P7V-SS-ANALYSIS-ID",
    )
    payload = to_jsonable(collection)
    if isinstance(payload, Mapping):
        _scan_owned_truth(bag, payload, "shen_sha")
        for forbidden in ("pattern", "grade", "driver", "bottleneck", "wealth_profile", "career_profile"):
            if forbidden in payload and payload.get(forbidden) not in (None, "", {}, []):
                bag.add(
                    "P7V-SS-NO-STRUCTURAL-OWNERSHIP",
                    IssueSeverity.CRITICAL,
                    "shen_sha",
                    "Shen Sha must not own structural truth",
                    field=forbidden,
                )
    for item in collection.items:
        if item.shen_sha_id not in KNOWN_STAR_IDS:
            bag.add(
                "P7V-SS-UNKNOWN-ID",
                IssueSeverity.CRITICAL,
                "shen_sha",
                "unknown star ID",
                field="shen_sha_id",
                actual=item.shen_sha_id,
            )
        if item.detected and item.modifier_state is ShenShaModifierState.APPLIED:
            if not item.supported_domains:
                bag.add(
                    "P7V-SS-UNSUPPORTED-PROMOTION",
                    IssueSeverity.CRITICAL,
                    "shen_sha",
                    "applied modifier requires a supported domain",
                    field=item.shen_sha_id,
                )
        if item.detected and item.state is not ShenShaInterpretationState.NOT_DETECTED:
            if not item.trace_ids:
                bag.add(
                    "P7V-SS-TRACE",
                    IssueSeverity.ERROR,
                    "shen_sha",
                    "detected star requires trace",
                    field=item.shen_sha_id,
                )
    return bag.finish()


def validate_shen_sha_ecosystem(
    result: ShenShaEcosystemResult,
    *,
    individual: ShenShaInterpretationCollection | None = None,
) -> ValidationResult:
    """Validate cluster IDs, member refs, and blocked-star activation."""
    bag = _Bag("validate_shen_sha_ecosystem", result.analysis_id)
    if result.state is EvaluationStatus.NOT_EVALUATED and not result.clusters:
        return bag.finish()
    _check_schema(bag, result.schema_version or SCHEMA_SHEN_SHA_ECOSYSTEM, "shen_sha_ecosystem")
    if individual is not None and individual.analysis_id and result.analysis_id:
        _match_id(
            bag,
            individual.analysis_id,
            result.analysis_id,
            "shen_sha_ecosystem",
            "analysis_id",
            "P7V-SS-ECO-ANALYSIS-ID",
        )
    known_stars = {item.shen_sha_id for item in individual.items} if individual is not None else set(KNOWN_STAR_IDS)
    lookup = {item.shen_sha_id: item for item in individual.items} if individual is not None else {}
    for cluster in result.clusters:
        if cluster.cluster_id not in CANONICAL_CLUSTER_IDS:
            bag.add(
                "P7V-SS-UNKNOWN-CLUSTER",
                IssueSeverity.CRITICAL,
                "shen_sha_ecosystem",
                "unknown cluster id",
                field="cluster_id",
                actual=cluster.cluster_id,
            )
        for member in cluster.members:
            if member.shen_sha_id and member.shen_sha_id not in known_stars:
                bag.add(
                    "P7V-SS-CLUSTER-MEMBER-REF",
                    IssueSeverity.CRITICAL,
                    "shen_sha_ecosystem",
                    "cluster member is not in individual Shen Sha results",
                    field=cluster.cluster_id,
                    actual=member.shen_sha_id,
                )
        if cluster.state is ShenShaClusterState.ACTIVE:
            if not cluster.applied_members:
                bag.add(
                    "P7V-SS-BLOCKED-CLUSTER-ACTIVE",
                    IssueSeverity.CRITICAL,
                    "shen_sha_ecosystem",
                    "blocked stars cannot form an applied cluster alone",
                    field=cluster.cluster_id,
                )
            if individual is not None:
                blocked_only = True
                for star_id in cluster.applied_members:
                    item = lookup.get(star_id)
                    if item is not None and item.modifier_state.value in APPLIED_MODIFIERS:
                        blocked_only = False
                        break
                if cluster.applied_members and blocked_only:
                    bag.add(
                        "P7V-SS-BLOCKED-CLUSTER-ACTIVE",
                        IssueSeverity.CRITICAL,
                        "shen_sha_ecosystem",
                        "blocked stars cannot form an applied cluster alone",
                        field=cluster.cluster_id,
                    )
        if cluster.state is ShenShaClusterState.ACTIVE and not cluster.trace_ids:
            bag.add(
                "P7V-SS-CLUSTER-TRACE",
                IssueSeverity.ERROR,
                "shen_sha_ecosystem",
                "applied cluster requires trace",
                field=cluster.cluster_id,
            )
    return bag.finish()


def validate_evidence_priority_result(
    result: EvidencePriorityResult,
    *,
    context: CanonicalAnalysisContext | None = None,
    payload: Mapping[str, Any] | None = None,
) -> ValidationResult:
    """Validate ranked evidence: tiers, traces, merge, Shen Sha ceiling, grade split."""
    analysis_id = result.analysis_id or (context.analysis_id if context else "")
    bag = _Bag("validate_evidence_priority_result", analysis_id)
    _check_schema(bag, result.schema_version or SCHEMA_EVIDENCE_PRIORITY, "evidence_priority")
    if context is not None:
        _match_id(
            bag,
            context.analysis_id,
            result.analysis_id or context.analysis_id,
            "evidence_priority",
            "analysis_id",
            "P7V-EPR-ANALYSIS-ID",
        )
    evaluated = result.status in EVALUATED_STATUSES
    if not evaluated:
        return bag.finish()
    if not result.trace_ids and not result.evidence_ids:
        bag.add(
            "P7V-EVIDENCE-EVALUATED-EMPTY",
            IssueSeverity.ERROR,
            "evidence_priority",
            "evaluated evidence requires source refs",
            field="evidence_ids",
            expected="evidence_ids or trace_ids",
            actual="empty",
        )
        return bag.finish()
    known_tiers = {item.value for item in PriorityTier}
    seen_keys: set[str] = set()
    ceiling = TIER_INDEX.get(SHEN_SHA_TIER_CEILING.value, 2)
    for finding in result.findings:
        if finding.tier.value not in known_tiers:
            bag.add(
                "P7V-EPR-UNKNOWN-TIER",
                IssueSeverity.ERROR,
                "evidence_priority",
                "unknown priority tier",
                field=finding.finding_id,
                actual=finding.tier.value,
            )
        if not finding.source_refs:
            bag.add(
                "P7V-EPR-SOURCE-MISSING",
                IssueSeverity.ERROR,
                "evidence_priority",
                "ranked finding requires source refs",
                field=finding.finding_id,
            )
        if not finding.trace_ids:
            bag.add(
                "P7V-EPR-TRACE-MISSING",
                IssueSeverity.ERROR,
                "evidence_priority",
                "ranked finding requires trace",
                field=finding.finding_id,
            )
        if finding.semantic_key:
            if finding.semantic_key in seen_keys:
                bag.add(
                    "P7V-EPR-DUPLICATE-SEMANTIC",
                    IssueSeverity.ERROR,
                    "evidence_priority",
                    "duplicate semantic finding after merge",
                    field=finding.semantic_key,
                )
            seen_keys.add(finding.semantic_key)
        if finding.source_kind in SHEN_SHA_SOURCE_KINDS:
            if TIER_INDEX.get(finding.tier.value, 99) < ceiling:
                bag.add(
                    "P7V-EPR-SHEN-SHA-CEILING",
                    IssueSeverity.CRITICAL,
                    "evidence_priority",
                    "Shen Sha cannot outrank its P2 ceiling",
                    field=finding.finding_id,
                    actual=finding.tier.value,
                )
            if finding.finding_id in result.dominant_evidence:
                bag.add(
                    "P7V-EPR-SHEN-SHA-DOMINANT",
                    IssueSeverity.CRITICAL,
                    "evidence_priority",
                    "Shen Sha cannot be dominant evidence",
                    field=finding.finding_id,
                )
        if finding.source_kind == "grade" and result.mc01_grade and result.score_engine_grade:
            if result.mc01_grade != result.score_engine_grade:
                if finding.customer_label == result.score_engine_grade:
                    bag.add(
                        "P7V-EPR-GRADE-SEMANTIC",
                        IssueSeverity.CRITICAL,
                        "evidence_priority",
                        "ScoreEngine grade must not replace MC-01 Grade",
                        field=finding.finding_id,
                        expected=result.mc01_grade,
                        actual=finding.customer_label,
                    )
    _ = payload
    return bag.finish()


def validate_domain_interpretation_result(
    section: DomainSection,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard domain IDs, Evidence Priority refs, and Shen Sha / ownership boundaries."""
    analysis_id = context.analysis_id if context is not None else ""
    bag = _Bag("validate_domain_interpretation_result", analysis_id)
    ep = context.runtime.interpretation.evidence_priority if context is not None else EvidencePriorityResult()
    ep_ids = set(ep.evidence_ids) | {item.finding_id for item in ep.findings if item.finding_id}
    if context is not None:
        _match_id(
            bag,
            context.analysis_id,
            ep.analysis_id or context.analysis_id,
            "domain",
            "evidence_priority.analysis_id",
            "P7V-DOMAIN-ANALYSIS-ID",
        )
    natals = [
        section.authority.natal,
        section.career.natal,
        section.wealth.natal,
        section.relationship.natal,
        section.legacy.natal,
        section.vitality.natal,
        *section.supporting.values(),
    ]
    seen: set[str] = set()
    for natal in natals:
        if natal.domain_id not in KNOWN_DOMAIN_IDS:
            bag.add(
                "P7V-DOMAIN-UNKNOWN-ID",
                IssueSeverity.ERROR,
                "domain",
                "unknown domain id",
                field="domain_id",
                actual=natal.domain_id,
            )
        if natal.domain_id in MAIN_DOMAIN_IDS and natal.domain_id in seen:
            bag.add(
                "P7V-DOMAIN-DUPLICATE",
                IssueSeverity.ERROR,
                "domain",
                "published domain duplicated",
                field=natal.domain_id,
            )
        seen.add(natal.domain_id)
        evaluated = natal.state not in (DomainState.NOT_EVALUATED, DomainState.UNRESOLVED)
        refs = natal.evidence_ids or natal.supporting_evidence_ids
        if evaluated and refs and ep_ids:
            unknown = [item for item in refs if item not in ep_ids]
            if unknown:
                bag.add(
                    "P7V-DOMAIN-EVIDENCE-REF",
                    IssueSeverity.ERROR,
                    "domain",
                    "domain evidence_ids must reference Evidence Priority",
                    field=f"{natal.domain_id}.evidence_ids",
                    actual=",".join(unknown[:4]),
                )
        source = f"{natal.driver_source} {natal.bottleneck_source} {natal.support_source}".lower()
        if any(kind in source for kind in DOMAIN_SHEN_SHA_KINDS) and natal.driver_source:
            if any(kind in natal.driver_source.lower() for kind in DOMAIN_SHEN_SHA_KINDS):
                bag.add(
                    "P7V-DOMAIN-SHEN-SHA-DRIVER",
                    IssueSeverity.CRITICAL,
                    "domain",
                    "Shen Sha cannot be Domain Driver",
                    field=f"{natal.domain_id}.driver_source",
                    actual=natal.driver_source,
                )
        _validate_domain_driver_contract(bag, natal)
        for key in ("pattern", "grade", "achievement", "wealth_profile", "career_profile"):
            if key in natal.dimensions:
                bag.add(
                    "P7V-DOMAIN-PROFILE-COPY",
                    IssueSeverity.CRITICAL,
                    "domain",
                    "domain must not duplicate MC-01 owned profiles",
                    field=f"{natal.domain_id}.dimensions.{key}",
                )
    for edge in section.graph.edges:
        if edge.relation not in GRAPH_RELATIONS:
            bag.add(
                "P7V-DOMAIN-GRAPH-RELATION",
                IssueSeverity.ERROR,
                "domain",
                "unknown domain graph relation",
                field="graph.edges.relation",
                actual=edge.relation,
            )
        if not edge.evidence_ids:
            bag.add(
                "P7V-DOMAIN-GRAPH-EVIDENCE",
                IssueSeverity.ERROR,
                "domain",
                "domain graph edge requires evidence",
                field=f"{edge.source}->{edge.target}",
            )
        if edge.source == edge.target:
            bag.add(
                "P7V-DOMAIN-GRAPH-SELF",
                IssueSeverity.ERROR,
                "domain",
                "domain graph edge cannot copy a node onto itself",
                field=edge.source,
            )
    return bag.finish()


def _validate_domain_driver_contract(_bag: _Bag, natal: DomainInterpretationResult) -> None:
    """Reject unknown, damage, dimension, and risk-as-driver values."""
    if natal.domain_id not in MAIN_DOMAIN_IDS:
        return
    if natal.state in {DomainState.NOT_EVALUATED, DomainState.UNRESOLVED}:
        return
    allowed = DOMAIN_DRIVER_IDS.get(natal.domain_id, frozenset())
    driver_id = natal.driver_id.strip()
    if not driver_id:
        _bag.add(
            "P7V-DOMAIN-DRIVER-MISSING",
            IssueSeverity.ERROR,
            "domain",
            "evaluated domain requires canonical driver_id",
            field=f"{natal.domain_id}.driver_id",
        )
        return
    if driver_id not in allowed:
        _bag.add(
            "P7V-DOMAIN-DRIVER-UNKNOWN",
            IssueSeverity.ERROR,
            "domain",
            "unknown domain driver",
            field=f"{natal.domain_id}.driver_id",
            actual=driver_id,
        )
    forbidden = set(MAJOR_DAMAGE_TYPES)
    if natal.domain_id == "authority":
        forbidden |= set(FORBIDDEN_AUTHORITY_DRIVER_IDS)
    if natal.domain_id == "wealth":
        forbidden |= set(FORBIDDEN_WEALTH_DRIVER_IDS)
    if natal.domain_id == "vitality":
        forbidden |= set(FORBIDDEN_VITALITY_DRIVER_IDS)
    if driver_id in forbidden:
        _bag.add(
            "P7V-DOMAIN-DRIVER-TYPE",
            IssueSeverity.CRITICAL,
            "domain",
            "damage, dimension, or risk cannot be Domain Driver",
            field=f"{natal.domain_id}.driver_id",
            actual=driver_id,
        )
    label = natal.driver.strip()
    if label and label in set(DAMAGE_LABELS.values()):
        _bag.add(
            "P7V-DOMAIN-DRIVER-DAMAGE",
            IssueSeverity.CRITICAL,
            "domain",
            "Damage cannot become Domain Driver",
            field=f"{natal.domain_id}.driver",
            actual=label,
        )
    expected_label = DRIVER_LABELS.get(driver_id, "")
    if driver_id not in {"not_applicable", "unresolved"} and expected_label and label != expected_label:
        _bag.add(
            "P7V-DOMAIN-DRIVER-LABEL",
            IssueSeverity.ERROR,
            "domain",
            "driver label must map from canonical driver_id",
            field=f"{natal.domain_id}.driver",
            expected=expected_label,
            actual=label,
        )
    if label and natal.bottleneck.strip() and label == natal.bottleneck.strip():
        _bag.add(
            "P7V-DOMAIN-DRIVER-BOTTLENECK",
            IssueSeverity.ERROR,
            "domain",
            "same semantic finding cannot be driver and bottleneck",
            field=f"{natal.domain_id}.driver",
            actual=label,
        )


def validate_luck_activation_result(
    result: LuckActivationResult,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard luck activation IDs, natal immutability, and temporal-only drivers."""
    analysis_id = context.analysis_id if context is not None else result.analysis_id
    bag = _Bag("validate_luck_activation_result", analysis_id)
    _check_schema(bag, result.schema_version or SCHEMA_LUCK_ACTIVATION, "luck_activation")
    if result.analysis_id and analysis_id:
        _match_id(
            bag,
            analysis_id,
            result.analysis_id,
            "luck_activation",
            "analysis_id",
            "P7V-LUCK-ANALYSIS-ID",
        )
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return bag.finish()
    if not result.cycle_id and not result.luck_cycle_id:
        bag.add(
            "P7V-LUCK-CYCLE-ID",
            IssueSeverity.ERROR,
            "luck_activation",
            "evaluated luck activation requires luck_cycle_id",
            field="luck_cycle_id",
        )
    if not result.time_window or "–" not in result.time_window:
        bag.add(
            "P7V-LUCK-TIME-WINDOW",
            IssueSeverity.ERROR,
            "luck_activation",
            "evaluated luck activation requires an explicit year window",
            field="time_window",
            actual=result.time_window,
        )
    natal_map = _natal_domain_map(context)
    natal_driver_ids = {
        item for values in DOMAIN_DRIVER_IDS.values() for item in values
    } - {"not_applicable", "unresolved"}
    seen: set[str] = set()
    for domain_id in MAIN_ACTIVATION_IDS:
        item = result.items.get(domain_id)
        if item is None:
            bag.add(
                "P7V-LUCK-MAIN-MISSING",
                IssueSeverity.ERROR,
                "luck_activation",
                "main domain missing activation result",
                field=domain_id,
            )
            continue
        _validate_activation_item(bag, item, natal_map.get(domain_id), natal_driver_ids)
        seen.add(domain_id)
    for domain_id, item in result.items.items():
        if domain_id in seen:
            continue
        if domain_id == "pattern":
            bag.add(
                "P7V-LUCK-PATTERN-TARGET",
                IssueSeverity.CRITICAL,
                "luck_activation",
                "Pattern is never an activation target",
                field="pattern",
            )
            continue
        if domain_id not in KNOWN_ACTIVATION_IDS:
            bag.add(
                "P7V-LUCK-UNKNOWN-ID",
                IssueSeverity.ERROR,
                "luck_activation",
                "unknown activation domain",
                field="domain_id",
                actual=domain_id,
            )
            continue
        _validate_activation_item(bag, item, natal_map.get(domain_id), natal_driver_ids)
    for item in result.items.values():
        for type_id in item.activation_types:
            if type_id not in ACTIVATION_TYPES:
                bag.add(
                    "P7V-LUCK-TYPE",
                    IssueSeverity.ERROR,
                    "luck_activation",
                    "unknown activation type",
                    field="activation_types",
                    actual=type_id,
                )
    for edge in result.graph.edges:
        if edge.relation not in ACTIVATION_GRAPH_RELATIONS:
            bag.add(
                "P7V-LUCK-GRAPH-RELATION",
                IssueSeverity.ERROR,
                "luck_activation",
                "unknown activation graph relation",
                field="graph.edges.relation",
                actual=edge.relation,
            )
        if edge.source in KNOWN_ACTIVATION_IDS and edge.target in KNOWN_ACTIVATION_IDS:
            bag.add(
                "P7V-LUCK-GRAPH-DOMAIN",
                IssueSeverity.CRITICAL,
                "luck_activation",
                "activation graph cannot connect domain to domain",
                field=f"{edge.source}->{edge.target}",
            )
        if edge.target and edge.target not in KNOWN_ACTIVATION_IDS:
            bag.add(
                "P7V-LUCK-GRAPH-TARGET",
                IssueSeverity.ERROR,
                "luck_activation",
                "activation graph target must be a known domain",
                field="graph.edges.target",
                actual=edge.target,
            )
    return bag.finish()


def _natal_domain_map(
    context: CanonicalAnalysisContext | None,
) -> dict[str, DomainInterpretationResult]:
    if context is None:
        return {}
    section = context.runtime.domains
    items = {
        "authority": section.authority.natal,
        "career": section.career.natal,
        "wealth": section.wealth.natal,
        "relationship": section.relationship.natal,
        "legacy": section.legacy.natal,
        "vitality": section.vitality.natal,
    }
    items.update(section.supporting)
    return items


def _validate_activation_item(
    bag: _Bag,
    item: DomainActivationResult,
    natal: DomainInterpretationResult | None,
    natal_driver_ids: set[str],
) -> None:
    if item.domain_id not in KNOWN_ACTIVATION_IDS:
        bag.add(
            "P7V-LUCK-UNKNOWN-ID",
            IssueSeverity.ERROR,
            "luck_activation",
            "unknown activation domain",
            field="domain_id",
            actual=item.domain_id,
        )
    if natal is not None:
        if item.natal_state and item.natal_state != natal.state.value:
            bag.add(
                "P7V-LUCK-NATAL-STATE",
                IssueSeverity.CRITICAL,
                "luck_activation",
                "luck must copy natal state without rewriting it",
                field=f"{item.domain_id}.natal_state",
                expected=natal.state.value,
                actual=item.natal_state,
            )
        if item.natal_driver_id and natal.driver_id and item.natal_driver_id != natal.driver_id:
            bag.add(
                "P7V-LUCK-NATAL-DRIVER",
                IssueSeverity.CRITICAL,
                "luck_activation",
                "luck must copy natal driver without rewriting it",
                field=f"{item.domain_id}.natal_driver_id",
                expected=natal.driver_id,
                actual=item.natal_driver_id,
            )
    driver_id = item.activation_driver_id.strip()
    if driver_id and driver_id not in ACTIVATION_DRIVER_IDS:
        bag.add(
            "P7V-LUCK-DRIVER-UNKNOWN",
            IssueSeverity.ERROR,
            "luck_activation",
            "unknown activation driver",
            field=f"{item.domain_id}.activation_driver_id",
            actual=driver_id,
        )
    if driver_id and driver_id in natal_driver_ids:
        bag.add(
            "P7V-LUCK-DRIVER-NATAL",
            IssueSeverity.CRITICAL,
            "luck_activation",
            "activation driver cannot copy natal Domain Driver",
            field=f"{item.domain_id}.activation_driver_id",
            actual=driver_id,
        )
    if item.activation_state is ActivationState.PEAK and item.natal_state in {
        "conditional",
        "fragmented",
        "weak",
        "unresolved",
        "blocked",
    }:
        bag.add(
            "P7V-LUCK-PEAK-CAPACITY",
            IssueSeverity.ERROR,
            "luck_activation",
            "peak activation cannot ignore natal carrying capacity",
            field=f"{item.domain_id}.activation_state",
        )


def validate_canonical_analysis_context(context: CanonicalAnalysisContext) -> ValidationResult:
    """Validate the full context chain and nested runtime."""
    bag = _Bag("validate_canonical_analysis_context", context.analysis_id)
    _require_analysis_id(bag, context.analysis_id, "context")
    _check_schema(bag, context.schema_version or SCHEMA_CONTEXT, "context")
    nested = (
        validate_interpretation_context(context.interpretation),
        validate_evidence_context(context.evidence),
        validate_domain_context(context.domain),
        validate_temporal_context(context.temporal),
        validate_optimization_context(context.optimization),
        validate_narrative_context(context.narrative),
        validate_canonical_runtime(context.runtime),
    )
    for result in nested:
        bag.issues.extend(result.issues)
    for child_id, label in (
        (context.interpretation.analysis_id, "interpretation.analysis_id"),
        (context.evidence.analysis_id, "evidence.analysis_id"),
        (context.domain.analysis_id, "domain.analysis_id"),
        (context.temporal.analysis_id, "temporal.analysis_id"),
        (context.optimization.analysis_id, "optimization.analysis_id"),
        (context.narrative.analysis_id, "narrative.analysis_id"),
        (context.runtime.analysis_id, "runtime.analysis_id"),
    ):
        _match_id(bag, context.analysis_id, child_id, "context", label)
    return bag.finish()


def validate_pack07_context(context: CanonicalAnalysisContext) -> ValidationResult:
    """Registry entry: validate Pack 07 context chain."""
    return validate_canonical_analysis_context(context)


def assert_valid(result: ValidationResult) -> None:
    """Fail closed on critical / error contract corruption."""
    if result.status is ValidationStatus.FAIL and result.errors:
        first = result.errors[0]
        raise DetailedInterpretationValidationError(f"{first.code}: {first.message}")


def payload_unchanged(before: Mapping[str, Any], after: Mapping[str, Any]) -> bool:
    """True when builders did not mutate the upstream mapping in place."""
    return to_jsonable(before) == to_jsonable(after)


PACK07_VALIDATOR_REGISTRY: dict[str, str] = {
    "validate_pack07_context": "validate_pack07_context",
    "validate_canonical_runtime": "validate_canonical_runtime",
    "validate_export_projection": "validate_export_projection",
    "validate_api_projection": "validate_api_projection",
    "validate_consulting_projection": "validate_consulting_projection",
    "validate_ten_gods_collection": "validate_ten_gods_collection",
    "validate_ten_god_combinations": "validate_ten_god_combinations",
    "validate_ten_god_ecosystem": "validate_ten_god_ecosystem",
    "validate_shen_sha_collection": "validate_shen_sha_collection",
    "validate_shen_sha_ecosystem": "validate_shen_sha_ecosystem",
    "validate_evidence_priority_result": "validate_evidence_priority_result",
    "validate_domain_interpretation_result": "validate_domain_interpretation_result",
    "validate_luck_activation_result": "validate_luck_activation_result",
    "validate_luck_interaction_result": "validate_luck_interaction_result",
}
