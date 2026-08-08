"""Narrative Composer Runtime — Sprint D1 orchestration."""

from __future__ import annotations

import logging
import uuid

from .component_ordering import ComponentOrdering
from .component_selector import ComponentSelector
from .confidence_resolver import ConfidenceResolver
from .dependency_resolver import DependencyResolver
from .evidence_validation import EvidenceValidator
from .exceptions import NarrativeRuntimeValidationError
from .models import (
    COMPONENT_DEPENDENCIES,
    NarrativeNode,
    NarrativeTree,
    RuntimeInput,
)
from .tree_builder import NarrativeTreeBuilder
from .validator import NarrativeValidator

logger = logging.getLogger(__name__)


class NarrativeComposerRuntime:
    """
    Compose a NarrativeTree from structural RuntimeInput.

    Pipeline:
    Evidence Validation → Component Selector → Tree draft →
    Dependency Resolver → Confidence Resolver → Ordering → Validator

    Does not generate paragraphs, prose, or templates.
    """

    def __init__(
        self,
        evidence_validator: EvidenceValidator | None = None,
        component_selector: ComponentSelector | None = None,
        dependency_resolver: DependencyResolver | None = None,
        confidence_resolver: ConfidenceResolver | None = None,
        component_ordering: ComponentOrdering | None = None,
        tree_builder: NarrativeTreeBuilder | None = None,
        narrative_validator: NarrativeValidator | None = None,
    ) -> None:
        self._evidence_validator = evidence_validator or EvidenceValidator()
        self._component_selector = component_selector or ComponentSelector()
        self._dependency_resolver = dependency_resolver or DependencyResolver()
        self._confidence_resolver = confidence_resolver or ConfidenceResolver()
        self._component_ordering = component_ordering or ComponentOrdering()
        self._tree_builder = tree_builder or NarrativeTreeBuilder()
        self._narrative_validator = narrative_validator or NarrativeValidator()

    def compose(self, runtime_input: RuntimeInput) -> NarrativeTree:
        """Compose NarrativeTree or raise on invalid analytical/interpretation gates."""
        if not runtime_input.analysis_valid:
            raise NarrativeRuntimeValidationError("AnalysisResult is invalid.")
        if not runtime_input.interpretation_valid:
            raise NarrativeRuntimeValidationError("InterpretationResult is invalid.")

        run_id = runtime_input.run_id.strip() or str(uuid.uuid4())
        logger.info("composer_runtime.start run_id=%s", run_id)

        evidence = self._evidence_validator.validate(runtime_input)
        bindings = self._component_selector.select(evidence, runtime_input)
        draft_nodes = self._tree_builder.build_draft_nodes(bindings)

        draft_status = {key: node.status for key, node in draft_nodes.items()}
        resolved_status = self._dependency_resolver.resolve(draft_status)

        evidence_by_id = {unit.id: unit for unit in evidence}
        confidences = self._confidence_resolver.resolve(
            evidence_by_id,
            bindings,
            resolved_status,
        )

        status_applied: dict = {}
        for component, node in draft_nodes.items():
            status_applied[component] = NarrativeNode(
                component_type=node.component_type,
                evidence_refs=node.evidence_refs,
                interpretation_refs=node.interpretation_refs,
                confidence=confidences.get(component, 0.0),
                priority=node.priority,
                dependencies=COMPONENT_DEPENDENCIES[component],
                status=resolved_status[component],
            )

        ordered = self._component_ordering.order(status_applied)
        issues = self._narrative_validator.validate_ordered_nodes(ordered)
        tree = self._tree_builder.build_tree(
            ordered,
            run_id=run_id,
            validation_issues=(),
            metadata={
                "evidence_count": len(evidence),
                "interpretation_ref_count": len(runtime_input.interpretation_refs),
                "runtime": "pack05_narrative_d1",
            },
        )
        tree = self._narrative_validator.apply_tree_status(tree, issues)
        logger.info(
            "composer_runtime.done run_id=%s status=%s issues=%s",
            run_id,
            tree.status.value,
            len(tree.validation_issues),
        )
        return tree
