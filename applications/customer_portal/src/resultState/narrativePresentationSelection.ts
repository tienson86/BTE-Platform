/**
 * Production Portal always renders Narrative V2.
 * Pack05 remains in ResultStore as a read-only archive.
 */

import {
  adaptActionPlanFromPresentation,
  adaptInterpretationFromPresentation,
  adaptOverviewFromPresentation,
} from "../adapters/narrativeV2DashboardAdapter";
import {
  adaptNarrativeV2Presentation,
  type NarrativeV2PresentationView,
} from "../adapters/narrativeV2PresentationAdapter";
import type { AnalysisDataDto } from "../models";
import {
  adaptOverviewCard,
  adaptOverviewExecutiveFacts,
  adaptOverviewFocus,
} from "../screens/commercial_dashboard/overviewAdapter";
import {
  ACTION_PLAN_EMPTY,
  ACTION_PLAN_TITLE,
  INTERPRETATION_EMPTY,
  INTERPRETATION_TITLE,
  INTERPRETATION_ZONE_LABELS,
} from "../screens/commercial_dashboard/cards";
import type {
  ActionPlanView,
  InterpretationView,
  OverviewView,
} from "../screens/commercial_dashboard/types";
import {
  NARRATIVE_PROVIDER_DEFAULT,
  resolveNarrativeProvider,
  type NarrativeProvider,
} from "./narrativeProvider";
import { recordNarrativeSelection } from "./narrativeReleaseMonitor";

export type SelectedNarrative = "v2";

export type NarrativePresentationSelection = {
  readonly requested: NarrativeProvider;
  readonly selected: SelectedNarrative;
  readonly fallback: boolean;
  readonly fallbackReason: string | null;
  readonly presentationVersion: string | null;
  readonly durationMs: number;
  readonly overview: OverviewView;
  readonly interpretation: InterpretationView;
  readonly actionPlan: ActionPlanView;
};

/**
 * Select production Narrative cards. Pack05 is never chosen.
 */
export function selectNarrativePresentation(
  analysis: AnalysisDataDto | null | undefined,
  requested: string = resolveNarrativeProvider(),
): NarrativePresentationSelection {
  void requested;
  const started =
    typeof performance !== "undefined" && typeof performance.now === "function"
      ? performance.now()
      : Date.now();
  const provider: NarrativeProvider = "v2";
  const v2View = readV2View(analysis);
  const usable = v2View != null && v2Usable(v2View);
  const overview =
    v2View != null && usable && hasOverview(v2View)
      ? attachExecutiveFacts(adaptOverviewFromPresentation(v2View), analysis)
      : adaptOverviewCard(analysis);
  const interpretation =
    v2View != null && usable
      ? adaptInterpretationFromPresentation(v2View)
      : emptyInterpretation();
  const actionPlan =
    v2View != null && usable ? adaptActionPlanFromPresentation(v2View) : emptyActionPlan();
  const ended =
    typeof performance !== "undefined" && typeof performance.now === "function"
      ? performance.now()
      : Date.now();
  const durationMs = Math.max(0, Math.round(ended - started));
  const selection: NarrativePresentationSelection = {
    requested: provider,
    selected: "v2",
    fallback: false,
    fallbackReason: usable ? null : v2View?.error ?? "presentation_unavailable",
    presentationVersion: usable && v2View != null ? v2View.version : null,
    durationMs,
    overview,
    interpretation,
    actionPlan,
  };
  recordNarrativeSelection({
    provider: selection.requested,
    selected: "v2",
    presentationVersion: selection.presentationVersion,
    fallback: false,
    fallbackReason: selection.fallbackReason,
    durationMs,
  });
  return selection;
}

function attachExecutiveFacts(
  overview: OverviewView,
  analysis: AnalysisDataDto | null | undefined,
): OverviewView {
  const facts = adaptOverviewExecutiveFacts(analysis);
  const focus = adaptOverviewFocus(analysis);
  return {
    ...overview,
    identity: facts.identity,
    balance: facts.balance,
    focusTitle: focus.title,
    focus: focus.items,
  };
}

function hasOverview(view: NarrativeV2PresentationView): boolean {
  return Boolean(view.overview?.headline || view.overview?.summary || view.overview?.conclusion);
}

function emptyInterpretation(): InterpretationView {
  return {
    title: INTERPRETATION_TITLE,
    available: false,
    lead: "",
    leadExtra: "",
    leadSource: "",
    zones: (["observation", "reasoning", "impact", "recommendation"] as const).map((id) => ({
      id,
      label: INTERPRETATION_ZONE_LABELS[id],
      body: "",
      extra: "",
      source: "",
    })),
    closing: "",
    closingSource: "",
    emptyMessage: INTERPRETATION_EMPTY,
  };
}

function emptyActionPlan(): ActionPlanView {
  return {
    title: ACTION_PLAN_TITLE,
    available: false,
    emptyMessage: ACTION_PLAN_EMPTY,
    priority: null,
    actions: [],
    extraActions: [],
    warnings: [],
    watch: [],
  };
}

function readV2View(
  analysis: AnalysisDataDto | null | undefined,
): NarrativeV2PresentationView | null {
  if (!analysis || analysis.narrative_v2_shadow == null) {
    return null;
  }
  return adaptNarrativeV2Presentation(analysis.narrative_v2_shadow);
}

function v2Usable(view: NarrativeV2PresentationView): boolean {
  if (!view.ok) return false;
  return Boolean(
    view.overview?.headline ||
      view.overview?.summary ||
      view.overview?.conclusion ||
      view.interpretation?.consulting_flow ||
      view.interpretation?.overview ||
      view.interpretation?.observation ||
      view.action_plan?.top_priority ||
      (view.action_plan?.actions.length ?? 0) > 0,
  );
}

export { NARRATIVE_PROVIDER_DEFAULT };
