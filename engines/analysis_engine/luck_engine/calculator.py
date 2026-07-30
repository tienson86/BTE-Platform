"""Deterministic Luck calculator (knowledge-driven)."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.analysis_engine.luck_engine.exceptions import (
    LuckExecutionError,
    LuckValidationError,
)
from engines.analysis_engine.luck_engine.knowledge_access import (
    ASSET_ACTIVATION,
    ASSET_CONFIDENCE,
    ASSET_DA_YUN,
    ASSET_FAVORABILITY,
    ASSET_INTERACTION,
    ASSET_LIU_NIAN,
    ASSET_LIU_RI,
    ASSET_LIU_SHI,
    ASSET_LIU_YUE,
    ASSET_PRIORITY,
    ASSET_TIMING,
    LAYER_ORDER,
    MODULE_ID,
    KnowledgeSession,
)
from engines.analysis_engine.luck_engine.models import (
    LuckInteractionOutcome,
    LuckLayerOutcome,
    LuckPillar,
    LuckResult,
    RejectedAlternative,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)

LAYER_ASSETS: dict[str, str] = {
    "da_yun": ASSET_DA_YUN,
    "liu_nian": ASSET_LIU_NIAN,
    "liu_yue": ASSET_LIU_YUE,
    "liu_ri": ASSET_LIU_RI,
    "liu_shi": ASSET_LIU_SHI,
}


class LuckCalculator:
    """Execute Luck analytical steps using Knowledge SDK assets only."""

    def calculate(
        self,
        context: AnalysisContext,
        *,
        session: KnowledgeSession,
        upstream: Mapping[str, StageResult],
    ) -> LuckResult:
        """Run the full deterministic Luck algorithm."""
        try:
            module = session.get_module(MODULE_ID)
            layer_assets = {
                layer: session.get_asset(asset_id)
                for layer, asset_id in LAYER_ASSETS.items()
            }
            interaction_asset = session.get_asset(ASSET_INTERACTION)
            timing_asset = session.get_asset(ASSET_TIMING)
            activation_asset = session.get_asset(ASSET_ACTIVATION)
            favorability_asset = session.get_asset(ASSET_FAVORABILITY)
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

            luck = self._luck_block(context)
            day_master = self._day_master(context)

            interactions = self._evaluate_interactions(
                upstream,
                interaction_asset.data,
                evidence,
            )
            interaction_effects = [item.effect for item in interactions]

            da_yun = self._evaluate_da_yun(
                luck=luck,
                layer_data=layer_assets["da_yun"].data,
                timing_data=timing_asset.data,
                activation_data=activation_asset.data,
                favorability_data=favorability_asset.data,
                priority_data=priority_asset.data,
                day_master=day_master,
                upstream=upstream,
                interaction_effects=interaction_effects,
                evidence=evidence,
            )
            active_da_yun = [item for item in da_yun if item.status == "active"]

            liu_nian = self._evaluate_flow_layer(
                layer="liu_nian",
                raw=luck.get("liu_nian") or {},
                parent_active=bool(active_da_yun),
                parent_layer="da_yun",
                layer_data=layer_assets["liu_nian"].data,
                timing_data=timing_asset.data,
                activation_data=activation_asset.data,
                favorability_data=favorability_asset.data,
                priority_data=priority_asset.data,
                day_master=day_master,
                upstream=upstream,
                interaction_effects=interaction_effects,
                evidence=evidence,
            )
            liu_yue = self._evaluate_flow_layer(
                layer="liu_yue",
                raw=luck.get("liu_yue") or {},
                parent_active=any(item.status == "active" for item in liu_nian),
                parent_layer="liu_nian",
                layer_data=layer_assets["liu_yue"].data,
                timing_data=timing_asset.data,
                activation_data=activation_asset.data,
                favorability_data=favorability_asset.data,
                priority_data=priority_asset.data,
                day_master=day_master,
                upstream=upstream,
                interaction_effects=interaction_effects,
                evidence=evidence,
            )
            liu_ri = self._evaluate_flow_layer(
                layer="liu_ri",
                raw=luck.get("liu_ri") or {},
                parent_active=any(item.status == "active" for item in liu_yue),
                parent_layer="liu_yue",
                layer_data=layer_assets["liu_ri"].data,
                timing_data=timing_asset.data,
                activation_data=activation_asset.data,
                favorability_data=favorability_asset.data,
                priority_data=priority_asset.data,
                day_master=day_master,
                upstream=upstream,
                interaction_effects=interaction_effects,
                evidence=evidence,
            )
            liu_shi = self._evaluate_flow_layer(
                layer="liu_shi",
                raw=luck.get("liu_shi") or {},
                parent_active=any(item.status == "active" for item in liu_ri),
                parent_layer="liu_ri",
                layer_data=layer_assets["liu_shi"].data,
                timing_data=timing_asset.data,
                activation_data=activation_asset.data,
                favorability_data=favorability_asset.data,
                priority_data=priority_asset.data,
                day_master=day_master,
                upstream=upstream,
                interaction_effects=interaction_effects,
                evidence=evidence,
            )

            all_layers = da_yun + liu_nian + liu_yue + liu_ri + liu_shi
            active_layers, rejected = self._resolve_priority(
                all_layers,
                priority_asset.data,
                evidence,
            )
            confidence = self._aggregate_confidence(
                all_layers,
                active_layers,
                interactions,
                confidence_asset.data,
            )

            diagnostics = (
                DiagnosticInfo(
                    code="luck_completed",
                    message="Luck evaluation completed",
                    level="info",
                    stage_id="luck",
                    details={
                        "layer_count": len(all_layers),
                        "active_count": len(active_layers),
                    },
                ),
            )

            return LuckResult(
                da_yun=tuple(self._sort_layers(da_yun)),
                liu_nian=tuple(self._sort_layers(liu_nian)),
                liu_yue=tuple(self._sort_layers(liu_yue)),
                liu_ri=tuple(self._sort_layers(liu_ri)),
                liu_shi=tuple(self._sort_layers(liu_shi)),
                interactions=tuple(
                    sorted(
                        interactions,
                        key=lambda item: (
                            -item.priority,
                            item.dimension,
                            item.effect,
                        ),
                    )
                ),
                active_layers=tuple(self._sort_layers(active_layers)),
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
                    "layer_count": len(all_layers),
                    "active_count": len(active_layers),
                    "active_layer_names": sorted(
                        {item.layer for item in active_layers}
                    ),
                    "current_da_yun_index": next(
                        (
                            item.pillar.index
                            for item in da_yun
                            if item.status == "active"
                        ),
                        None,
                    ),
                },
            )
        except (LuckValidationError, LuckExecutionError):
            raise
        except Exception as exc:
            raise LuckExecutionError(
                f"Luck calculation failed: {exc}",
                details={"exception_type": type(exc).__name__},
            ) from exc

    def _evaluate_da_yun(
        self,
        *,
        luck: Mapping[str, Any],
        layer_data: Mapping[str, Any],
        timing_data: Mapping[str, Any],
        activation_data: Mapping[str, Any],
        favorability_data: Mapping[str, Any],
        priority_data: Mapping[str, Any],
        day_master: str,
        upstream: Mapping[str, StageResult],
        interaction_effects: Sequence[str],
        evidence: list[RuleEvidence],
    ) -> list[LuckLayerOutcome]:
        sequence = list(luck.get("da_yun_sequence") or [])
        if not sequence:
            raise LuckValidationError("da_yun_sequence is empty")
        current_age = luck.get("current_age")
        outcomes: list[LuckLayerOutcome] = []
        layer_priority = int(
            (priority_data.get("layer_priority") or {}).get("da_yun", 100)
        )

        for raw in sequence:
            pillar = LuckPillar(
                stem=str(raw["stem"]),
                branch=str(raw["branch"]),
                index=int(raw.get("index", 0)),
                label=str(raw.get("label") or f"da_yun_{raw.get('index', 0)}"),
            )
            start_age = raw.get("start_age")
            end_age = raw.get("end_age")
            in_range = (
                current_age is not None
                and start_age is not None
                and end_age is not None
                and int(start_age) <= int(current_age) <= int(end_age)
            )
            activation = "active" if in_range else "inactive"
            if self._activation_requires_age(activation_data, "da_yun") and not in_range:
                status = "inactive"
            else:
                status = "active" if in_range else "inactive"

            timing_phase = self._timing_phase(
                current_age=current_age,
                start_age=start_age,
                end_age=end_age,
                timing_data=timing_data,
            )
            favorability, reasons = self._favorability_for_pillar(
                pillar,
                day_master=day_master,
                favorability_data=favorability_data,
                upstream=upstream,
                interaction_effects=interaction_effects,
            )
            outcome = LuckLayerOutcome(
                layer="da_yun",
                pillar=pillar,
                status=status,
                favorability=favorability,
                activation=activation,
                timing_phase=timing_phase,
                priority=layer_priority,
                parent_layer=None,
                reason_codes=tuple(reasons),
                details={
                    "start_age": start_age,
                    "end_age": end_age,
                    "current_age": current_age,
                },
            )
            outcomes.append(outcome)
            evidence.append(
                RuleEvidence(
                    rule_id=f"da_yun:{pillar.index}:{status}:{favorability}",
                    version="1.0.0",
                    category="da_yun",
                    priority=layer_priority,
                    reference=ASSET_DA_YUN,
                )
            )
        return outcomes

    def _evaluate_flow_layer(
        self,
        *,
        layer: str,
        raw: Mapping[str, Any],
        parent_active: bool,
        parent_layer: str,
        layer_data: Mapping[str, Any],
        timing_data: Mapping[str, Any],
        activation_data: Mapping[str, Any],
        favorability_data: Mapping[str, Any],
        priority_data: Mapping[str, Any],
        day_master: str,
        upstream: Mapping[str, StageResult],
        interaction_effects: Sequence[str],
        evidence: list[RuleEvidence],
    ) -> list[LuckLayerOutcome]:
        pillar = LuckPillar(
            stem=str(raw["stem"]),
            branch=str(raw["branch"]),
            index=int(raw.get("index", 0)),
            label=str(raw.get("label") or layer),
        )
        require_parent = bool(layer_data.get("requires_parent_active", True))
        activation_ok = parent_active or not require_parent
        if self._activation_requires_parent(activation_data, layer) and not parent_active:
            activation_ok = False

        status = "active" if activation_ok else "blocked"
        activation = "active" if activation_ok else "inactive"
        timing_phase = str(timing_data.get("default_phase") or "peak")
        favorability, reasons = self._favorability_for_pillar(
            pillar,
            day_master=day_master,
            favorability_data=favorability_data,
            upstream=upstream,
            interaction_effects=interaction_effects,
        )
        if status == "blocked":
            reasons = tuple(sorted(set(reasons) | {"parent_inactive"}))

        priority = int((priority_data.get("layer_priority") or {}).get(layer, 0))
        outcome = LuckLayerOutcome(
            layer=layer,
            pillar=pillar,
            status=status,
            favorability=favorability,
            activation=activation,
            timing_phase=timing_phase,
            priority=priority,
            parent_layer=parent_layer,
            reason_codes=reasons,
            details=dict(raw),
        )
        evidence.append(
            RuleEvidence(
                rule_id=f"{layer}:{status}:{favorability}",
                version="1.0.0",
                category=layer,
                priority=priority,
                reference=LAYER_ASSETS[layer],
            )
        )
        return [outcome]

    def _evaluate_interactions(
        self,
        upstream: Mapping[str, StageResult],
        interaction_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[LuckInteractionOutcome]:
        strength_class = str(
            (upstream["strength"].payload or {}).get("classification") or ""
        )
        useful = set(
            str(item)
            for item in (
                (upstream["useful_god"].payload or {}).get("useful_gods")
                or (upstream["useful_god"].payload or {}).get("favorable")
                or []
            )
        )
        has_clash = bool((upstream["combination"].payload or {}).get("clashes"))
        inauspicious = bool((upstream["shensha"].payload or {}).get("inauspicious"))

        outcomes: list[LuckInteractionOutcome] = []
        for row in interaction_data.get("rows") or []:
            dimension = str(row.get("dimension"))
            matched = False
            upstream_class = ""
            if dimension == "strength" and str(row.get("classification")) == strength_class:
                matched = True
                upstream_class = strength_class
            elif dimension == "useful_god" and bool(row.get("overlap")) and useful:
                matched = True
                upstream_class = "useful_overlap"
            elif dimension == "combination" and bool(row.get("has_clash")) == has_clash:
                matched = True
                upstream_class = "clash" if has_clash else "no_clash"
            elif (
                dimension == "shensha"
                and bool(row.get("has_inauspicious")) == inauspicious
            ):
                matched = True
                upstream_class = "inauspicious" if inauspicious else "clear"

            if not matched:
                continue
            outcome = LuckInteractionOutcome(
                layer="all",
                dimension=dimension,
                upstream_class=upstream_class,
                effect=str(row.get("effect")),
                priority=int(row.get("priority", 0)),
            )
            outcomes.append(outcome)
            evidence.append(
                RuleEvidence(
                    rule_id=f"interaction:{dimension}:{outcome.effect}",
                    version="1.0.0",
                    category="interaction",
                    priority=outcome.priority,
                    reference=ASSET_INTERACTION,
                )
            )
        return outcomes

    def _favorability_for_pillar(
        self,
        pillar: LuckPillar,
        *,
        day_master: str,
        favorability_data: Mapping[str, Any],
        upstream: Mapping[str, StageResult],
        interaction_effects: Sequence[str],
    ) -> tuple[str, list[str]]:
        stem_element_map = favorability_data.get("stem_element") or {}
        branch_element_map = favorability_data.get("branch_element") or {}
        generates = favorability_data.get("generates") or {}
        controls = favorability_data.get("controls") or {}
        base_map = favorability_data.get("base_by_element_vs_day_master") or {}
        effect_map = favorability_data.get("effect_map") or {}
        priority_order = list(
            favorability_data.get("priority_order")
            or ["unfavorable", "favorable", "conditional", "neutral"]
        )

        dm_el = stem_element_map.get(day_master)
        luck_el = stem_element_map.get(pillar.stem) or branch_element_map.get(
            pillar.branch
        )
        relation = "same"
        if dm_el and luck_el:
            if dm_el == luck_el:
                relation = "same"
            elif generates.get(luck_el) == dm_el:
                relation = "generates_dm"
            elif generates.get(dm_el) == luck_el:
                relation = "generated_by_dm"
            elif controls.get(luck_el) == dm_el:
                relation = "controls_dm"
            elif controls.get(dm_el) == luck_el:
                relation = "controlled_by_dm"

        candidates: list[tuple[int, str, str]] = [
            (10, str(base_map.get(relation, "neutral")), f"relation:{relation}")
        ]

        useful = {
            str(item)
            for item in (
                (upstream["useful_god"].payload or {}).get("useful_gods")
                or (upstream["useful_god"].payload or {}).get("favorable")
                or []
            )
        }
        # If useful god payload contains matching stem/branch/element tokens, boost.
        if pillar.stem in useful or pillar.branch in useful or luck_el in useful:
            candidates.append((80, "favorable", "useful_god_overlap"))

        for effect in interaction_effects:
            mapped = effect_map.get(effect)
            if mapped:
                candidates.append((40, str(mapped), effect))

        selected = sorted(
            candidates,
            key=lambda item: (
                -item[0],
                priority_order.index(item[1])
                if item[1] in priority_order
                else len(priority_order),
                item[2],
            ),
        )[0]
        reasons = sorted({item[2] for item in candidates if item[1] == selected[1]})
        return selected[1], reasons

    def _timing_phase(
        self,
        *,
        current_age: Any,
        start_age: Any,
        end_age: Any,
        timing_data: Mapping[str, Any],
    ) -> str:
        if current_age is None or start_age is None or end_age is None:
            return str(timing_data.get("default_phase") or "peak")
        start = int(start_age)
        end = int(end_age)
        age = int(current_age)
        if end <= start:
            return str(timing_data.get("default_phase") or "peak")
        ratio = (age - start) / float(end - start)
        for phase, bounds in (timing_data.get("phases") or {}).items():
            if float(bounds.get("min_ratio", 0.0)) <= ratio < float(
                bounds.get("max_ratio", 1.0)
            ):
                return str(phase)
        return str(timing_data.get("default_phase") or "peak")

    def _resolve_priority(
        self,
        layers: Sequence[LuckLayerOutcome],
        priority_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> tuple[list[LuckLayerOutcome], list[RejectedAlternative]]:
        active = [item for item in layers if item.status == "active"]
        rejected: list[RejectedAlternative] = []
        for item in layers:
            if item.status != "active":
                rejected.append(
                    RejectedAlternative(
                        subject=f"{item.layer}:{item.pillar.label}",
                        rejected_value="active",
                        selected_value=item.status,
                        reason_code=item.reason_codes[0]
                        if item.reason_codes
                        else item.status,
                    )
                )
        evidence.append(
            RuleEvidence(
                rule_id=f"priority:active:{len(active)}",
                version="1.0.0",
                category="priority",
                priority=100,
                reference=ASSET_PRIORITY,
            )
        )
        return active, rejected

    def _aggregate_confidence(
        self,
        layers: Sequence[LuckLayerOutcome],
        active: Sequence[LuckLayerOutcome],
        interactions: Sequence[LuckInteractionOutcome],
        confidence_data: Mapping[str, Any],
    ) -> ConfidenceEvaluation:
        weights = confidence_data.get("weights") or {}
        components = {
            "layers": 1.0 if layers else 0.0,
            "activation": (len(active) / max(1, len(LAYER_ORDER))),
            "interaction": 1.0 if interactions else 0.5,
            "favorability": 1.0
            if any(item.favorability for item in layers)
            else 0.0,
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
    def _activation_requires_age(
        activation_data: Mapping[str, Any],
        layer: str,
    ) -> bool:
        for row in activation_data.get("rules") or []:
            if str(row.get("layer")) == layer and row.get(
                "require_current_age_in_range"
            ):
                return True
        return False

    @staticmethod
    def _activation_requires_parent(
        activation_data: Mapping[str, Any],
        layer: str,
    ) -> bool:
        for row in activation_data.get("rules") or []:
            if str(row.get("layer")) == layer and row.get("require_parent_active"):
                return True
        return False

    @staticmethod
    def _luck_block(context: AnalysisContext) -> dict[str, Any]:
        chart = dict(context.chart)
        luck = chart.get("luck")
        if isinstance(luck, dict):
            return dict(luck)
        meta = dict(context.metadata)
        luck_meta = meta.get("luck")
        if isinstance(luck_meta, dict):
            return dict(luck_meta)
        raise LuckValidationError("chart.luck is required")

    @staticmethod
    def _day_master(context: AnalysisContext) -> str:
        chart = dict(context.chart)
        if chart.get("day_master"):
            return str(chart["day_master"])
        stems = chart.get("stems") or {}
        if isinstance(stems, dict) and stems.get("day"):
            return str(stems["day"])
        raise LuckValidationError("day_master is required")

    @staticmethod
    def _sort_layers(items: Sequence[LuckLayerOutcome]) -> list[LuckLayerOutcome]:
        return sorted(
            items,
            key=lambda item: (
                -item.priority,
                item.layer,
                item.pillar.index,
                item.pillar.stem,
                item.pillar.branch,
            ),
        )
