"""IE-2 selection validation. No prose checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.interpretation_engine.knowledge.composition_context import (
    COMPOSITION_VERSION,
    CompositionContext,
    PlaceholderIntegrityError,
)
from engines.interpretation_engine.knowledge.composition_result import SentenceCandidate
from engines.interpretation_engine.knowledge.evidence_selector import EvidenceBundle
from engines.interpretation_engine.knowledge.knowledge_selector import KnowledgeSelection
from engines.interpretation_engine.knowledge.placeholder_binder import PlaceholderBinding
from engines.interpretation_engine.knowledge.reasoning_selector import ReasoningSelection
from engines.interpretation_engine.knowledge.selector_registry import (
    CANONICAL_SELECTOR_ORDER,
    SelectorRegistry,
)
from engines.interpretation_engine.knowledge.template_selector import TemplateSelection

CODE_CONTRACT_OK = "CONTRACT-OK"
CODE_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
CODE_REGISTRY_OK = "REGISTRY-OK"
CODE_PLACEHOLDER_OK = "PLACEHOLDER-OK"
CODE_PLACEHOLDER_VIOLATION = "PLACEHOLDER-VIOLATION"
CODE_TEMPLATE_OK = "TEMPLATE-OK"
CODE_KNOWLEDGE_OK = "KNOWLEDGE-OK"
CODE_REASONING_OK = "REASONING-OK"
CODE_DUP_CANDIDATE = "DUP-CANDIDATE"
CODE_VERSION_INCOMPATIBLE = "VERSION-INCOMPATIBLE"
CODE_VALIDATION_OK = "VALIDATION-OK"

REQUIRED_ANALYSIS_VERSION = "2.0.0"
REQUIRED_DECISION_VERSION = "1.0.0"
REQUIRED_LUCK_VERSION = "1.0.0"
REQUIRED_INTERPRETATION_VERSION = "1.0.0"

FORBIDDEN_TEXT_FIELDS: tuple[str, ...] = (
    "narrative",
    "sentence",
    "sentences",
    "report_text",
    "consultant_copy",
    "generated_text",
    "template_body",
)


@dataclass(slots=True)
class CompositionValidationReport:
    """Machine-readable IE-2 validation report."""

    success: bool
    codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the validation report."""
        return {
            "success": self.success,
            "codes": list(self.codes),
            "details": dict(self.details),
        }


def validate_versions(context: CompositionContext) -> None:
    """Require AX-2 / AX-3 / AX-4 / IE-1 / IE-2 versions."""
    analysis_version = str(context.analysis_snapshot().get("pipeline_version") or "")
    decision_version = str(context.decision_snapshot().get("decision_pipeline_version") or "")
    luck_version = str(context.luck_snapshot().get("luck_pipeline_version") or "")
    interpretation_version = str(
        context.interpretation_snapshot().get("interpretation_version") or ""
    )
    if context.composition_version != COMPOSITION_VERSION:
        raise ValueError(f"composition_version_incompatible:{context.composition_version}")
    if analysis_version != REQUIRED_ANALYSIS_VERSION:
        raise ValueError(f"analysis_pipeline_incompatible:{analysis_version}")
    if decision_version != REQUIRED_DECISION_VERSION:
        raise ValueError(f"decision_pipeline_incompatible:{decision_version}")
    if luck_version != REQUIRED_LUCK_VERSION:
        raise ValueError(f"luck_pipeline_incompatible:{luck_version}")
    if interpretation_version != REQUIRED_INTERPRETATION_VERSION:
        raise ValueError(f"interpretation_version_incompatible:{interpretation_version}")


def validate_registry(registry: SelectorRegistry) -> None:
    """Require the canonical deterministic selector catalog."""
    if registry.registered_ids() != CANONICAL_SELECTOR_ORDER:
        raise ValueError("registry_selector_mismatch")
    if registry.resolve_order() != CANONICAL_SELECTOR_ORDER:
        raise ValueError("registry_order_mismatch")
    for selector_id in CANONICAL_SELECTOR_ORDER:
        record = registry.get(selector_id)
        if not record.enabled or not record.deterministic:
            raise ValueError(f"selector_not_deterministic:{selector_id}")


def validate_knowledge_references(knowledge: Sequence[KnowledgeSelection]) -> None:
    """Require unique released knowledge identifiers."""
    ids = [item.knowledge_id for item in knowledge]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate_knowledge_id")
    for item in knowledge:
        if item.spec.status != "released":
            raise ValueError(f"knowledge_not_released:{item.knowledge_id}")


def validate_reasoning_references(
    knowledge: Sequence[KnowledgeSelection],
    reasoning: Sequence[ReasoningSelection],
) -> None:
    """Require reasoning ids to belong to selected knowledge and remain unmodified."""
    by_kn = {item.knowledge_id: item.spec for item in knowledge}
    reasoning_ids = [item.reasoning_id for item in reasoning]
    if len(reasoning_ids) != len(set(reasoning_ids)):
        raise ValueError("duplicate_reasoning_id")
    for item in reasoning:
        spec = by_kn.get(item.knowledge_id)
        if spec is None:
            raise ValueError(f"orphaned_reasoning:{item.reasoning_id}")
        if item.chain_id != spec.reasoning_chain_id or item.graph_id != spec.reasoning_graph_id:
            raise ValueError(f"reasoning_modified:{item.reasoning_id}")


def validate_template_references(
    knowledge: Sequence[KnowledgeSelection],
    templates: Sequence[TemplateSelection],
) -> None:
    """Require template ids to match selected knowledge declarations."""
    expected = {item.knowledge_id: item.spec.template_id for item in knowledge}
    template_ids = [item.template_id for item in templates]
    if len(template_ids) != len(set(template_ids)):
        raise ValueError("duplicate_template_id")
    for item in templates:
        declared = expected.get(item.knowledge_id)
        if declared != item.template_id:
            raise ValueError(f"template_mismatch:{item.template_id}")


def validate_placeholder_integrity(
    context: CompositionContext,
    placeholders: Sequence[PlaceholderBinding],
) -> None:
    """Require placeholder paths to resolve on published contract roots."""
    for binding in placeholders:
        try:
            context.resolve_published(binding.binding_path)
        except PlaceholderIntegrityError as exc:
            raise ValueError(str(exc)) from exc
        if any(name in binding.binding_path.lower() for name in FORBIDDEN_TEXT_FIELDS):
            raise ValueError(f"forbidden_placeholder:{binding.binding_path}")


def validate_duplicate_candidates(candidates: Sequence[SentenceCandidate]) -> None:
    """Reject duplicate sentence candidate identifiers."""
    ids = [item.sentence_id for item in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate_sentence_id")
    required = (
        "sentence_id",
        "template_id",
        "placeholder_values",
        "evidence_ids",
        "reasoning_ids",
        "confidence",
        "references",
    )
    for item in candidates:
        payload = item.to_dict()
        missing = [name for name in required if name not in payload]
        if missing:
            raise ValueError(f"candidate_contract:{item.sentence_id}:{','.join(missing)}")
        for forbidden in FORBIDDEN_TEXT_FIELDS:
            if forbidden in payload:
                raise ValueError(f"forbidden_candidate_field:{forbidden}")


def validate_composition(
    *,
    context: CompositionContext,
    registry: SelectorRegistry,
    knowledge: Sequence[KnowledgeSelection],
    evidence: Sequence[EvidenceBundle],
    reasoning: Sequence[ReasoningSelection],
    templates: Sequence[TemplateSelection],
    placeholders: Sequence[PlaceholderBinding],
    candidates: Sequence[SentenceCandidate],
) -> CompositionValidationReport:
    """Run the IE-2 validation suite."""
    codes: list[str] = []
    details: dict[str, Any] = {}
    try:
        validate_versions(context)
        validate_registry(registry)
        codes.append(CODE_REGISTRY_OK)
        validate_knowledge_references(knowledge)
        codes.append(CODE_KNOWLEDGE_OK)
        validate_reasoning_references(knowledge, reasoning)
        codes.append(CODE_REASONING_OK)
        validate_template_references(knowledge, templates)
        codes.append(CODE_TEMPLATE_OK)
        validate_placeholder_integrity(context, placeholders)
        codes.append(CODE_PLACEHOLDER_OK)
        validate_duplicate_candidates(candidates)
        codes.extend((CODE_CONTRACT_OK, CODE_VALIDATION_OK))
        return CompositionValidationReport(success=True, codes=tuple(codes), details=details)
    except ValueError as exc:
        message = str(exc)
        if "incompatible" in message:
            codes.append(CODE_VERSION_INCOMPATIBLE)
        elif "duplicate_sentence" in message:
            codes.append(CODE_DUP_CANDIDATE)
        elif "placeholder" in message or "unpublished_root" in message:
            codes.append(CODE_PLACEHOLDER_VIOLATION)
        else:
            codes.append(CODE_CONTRACT_VIOLATION)
        details["error"] = message
        return CompositionValidationReport(success=False, codes=tuple(codes), details=details)
