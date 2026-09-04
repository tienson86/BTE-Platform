/**
 * Copy NarrativeV2Presentation into existing dashboard card views.
 * Does not compose, rewrite, join, or interpret Narrative.
 */

import type { NarrativeV2PresentationView } from "./narrativeV2PresentationAdapter";
import {
  ACTION_PLAN_EMPTY,
  ACTION_PLAN_TITLE,
  INTERPRETATION_EMPTY,
  INTERPRETATION_TITLE,
  INTERPRETATION_ZONE_LABELS,
  OVERVIEW_SUBTITLE,
  OVERVIEW_TITLE,
} from "../screens/commercial_dashboard/cards";
import type {
  ActionItemView,
  ActionPlanView,
  InterpretationView,
  InterpretationZoneId,
  InterpretationZoneView,
  OverviewView,
} from "../screens/commercial_dashboard/types";

const LEAK =
  /\{|\}|Traceback|stack trace|rule_id|source_unit|pipeline_trace|engine_id|schema_version/i;

/**
 * Copy Presentation overview fields into the Overview card slots.
 */
export function adaptOverviewFromPresentation(
  view: NarrativeV2PresentationView,
): OverviewView {
  const overview = view.overview;
  const headline = customerCopy(overview?.headline ?? null);
  const summary = customerCopy(overview?.summary ?? null);
  const conclusion = customerCopy(overview?.conclusion ?? null);
  return {
    title: OVERVIEW_TITLE,
    subtitle: OVERVIEW_SUBTITLE,
    insight: headline,
    insightSource: headline ? "narrative_v2.overview.headline" : "",
    summary,
    summarySource: summary ? "narrative_v2.overview.summary" : "",
    conclusion,
    conclusionSource: conclusion ? "narrative_v2.overview.conclusion" : "",
    identity: [],
    balance: [],
  };
}

/**
 * Copy Presentation interpretation fields independently. Does not join zones.
 */
export function adaptInterpretationFromPresentation(
  view: NarrativeV2PresentationView,
): InterpretationView {
  const interpretation = view.interpretation;
  const lead =
    customerCopy(interpretation?.consulting_flow ?? null) ||
    customerCopy(interpretation?.overview ?? null);
  const zones: InterpretationZoneView[] = (
    ["observation", "reasoning", "impact", "recommendation"] as const
  ).map((id) => copyZone(id, interpretation?.[id] ?? null));
  const closing = customerCopy(interpretation?.closing ?? null);
  return {
    title: INTERPRETATION_TITLE,
    available: Boolean(lead || closing || zones.some((zone) => zone.body)),
    lead,
    leadExtra: "",
    leadSource: lead
      ? interpretation?.consulting_flow
        ? "narrative_v2.interpretation.consulting_flow"
        : "narrative_v2.interpretation.overview"
      : "",
    zones,
    closing,
    closingSource: closing ? "narrative_v2.interpretation.closing" : "",
    emptyMessage: INTERPRETATION_EMPTY,
  };
}

/**
 * Copy Presentation action_plan fields into the Action Plan card.
 */
export function adaptActionPlanFromPresentation(
  view: NarrativeV2PresentationView,
): ActionPlanView {
  const plan = view.action_plan;
  const priority = copyItem(
    plan?.top_priority?.title ?? null,
    plan?.top_priority?.description ?? null,
    "",
    "narrative_v2.action_plan.top_priority",
  );
  const actions = (plan?.actions ?? [])
    .map((item) =>
      copyItem(item.title, item.description, item.category, "narrative_v2.action_plan.actions"),
    )
    .filter((item): item is ActionItemView => item != null);
  const warnings = (plan?.warnings ?? [])
    .map((item) =>
      copyItem(item.title, item.description, "", "narrative_v2.action_plan.warnings"),
    )
    .filter((item): item is ActionItemView => item != null);
  const watch = plan?.current_period
    ? copyItem(
        plan.current_period.title,
        plan.current_period.description,
        "",
        "narrative_v2.action_plan.current_period",
      )
    : null;
  const available = Boolean(priority || actions.length || warnings.length || watch);
  return {
    title: ACTION_PLAN_TITLE,
    available,
    emptyMessage: ACTION_PLAN_EMPTY,
    priority,
    actions,
    extraActions: [],
    warnings,
    watch: watch ? [watch] : [],
  };
}

function copyZone(id: InterpretationZoneId, value: string | null): InterpretationZoneView {
  const body = customerCopy(value);
  return {
    id,
    label: INTERPRETATION_ZONE_LABELS[id],
    body,
    extra: "",
    source: body ? `narrative_v2.interpretation.${id}` : "",
  };
}

function copyItem(
  title: string | null,
  detail: string | null,
  domain: string,
  source: string,
): ActionItemView | null {
  const nextTitle = customerCopy(title);
  const nextDetail = customerCopy(detail);
  if (!nextTitle && !nextDetail) return null;
  return {
    title: nextTitle || nextDetail,
    detail: nextTitle ? nextDetail : "",
    domain: customerCopy(domain),
    source,
  };
}

function customerCopy(value: string | null | undefined): string {
  if (typeof value !== "string") return "";
  const text = value.trim();
  if (!text || LEAK.test(text)) return "";
  return value;
}
