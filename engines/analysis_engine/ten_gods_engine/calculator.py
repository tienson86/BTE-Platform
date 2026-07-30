"""Deterministic Ten Gods calculator (knowledge-driven)."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)
from engines.analysis_engine.ten_gods_engine.exceptions import (
    TenGodsConflictResolutionError,
    TenGodsExecutionError,
    TenGodsValidationError,
)
from engines.analysis_engine.ten_gods_engine.knowledge_access import (
    ASSET_CONFIDENCE,
    ASSET_FAVORABILITY,
    ASSET_IDENTITIES,
    ASSET_LIFE_AREAS,
    ASSET_PATTERN_INTERACTIONS,
    ASSET_PRIORITY,
    ASSET_RELATIONSHIPS,
    ASSET_STEM_RELATIONS,
    ASSET_STRENGTH_INTERACTIONS,
    ASSET_TEMPERATURE_INTERACTIONS,
    ASSET_USEFUL_GOD_INTERACTIONS,
    MODULE_ID,
    KnowledgeSession,
)
from engines.analysis_engine.ten_gods_engine.models import (
    FavorabilityOutcome,
    InteractionOutcome,
    LifeAreaConcept,
    RejectedAlternative,
    RelationshipOutcome,
    TenGodPresence,
    TenGodsResult,
)


class TenGodsCalculator:
    """Execute Ten Gods analytical steps using Knowledge SDK assets only."""

    def calculate(
        self,
        context: AnalysisContext,
        *,
        session: KnowledgeSession,
        upstream: Mapping[str, StageResult],
    ) -> TenGodsResult:
        """Run the full deterministic Ten Gods algorithm."""
        try:
            module = session.get_module(MODULE_ID)
            identities = session.get_asset(ASSET_IDENTITIES)
            stem_relations = session.get_asset(ASSET_STEM_RELATIONS)
            relationships = session.get_asset(ASSET_RELATIONSHIPS)
            strength_ix = session.get_asset(ASSET_STRENGTH_INTERACTIONS)
            temperature_ix = session.get_asset(ASSET_TEMPERATURE_INTERACTIONS)
            pattern_ix = session.get_asset(ASSET_PATTERN_INTERACTIONS)
            useful_god_ix = session.get_asset(ASSET_USEFUL_GOD_INTERACTIONS)
            favorability_asset = session.get_asset(ASSET_FAVORABILITY)
            life_areas_asset = session.get_asset(ASSET_LIFE_AREAS)
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

            presence = self._derive_presence(
                context,
                identities.data,
                stem_relations.data,
                evidence,
            )
            relationship_outcomes = self._evaluate_relationships(
                presence,
                relationships.data,
                evidence,
            )
            interactions = self._evaluate_interactions(
                presence,
                upstream,
                strength_ix.data,
                temperature_ix.data,
                pattern_ix.data,
                useful_god_ix.data,
                evidence,
            )
            favorability, rejected = self._resolve_favorability(
                presence,
                interactions,
                upstream,
                favorability_asset.data,
                priority_asset.data,
                evidence,
            )
            life_areas = self._evaluate_life_areas(
                presence,
                life_areas_asset.data,
                evidence,
            )
            confidence = self._aggregate_confidence(
                presence,
                relationship_outcomes,
                interactions,
                favorability,
                life_areas,
                confidence_asset.data,
            )
            diagnostics = (
                DiagnosticInfo(
                    code="ten_gods_completed",
                    message="Ten Gods evaluation completed",
                    level="info",
                    stage_id="ten_gods",
                    details={"presence_count": len(presence)},
                ),
            )
            unique_ids = tuple(sorted({item.god_id for item in presence}))
            return TenGodsResult(
                presence=tuple(presence),
                relationships=tuple(relationship_outcomes),
                interactions=tuple(interactions),
                favorability=tuple(favorability),
                life_areas=tuple(life_areas),
                rejected_alternatives=tuple(rejected),
                confidence=confidence,
                evidence=tuple(evidence),
                diagnostics=diagnostics,
                knowledge_module_id=MODULE_ID,
                knowledge_version=module.version,
                summary={
                    "unique_god_ids": list(unique_ids),
                    "presence_count": len(presence),
                    "dominant_god_id": unique_ids[0] if unique_ids else None,
                },
            )
        except (
            TenGodsValidationError,
            TenGodsConflictResolutionError,
            TenGodsExecutionError,
        ):
            raise
        except Exception as exc:
            raise TenGodsExecutionError(
                f"Ten Gods calculation failed: {exc}",
                details={"exception_type": type(exc).__name__},
            ) from exc

    def _derive_presence(
        self,
        context: AnalysisContext,
        identities: Mapping[str, Any],
        stem_relations: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[TenGodPresence]:
        day_master = self._day_master(context)
        stems = self._pillar_stems(context)
        identity_map = identities.get("identities") or {}
        stem_meta = stem_relations.get("stem_meta") or {}
        generates = stem_relations.get("generates") or {}
        controls = stem_relations.get("controls") or {}
        relation_to_god = stem_relations.get("relation_to_god") or {}

        if day_master not in stem_meta:
            raise TenGodsValidationError(
                f"Unknown day_master stem in knowledge: {day_master}",
                details={"day_master": day_master},
            )

        presence: list[TenGodPresence] = []
        for pillar, stem in stems:
            if pillar == "day":
                continue
            if stem not in stem_meta:
                raise TenGodsValidationError(
                    f"Unknown stem in knowledge: {stem}",
                    details={"pillar": pillar, "stem": stem},
                )
            god_id = self._resolve_god_id(
                day_master,
                stem,
                stem_meta=stem_meta,
                generates=generates,
                controls=controls,
                relation_to_god=relation_to_god,
            )
            meta = identity_map.get(god_id) or {}
            presence.append(
                TenGodPresence(
                    god_id=god_id,
                    label=str(meta.get("label") or god_id),
                    source_pillar=pillar,
                    source_stem=stem,
                    polarity_class=str(meta.get("polarity_class") or ""),
                )
            )
            evidence.append(
                RuleEvidence(
                    rule_id=f"presence:{pillar}:{god_id}",
                    version="1.0.0",
                    category="presence",
                    priority=50,
                    reference=ASSET_STEM_RELATIONS,
                    details={"pillar": pillar, "stem": stem, "god_id": god_id},
                )
            )

        presence.sort(key=lambda item: (item.source_pillar, item.god_id, item.source_stem))
        return presence

    def _resolve_god_id(
        self,
        day_master: str,
        other_stem: str,
        *,
        stem_meta: Mapping[str, Sequence[str]],
        generates: Mapping[str, str],
        controls: Mapping[str, str],
        relation_to_god: Mapping[str, Mapping[str, str]],
    ) -> str:
        dm_el, dm_pol = stem_meta[day_master]
        other_el, other_pol = stem_meta[other_stem]
        same_polarity = "same_polarity" if dm_pol == other_pol else "diff_polarity"

        if dm_el == other_el:
            relation = "same_element"
        elif generates.get(other_el) == dm_el:
            relation = "generated_by_other"
        elif generates.get(dm_el) == other_el:
            relation = "generates_other"
        elif controls.get(dm_el) == other_el:
            relation = "controls_other"
        elif controls.get(other_el) == dm_el:
            relation = "controlled_by_other"
        else:
            raise TenGodsExecutionError(
                "Unable to resolve Ten God relation",
                details={"day_master": day_master, "other_stem": other_stem},
            )

        mapping = relation_to_god.get(relation) or {}
        god_id = mapping.get(same_polarity)
        if not god_id:
            raise TenGodsExecutionError(
                "Missing relation_to_god mapping",
                details={"relation": relation, "polarity": same_polarity},
            )
        return str(god_id)

    def _evaluate_relationships(
        self,
        presence: Sequence[TenGodPresence],
        relationships: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[RelationshipOutcome]:
        present_ids = {item.god_id for item in presence}
        outcomes: list[RelationshipOutcome] = []
        for row in relationships.get("pairs") or []:
            left = str(row["left"])
            right = str(row["right"])
            if left in present_ids and right in present_ids:
                outcome = RelationshipOutcome(
                    left_god_id=left,
                    right_god_id=right,
                    relation=str(row["relation"]),
                    priority=int(row.get("priority", 0)),
                )
                outcomes.append(outcome)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"relationship:{left}:{right}",
                        version="1.0.0",
                        category="relationship",
                        priority=outcome.priority,
                        reference=ASSET_RELATIONSHIPS,
                    )
                )
        outcomes.sort(
            key=lambda item: (
                -item.priority,
                item.left_god_id,
                item.right_god_id,
                item.relation,
            )
        )
        return outcomes

    def _evaluate_interactions(
        self,
        presence: Sequence[TenGodPresence],
        upstream: Mapping[str, StageResult],
        strength_data: Mapping[str, Any],
        temperature_data: Mapping[str, Any],
        pattern_data: Mapping[str, Any],
        useful_god_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[InteractionOutcome]:
        present_ids = {item.god_id for item in presence}
        outcomes: list[InteractionOutcome] = []

        strength_class = str(
            (upstream["strength"].payload or {}).get("classification") or "balanced"
        )
        temperature_class = str(
            (upstream["temperature"].payload or {}).get("classification")
            or "balanced"
        )
        pattern_id = str(
            (upstream["pattern"].payload or {}).get("pattern_id") or "*"
        )
        useful_payload = upstream["useful_god"].payload or {}
        useful_gods = {
            str(item)
            for item in (
                useful_payload.get("useful_gods")
                or useful_payload.get("favorable")
                or []
            )
        }
        unfavorable_gods = {
            str(item) for item in (useful_payload.get("unfavorable") or [])
        }

        outcomes.extend(
            self._match_interaction_rows(
                dimension="strength",
                upstream_class=strength_class,
                rows=strength_data.get("rows") or [],
                present_ids=present_ids,
                class_key="strength_class",
                evidence=evidence,
                reference=ASSET_STRENGTH_INTERACTIONS,
            )
        )
        outcomes.extend(
            self._match_interaction_rows(
                dimension="temperature",
                upstream_class=temperature_class,
                rows=temperature_data.get("rows") or [],
                present_ids=present_ids,
                class_key="temperature_class",
                evidence=evidence,
                reference=ASSET_TEMPERATURE_INTERACTIONS,
            )
        )
        outcomes.extend(
            self._match_interaction_rows(
                dimension="pattern",
                upstream_class=pattern_id,
                rows=pattern_data.get("rows") or [],
                present_ids=present_ids,
                class_key="pattern_id",
                evidence=evidence,
                reference=ASSET_PATTERN_INTERACTIONS,
            )
        )

        for row in useful_god_data.get("rows") or []:
            role = str(row.get("role"))
            god_pattern = str(row.get("god_id") or "*")
            targets = useful_gods if role == "useful" else unfavorable_gods
            for god_id in sorted(targets):
                if god_id not in present_ids:
                    continue
                if god_pattern not in {"*", god_id}:
                    continue
                canonical = self._canonicalize_god_token(god_id, present_ids)
                if canonical is None:
                    continue
                outcome = InteractionOutcome(
                    dimension="useful_god",
                    upstream_class=role,
                    god_id=canonical,
                    effect=str(row.get("effect")),
                    priority=int(row.get("priority", 0)),
                )
                outcomes.append(outcome)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"interaction:useful_god:{role}:{canonical}",
                        version="1.0.0",
                        category="interaction",
                        priority=outcome.priority,
                        reference=ASSET_USEFUL_GOD_INTERACTIONS,
                    )
                )

        outcomes.sort(
            key=lambda item: (
                -item.priority,
                item.dimension,
                item.god_id,
                item.effect,
            )
        )
        return outcomes

    def _match_interaction_rows(
        self,
        *,
        dimension: str,
        upstream_class: str,
        rows: Sequence[Mapping[str, Any]],
        present_ids: set[str],
        class_key: str,
        evidence: list[RuleEvidence],
        reference: str,
    ) -> list[InteractionOutcome]:
        matched: list[InteractionOutcome] = []
        for row in rows:
            row_class = str(row.get(class_key) or "*")
            if row_class not in {upstream_class, "*"}:
                continue
            god_id = str(row.get("god_id") or "*")
            targets = sorted(present_ids) if god_id == "*" else [god_id]
            for target in targets:
                if target not in present_ids:
                    continue
                outcome = InteractionOutcome(
                    dimension=dimension,
                    upstream_class=upstream_class,
                    god_id=target,
                    effect=str(row.get("effect")),
                    priority=int(row.get("priority", 0)),
                )
                matched.append(outcome)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"interaction:{dimension}:{target}:{outcome.effect}",
                        version="1.0.0",
                        category="interaction",
                        priority=outcome.priority,
                        reference=reference,
                    )
                )
        return matched

    def _resolve_favorability(
        self,
        presence: Sequence[TenGodPresence],
        interactions: Sequence[InteractionOutcome],
        upstream: Mapping[str, StageResult],
        favorability_data: Mapping[str, Any],
        priority_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> tuple[list[FavorabilityOutcome], list[RejectedAlternative]]:
        base = favorability_data.get("base") or {}
        effect_map = favorability_data.get("effect_map") or {}
        priority_order = list(
            favorability_data.get("priority_order")
            or ["unfavorable", "favorable", "conditional", "neutral"]
        )
        god_priority = priority_data.get("god_priority") or {}

        present_ids = sorted(
            {item.god_id for item in presence},
            key=lambda god_id: (-int(god_priority.get(god_id, 0)), god_id),
        )

        # useful god labels may be display names; map via presence labels later if needed
        _ = upstream

        outcomes: list[FavorabilityOutcome] = []
        rejected: list[RejectedAlternative] = []

        for god_id in present_ids:
            candidates: list[tuple[int, str, str]] = []
            base_value = str(base.get(god_id) or "neutral")
            candidates.append((0, base_value, "base"))

            for interaction in interactions:
                if interaction.god_id != god_id:
                    continue
                mapped = effect_map.get(interaction.effect)
                if not mapped:
                    continue
                candidates.append(
                    (int(interaction.priority), str(mapped), interaction.effect)
                )

            selected, rejected_local = self._select_favorability(
                god_id=god_id,
                candidates=candidates,
                priority_order=priority_order,
            )
            outcomes.append(selected)
            rejected.extend(rejected_local)
            evidence.append(
                RuleEvidence(
                    rule_id=f"favorability:{god_id}:{selected.favorability}",
                    version="1.0.0",
                    category="favorability",
                    priority=int(god_priority.get(god_id, 0)),
                    reference=ASSET_FAVORABILITY,
                    details={"reason_codes": list(selected.reason_codes)},
                )
            )

        outcomes.sort(key=lambda item: item.god_id)
        rejected.sort(
            key=lambda item: (item.subject, item.rejected_value, item.selected_value)
        )
        return outcomes, rejected

    def _select_favorability(
        self,
        *,
        god_id: str,
        candidates: Sequence[tuple[int, str, str]],
        priority_order: Sequence[str],
    ) -> tuple[FavorabilityOutcome, list[RejectedAlternative]]:
        if not candidates:
            raise TenGodsConflictResolutionError(
                f"No favorability candidates for {god_id}",
                details={"god_id": god_id},
            )

        # Higher interaction priority first; ties broken by declared favorability order.
        ordered = sorted(
            candidates,
            key=lambda item: (
                -item[0],
                priority_order.index(item[1])
                if item[1] in priority_order
                else len(priority_order),
                item[2],
            ),
        )
        best_priority = ordered[0][0]
        top = [item for item in ordered if item[0] == best_priority]
        top.sort(
            key=lambda item: (
                priority_order.index(item[1])
                if item[1] in priority_order
                else len(priority_order),
                item[2],
            )
        )
        selected_value = top[0][1]
        reason_codes = tuple(sorted({item[2] for item in top if item[1] == selected_value}))
        selected = FavorabilityOutcome(
            god_id=god_id,
            favorability=selected_value,
            reason_codes=reason_codes,
        )
        rejected = [
            RejectedAlternative(
                subject=f"favorability:{god_id}",
                rejected_value=item[1],
                selected_value=selected_value,
                reason_code=item[2],
            )
            for item in ordered
            if item[1] != selected_value
        ]
        return selected, rejected

    def _evaluate_life_areas(
        self,
        presence: Sequence[TenGodPresence],
        life_areas_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[LifeAreaConcept]:
        present_ids = {item.god_id for item in presence}
        concepts: list[LifeAreaConcept] = []
        for row in life_areas_data.get("rows") or []:
            god_id = str(row["god_id"])
            if god_id not in present_ids:
                continue
            concept = LifeAreaConcept(
                area=str(row["area"]),
                god_id=god_id,
                concept_id=str(row["concept_id"]),
                tag=str(row["tag"]),
            )
            concepts.append(concept)
            evidence.append(
                RuleEvidence(
                    rule_id=f"life_area:{concept.area}:{god_id}",
                    version="1.0.0",
                    category="life_area",
                    priority=40,
                    reference=ASSET_LIFE_AREAS,
                )
            )
        concepts.sort(key=lambda item: (item.area, item.god_id, item.concept_id))
        return concepts

    def _aggregate_confidence(
        self,
        presence: Sequence[TenGodPresence],
        relationships: Sequence[RelationshipOutcome],
        interactions: Sequence[InteractionOutcome],
        favorability: Sequence[FavorabilityOutcome],
        life_areas: Sequence[LifeAreaConcept],
        confidence_data: Mapping[str, Any],
    ) -> ConfidenceEvaluation:
        weights = confidence_data.get("weights") or {}
        # Deterministic saturation: presence contributes fully when >=1, etc.
        components = {
            "presence": 1.0 if presence else 0.0,
            "relationship": 1.0 if relationships else 0.5,
            "interaction": min(1.0, len(interactions) / 3.0) if interactions else 0.0,
            "favorability": 1.0 if favorability else 0.0,
            "life_area": 1.0 if life_areas else 0.5,
        }
        score = 0.0
        for key, weight in weights.items():
            score += float(weight) * float(components.get(key, 0.0))
        score = round(min(1.0, max(0.0, score)), 4)

        level = "low"
        for row in confidence_data.get("levels") or []:
            if score >= float(row.get("min", 0.0)):
                level = str(row.get("level"))
                break

        return ConfidenceEvaluation(
            score=score,
            level=level,
            details={"components": components, "weights": dict(weights)},
        )

    @staticmethod
    def _day_master(context: AnalysisContext) -> str:
        chart = dict(context.chart)
        value = chart.get("day_master") or chart.get("day_stem")
        if value:
            return str(value)
        stems = chart.get("stems") or {}
        if isinstance(stems, dict) and stems.get("day"):
            return str(stems["day"])
        raise TenGodsValidationError("day_master missing from chart")

    @staticmethod
    def _pillar_stems(context: AnalysisContext) -> list[tuple[str, str]]:
        chart = dict(context.chart)
        stems = chart.get("stems")
        if isinstance(stems, dict) and stems:
            order = ("year", "month", "day", "hour")
            result = [
                (pillar, str(stems[pillar]))
                for pillar in order
                if pillar in stems and stems[pillar]
            ]
            if result:
                return result

        pillars = chart.get("pillars")
        if isinstance(pillars, dict) and pillars:
            order = ("year", "month", "day", "hour")
            result = []
            for pillar in order:
                node = pillars.get(pillar) or {}
                if isinstance(node, dict) and node.get("stem"):
                    result.append((pillar, str(node["stem"])))
            if result:
                return result

        day_master = str(chart.get("day_master") or "")
        if day_master:
            # Minimal chart: only day master known — no non-day presence.
            return [("day", day_master)]

        raise TenGodsValidationError(
            "chart stems/pillars are required for Ten Gods presence",
        )

    @staticmethod
    def _canonicalize_god_token(
        token: str,
        present_ids: set[str],
    ) -> str | None:
        if token in present_ids:
            return token
        normalized = token.strip().lower().replace(" ", "_")
        aliases = {
            "bi jian": "bi_jian",
            "jie cai": "jie_cai",
            "shi shen": "shi_shen",
            "shang guan": "shang_guan",
            "pian cai": "pian_cai",
            "zheng cai": "zheng_cai",
            "qi sha": "qi_sha",
            "zheng guan": "zheng_guan",
            "pian yin": "pian_yin",
            "zheng yin": "zheng_yin",
            "tỷ kiên": "bi_jian",
            "kiếp tài": "jie_cai",
            "thực thần": "shi_shen",
            "thương quan": "shang_guan",
            "thiên tài": "pian_cai",
            "chính tài": "zheng_cai",
            "thất sát": "qi_sha",
            "chính quan": "zheng_guan",
            "thiên ấn": "pian_yin",
            "chính ấn": "zheng_yin",
        }
        god_id = aliases.get(normalized, normalized)
        return god_id if god_id in present_ids else None
