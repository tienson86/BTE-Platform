"""Deterministic Combination calculator (knowledge-driven)."""

from __future__ import annotations

from itertools import combinations
from typing import Any, Mapping, Sequence

from engines.analysis_engine.combination_engine.exceptions import (
    CombinationExecutionError,
    CombinationValidationError,
)
from engines.analysis_engine.combination_engine.knowledge_access import (
    ASSET_BRANCH_COMBINATIONS,
    ASSET_CLASH,
    ASSET_CONFIDENCE,
    ASSET_DESTRUCTION,
    ASSET_HARM,
    ASSET_HIDDEN_COMBINATION,
    ASSET_PRIORITY,
    ASSET_PUNISHMENT,
    ASSET_STEM_COMBINATIONS,
    ASSET_TRANSFORMATION,
    ASSET_UPSTREAM_QUALIFIERS,
    MODULE_ID,
    KnowledgeSession,
)
from engines.analysis_engine.combination_engine.models import (
    CombinationResult,
    RejectedAlternative,
    RelationOutcome,
    TransformationOutcome,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)

PILLAR_ORDER: tuple[str, ...] = ("year", "month", "day", "hour")


class CombinationCalculator:
    """Execute Combination analytical steps using Knowledge SDK assets only."""

    def calculate(
        self,
        context: AnalysisContext,
        *,
        session: KnowledgeSession,
        upstream: Mapping[str, StageResult],
    ) -> CombinationResult:
        """Run the full deterministic Combination algorithm."""
        try:
            module = session.get_module(MODULE_ID)
            stem_asset = session.get_asset(ASSET_STEM_COMBINATIONS)
            branch_asset = session.get_asset(ASSET_BRANCH_COMBINATIONS)
            clash_asset = session.get_asset(ASSET_CLASH)
            harm_asset = session.get_asset(ASSET_HARM)
            punish_asset = session.get_asset(ASSET_PUNISHMENT)
            destroy_asset = session.get_asset(ASSET_DESTRUCTION)
            hidden_asset = session.get_asset(ASSET_HIDDEN_COMBINATION)
            transform_asset = session.get_asset(ASSET_TRANSFORMATION)
            qualifier_asset = session.get_asset(ASSET_UPSTREAM_QUALIFIERS)
            priority_asset = session.get_asset(ASSET_PRIORITY)
            confidence_asset = session.get_asset(ASSET_CONFIDENCE)

            evidence: list[RuleEvidence] = [
                RuleEvidence(
                    rule_id=MODULE_ID,
                    version=module.version,
                    category="module",
                    priority=100,
                    reference=MODULE_ID,
                )
            ]

            stems = self._pillar_values(context, "stems", "stem")
            branches = self._pillar_values(context, "branches", "branch")

            stem_combinations = self._detect_pairs(
                relation_type="stem_combination",
                pillar_values=stems,
                pairs=stem_asset.data.get("pairs") or [],
                priority=int(stem_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_STEM_COMBINATIONS,
                include_result_element=True,
            )
            branch_six = self._detect_pairs(
                relation_type="branch_combination",
                pillar_values=branches,
                pairs=branch_asset.data.get("six_combinations") or [],
                priority=int(branch_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_BRANCH_COMBINATIONS,
                include_result_element=True,
            )
            branch_triads = self._detect_groups(
                relation_type="branch_combination",
                pillar_values=branches,
                groups=branch_asset.data.get("triads") or [],
                priority=int(branch_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_BRANCH_COMBINATIONS,
            )
            branch_combinations = branch_six + branch_triads

            clashes = self._detect_pairs(
                relation_type="clash",
                pillar_values=branches,
                pairs=clash_asset.data.get("pairs") or [],
                priority=int(clash_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_CLASH,
            )
            harms = self._detect_pairs(
                relation_type="harm",
                pillar_values=branches,
                pairs=harm_asset.data.get("pairs") or [],
                priority=int(harm_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_HARM,
            )
            punishments = self._detect_punishments(
                branches,
                punish_asset.data.get("rules") or [],
                priority=int(punish_asset.data.get("priority", 0)),
                evidence=evidence,
            )
            destructions = self._detect_pairs(
                relation_type="destruction",
                pillar_values=branches,
                pairs=destroy_asset.data.get("pairs") or [],
                priority=int(destroy_asset.data.get("priority", 0)),
                evidence=evidence,
                reference=ASSET_DESTRUCTION,
            )
            hidden = self._detect_hidden(
                branches,
                stems,
                hidden_asset.data,
                evidence=evidence,
            )

            candidates = (
                stem_combinations
                + branch_combinations
                + clashes
                + harms
                + punishments
                + destructions
                + hidden
            )

            qualifier_effects = self._upstream_qualifiers(
                upstream,
                qualifier_asset.data,
                evidence,
            )
            transformations, transform_rejected = self._evaluate_transformations(
                stem_combinations + branch_six,
                clashes,
                transform_asset.data,
                qualifier_effects,
                evidence,
            )
            active, rejected = self._resolve_conflicts(
                candidates,
                clashes,
                priority_asset.data,
                evidence,
            )
            rejected.extend(transform_rejected)

            confidence = self._aggregate_confidence(
                active,
                transformations,
                rejected,
                qualifier_effects,
                confidence_asset.data,
            )

            diagnostics = (
                DiagnosticInfo(
                    code="combination_completed",
                    message="Combination evaluation completed",
                    level="info",
                    stage_id="combination",
                    details={
                        "candidate_count": len(candidates),
                        "active_count": len(active),
                    },
                ),
            )

            return CombinationResult(
                stem_combinations=tuple(self._sort_relations(stem_combinations)),
                branch_combinations=tuple(self._sort_relations(branch_combinations)),
                clashes=tuple(self._sort_relations(clashes)),
                harms=tuple(self._sort_relations(harms)),
                punishments=tuple(self._sort_relations(punishments)),
                destructions=tuple(self._sort_relations(destructions)),
                hidden_combinations=tuple(self._sort_relations(hidden)),
                transformations=tuple(
                    sorted(
                        transformations,
                        key=lambda item: (
                            -item.priority,
                            item.source_relation_id,
                            item.success,
                        ),
                    )
                ),
                active_relations=tuple(self._sort_relations(active)),
                rejected_alternatives=tuple(
                    sorted(
                        rejected,
                        key=lambda item: (
                            item.subject,
                            item.rejected_value,
                            item.selected_value,
                        ),
                    )
                ),
                confidence=confidence,
                evidence=tuple(evidence),
                diagnostics=diagnostics,
                knowledge_module_id=MODULE_ID,
                knowledge_version=module.version,
                summary={
                    "candidate_count": len(candidates),
                    "active_count": len(active),
                    "transform_success_count": sum(
                        1 for item in transformations if item.success
                    ),
                    "relation_types": sorted({item.relation_type for item in active}),
                },
            )
        except (CombinationValidationError, CombinationExecutionError):
            raise
        except Exception as exc:
            raise CombinationExecutionError(
                f"Combination calculation failed: {exc}",
                details={"exception_type": type(exc).__name__},
            ) from exc

    def _detect_pairs(
        self,
        *,
        relation_type: str,
        pillar_values: Mapping[str, str],
        pairs: Sequence[Mapping[str, Any]],
        priority: int,
        evidence: list[RuleEvidence],
        reference: str,
        include_result_element: bool = False,
    ) -> list[RelationOutcome]:
        value_to_pillars: dict[str, list[str]] = {}
        for pillar, value in pillar_values.items():
            value_to_pillars.setdefault(value, []).append(pillar)

        outcomes: list[RelationOutcome] = []
        seen: set[tuple[str, tuple[str, ...]]] = set()

        for row in pairs:
            left = str(row["a"])
            right = str(row["b"])
            relation_id = str(row["relation_id"])
            left_pillars = value_to_pillars.get(left, [])
            right_pillars = value_to_pillars.get(right, [])
            if left == right:
                # self-pair needs two distinct pillars with same value
                if len(left_pillars) < 2:
                    continue
                for p1, p2 in combinations(sorted(left_pillars), 2):
                    key = (relation_id, (p1, p2))
                    if key in seen:
                        continue
                    seen.add(key)
                    outcome = RelationOutcome(
                        relation_type=relation_type,
                        relation_id=relation_id,
                        members=(left, right),
                        pillars=(p1, p2),
                        status="active",
                        result_element=str(row["result_element"])
                        if include_result_element and row.get("result_element")
                        else None,
                        priority=priority,
                    )
                    outcomes.append(outcome)
                continue

            if not left_pillars or not right_pillars:
                continue
            for p_left in left_pillars:
                for p_right in right_pillars:
                    pillars = tuple(sorted((p_left, p_right), key=self._pillar_rank))
                    key = (relation_id, pillars)
                    if key in seen:
                        continue
                    seen.add(key)
                    members = tuple(sorted((left, right)))
                    outcome = RelationOutcome(
                        relation_type=relation_type,
                        relation_id=relation_id,
                        members=members,
                        pillars=pillars,
                        status="active",
                        result_element=str(row["result_element"])
                        if include_result_element and row.get("result_element")
                        else None,
                        priority=priority,
                        details={"raw_pair": [left, right]},
                    )
                    outcomes.append(outcome)
                    evidence.append(
                        RuleEvidence(
                            rule_id=f"{relation_type}:{relation_id}:{pillars[0]}:{pillars[1]}",
                            version="1.0.0",
                            category=relation_type,
                            priority=priority,
                            reference=reference,
                        )
                    )
        return outcomes

    def _detect_groups(
        self,
        *,
        relation_type: str,
        pillar_values: Mapping[str, str],
        groups: Sequence[Mapping[str, Any]],
        priority: int,
        evidence: list[RuleEvidence],
        reference: str,
    ) -> list[RelationOutcome]:
        present = set(pillar_values.values())
        outcomes: list[RelationOutcome] = []
        for row in groups:
            members = tuple(sorted(str(item) for item in row.get("members") or []))
            if not members:
                continue
            if not set(members).issubset(present):
                continue
            pillars: list[str] = []
            for member in members:
                for pillar, value in pillar_values.items():
                    if value == member and pillar not in pillars:
                        pillars.append(pillar)
                        break
            pillars_sorted = tuple(sorted(pillars, key=self._pillar_rank))
            outcome = RelationOutcome(
                relation_type=relation_type,
                relation_id=str(row["relation_id"]),
                members=members,
                pillars=pillars_sorted,
                status="active",
                result_element=str(row["result_element"])
                if row.get("result_element")
                else None,
                priority=priority,
                details={"mode": "triad"},
            )
            outcomes.append(outcome)
            evidence.append(
                RuleEvidence(
                    rule_id=f"{relation_type}:{outcome.relation_id}",
                    version="1.0.0",
                    category=relation_type,
                    priority=priority,
                    reference=reference,
                )
            )
        return outcomes

    def _detect_punishments(
        self,
        branches: Mapping[str, str],
        rules: Sequence[Mapping[str, Any]],
        *,
        priority: int,
        evidence: list[RuleEvidence],
    ) -> list[RelationOutcome]:
        outcomes: list[RelationOutcome] = []
        present_values = list(branches.values())
        value_to_pillars: dict[str, list[str]] = {}
        for pillar, value in branches.items():
            value_to_pillars.setdefault(value, []).append(pillar)

        for row in rules:
            mode = str(row.get("mode") or "pair")
            relation_id = str(row["relation_id"])
            if mode == "triad":
                members = [str(item) for item in row.get("members") or []]
                if set(members).issubset(set(present_values)):
                    pillars = []
                    for member in members:
                        pillars.append(sorted(value_to_pillars[member])[0])
                    outcome = RelationOutcome(
                        relation_type="punishment",
                        relation_id=relation_id,
                        members=tuple(sorted(members)),
                        pillars=tuple(sorted(pillars, key=self._pillar_rank)),
                        status="active",
                        priority=priority,
                        details={"mode": mode},
                    )
                    outcomes.append(outcome)
            elif mode == "self":
                value = str(row["a"])
                pillars = value_to_pillars.get(value, [])
                if len(pillars) >= 2:
                    for p1, p2 in combinations(sorted(pillars), 2):
                        outcome = RelationOutcome(
                            relation_type="punishment",
                            relation_id=relation_id,
                            members=(value, value),
                            pillars=(p1, p2),
                            status="active",
                            priority=priority,
                            details={"mode": mode},
                        )
                        outcomes.append(outcome)
            else:
                left = str(row["a"])
                right = str(row["b"])
                if left in value_to_pillars and right in value_to_pillars:
                    for p_left in value_to_pillars[left]:
                        for p_right in value_to_pillars[right]:
                            if p_left == p_right:
                                continue
                            pillars = tuple(
                                sorted((p_left, p_right), key=self._pillar_rank)
                            )
                            outcome = RelationOutcome(
                                relation_type="punishment",
                                relation_id=relation_id,
                                members=tuple(sorted((left, right))),
                                pillars=pillars,
                                status="active",
                                priority=priority,
                                details={"mode": mode},
                            )
                            outcomes.append(outcome)

            if outcomes and outcomes[-1].relation_id == relation_id:
                evidence.append(
                    RuleEvidence(
                        rule_id=f"punishment:{relation_id}",
                        version="1.0.0",
                        category="punishment",
                        priority=priority,
                        reference=ASSET_PUNISHMENT,
                    )
                )
        # Deduplicate
        unique: dict[tuple[str, tuple[str, ...]], RelationOutcome] = {}
        for item in outcomes:
            unique[(item.relation_id, item.pillars)] = item
        return list(unique.values())

    def _detect_hidden(
        self,
        branches: Mapping[str, str],
        stems: Mapping[str, str],
        hidden_data: Mapping[str, Any],
        *,
        evidence: list[RuleEvidence],
    ) -> list[RelationOutcome]:
        hidden_map = hidden_data.get("hidden_stems") or {}
        stem_pairs = hidden_data.get("stem_pairs") or []
        priority = int(hidden_data.get("priority", 0))
        chart_stems = set(stems.values())

        hidden_by_pillar: dict[str, list[str]] = {}
        for pillar, branch in branches.items():
            hidden_by_pillar[pillar] = list(hidden_map.get(branch) or [])

        outcomes: list[RelationOutcome] = []
        seen: set[tuple[str, tuple[str, ...]]] = set()
        pillars = list(branches.keys())
        for p1, p2 in combinations(sorted(pillars, key=self._pillar_rank), 2):
            hidden_left = hidden_by_pillar.get(p1, [])
            hidden_right = hidden_by_pillar.get(p2, [])
            for row in stem_pairs:
                a = str(row["a"])
                b = str(row["b"])
                relation_id = f"hidden_{row['relation_id']}"
                matched = (
                    (a in hidden_left and b in hidden_right)
                    or (b in hidden_left and a in hidden_right)
                    or (a in hidden_left and b in chart_stems)
                    or (b in hidden_left and a in chart_stems)
                    or (a in hidden_right and b in chart_stems)
                    or (b in hidden_right and a in chart_stems)
                )
                if not matched:
                    continue
                pillar_key = tuple(sorted((p1, p2), key=self._pillar_rank))
                key = (relation_id, pillar_key)
                if key in seen:
                    continue
                seen.add(key)
                outcome = RelationOutcome(
                    relation_type="hidden_combination",
                    relation_id=relation_id,
                    members=tuple(sorted((a, b))),
                    pillars=pillar_key,
                    status="active",
                    result_element=str(row["result_element"])
                    if row.get("result_element")
                    else None,
                    priority=priority,
                )
                outcomes.append(outcome)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"hidden_combination:{relation_id}:{pillar_key[0]}:{pillar_key[1]}",
                        version="1.0.0",
                        category="hidden_combination",
                        priority=priority,
                        reference=ASSET_HIDDEN_COMBINATION,
                    )
                )
        return outcomes

    def _upstream_qualifiers(
        self,
        upstream: Mapping[str, StageResult],
        qualifier_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[str]:
        effects: list[str] = []
        strength_class = str(
            (upstream["strength"].payload or {}).get("classification") or ""
        )
        ten_gods_payload = upstream["ten_gods"].payload or {}
        has_ten_gods = bool(ten_gods_payload.get("presence"))

        for row in qualifier_data.get("rows") or []:
            dimension = str(row.get("dimension"))
            if dimension == "strength":
                if str(row.get("classification")) == strength_class:
                    effects.append(str(row.get("effect")))
                    evidence.append(
                        RuleEvidence(
                            rule_id=f"qualifier:strength:{strength_class}",
                            version="1.0.0",
                            category="upstream_qualifier",
                            priority=int(row.get("priority", 0)),
                            reference=ASSET_UPSTREAM_QUALIFIERS,
                        )
                    )
            elif dimension == "ten_gods":
                if bool(row.get("has_presence")) == has_ten_gods:
                    effects.append(str(row.get("effect")))
                    evidence.append(
                        RuleEvidence(
                            rule_id="qualifier:ten_gods:presence",
                            version="1.0.0",
                            category="upstream_qualifier",
                            priority=int(row.get("priority", 0)),
                            reference=ASSET_UPSTREAM_QUALIFIERS,
                        )
                    )
        return sorted(set(effects))

    def _evaluate_transformations(
        self,
        combination_candidates: Sequence[RelationOutcome],
        clashes: Sequence[RelationOutcome],
        transform_data: Mapping[str, Any],
        qualifier_effects: Sequence[str],
        evidence: list[RuleEvidence],
    ) -> tuple[list[TransformationOutcome], list[RejectedAlternative]]:
        clash_members = {
            member for clash in clashes for member in clash.members
        }
        clash_blocks = bool(transform_data.get("clash_blocks_transform", True))
        priority = int(transform_data.get("priority", 0))
        outcomes: list[TransformationOutcome] = []
        rejected: list[RejectedAlternative] = []

        for candidate in combination_candidates:
            reason_codes: list[str] = []
            success = True
            if clash_blocks and set(candidate.members) & clash_members:
                success = False
                reason_codes.append("blocked_by_clash")
            if "weaken_transform" in qualifier_effects:
                success = False
                reason_codes.append("weak_strength")
            if "stabilize_transform" in qualifier_effects and success:
                reason_codes.append("stabilized_by_strength")
            if not reason_codes:
                reason_codes.append("default_success" if success else "default_failure")

            outcome = TransformationOutcome(
                source_relation_id=candidate.relation_id,
                success=success,
                result_element=candidate.result_element if success else None,
                reason_codes=tuple(sorted(set(reason_codes))),
                priority=priority,
            )
            outcomes.append(outcome)
            evidence.append(
                RuleEvidence(
                    rule_id=f"transformation:{candidate.relation_id}:{success}",
                    version="1.0.0",
                    category="transformation",
                    priority=priority,
                    reference=ASSET_TRANSFORMATION,
                    details={"reason_codes": list(outcome.reason_codes)},
                )
            )
            if not success and candidate.result_element:
                rejected.append(
                    RejectedAlternative(
                        subject=f"transformation:{candidate.relation_id}",
                        rejected_value=str(candidate.result_element),
                        selected_value="none",
                        reason_code=outcome.reason_codes[0],
                    )
                )
        return outcomes, rejected

    def _resolve_conflicts(
        self,
        candidates: Sequence[RelationOutcome],
        clashes: Sequence[RelationOutcome],
        priority_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> tuple[list[RelationOutcome], list[RejectedAlternative]]:
        type_priority = priority_data.get("type_priority") or {}
        clash_pillars = {pillar for clash in clashes for pillar in clash.pillars}

        # Clash blocks overlapping branch combinations on shared pillars.
        active: list[RelationOutcome] = []
        rejected: list[RejectedAlternative] = []
        for candidate in candidates:
            blocked = False
            if (
                candidate.relation_type
                in {"branch_combination", "hidden_combination"}
                and set(candidate.pillars) & clash_pillars
                and candidate.relation_type != "clash"
            ):
                blocked = True
            status = "blocked" if blocked else "active"
            updated = RelationOutcome(
                relation_type=candidate.relation_type,
                relation_id=candidate.relation_id,
                members=candidate.members,
                pillars=candidate.pillars,
                status=status,
                result_element=None if blocked else candidate.result_element,
                priority=int(
                    type_priority.get(candidate.relation_type, candidate.priority)
                ),
                details=dict(candidate.details),
            )
            if blocked:
                rejected.append(
                    RejectedAlternative(
                        subject=f"{candidate.relation_type}:{candidate.relation_id}",
                        rejected_value="active",
                        selected_value="blocked",
                        reason_code="overlap_with_clash",
                    )
                )
                evidence.append(
                    RuleEvidence(
                        rule_id=f"conflict:{candidate.relation_id}:blocked",
                        version="1.0.0",
                        category="conflict_resolution",
                        priority=updated.priority,
                        reference=ASSET_PRIORITY,
                    )
                )
            else:
                active.append(updated)

        active.sort(
            key=lambda item: (
                -item.priority,
                item.relation_type,
                item.relation_id,
                item.pillars,
            )
        )
        return active, rejected

    def _aggregate_confidence(
        self,
        active: Sequence[RelationOutcome],
        transformations: Sequence[TransformationOutcome],
        rejected: Sequence[RejectedAlternative],
        qualifier_effects: Sequence[str],
        confidence_data: Mapping[str, Any],
    ) -> ConfidenceEvaluation:
        weights = confidence_data.get("weights") or {}
        components = {
            "detection": 1.0 if active else 0.4,
            "transformation": (
                sum(1.0 for item in transformations if item.success)
                / max(1, len(transformations))
                if transformations
                else 0.5
            ),
            "resolution": 1.0 if rejected or active else 0.5,
            "upstream": 1.0 if qualifier_effects else 0.5,
        }
        score = 0.0
        for key, weight in weights.items():
            score += float(weight) * float(components.get(key, 0.0))
        score = round(min(1.0, max(0.0, score)), 4)

        level = "low"
        levels = sorted(
            confidence_data.get("levels") or [],
            key=lambda row: float(row.get("min", 0.0)),
            reverse=True,
        )
        for row in levels:
            if score >= float(row.get("min", 0.0)):
                level = str(row.get("level"))
                break

        return ConfidenceEvaluation(
            score=score,
            level=level,
            details={"components": components, "weights": dict(weights)},
        )

    @staticmethod
    def _pillar_values(
        context: AnalysisContext,
        key: str,
        pillar_field: str,
    ) -> dict[str, str]:
        chart = dict(context.chart)
        direct = chart.get(key)
        result: dict[str, str] = {}
        if isinstance(direct, dict):
            for pillar in PILLAR_ORDER:
                if pillar in direct and direct[pillar]:
                    result[pillar] = str(direct[pillar])
            for pillar, value in direct.items():
                if pillar not in result and value:
                    result[str(pillar)] = str(value)
            return result

        pillars = chart.get("pillars")
        if isinstance(pillars, dict):
            for pillar in PILLAR_ORDER:
                node = pillars.get(pillar) or {}
                if isinstance(node, dict) and node.get(pillar_field):
                    result[pillar] = str(node[pillar_field])
        return result

    @staticmethod
    def _pillar_rank(pillar: str) -> tuple[int, str]:
        try:
            return (PILLAR_ORDER.index(pillar), pillar)
        except ValueError:
            return (len(PILLAR_ORDER), pillar)

    @staticmethod
    def _sort_relations(
        items: Sequence[RelationOutcome],
    ) -> list[RelationOutcome]:
        return sorted(
            items,
            key=lambda item: (
                -item.priority,
                item.relation_type,
                item.relation_id,
                item.pillars,
                item.members,
            ),
        )
