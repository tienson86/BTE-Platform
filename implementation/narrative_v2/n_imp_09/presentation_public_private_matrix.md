# Presentation public / private matrix

Sprint: N-IMP-09
Contract: `knowledge/narrative_v2/04_PRESENTATION_CONTRACT.md`

Legend: Public = allowed on `NarrativeV2Presentation`. Serialized = included in customer JSON.

## Root

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| status | Presentation aggregation | yes | yes | yes | Canonical complete/partial/insufficient/invalid |
| overview | OverviewSummary | no (copy) | yes | yes | Frozen OverviewPresentation |
| interpretation | InterpretationNarrative | no (copy) | yes | yes | Frozen InterpretationPresentation strings |
| action_plan | ActionPlanNarrative | no (copy) | yes | yes | Frozen ActionPlanPresentation |
| commercial | Commercial Builder | n/a | optional | null | Builder not implemented |
| metadata | Presentation | yes | yes | yes | Public-safe four fields only |

## Overview

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| headline | OverviewSummary.headline | no | yes | yes | Copy only |
| summary | OverviewSummary.summary | no | yes | yes | Copy only |
| identity | OverviewSummary.identity | no | yes | null | Field allowed; upstream empty |
| balance | OverviewSummary.balance | no | yes | null | Field allowed; upstream empty |
| conclusion | OverviewSummary.conclusion | no | yes | null | Field allowed; upstream empty |
| references | OverviewSummary.references | yes | no | no | Spec §31: customer must not see references |
| metadata | OverviewSummary.metadata | yes | no | no | Runtime internals |

## Interpretation

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| overview | InterpretationNarrative.overview | no | yes | yes | Frozen contract |
| observation | InterpretationNarrative.observation | no | yes | yes | Frozen contract; string, not nested title object |
| reasoning | InterpretationNarrative.reasoning | no | yes | yes | Frozen contract |
| impact | InterpretationNarrative.impact | no | yes | yes | Frozen contract |
| recommendation | InterpretationNarrative.recommendation | no | yes | yes | Frozen contract |
| closing | InterpretationNarrative.closing | no | yes | yes | Frozen contract |
| meaning | InterpretationNarrative.meaning | yes | no | no | Not listed on InterpretationPresentation |
| flow | ConsultingNarrative.flow | yes | no | no | PRESENTATION CONTRACT GAP — CONSULTING FLOW |
| ConversationNarrative | N-IMP-07A | yes | no | no | Internal composer output |
| ConsultingNarrative | N-IMP-07B/07C | yes | no | no | Internal style output |
| references | InterpretationNarrative.references | yes | no | no | Internal provenance |

## Action Plan

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| top_priority.title | TopPriority.title | no | yes | yes | Frozen TopPriority |
| top_priority.description | TopPriority.description | no | yes | yes | Frozen TopPriority |
| top_priority.decision_id | TopPriority.decision_id | yes | no | no | Engine / decision id |
| actions[].title | ActionItem.title | no | yes | yes | Frozen ActionItem |
| actions[].description | ActionItem.description | no | yes | yes | Frozen ActionItem |
| actions[].category | ActionItem.category | no | yes | yes | Frozen ActionItem |
| actions[].action_id | ActionItem.action_id | yes | no | no | Internal id |
| actions[].decision_id | ActionItem.decision_id | yes | no | no | Internal id |
| actions[].priority | ActionItem.priority | yes | no | no | Not on public ActionItem |
| actions[].source_knowledge_ids | ActionItem.source_knowledge_ids | yes | no | no | Knowledge ids |
| warnings[].title | WarningItem.title | no | yes | yes | Frozen Warning |
| warnings[].description | WarningItem.description | no | yes | yes | Frozen Warning |
| warnings[].warning_id | WarningItem.warning_id | yes | no | no | Internal id |
| warnings[].severity | WarningItem.severity | yes | no | no | Not on public Warning |
| current_period | CurrentPeriod | no | yes | null | Allowed; upstream unpublished |
| current_period.source_knowledge_ids | CurrentPeriod | yes | no | no | Knowledge ids |
| ActionPlan.references | ActionPlanNarrative.references | yes | no | no | Internal provenance |

## Commercial

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| career/finance/relationship/health/leadership | Commercial Builder | n/a | optional | absent | `build_commercial` NotImplemented |

## Metadata

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| status | aggregation | yes | yes | yes | Mirrors root status |
| language | runtime locale | no | yes | yes | `vi` |
| version | contract | no | yes | yes | `bte.presentation.v2` |
| created_at | builder clock | no | yes | yes | Frozen injectable timestamp |
| narrative_version | runtime | yes | no | no | Not in frozen metadata contract |
| schema extras | — | — | no | no | Do not silently add fields |

## Never public

| Field | Source | Internal | Public | Serialized | Reason |
|---|---|---|---|---|---|
| CanonicalAnalysis | Orchestrator | yes | no | no | Consumer reads Presentation only |
| Evidence | Evidence Builder | yes | no | no | Internal |
| Reasoning | Reasoning Builder | yes | no | no | Internal |
| Knowledge | Knowledge Resolver | yes | no | no | Internal |
| Rewrite | Rewrite Engine | yes | no | no | Internal |
| pipeline_trace | Runtime | yes | no | no | Debug |
| runtime_metrics | Runtime | yes | no | no | Debug |
| events / errors stack | Runtime | yes | no | no | Debug |
| builder registry | Runtime | yes | no | no | Debug |
| rule ids / NR-REL-* | Knowledge/rules | yes | no | no | Customer safety |
| source_unit_ids | Rewrite | yes | no | no | Customer safety |
