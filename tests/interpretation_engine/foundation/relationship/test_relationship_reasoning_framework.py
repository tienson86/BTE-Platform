"""Sprint R1 — Relationship Reasoning Framework tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    CANONICAL_REASONING_CLASSES,
    INTERPRETATION_CLASS_DECISION,
    INTERPRETATION_CLASS_RELATIONSHIP,
    INTERPRETATION_CLASS_STATE,
)
from engines.interpretation_engine.foundation.relationship import (
    BROKEN_EVIDENCE,
    CANONICAL_RELATIONSHIP_TYPES,
    DUPLICATE_EDGE,
    GenericRelationshipExplainer,
    INVALID_CONFIDENCE,
    MISSING_PARTICIPANT,
    RelationshipApplication,
    RelationshipAssessment,
    RelationshipEdge,
    RelationshipEvidence,
    RelationshipExplainer,
    RelationshipGraph,
    RelationshipInput,
    RelationshipMeaning,
    RelationshipNode,
    RelationshipRecord,
    RelationshipWarning,
    SELF_LOOP,
    UNKNOWN_RELATIONSHIP_TYPE,
    compute_relationship_metrics,
    validate_relationship_assessment,
)
from engines.interpretation_engine.foundation.status import DataAvailability

_FRAMEWORK_ROOT = Path("engines/interpretation_engine/foundation/relationship")
_FORBIDDEN_IMPLEMENTATION_TERMS = (
    "Pattern",
    "Ten Gods",
    "TenGods",
    "ten_gods",
    "Shen Sha",
    "ShenSha",
    "shensha",
)


def test_reasoning_taxonomy_has_exactly_three_classes() -> None:
    """Decision, State, and Relationship are the only frozen reasoning classes."""
    assert CANONICAL_REASONING_CLASSES == (
        INTERPRETATION_CLASS_DECISION,
        INTERPRETATION_CLASS_STATE,
        INTERPRETATION_CLASS_RELATIONSHIP,
    )
    assert len(CANONICAL_REASONING_CLASSES) == 3


def test_canonical_relationship_types() -> None:
    """Framework supports the required semantic types without encoding rules."""
    assert CANONICAL_RELATIONSHIP_TYPES == (
        "supports",
        "generates",
        "drains",
        "controls",
        "balances",
        "conflicts",
        "transforms",
        "combines",
    )


def test_graph_contracts() -> None:
    """Nodes and edges preserve source, target, type, weight, confidence, rule_ids."""
    assessment = _explain_two_edges()
    graph = assessment.graph
    assert isinstance(graph, RelationshipGraph)
    assert {node.node_id for node in graph.nodes} == {"alpha", "beta", "gamma"}
    assert len(graph.edges) == 2
    first = graph.edges[0]
    assert first.source == "alpha"
    assert first.target == "beta"
    assert first.relationship_type == "generates"
    assert first.weight == 0.5
    assert first.confidence == 0.8
    assert first.rule_ids == ("rule_a",)
    outgoing = graph.edges_from("beta")
    assert len(outgoing) == 1
    assert outgoing[0].target == "gamma"
    incoming = graph.edges_to("beta")
    assert len(incoming) == 1
    assert incoming[0].source == "alpha"


def test_relationship_assessment_contract() -> None:
    """Assessment exposes participants, type fields, evidence, and no winner."""
    assessment = _explain_one_edge()
    assert isinstance(assessment, RelationshipAssessment)
    assert assessment.interpretation_class == INTERPRETATION_CLASS_RELATIONSHIP
    assert [node.node_id for node in assessment.participants] == ["alpha", "beta"]
    assert assessment.relationship_type == "supports"
    assert assessment.direction == "source_to_target"
    assert assessment.strength == 0.4
    assert assessment.conditions == ("present",)
    assert assessment.rule_ids == ("rule_a",)
    payload = assessment.to_dict()
    assert "winner" not in payload
    assert "alternatives" not in payload
    assert "decision" not in payload
    assert "strength_level" not in payload
    assert payload["graph"]["edges"]


def test_multi_edge_assessment_does_not_pick_a_primary() -> None:
    """Multiple relationships stay a graph; assessment does not invent a winner type."""
    assessment = _explain_two_edges()
    assert assessment.relationship_type == ""
    assert len(assessment.graph.edges) == 2


def test_explainer_does_not_invent_relationships() -> None:
    """Only upstream records become edges."""
    assessment = _explain_one_edge()
    assert len(assessment.graph.edges) == 1
    assert assessment.graph.edges[0].source == "alpha"
    assert assessment.graph.edges[0].target == "beta"


def test_meaning_is_knowledge_seam_not_reasoning() -> None:
    """Meaning is copied when supplied; generic explainer does not author it."""
    empty = _explain_one_edge()
    assert empty.meaning == ()
    supplied = GenericRelationshipExplainer().explain(
        RelationshipInput(
            domain="demo",
            records=(_record(),),
            evidence=(_evidence(),),
            meaning=(
                RelationshipMeaning(
                    statement="authored elsewhere",
                    evidence_ids=("ev_1",),
                    knowledge_key="demo.key",
                ),
            ),
        )
    )
    assert len(supplied.meaning) == 1
    assert supplied.meaning[0].knowledge_key == "demo.key"
    assert supplied.graph.edges[0].knowledge_key == ""


def test_validation_codes() -> None:
    """Validator detects the R1 structural failures."""
    node = RelationshipNode(node_id="alpha")
    graph = RelationshipGraph(
        nodes=(node,),
        edges=(
            RelationshipEdge(
                edge_id="e1",
                source="alpha",
                target="alpha",
                relationship_type="invented",
                confidence=1.5,
                evidence_ids=("missing_ev",),
            ),
            RelationshipEdge(
                edge_id="e2",
                source="alpha",
                target="",
                relationship_type="supports",
                confidence=0.2,
            ),
            RelationshipEdge(
                edge_id="e3",
                source="alpha",
                target="alpha",
                relationship_type="invented",
                confidence=0.2,
            ),
        ),
    )
    assessment = RelationshipAssessment(
        domain="demo",
        graph=graph,
        evidence=(),
        meaning=(),
        applications=(),
        warnings=(),
        confidence=0.2,
        diagnostics=(),
        status=DataAvailability.AVAILABLE,
    )
    result = validate_relationship_assessment(assessment)
    codes = {issue.code for issue in result.issues}
    assert MISSING_PARTICIPANT in codes
    assert SELF_LOOP in codes
    assert UNKNOWN_RELATIONSHIP_TYPE in codes
    assert BROKEN_EVIDENCE in codes
    assert DUPLICATE_EDGE in codes
    assert INVALID_CONFIDENCE in codes
    assert result.passed is False
    assert result.status == DataAvailability.INVALID


def test_metrics() -> None:
    """Metrics report node/edge counts, support, and evidence coverage."""
    assessment = _explain_two_edges()
    metrics = assessment.metrics
    assert metrics is not None
    assert metrics.node_count == 3
    assert metrics.edge_count == 2
    assert metrics.supported_relationships == 1
    assert metrics.unsupported_relationships == 1
    assert metrics.evidence_coverage == 1.0
    recomputed = compute_relationship_metrics(assessment)
    assert recomputed.to_dict() == metrics.to_dict()


def test_explainability_chain() -> None:
    """Every relationship traces facts → relationship → evidence → knowledge seam."""
    assessment = _explain_one_edge()
    edge = assessment.graph.edges[0]
    assert edge.fact_refs
    evidence_ids = {item.evidence_id for item in assessment.evidence}
    for ref in edge.evidence_ids:
        assert ref in evidence_ids
    assert edge.knowledge_key == ""
    validation = validate_relationship_assessment(assessment)
    assert validation.passed is True
    assert not any(issue.code == BROKEN_EVIDENCE for issue in validation.issues)


def test_generic_api() -> None:
    """RelationshipExplainer.explain() is the public generic interface."""
    explainer: RelationshipExplainer = GenericRelationshipExplainer()
    result = explainer.explain(
        RelationshipInput(domain="demo", records=(_record(),), evidence=(_evidence(),))
    )
    assert isinstance(result, RelationshipAssessment)
    sequence_result = explainer.explain((_record(),))
    assert sequence_result.graph.edges[0].relationship_type == "supports"


def test_explain_rejects_unknown_input() -> None:
    """Hidden coercion from arbitrary objects is not allowed."""
    with pytest.raises(TypeError):
        GenericRelationshipExplainer().explain({"source": "alpha"})


def test_knowledge_contracts_exist_without_population() -> None:
    """Application and warning contracts exist; R1 does not populate domains."""
    item = RelationshipApplication(
        area="career",
        statement="pass-through only",
        evidence_ids=("ev_1",),
        confidence=0.5,
    )
    warning = RelationshipWarning(
        condition="overload",
        risk="imbalance",
        mitigation="restore support",
        evidence_ids=("ev_1",),
    )
    assessment = GenericRelationshipExplainer().explain(
        RelationshipInput(
            domain="demo",
            records=(_record(),),
            evidence=(_evidence(),),
            applications=(item,),
            warnings=(warning,),
        )
    )
    assert assessment.applications[0].area == "career"
    assert assessment.warnings[0].condition == "overload"


def test_no_ui_dependency() -> None:
    """Relationship framework has no UI dependency."""
    for path in _framework_files():
        source = path.read_text(encoding="utf-8")
        assert "customer_portal" not in source
        assert "portal" not in path.parts


def test_no_narrative_dependency() -> None:
    """Relationship framework has no narrative dependency."""
    for path in _framework_files():
        source = path.read_text(encoding="utf-8")
        assert "NarrativeEngine" not in source
        assert "narrative_engine" not in source


def test_implementation_stays_generic() -> None:
    """Framework implementation does not name future knowledge domains."""
    for path in _framework_files():
        source = path.read_text(encoding="utf-8")
        for term in _FORBIDDEN_IMPLEMENTATION_TERMS:
            assert term not in source, f"{term} found in {path}"


def test_empty_input_is_missing() -> None:
    """No upstream records → missing, not an invented empty success graph."""
    assessment = GenericRelationshipExplainer().explain(
        RelationshipInput(domain="demo", records=())
    )
    assert assessment.status == DataAvailability.MISSING
    assert assessment.graph.edges == ()
    assert assessment.metrics is not None
    assert assessment.metrics.edge_count == 0


def _explain_one_edge() -> RelationshipAssessment:
    """One supported relationship from upstream records."""
    return GenericRelationshipExplainer().explain(
        RelationshipInput(
            domain="demo",
            records=(_record(),),
            evidence=(_evidence(),),
        )
    )


def _explain_two_edges() -> RelationshipAssessment:
    """Two-edge graph: one supported, one unsupported."""
    supported = RelationshipRecord(
        source="alpha",
        target="beta",
        relationship_type="generates",
        weight=0.5,
        confidence=0.8,
        rule_ids=("rule_a",),
        evidence_ids=("ev_1",),
        record_id="e1",
    )
    unsupported = RelationshipRecord(
        source="beta",
        target="gamma",
        relationship_type="drains",
        confidence=0.6,
        record_id="e2",
    )
    return GenericRelationshipExplainer().explain(
        RelationshipInput(
            domain="demo",
            records=(supported, unsupported),
            evidence=(_evidence(),),
        )
    )


def _record() -> RelationshipRecord:
    """Generic upstream record."""
    return RelationshipRecord(
        source="alpha",
        target="beta",
        relationship_type="supports",
        direction="source_to_target",
        strength=0.4,
        conditions=("present",),
        evidence_ids=("ev_1",),
        rule_ids=("rule_a",),
        confidence=0.7,
        source_kind="entity",
        target_kind="entity",
    )


def _evidence() -> RelationshipEvidence:
    """Generic upstream evidence."""
    return RelationshipEvidence(
        evidence_id="ev_1",
        source_engine="upstream",
        source_field="link",
        rule_id="rule_a",
        fact="alpha_supports_beta",
        value="present",
        confidence=0.9,
    )


def _framework_files() -> tuple[Path, ...]:
    """Python files in the relationship framework package."""
    return tuple(sorted(_FRAMEWORK_ROOT.glob("*.py")))
