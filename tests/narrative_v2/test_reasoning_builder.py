"""Reasoning Builder tests (N-IMP-03)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.evidence import (
    EvidenceBuilder,
    EvidenceItem,
    EvidenceReference,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE, STATUS_MISSING
from engines.narrative_v2.evidence.evidence_registry import ALLOWED_DOMAINS
from engines.narrative_v2.reasoning import (
    NarrativeReasoningContext,
    ReasoningBuilder,
    ReasoningError,
    ReasoningRegistry,
    ReasoningRule,
)
from engines.narrative_v2.reasoning.reasoning_edge import RELATION_CONSTRAINS, RELATION_SUPPORTS
from engines.narrative_v2.reasoning.reasoning_node import KIND_OBSERVATION, STATUS_CONFLICT

REASONING_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "reasoning"

CUSTOMER_MARKERS: tuple[str, ...] = (
    "Bạn có nội lực tốt",
    "Bạn làm việc có hệ thống",
    "Bạn nên bổ Hỏa",
    "Bạn thuận lợi tình duyên",
    "Đây là vận tốt",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _item(
    evidence_id: str,
    domain: str,
    key: str,
    value: object,
    *,
    status: str = STATUS_AVAILABLE,
) -> EvidenceItem:
    path = evidence_id.removeprefix("evidence.").replace(".", ".", 1)
    source_path = evidence_id.removeprefix("evidence.")
    return EvidenceItem(
        evidence_id=evidence_id,
        domain=domain,
        key=key,
        label=key,
        value=value,  # type: ignore[arg-type]
        source_path=source_path,
        status=status,
        references=(EvidenceReference(source_path=source_path, domain=domain),),
    )


def _evidence(*items: EvidenceItem) -> NarrativeEvidenceContext:
    by_domain: dict[str, list[EvidenceItem]] = {domain: [] for domain in ALLOWED_DOMAINS}
    for item in items:
        by_domain[item.domain].append(item)
    return NarrativeEvidenceContext(
        identity=tuple(by_domain["identity"]),
        calendar=tuple(by_domain["calendar"]),
        bazi=tuple(by_domain["bazi"]),
        strength=tuple(by_domain["strength"]),
        temperature=tuple(by_domain["temperature"]),
        pattern=tuple(by_domain["pattern"]),
        useful_god=tuple(by_domain["useful_god"]),
        five_elements=tuple(by_domain["five_elements"]),
        ten_gods=tuple(by_domain["ten_gods"]),
        shensha=tuple(by_domain["shensha"]),
        luck=tuple(by_domain["luck"]),
        references=tuple(ref for item in items for ref in item.references),
        metadata=(),
        items=items,
        contract_gaps=(),
    )


def _blob(context: NarrativeReasoningContext) -> str:
    parts: list[str] = [context.status]
    for node in context.nodes:
        parts.extend(
            [
                node.reasoning_id,
                node.semantic_key,
                node.domain,
                node.kind,
                node.relation,
                node.status,
            ]
        )
        parts.extend(node.evidence_ids)
        parts.extend(value for _, value in node.metadata)
    for gap in context.contract_gaps:
        parts.extend([gap.field, gap.reason])
    return " ".join(parts)


def test_r1_builder_accepts_evidence_context_only(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert isinstance(context, NarrativeReasoningContext)


def test_r2_direct_canonical_analysis_rejected(
    case_0001_canonical: dict[str, Any],
) -> None:
    with pytest.raises(ReasoningError, match="NarrativeEvidenceContext only"):
        ReasoningBuilder().build(case_0001_canonical)


def test_r3_returns_narrative_reasoning_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert isinstance(context, NarrativeReasoningContext)
    assert context.nodes
    assert context.observations


def test_r4_stable_reasoning_ids(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    ids = [node.reasoning_id for node in context.nodes]
    for node in context.nodes:
        assert node.reasoning_id.startswith("reasoning.")
    assert len(ids) == len(set(ids))


def test_r5_stable_ordering(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    keys = [(node.priority, node.reasoning_id) for node in context.nodes]
    assert keys == sorted(keys)


def test_r6_all_nodes_trace_to_evidence(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    known = {item.evidence_id for item in evidence.items}
    for node in context.nodes:
        if node.kind == "boundary":
            continue
        assert node.evidence_ids
        for evidence_id in node.evidence_ids:
            assert evidence_id in known


def test_r7_missing_evidence_is_not_inferred() -> None:
    evidence = _evidence(
        _item("evidence.strength.level", "strength", "strength_level", "strong"),
    )
    context = ReasoningBuilder().build(evidence)
    assert context.node("reasoning.observation.core.pattern_context") is None
    assert context.node("reasoning.observation.core.useful_god_context") is None
    boundary = context.node("reasoning.boundary.core.pattern_context.insufficient")
    assert boundary is not None
    assert boundary.status == "insufficient"


def test_r8_no_customer_prose(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    blob = _blob(ReasoningBuilder().build(evidence))
    for marker in CUSTOMER_MARKERS:
        assert marker not in blob


def test_r9_no_recommendation(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert not hasattr(context, "recommendation")
    blob = _blob(context).lower()
    assert "recommendation" not in blob


def test_r10_no_action(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert not hasattr(context, "action")
    for node in context.nodes:
        assert "action" not in node.reasoning_id
        assert "action" not in node.semantic_key


def test_r11_no_astrology_recalculation() -> None:
    source = (REASONING_DIR / "reasoning_builder.py").read_text(encoding="utf-8")
    forbidden = (
        "ten_god_name(",
        "day_master_element(",
        "branch_element(",
        "stem_element(",
        "hidden_stems(",
        "calculate(",
        "strength_level ==",
        '== "strong"',
    )
    for token in forbidden:
        assert token not in source


def test_r12_unsupported_rule_is_not_invented() -> None:
    registry = ReasoningRegistry()
    assert registry.get("NR-REL-999") is None
    evidence = _evidence(
        _item("evidence.strength.level", "strength", "strength_level", "strong"),
    )
    context = ReasoningBuilder().build(evidence)
    keys = {node.semantic_key for node in context.nodes}
    assert "reasoning.identity.structured_self_direction" not in keys
    assert "independent" not in keys


def test_r13_conflict_and_qualification_can_be_represented() -> None:
    supports = ReasoningRule(
        rule_id="NR-REL-001",
        status="approved",
        required_evidence=("evidence.strength.level", "evidence.pattern.primary"),
        optional_evidence=(),
        relation_type=RELATION_SUPPORTS,
        output_semantic_key="core.pattern_context",
        priority=10,
        references=("knowledge/narrative_v2/00_ARCHITECTURE.md",),
        domain="pattern",
        kind=KIND_OBSERVATION,
    )
    constrains = ReasoningRule(
        rule_id="NR-REL-002",
        status="approved",
        required_evidence=("evidence.strength.level", "evidence.pattern.primary"),
        optional_evidence=(),
        relation_type=RELATION_CONSTRAINS,
        output_semantic_key="core.pattern_context",
        priority=20,
        references=("knowledge/narrative_v2/00_ARCHITECTURE.md",),
        domain="pattern",
        kind=KIND_OBSERVATION,
    )
    evidence = _evidence(
        _item("evidence.strength.level", "strength", "strength_level", "strong"),
        _item("evidence.pattern.primary", "pattern", "pattern", "chinh_an"),
    )
    registry = ReasoningRegistry(rules=(supports, constrains))
    context = ReasoningBuilder(registry=registry).build(evidence)
    types = {edge.relation_type for edge in context.edges}
    assert RELATION_SUPPORTS in types
    assert RELATION_CONSTRAINS in types
    target = context.node("reasoning.observation.core.pattern_context")
    assert target is not None
    assert target.status == STATUS_CONFLICT
    assert len(context.edges) >= 2


def test_r16_same_evidence_identical_reasoning(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    first = ReasoningBuilder().build(evidence)
    second = ReasoningBuilder().build(evidence)
    assert first.nodes == second.nodes
    assert first.edges == second.edges
    assert first.contract_gaps == second.contract_gaps


def test_r17_r18_no_pack05_or_portal_imports() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api.services.narrative_result_truth",
    )
    for path in REASONING_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            ), f"{path} imports {name}"


def test_semantic_negatives_do_not_create_customer_meaning(
    case_0001_canonical: dict[str, Any],
) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    blob = _blob(context)
    assert "Bạn có nội lực tốt." not in blob
    assert "Bạn làm việc có hệ thống." not in blob
    assert "Bạn nên bổ Hỏa." not in blob
    assert "Bạn thuận lợi tình duyên." not in blob
    assert "Đây là vận tốt." not in blob
    keys = {node.semantic_key for node in context.nodes}
    assert "independent" not in keys


def test_strength_alone_does_not_create_pattern_meaning() -> None:
    evidence = _evidence(
        _item("evidence.strength.level", "strength", "strength_level", "strong"),
    )
    blob = _blob(ReasoningBuilder().build(evidence))
    assert "Bạn có nội lực tốt" not in blob
    assert "independent" not in blob


def test_pattern_alone_does_not_create_system_meaning() -> None:
    evidence = _evidence(
        _item("evidence.pattern.primary", "pattern", "pattern", "chinh_an"),
    )
    blob = _blob(ReasoningBuilder().build(evidence))
    assert "Bạn làm việc có hệ thống" not in blob


def test_useful_god_alone_does_not_create_action() -> None:
    evidence = _evidence(
        _item("evidence.useful_god.element", "useful_god", "useful_element", "Hỏa"),
        _item("evidence.useful_god.primary", "useful_god", "useful_god", "Chính Quan"),
    )
    blob = _blob(ReasoningBuilder().build(evidence))
    assert "Bạn nên bổ Hỏa" not in blob
    assert "nên bổ" not in blob


def test_hong_luan_does_not_create_relationship_meaning() -> None:
    evidence = _evidence(
        _item(
            "evidence.shensha.names",
            "shensha",
            "names",
            ("Hồng Loan",),
        ),
    )
    context = ReasoningBuilder().build(evidence)
    blob = _blob(context)
    assert "Bạn thuận lợi tình duyên" not in blob
    assert context.node("reasoning.observation.core.pattern_context") is None
    gap_fields = {gap.field for gap in context.contract_gaps}
    assert "reasoning.shensha.meaning" in gap_fields


def test_current_luck_does_not_create_quality_meaning() -> None:
    evidence = _evidence(
        _item("evidence.luck.current_cycle", "luck", "current_cycle", "Ất Tỵ"),
    )
    context = ReasoningBuilder().build(evidence)
    blob = _blob(context)
    assert "Đây là vận tốt" not in blob
    node = context.node("reasoning.observation.core.luck_temporal_context")
    assert node is not None
    assert node.semantic_key == "core.luck_temporal_context"


def test_case_0001_structural_graph(case_0001_canonical: dict[str, Any]) -> None:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    context = ReasoningBuilder().build(evidence)
    assert context.node("reasoning.observation.core.pattern_context") is not None
    assert context.node("reasoning.observation.core.useful_god_context") is not None
    assert context.node("reasoning.observation.core.temperature_balancing_context") is not None
    assert context.node("reasoning.observation.core.pattern_ten_gods_relation") is not None
    assert context.node("reasoning.observation.core.luck_temporal_context") is not None
    assert context.node("reasoning.observation.strength.level") is not None
    assert context.impacts == ()
