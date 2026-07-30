"""Deterministic ShenSha calculator (knowledge-driven)."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
    StageResult,
)
from engines.analysis_engine.shensha_engine.exceptions import (
    ShenShaExecutionError,
    ShenShaValidationError,
)
from engines.analysis_engine.shensha_engine.knowledge_access import (
    ASSET_CALCULATION_REFERENCES,
    ASSET_COMPATIBILITY,
    ASSET_CONFIDENCE,
    ASSET_EXCEPTIONS,
    ASSET_IDENTITIES,
    ASSET_INTERACTIONS,
    ASSET_LOOKUP_TABLES,
    ASSET_MAPPING_TABLES,
    ASSET_PRIORITY,
    ASSET_UPSTREAM_QUALIFIERS,
    MODULE_ID,
    KnowledgeSession,
)
from engines.analysis_engine.shensha_engine.models import (
    CompatibilityOutcome,
    ExceptionOutcome,
    InteractionOutcome,
    RejectedAlternative,
    ShenShaPresence,
    ShenShaResult,
)

PILLAR_ORDER: tuple[str, ...] = ("year", "month", "day", "hour")


class ShenShaCalculator:
    """Execute ShenSha analytical steps using Knowledge SDK assets only."""

    def calculate(
        self,
        context: AnalysisContext,
        *,
        session: KnowledgeSession,
        upstream: Mapping[str, StageResult],
    ) -> ShenShaResult:
        """Run the full deterministic ShenSha algorithm."""
        try:
            module = session.get_module(MODULE_ID)
            calc_refs = session.get_asset(ASSET_CALCULATION_REFERENCES)
            lookups = session.get_asset(ASSET_LOOKUP_TABLES)
            mappings = session.get_asset(ASSET_MAPPING_TABLES)
            identities = session.get_asset(ASSET_IDENTITIES)
            interactions_asset = session.get_asset(ASSET_INTERACTIONS)
            compatibility_asset = session.get_asset(ASSET_COMPATIBILITY)
            exceptions_asset = session.get_asset(ASSET_EXCEPTIONS)
            qualifiers_asset = session.get_asset(ASSET_UPSTREAM_QUALIFIERS)
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

            anchors = self._resolve_anchors(context, calc_refs.data, evidence)
            branches = self._pillar_map(context, "branches", "branch")
            presence = self._detect_presence(
                anchors=anchors,
                branches=branches,
                lookup_data=lookups.data,
                mapping_data=mappings.data,
                identity_data=identities.data,
                priority_data=priority_asset.data,
                evidence=evidence,
            )

            qualifier_effects = self._upstream_qualifiers(
                upstream,
                qualifiers_asset.data,
                evidence,
            )
            exception_outcomes, rejected = self._apply_exceptions(
                presence,
                upstream,
                exceptions_asset.data,
                evidence,
            )
            presence = self._apply_exception_status(presence, exception_outcomes)
            presence = self._apply_qualifier_status(presence, qualifier_effects)

            interaction_outcomes = self._evaluate_interactions(
                presence,
                interactions_asset.data,
                evidence,
            )
            compatibility_outcomes = self._evaluate_compatibility(
                presence,
                compatibility_asset.data,
                evidence,
            )

            auspicious = tuple(
                item
                for item in presence
                if item.polarity == "auspicious" and item.status != "suppressed"
            )
            inauspicious = tuple(
                item
                for item in presence
                if item.polarity == "inauspicious" and item.status != "suppressed"
            )

            confidence = self._aggregate_confidence(
                presence,
                interaction_outcomes,
                compatibility_outcomes,
                exception_outcomes,
                qualifier_effects,
                confidence_asset.data,
            )

            diagnostics = (
                DiagnosticInfo(
                    code="shensha_completed",
                    message="ShenSha evaluation completed",
                    level="info",
                    stage_id="shensha",
                    details={"presence_count": len(presence)},
                ),
            )

            sorted_presence = tuple(self._sort_presence(presence))
            return ShenShaResult(
                auspicious=tuple(self._sort_presence(auspicious)),
                inauspicious=tuple(self._sort_presence(inauspicious)),
                presence=sorted_presence,
                interactions=tuple(
                    sorted(
                        interaction_outcomes,
                        key=lambda item: (
                            -item.priority,
                            item.left_id,
                            item.right_id,
                            item.relation,
                        ),
                    )
                ),
                compatibility=tuple(
                    sorted(
                        compatibility_outcomes,
                        key=lambda item: (item.shensha_id, item.compatibility),
                    )
                ),
                exceptions=tuple(
                    sorted(
                        exception_outcomes,
                        key=lambda item: (
                            -item.priority,
                            item.shensha_id,
                            item.action,
                        ),
                    )
                ),
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
                    "presence_count": len(sorted_presence),
                    "active_count": sum(
                        1 for item in sorted_presence if item.status == "active"
                    ),
                    "auspicious_count": len(auspicious),
                    "inauspicious_count": len(inauspicious),
                    "shensha_ids": sorted({item.shensha_id for item in sorted_presence}),
                },
            )
        except (ShenShaValidationError, ShenShaExecutionError):
            raise
        except Exception as exc:
            raise ShenShaExecutionError(
                f"ShenSha calculation failed: {exc}",
                details={"exception_type": type(exc).__name__},
            ) from exc

    def _resolve_anchors(
        self,
        context: AnalysisContext,
        calc_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> dict[str, str]:
        anchors: dict[str, str] = {}
        for row in calc_data.get("anchors") or []:
            anchor_id = str(row["anchor_id"])
            source = str(row["source"])
            value = self._resolve_source(context, source)
            if not value and row.get("fallback"):
                value = self._resolve_source(context, str(row["fallback"]))
            if not value:
                raise ShenShaValidationError(
                    f"Unable to resolve ShenSha anchor: {anchor_id}",
                    details={"source": source},
                )
            anchors[anchor_id] = value
            evidence.append(
                RuleEvidence(
                    rule_id=f"anchor:{anchor_id}:{value}",
                    version="1.0.0",
                    category="calculation_reference",
                    priority=50,
                    reference=ASSET_CALCULATION_REFERENCES,
                )
            )
        return anchors

    def _detect_presence(
        self,
        *,
        anchors: Mapping[str, str],
        branches: Mapping[str, str],
        lookup_data: Mapping[str, Any],
        mapping_data: Mapping[str, Any],
        identity_data: Mapping[str, Any],
        priority_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[ShenShaPresence]:
        mappings = mapping_data.get("mappings") or {}
        identities = identity_data.get("identities") or {}
        priorities = priority_data.get("shensha_priority") or {}
        presence: list[ShenShaPresence] = []
        seen: set[tuple[str, str, str]] = set()

        for table in lookup_data.get("tables") or []:
            table_id = str(table["table_id"])
            anchor_id = str(table["anchor_id"])
            match_mode = str(table.get("match_mode") or "branch_equals")
            lookup = table.get("lookup") or {}
            anchor_value = anchors.get(anchor_id)
            if not anchor_value or anchor_value not in lookup:
                continue

            expected = lookup[anchor_value]
            expected_values = (
                list(expected) if isinstance(expected, (list, tuple)) else [expected]
            )
            expected_values = [str(item) for item in expected_values]

            for pillar, branch in branches.items():
                matched = False
                if match_mode == "branch_in_list":
                    matched = branch in expected_values
                elif match_mode == "branch_equals":
                    matched = branch in expected_values
                if not matched:
                    continue

                mapping = mappings.get(table_id) or {}
                shensha_id = str(mapping.get("shensha_id") or table_id)
                polarity = str(
                    mapping.get("polarity")
                    or (identities.get(shensha_id) or {}).get("default_polarity")
                    or "conditional"
                )
                label = str((identities.get(shensha_id) or {}).get("label") or shensha_id)
                key = (shensha_id, pillar, branch)
                if key in seen:
                    continue
                seen.add(key)
                item = ShenShaPresence(
                    shensha_id=shensha_id,
                    label=label,
                    polarity=polarity,
                    anchor=anchor_id,
                    anchor_value=anchor_value,
                    location_pillar=pillar,
                    location_value=branch,
                    status="active",
                    priority=int(priorities.get(shensha_id, 0)),
                )
                presence.append(item)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"presence:{shensha_id}:{pillar}:{branch}",
                        version="1.0.0",
                        category="presence",
                        priority=item.priority,
                        reference=ASSET_LOOKUP_TABLES,
                        details={"table_id": table_id},
                    )
                )
        return presence

    def _evaluate_interactions(
        self,
        presence: Sequence[ShenShaPresence],
        interaction_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[InteractionOutcome]:
        active_ids = {
            item.shensha_id for item in presence if item.status != "suppressed"
        }
        outcomes: list[InteractionOutcome] = []
        for row in interaction_data.get("pairs") or []:
            left = str(row["left"])
            right = str(row["right"])
            if left in active_ids and right in active_ids:
                outcome = InteractionOutcome(
                    left_id=left,
                    right_id=right,
                    relation=str(row["relation"]),
                    effect=str(row["effect"]),
                    priority=int(row.get("priority", 0)),
                )
                outcomes.append(outcome)
                evidence.append(
                    RuleEvidence(
                        rule_id=f"interaction:{left}:{right}",
                        version="1.0.0",
                        category="interaction",
                        priority=outcome.priority,
                        reference=ASSET_INTERACTIONS,
                    )
                )
        return outcomes

    def _evaluate_compatibility(
        self,
        presence: Sequence[ShenShaPresence],
        compatibility_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> list[CompatibilityOutcome]:
        present_ids = {item.shensha_id for item in presence}
        outcomes: list[CompatibilityOutcome] = []
        for row in compatibility_data.get("rows") or []:
            shensha_id = str(row["shensha_id"])
            if shensha_id not in present_ids:
                continue
            outcome = CompatibilityOutcome(
                shensha_id=shensha_id,
                compatibility=str(row["compatibility"]),
                reason_codes=("default_mapping",),
            )
            outcomes.append(outcome)
            evidence.append(
                RuleEvidence(
                    rule_id=f"compatibility:{shensha_id}:{outcome.compatibility}",
                    version="1.0.0",
                    category="compatibility",
                    priority=40,
                    reference=ASSET_COMPATIBILITY,
                )
            )
        return outcomes

    def _apply_exceptions(
        self,
        presence: Sequence[ShenShaPresence],
        upstream: Mapping[str, StageResult],
        exception_data: Mapping[str, Any],
        evidence: list[RuleEvidence],
    ) -> tuple[list[ExceptionOutcome], list[RejectedAlternative]]:
        strength_class = str(
            (upstream["strength"].payload or {}).get("classification") or ""
        )
        combination_payload = upstream["combination"].payload or {}
        has_clash = bool(combination_payload.get("clashes"))

        present_ids = {item.shensha_id for item in presence}
        outcomes: list[ExceptionOutcome] = []
        rejected: list[RejectedAlternative] = []

        for row in exception_data.get("rules") or []:
            shensha_id = str(row["shensha_id"])
            if shensha_id not in present_ids:
                continue
            matched = False
            if row.get("when_strength") and str(row["when_strength"]) == strength_class:
                matched = True
            if row.get("when_combination_has_clash") and has_clash:
                matched = True
            if not matched:
                continue

            action = str(row["action"])
            reason = str(row["reason_code"])
            priority = int(row.get("priority", 0))
            outcomes.append(
                ExceptionOutcome(
                    shensha_id=shensha_id,
                    action=action,
                    reason_code=reason,
                    priority=priority,
                )
            )
            evidence.append(
                RuleEvidence(
                    rule_id=f"exception:{shensha_id}:{action}",
                    version="1.0.0",
                    category="exception",
                    priority=priority,
                    reference=ASSET_EXCEPTIONS,
                    details={"reason_code": reason},
                )
            )
            if action == "suppress":
                rejected.append(
                    RejectedAlternative(
                        subject=f"presence:{shensha_id}",
                        rejected_value="active",
                        selected_value="suppressed",
                        reason_code=reason,
                    )
                )
        return outcomes, rejected

    def _apply_exception_status(
        self,
        presence: Sequence[ShenShaPresence],
        exceptions: Sequence[ExceptionOutcome],
    ) -> list[ShenShaPresence]:
        actions = {
            item.shensha_id: item.action
            for item in sorted(exceptions, key=lambda row: row.priority)
        }
        updated: list[ShenShaPresence] = []
        for item in presence:
            action = actions.get(item.shensha_id)
            status = item.status
            if action == "suppress":
                status = "suppressed"
            elif action == "qualify":
                status = "qualified"
            updated.append(
                ShenShaPresence(
                    shensha_id=item.shensha_id,
                    label=item.label,
                    polarity=item.polarity,
                    anchor=item.anchor,
                    anchor_value=item.anchor_value,
                    location_pillar=item.location_pillar,
                    location_value=item.location_value,
                    status=status,
                    priority=item.priority,
                )
            )
        return updated

    def _apply_qualifier_status(
        self,
        presence: Sequence[ShenShaPresence],
        qualifier_effects: Sequence[str],
    ) -> list[ShenShaPresence]:
        if "amplify_auspicious" not in qualifier_effects:
            return list(presence)
        updated: list[ShenShaPresence] = []
        for item in presence:
            priority = item.priority
            if item.polarity == "auspicious" and item.status == "active":
                priority = item.priority + 5
            updated.append(
                ShenShaPresence(
                    shensha_id=item.shensha_id,
                    label=item.label,
                    polarity=item.polarity,
                    anchor=item.anchor,
                    anchor_value=item.anchor_value,
                    location_pillar=item.location_pillar,
                    location_value=item.location_value,
                    status=item.status,
                    priority=priority,
                )
            )
        return updated

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
        has_clash = bool((upstream["combination"].payload or {}).get("clashes"))

        for row in qualifier_data.get("rows") or []:
            dimension = str(row.get("dimension"))
            if dimension == "strength" and str(row.get("classification")) == strength_class:
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
            elif dimension == "combination" and bool(row.get("has_clash")) == has_clash:
                effects.append(str(row.get("effect")))
                evidence.append(
                    RuleEvidence(
                        rule_id="qualifier:combination:clash",
                        version="1.0.0",
                        category="upstream_qualifier",
                        priority=int(row.get("priority", 0)),
                        reference=ASSET_UPSTREAM_QUALIFIERS,
                    )
                )
        return sorted(set(effects))

    def _aggregate_confidence(
        self,
        presence: Sequence[ShenShaPresence],
        interactions: Sequence[InteractionOutcome],
        compatibility: Sequence[CompatibilityOutcome],
        exceptions: Sequence[ExceptionOutcome],
        qualifier_effects: Sequence[str],
        confidence_data: Mapping[str, Any],
    ) -> ConfidenceEvaluation:
        weights = confidence_data.get("weights") or {}
        components = {
            "presence": 1.0 if presence else 0.0,
            "interaction": 1.0 if interactions else 0.5,
            "compatibility": 1.0 if compatibility else 0.5,
            "exception": 1.0 if exceptions else 0.5,
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

    def _resolve_source(self, context: AnalysisContext, source: str) -> str | None:
        chart = dict(context.chart)
        if source == "day_master" and chart.get("day_master"):
            return str(chart["day_master"])
        if "." in source:
            bucket_name, key = source.split(".", 1)
            bucket = chart.get(bucket_name)
            if isinstance(bucket, dict) and bucket.get(key):
                return str(bucket[key])
            pillars = chart.get("pillars")
            field = "stem" if bucket_name == "stems" else "branch"
            if isinstance(pillars, dict):
                node = pillars.get(key) or {}
                if isinstance(node, dict) and node.get(field):
                    return str(node[field])
        if source in chart and chart[source]:
            return str(chart[source])
        return None

    def _pillar_map(
        self,
        context: AnalysisContext,
        key: str,
        pillar_field: str,
    ) -> dict[str, str]:
        chart = dict(context.chart)
        result: dict[str, str] = {}
        direct = chart.get(key)
        if isinstance(direct, dict):
            for pillar in PILLAR_ORDER:
                if pillar in direct and direct[pillar]:
                    result[pillar] = str(direct[pillar])
            return result
        pillars = chart.get("pillars")
        if isinstance(pillars, dict):
            for pillar in PILLAR_ORDER:
                node = pillars.get(pillar) or {}
                if isinstance(node, dict) and node.get(pillar_field):
                    result[pillar] = str(node[pillar_field])
        return result

    @staticmethod
    def _sort_presence(items: Sequence[ShenShaPresence]) -> list[ShenShaPresence]:
        return sorted(
            items,
            key=lambda item: (
                -item.priority,
                item.shensha_id,
                item.location_pillar,
                item.location_value,
            ),
        )
