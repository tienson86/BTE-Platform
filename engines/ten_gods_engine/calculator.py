"""Ten Gods Core Engine calculator."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from engines.ten_gods_engine.constants import (
    GOD_ID_TO_LABEL,
    PILLAR_ORDER,
    TEN_GOD_IDS,
    VISIBLE_STEM_WEIGHT,
)
from engines.ten_gods_engine.dominance import resolve_dominance
from engines.ten_gods_engine.exceptions import TenGodsValidationError
from engines.ten_gods_engine.hierarchy import assign_hierarchy
from engines.ten_gods_engine.interaction_matrix import build_interaction_matrix
from engines.ten_gods_engine.loader import HiddenStemWeightLoader
from engines.bazi_engine.ten_god import stem_mapping_facts
from engines.ten_gods_engine.mapper import day_master_info, map_stem_to_ten_god
from engines.ten_gods_engine.models import (
    DayMasterInfo,
    DiagnosticEntry,
    DistributionEntry,
    HiddenTenGodEntry,
    TenGodsResult,
    VisibleTenGodEntry,
    WeightEntry,
)
from engines.ten_gods_engine.relationships import build_relationship_graph


@dataclass(frozen=True, slots=True)
class PillarInput:
    """One pillar stem and branch."""

    stem: str
    branch: str


class TenGodsCalculator:
    """Map visible and hidden stems to Ten Gods and aggregate analytics."""

    def __init__(
        self,
        *,
        hidden_loader: HiddenStemWeightLoader | None = None,
    ) -> None:
        self._hidden_loader = hidden_loader or HiddenStemWeightLoader()

    def calculate(
        self,
        *,
        day_master: str,
        pillars: dict[str, PillarInput],
        case_id: str | None = None,
    ) -> TenGodsResult:
        """Run full Ten Gods pipeline for a four-pillar chart."""
        self._validate_pillars(day_master, pillars)

        dm_raw = day_master_info(day_master)
        dm = DayMasterInfo(
            stem=dm_raw["stem"],
            element=dm_raw["element"],
            yin_yang=dm_raw["yin_yang"],
        )

        visible, hidden, weights, missing = self._map_layers(
            day_master=day_master,
            pillars=pillars,
        )
        distribution = self._build_distribution(visible, hidden, weights)
        dominant = resolve_dominance(distribution)
        hierarchy = assign_hierarchy(distribution, dominant)

        present_ids = {
            entry.god_id
            for entry in (*visible, *hidden)
        }
        relationships = build_relationship_graph(present_ids)
        interaction_matrix = build_interaction_matrix(present_ids)

        diagnostics = (
            DiagnosticEntry(
                code="ten_gods_core_completed",
                message="Ten Gods Core Engine calculation completed",
                level="info",
            ),
        )
        if case_id:
            diagnostics = (
                DiagnosticEntry(
                    code="case_id",
                    message=f"case_id={case_id}",
                    level="info",
                ),
                *diagnostics,
            )

        return TenGodsResult(
            day_master=dm,
            visible=visible,
            hidden=hidden,
            distribution=distribution,
            weights=weights,
            dominant=dominant,
            hierarchy=hierarchy,
            relationships=relationships,
            interaction_matrix=interaction_matrix,
            missing_data=tuple(sorted(missing)),
            diagnostics=diagnostics,
        )

    def _validate_pillars(
        self,
        day_master: str,
        pillars: dict[str, PillarInput],
    ) -> None:
        if not day_master:
            raise TenGodsValidationError("day_master is required")
        for pillar in PILLAR_ORDER:
            if pillar not in pillars:
                raise TenGodsValidationError(f"Missing pillar '{pillar}'")
            node = pillars[pillar]
            if not node.stem or not node.branch:
                raise TenGodsValidationError(
                    f"Pillar '{pillar}' requires stem and branch",
                )
        if pillars["day"].stem != day_master:
            raise TenGodsValidationError(
                "day pillar stem must equal day_master",
            )

    def _map_layers(
        self,
        *,
        day_master: str,
        pillars: dict[str, PillarInput],
    ) -> tuple[
        tuple[VisibleTenGodEntry, ...],
        tuple[HiddenTenGodEntry, ...],
        tuple[WeightEntry, ...],
        set[str],
    ]:
        visible: list[VisibleTenGodEntry] = []
        hidden: list[HiddenTenGodEntry] = []
        weights: list[WeightEntry] = []
        missing: set[str] = set()

        for pillar in PILLAR_ORDER:
            node = pillars[pillar]
            label, god_id = map_stem_to_ten_god(
                day_master,
                node.stem,
                pillar=pillar,
                visibility="visible",
            )
            facts = stem_mapping_facts(day_master, node.stem)
            evidence = f"visible:{pillar}:{node.stem}"
            visible.append(
                VisibleTenGodEntry(
                    pillar=pillar,
                    stem=node.stem,
                    ten_god=label,
                    god_id=god_id,
                    visibility="visible",
                    evidence=evidence,
                    element=facts["element"],
                    yin_yang=facts["yin_yang"],
                    element_relation=facts["element_relation"],
                    polarity_relation=facts["polarity_relation"],
                )
            )
            weights.append(
                WeightEntry(
                    god_id=god_id,
                    label=label,
                    layer="visible",
                    pillar=pillar,
                    weight=VISIBLE_STEM_WEIGHT,
                    evidence=evidence,
                )
            )

            try:
                slots = self._hidden_loader.load_branch_slots(node.branch)
            except Exception as exc:
                missing.add(f"hidden_weights:{node.branch}")
                raise TenGodsValidationError(
                    f"Hidden stem weights unavailable for branch '{node.branch}'",
                ) from exc

            for slot in slots:
                h_label, h_god_id = map_stem_to_ten_god(
                    day_master,
                    slot.hidden_stem,
                    pillar=pillar,
                    visibility="hidden",
                )
                h_facts = stem_mapping_facts(day_master, slot.hidden_stem)
                h_evidence = (
                    f"hidden:{pillar}:{node.branch}:"
                    f"{slot.position_name}:{slot.hidden_stem}"
                )
                hidden.append(
                    HiddenTenGodEntry(
                        pillar=pillar,
                        branch=node.branch,
                        hidden_stem=slot.hidden_stem,
                        hidden_position=slot.hidden_position,
                        position_name=slot.position_name,
                        weight=slot.weight,
                        ten_god=h_label,
                        god_id=h_god_id,
                        evidence=h_evidence,
                        element=h_facts["element"],
                        yin_yang=h_facts["yin_yang"],
                        element_relation=h_facts["element_relation"],
                        polarity_relation=h_facts["polarity_relation"],
                    )
                )
                weights.append(
                    WeightEntry(
                        god_id=h_god_id,
                        label=h_label,
                        layer="hidden",
                        pillar=pillar,
                        weight=slot.weight,
                        evidence=h_evidence,
                    )
                )

        visible.sort(key=lambda item: (PILLAR_ORDER.index(item.pillar), item.god_id))
        hidden.sort(
            key=lambda item: (
                PILLAR_ORDER.index(item.pillar),
                item.hidden_position,
                item.god_id,
            )
        )
        weights.sort(
            key=lambda item: (
                item.layer,
                PILLAR_ORDER.index(item.pillar),
                item.god_id,
                item.evidence,
            )
        )
        return tuple(visible), tuple(hidden), tuple(weights), missing

    def _build_distribution(
        self,
        visible: tuple[VisibleTenGodEntry, ...],
        hidden: tuple[HiddenTenGodEntry, ...],
        weights: tuple[WeightEntry, ...],
    ) -> tuple[DistributionEntry, ...]:
        occurrence: dict[str, int] = defaultdict(int)
        visible_count: dict[str, int] = defaultdict(int)
        hidden_weight: dict[str, float] = defaultdict(float)
        weighted: dict[str, float] = defaultdict(float)

        for entry in visible:
            occurrence[entry.god_id] += 1
            visible_count[entry.god_id] += 1
        for entry in hidden:
            occurrence[entry.god_id] += 1
            hidden_weight[entry.god_id] += entry.weight

        for entry in weights:
            weighted[entry.god_id] += entry.weight

        distribution: list[DistributionEntry] = []
        all_ids = sorted(
            set(TEN_GOD_IDS) | set(weighted.keys()) | {"day_master"},
            key=lambda god_id: (god_id != "day_master", god_id),
        )
        for god_id in all_ids:
            if god_id == "day_master":
                label = "Nhật Chủ"
            else:
                label = GOD_ID_TO_LABEL.get(god_id, god_id)
            distribution.append(
                DistributionEntry(
                    god_id=god_id,
                    label=label,
                    occurrence_count=occurrence.get(god_id, 0),
                    weighted_contribution=round(weighted.get(god_id, 0.0), 4),
                    visible_count=visible_count.get(god_id, 0),
                    hidden_weight=round(hidden_weight.get(god_id, 0.0), 4),
                )
            )
        return tuple(distribution)
