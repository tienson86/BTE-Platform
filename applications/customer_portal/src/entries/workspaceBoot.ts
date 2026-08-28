/**
 * Workspace boot — ResultStore current result → BaziWorkspaceViewModel.
 * Same current-result resolver as /result. Does not rerun Analyze.
 */

import { adaptBaziWorkspace } from "../features/result_workspace/adapter";
import type { BaziWorkspaceViewModel } from "../features/result_workspace/adapter/types";
import {
  historyIdFromSearch,
  resolveCurrentStoredResult,
  type StoredResultRecord,
} from "../resultState/currentResult";

export type StoredResult = StoredResultRecord;

export type WorkspaceBootProps = {
  readonly preview: boolean;
  readonly noResult: boolean;
  readonly viewModel: BaziWorkspaceViewModel | null;
  readonly analysisId: string;
  readonly source: "current" | "history" | "empty" | "preview";
};

/**
 * Resolve workspace props from ResultStore + URL.
 * `?preview=1` is the only path that uses the isolated fixture.
 */
export function resolveWorkspaceBoot(
  stored: StoredResult | null,
  search: string = "",
  historyView: StoredResult | null = null,
): WorkspaceBootProps {
  const params = new URLSearchParams(search.startsWith("?") ? search.slice(1) : search);
  if (params.get("preview") === "1") {
    return {
      preview: true,
      noResult: false,
      viewModel: null,
      analysisId: "",
      source: "preview",
    };
  }

  const historyId = historyIdFromSearch(search);
  const resolved = resolveCurrentStoredResult({
    current: stored,
    historyView,
    fromHistory: Boolean(historyId),
    historyId,
  });

  if (!resolved?.data) {
    return {
      preview: false,
      noResult: true,
      viewModel: null,
      analysisId: "",
      source: "empty",
    };
  }

  const viewModel = adaptBaziWorkspace(resolved.data, {
    analysisId: resolved.analysisId,
    input: resolved.input,
  });
  return {
    preview: false,
    noResult: false,
    viewModel,
    analysisId: resolved.analysisId,
    source: resolved.source === "history" ? "history" : "current",
  };
}
