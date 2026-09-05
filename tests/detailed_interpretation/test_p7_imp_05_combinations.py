"""P7-IMP-05 Ten God combination and ecosystem vertical slice."""

from __future__ import annotations

from copy import deepcopy

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.diagnostics import build_pack07_diagnostics
from engines.detailed_interpretation_engine.enums import (
    ChainQuality,
    CombinationState,
    DayMasterBand,
    DiagnosticStatus,
    EvaluationStatus,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodRootState,
    TenGodStructuralRole,
    TenGodVisibilitySummary,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import V1_COMBINATION_IDS
from engines.detailed_interpretation_engine.ten_gods.combinations.engine import (
    interpret_ten_god_combinations,
)
from engines.detailed_interpretation_engine.ten_gods.constants import CANONICAL_TEN_GOD_IDS, GOD_ID_TO_LABEL
from engines.detailed_interpretation_engine.ten_gods.ecosystem.engine import interpret_ten_gods_ecosystem
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods, interpret_ten_gods
from engines.detailed_interpretation_engine.ten_gods.models import (
    TenGodInterpretationCollection,
    TenGodInterpretationResult,
    TenGodVisibilityInventory,
)
from engines.ten_gods_engine.runtime.case_0001 import run_case_0001
from applications.api.services.ten_gods_truth import shape_ten_gods_payload


def _vis(*, visible: bool = False, residual: bool = False, month: bool = False) -> TenGodVisibilityInventory:
    if residual:
        return TenGodVisibilityInventory(
            branch_hidden=True,
            residual_qi=True,
            summary=TenGodVisibilitySummary.HIDDEN,
        )
    return TenGodVisibilityInventory(
        year_stem=visible and not month,
        month_stem=month,
        summary=TenGodVisibilitySummary.EXPOSED if visible or month else TenGodVisibilitySummary.ABSENT,
    )


def _god(
    god_id: str,
    *,
    presence: TenGodPresenceState = TenGodPresenceState.ABSENT,
    strength: TenGodEffectiveStrength = TenGodEffectiveStrength.NOT_APPLICABLE,
    role: TenGodStructuralRole = TenGodStructuralRole.NEUTRAL,
    residual: bool = False,
    month: bool = False,
    pattern: str = "Chính Ấn",
    dm: str = "moderate",
) -> TenGodInterpretationResult:
    visible = presence in {
        TenGodPresenceState.VISIBLE,
        TenGodPresenceState.VISIBLE_AND_ROOTED,
        TenGodPresenceState.REPEATED,
        TenGodPresenceState.CONCENTRATED,
        TenGodPresenceState.STRUCTURALLY_DOMINANT,
    }
    return TenGodInterpretationResult(
        ten_god_id=god_id,
        state=EvaluationStatus.RESOLVED,
        presence_state=presence,
        visibility=_vis(visible=visible, residual=residual, month=month),
        root_state=TenGodRootState.STRONG_ROOT if presence is TenGodPresenceState.VISIBLE_AND_ROOTED else TenGodRootState.NO_ROOT,
        effective_strength=strength,
        structural_role=role,
        day_master_context=DayMasterBand(dm),
        pattern_context=pattern,
        evidence_ids=(f"E-{god_id}",) if presence is not TenGodPresenceState.ABSENT else (),
        trace_ids=(f"TR-P7-TG-{god_id}",),
    )


def _natal(
    present: dict[str, dict[str, object]],
    *,
    dm: str = "moderate",
    pattern: str = "Chính Ấn",
) -> TenGodInterpretationCollection:
    items = []
    for god_id in CANONICAL_TEN_GOD_IDS:
        fields = present.get(god_id, {})
        items.append(
            _god(
                god_id,
                presence=fields.get("presence", TenGodPresenceState.ABSENT),
                strength=fields.get("strength", TenGodEffectiveStrength.NOT_APPLICABLE),
                role=fields.get("role", TenGodStructuralRole.NEUTRAL),
                residual=bool(fields.get("residual", False)),
                month=bool(fields.get("month", False)),
                pattern=pattern,
                dm=dm,
            )
        )
    return TenGodInterpretationCollection(
        analysis_id="an-p7-comb-001",
        state=EvaluationStatus.PARTIALLY_RESOLVED,
        items=tuple(items),
        summary=("source:ten_gods_engine", "mc01:not_bound"),
    )


def _visible(strength: TenGodEffectiveStrength = TenGodEffectiveStrength.MODERATE, **extra: object) -> dict[str, object]:
    return {
        "presence": TenGodPresenceState.VISIBLE_AND_ROOTED,
        "strength": strength,
        "month": True,
        **extra,
    }


def _residual() -> dict[str, object]:
    return {
        "presence": TenGodPresenceState.HIDDEN_ONLY,
        "strength": TenGodEffectiveStrength.VERY_WEAK,
        "residual": True,
        "count": 3,
    }


def _by_id(collection, combination_id: str):
    return next(item for item in collection.items if item.combination_id == combination_id)


def test_all_v1_combinations_are_supported() -> None:
    natal = _natal({})
    collection = interpret_ten_god_combinations(natal, mc01_bound=False)
    assert tuple(item.combination_id for item in collection.items) == V1_COMBINATION_IDS


def test_shi_shen_generates_wealth_active() -> None:
    natal = _natal(
        {
            "shi_shen": _visible(TenGodEffectiveStrength.STRONG),
            "pian_cai": _visible(TenGodEffectiveStrength.MODERATE),
        }
    )
    result = _by_id(interpret_ten_god_combinations(natal), "shi_shen_generates_wealth")
    assert result.state is CombinationState.CONFIRMED
    assert result.chain_quality is not ChainQuality.BROKEN


def test_shi_shen_and_wealth_residual_coexistence_is_inactive() -> None:
    natal = _natal({"shi_shen": _residual(), "pian_cai": _residual()})
    result = _by_id(interpret_ten_god_combinations(natal), "shi_shen_generates_wealth")
    assert result.state is CombinationState.INACTIVE


def test_shang_guan_generates_wealth_active() -> None:
    natal = _natal(
        {
            "shang_guan": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_cai": _visible(),
        }
    )
    assert _by_id(interpret_ten_god_combinations(natal), "shang_guan_generates_wealth").state is CombinationState.CONFIRMED


def test_wealth_generates_officer_active() -> None:
    natal = _natal(
        {
            "zheng_cai": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_guan": _visible(),
        }
    )
    assert _by_id(interpret_ten_god_combinations(natal), "wealth_generates_officer").state is CombinationState.CONFIRMED


def test_wealth_officer_resource_chain_broken_intermediate() -> None:
    natal = _natal(
        {
            "zheng_cai": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_yin": _visible(TenGodEffectiveStrength.STRONG),
        }
    )
    result = _by_id(interpret_ten_god_combinations(natal), "wealth_officer_resource_chain")
    assert result.state is CombinationState.BROKEN
    assert result.chain_quality is ChainQuality.BROKEN
    assert result.chain_quality is not ChainQuality.STRONG


def test_valid_three_node_chain_and_dedupe() -> None:
    natal = _natal(
        {
            "zheng_cai": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_guan": _visible(TenGodEffectiveStrength.MODERATE),
            "zheng_yin": _visible(TenGodEffectiveStrength.MODERATE),
        }
    )
    collection = interpret_ten_god_combinations(natal)
    three = _by_id(collection, "wealth_officer_resource_chain")
    assert three.state is CombinationState.CONFIRMED
    assert _by_id(collection, "wealth_generates_officer").source_chain_id == three.chain.chain_id
    assert _by_id(collection, "officer_generates_resource").source_combination_id == three.combination_id


def test_sha_yin_coexist_but_unresolved_without_mc01() -> None:
    natal = _natal(
        {
            "qi_sha": _visible(TenGodEffectiveStrength.STRONG),
            "pian_yin": _visible(TenGodEffectiveStrength.MODERATE),
        }
    )
    result = _by_id(interpret_ten_god_combinations(natal), "killer_resource_day_master_chain")
    assert result.state is CombinationState.UNRESOLVED
    assert result.rescue_ids == ()
    assert "unresolved_dependency" in result.conditions


def test_peer_and_wealth_coexist_but_not_rob() -> None:
    natal = _natal(
        {
            "jie_cai": _visible(TenGodEffectiveStrength.STRONG),
            "pian_cai": _visible(),
        }
    )
    result = _by_id(interpret_ten_god_combinations(natal), "peer_competes_wealth")
    assert result.state is not CombinationState.CONFIRMED
    assert result.damage_ids == ()


def test_weak_day_master_overload_is_unresolved_without_mc01() -> None:
    natal = _natal(
        {"pian_cai": _visible(TenGodEffectiveStrength.VERY_STRONG)},
        dm="weak",
    )
    result = _by_id(interpret_ten_god_combinations(natal), "wealth_exceeds_day_master")
    assert result.state is CombinationState.UNRESOLVED
    assert result.damage_ids == ()


def test_negative_hurting_officer_not_automatic() -> None:
    natal = _natal(
        {
            "shang_guan": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_guan": _visible(),
        }
    )
    result = _by_id(interpret_ten_god_combinations(natal), "hurting_officer_meets_officer")
    assert result.state is not CombinationState.CONFIRMED
    assert result.damage_ids == ()


def test_negative_owl_and_mixed_and_peer() -> None:
    natal = _natal(
        {
            "pian_yin": _visible(TenGodEffectiveStrength.STRONG),
            "shi_shen": _visible(),
            "zheng_guan": _visible(),
            "qi_sha": _visible(),
        }
    )
    collection = interpret_ten_god_combinations(natal)
    assert _by_id(collection, "owl_robs_food_combination").state is not CombinationState.CONFIRMED
    assert _by_id(collection, "officer_killer_mixed").state is not CombinationState.CONFIRMED
    assert all(item.damage_ids == () for item in collection.items)


def test_mc01_boundary_no_damage_rescue_or_pattern_election() -> None:
    natal = _natal(
        {
            "shang_guan": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_guan": _visible(TenGodEffectiveStrength.MODERATE, role=TenGodStructuralRole.PRIMARY_PATTERN),
        },
        pattern="Chính Quan",
    )
    collection = interpret_ten_god_combinations(natal, mc01_bound=False)
    assert all(item.damage_ids == () and item.rescue_ids == () for item in collection.items)
    eco = interpret_ten_gods_ecosystem(natal, collection, mc01_bound=False)
    assert eco.driver.subject == "zheng_guan"
    assert "count" not in eco.driver.basis
    assert eco.driver.basis  # pattern, not frequency


def test_ecosystem_driver_is_not_highest_count() -> None:
    natal = _natal(
        {
            "zheng_guan": _visible(TenGodEffectiveStrength.MODERATE, role=TenGodStructuralRole.PRIMARY_PATTERN),
            "shi_shen": {**_residual(), "count": 5},
        },
        pattern="Chính Quan",
    )
    collection = interpret_ten_god_combinations(natal)
    eco = interpret_ten_gods_ecosystem(natal, collection, mc01_bound=False)
    assert eco.driver.subject == "zheng_guan"
    assert eco.driver.subject != "shi_shen"
    assert "not_occurrence_count" in eco.driver.basis


def test_no_active_chain_means_no_bottleneck() -> None:
    natal = _natal({"zheng_yin": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN)}, pattern="Chính Ấn")
    collection = interpret_ten_god_combinations(natal)
    eco = interpret_ten_gods_ecosystem(natal, collection)
    assert eco.bottleneck.state is EvaluationStatus.NOT_APPLICABLE
    assert not eco.bottleneck.subject


def test_bottleneck_belongs_to_active_chain() -> None:
    natal = _natal(
        {
            "shi_shen": _visible(TenGodEffectiveStrength.STRONG),
            "pian_cai": _visible(TenGodEffectiveStrength.WEAK),
        }
    )
    collection = interpret_ten_god_combinations(natal)
    eco = interpret_ten_gods_ecosystem(natal, collection)
    assert eco.bottleneck.state in {EvaluationStatus.RESOLVED, EvaluationStatus.PARTIALLY_RESOLVED}
    assert eco.bottleneck.source_chain_ids
    assert eco.bottleneck.subject


def test_blocked_output_when_wealth_missing() -> None:
    natal = _natal({"shi_shen": _visible(TenGodEffectiveStrength.STRONG)})
    collection = interpret_ten_god_combinations(natal)
    eco = interpret_ten_gods_ecosystem(natal, collection)
    assert eco.blocked.subject in {"shi_shen", "output"}
    assert eco.blocked.state is EvaluationStatus.RESOLVED


def test_family_profiles_output_wealth_resource_authority_peer() -> None:
    natal = _natal(
        {
            "shi_shen": _visible(TenGodEffectiveStrength.VERY_STRONG),
            "pian_cai": _visible(TenGodEffectiveStrength.VERY_STRONG),
            "zheng_yin": _visible(TenGodEffectiveStrength.VERY_STRONG),
            "zheng_guan": _visible(TenGodEffectiveStrength.VERY_STRONG, role=TenGodStructuralRole.PRIMARY_PATTERN),
            "jie_cai": _visible(TenGodEffectiveStrength.VERY_STRONG),
        },
        pattern="Chính Quan",
        dm="weak",
    )
    eco = interpret_ten_gods_ecosystem(natal, interpret_ten_god_combinations(natal, mc01_bound=False))
    families = {row.family_id: row.dominance for row in eco.family_balances}
    assert families["output"] == "dominant"
    assert families["wealth"] == "dominant"
    assert families["resource"] == "dominant"
    assert families["authority"] == "dominant"
    assert families["peer"] == "dominant"


def test_missing_family_is_not_labeled_bad() -> None:
    natal = _natal({"zheng_guan": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN)}, pattern="Chính Quan")
    eco = interpret_ten_gods_ecosystem(natal, interpret_ten_god_combinations(natal))
    assert "bad" not in eco.missing.basis
    assert "unfavorable" not in " ".join(eco.missing.basis)


def test_metamorphic_break_link_and_remove_chain() -> None:
    intact = _natal(
        {
            "zheng_cai": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_guan": _visible(TenGodEffectiveStrength.MODERATE),
            "zheng_yin": _visible(TenGodEffectiveStrength.MODERATE),
        }
    )
    broken = _natal(
        {
            "zheng_cai": _visible(TenGodEffectiveStrength.STRONG),
            "zheng_yin": _visible(TenGodEffectiveStrength.MODERATE),
        }
    )
    intact_combos = interpret_ten_god_combinations(intact)
    broken_combos = interpret_ten_god_combinations(broken)
    assert _by_id(intact_combos, "wealth_officer_resource_chain").chain_quality is not ChainQuality.BROKEN
    broken_chain = _by_id(broken_combos, "wealth_officer_resource_chain")
    assert broken_chain.chain_quality is ChainQuality.BROKEN
    intact_eco = interpret_ten_gods_ecosystem(intact, intact_combos)
    empty = interpret_ten_gods_ecosystem(
        _natal({"zheng_yin": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN)}, pattern="Chính Ấn"),
        interpret_ten_god_combinations(
            _natal({"zheng_yin": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN)}, pattern="Chính Ấn")
        ),
    )
    if intact_eco.bottleneck.subject:
        assert empty.bottleneck.subject != intact_eco.bottleneck.subject or empty.bottleneck.state is EvaluationStatus.NOT_APPLICABLE


def test_metamorphic_count_increase_does_not_flip_driver() -> None:
    base = _natal(
        {
            "zheng_guan": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN),
            "shi_shen": _residual(),
        },
        pattern="Chính Quan",
    )
    heavier = _natal(
        {
            "zheng_guan": _visible(role=TenGodStructuralRole.PRIMARY_PATTERN),
            "shi_shen": {**_residual(), "count": 8},
        },
        pattern="Chính Quan",
    )
    left = interpret_ten_gods_ecosystem(base, interpret_ten_god_combinations(base))
    right = interpret_ten_gods_ecosystem(heavier, interpret_ten_god_combinations(heavier))
    assert left.driver.subject == right.driver.subject == "zheng_guan"


def test_runtime_binding_path_and_diagnostics() -> None:
    payload = {
        "analysis_id": "an-p7-comb-001",
        "pattern": {"cach_cuc": "Chính Ấn"},
        "score": {"grade": "B"},
        "strength": {"strength_level": "balanced"},
        "ten_gods": {
            "source": "engines.ten_gods_engine",
            "visible": [
                {
                    "pillar": "hour",
                    "stem": "Giáp",
                    "ten_god": GOD_ID_TO_LABEL["shi_shen"],
                    "god_id": "shi_shen",
                    "element": "Mộc",
                },
                {
                    "pillar": "year",
                    "stem": "Ất",
                    "ten_god": GOD_ID_TO_LABEL["pian_cai"],
                    "god_id": "pian_cai",
                    "element": "Mộc",
                },
            ],
            "hidden": [],
        },
    }
    snapshot = deepcopy(payload)
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(payload),
        payload,
    )
    assert payload == snapshot
    ten_gods = context.runtime.interpretation.ten_gods
    assert ten_gods.natal.items
    assert ten_gods.combinations.items
    assert ten_gods.ecosystem.analysis_id == "an-p7-comb-001"
    diagnostics = build_pack07_diagnostics(context)
    assert diagnostics.ten_god_combination is DiagnosticStatus.PARTIAL
    assert diagnostics.ten_gods_ecosystem is DiagnosticStatus.PARTIAL
    assert diagnostics.shen_sha is DiagnosticStatus.NOT_IMPLEMENTED
    empty = build_pack07_diagnostics(build_canonical_analysis_context_from_payload({"analysis_id": "dev-empty"}))
    assert empty.ten_god_combination is DiagnosticStatus.NOT_IMPLEMENTED
    assert empty.ten_gods_ecosystem is DiagnosticStatus.NOT_IMPLEMENTED


def test_case_0001_does_not_hardcode_conclusions() -> None:
    shaped = shape_ten_gods_payload(run_case_0001())
    payload = {
        "analysis_id": "CASE-0001",
        "pattern": {"cach_cuc": "Chính Ấn"},
        "strength": {"strength_level": "balanced"},
        "ten_gods": shaped,
    }
    natal = interpret_ten_gods(payload, analysis_id="CASE-0001")
    combos = interpret_ten_god_combinations(natal, mc01_bound=False)
    eco = interpret_ten_gods_ecosystem(natal, combos, mc01_bound=False)
    confirmed = [item.combination_id for item in combos.items if item.state is CombinationState.CONFIRMED]
    unresolved = [item.combination_id for item in combos.items if item.state is CombinationState.UNRESOLVED]
    assert "thien_quan" not in confirmed
    assert eco.driver.basis and "count" not in eco.driver.basis
    assert all(item.damage_ids == () for item in combos.items)
    assert combos.state is EvaluationStatus.PARTIALLY_RESOLVED
    assert isinstance(confirmed, list)
    assert isinstance(unresolved, list)
