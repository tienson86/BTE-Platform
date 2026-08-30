/**
 * Choose which stored Presentation the Portal renders.
 * ResultStore keeps Pack05 and Narrative V2 independently.
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
import { adaptActionPlanCard } from "../screens/commercial_dashboard/actionPlanAdapter";
import { adaptInterpretationCard } from "../screens/commercial_dashboard/interpretationAdapter";
import { adaptOverviewCard } from "../screens/commercial_dashboard/overviewAdapter";
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

export type SelectedNarrative = "pack05" | "v2";

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
 * Select Overview / Interpretation / Action Plan for the production dashboard.
 */
export function selectNarrativePresentation(
  analysis: AnalysisDataDto | null | undefined,
  requested: NarrativeProvider = resolveNarrativeProvider(),
): NarrativePresentationSelection {
  const started =
    typeof performance !== "undefined" && typeof performance.now === "function"
      ? performance.now()
      : Date.now();
  const v2View = requested === "pack05" ? null : readV2View(analysis);
  const pack05 = {
    overview: adaptOverviewCard(analysis),
    interpretation: adaptInterpretationCard(analysis),
    actionPlan: adaptActionPlanCard(analysis),
  };

  let selection: Omit<NarrativePresentationSelection, "durationMs">;
  if (requested === "pack05") {
    selection = pack05Selection(requested, pack05, null);
  } else if (v2View && v2Usable(v2View)) {
    selection = {
      requested,
      selected: "v2",
      fallback: false,
      fallbackReason: null,
      presentationVersion: v2View.version,
      overview: adaptOverviewFromPresentation(v2View),
      interpretation: adaptInterpretationFromPresentation(v2View),
      actionPlan: adaptActionPlanFromPresentation(v2View),
    };
  } else {
    const reason = v2View?.error ?? "presentation_unavailable";
    selection = pack05Selection(requested, pack05, reason);
  }

  const ended =
    typeof performance !== "undefined" && typeof performance.now === "function"
      ? performance.now()
      : Date.now();
  const durationMs = Math.max(0, Math.round(ended - started));
  recordNarrativeSelection({
    provider: selection.requested,
    selected: selection.selected,
    presentationVersion: selection.presentationVersion,
    fallback: selection.fallback,
    fallbackReason: selection.fallbackReason,
    durationMs,
  });
  return { ...selection, durationMs };
}

function pack05Selection(
  requested: NarrativeProvider,
  pack05: {
    readonly overview: OverviewView;
    readonly interpretation: InterpretationView;
    readonly actionPlan: ActionPlanView;
  },
  fallbackReason: string | null,
): Omit<NarrativePresentationSelection, "durationMs"> {
  return {
    requested,
    selected: "pack05",
    fallback: fallbackReason != null,
    fallbackReason,
    presentationVersion: null,
    overview: pack05.overview,
    interpretation: pack05.interpretation,
    actionPlan: pack05.actionPlan,
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
