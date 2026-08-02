import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  UnavailableState,
} from "../shared";
import type { PresentationStatus } from "../../view_models/executive_summary";

export type PresentationGateLabels = {
  loadingTitle?: string;
  emptyTitle?: string;
  unavailableTitle?: string;
  errorTitle?: string;
  errorDescription?: string;
};

/**
 * Renders Shared presentation states for Business Components.
 * Not a Pack 06 inventory component — internal composition helper only.
 */
export function renderPresentationGate(
  status: PresentationStatus | undefined,
  labels: PresentationGateLabels,
  ready: ReactNode,
): ReactNode {
  const resolved = status ?? "ready";

  if (resolved === "loading") {
    return <LoadingState title={labels.loadingTitle ?? "Loading"} />;
  }
  if (resolved === "empty") {
    return <EmptyState title={labels.emptyTitle ?? "No data available"} />;
  }
  if (resolved === "unavailable") {
    return (
      <UnavailableState title={labels.unavailableTitle ?? "Content unavailable"} />
    );
  }
  if (resolved === "error") {
    return (
      <ErrorState
        title={labels.errorTitle ?? "Unable to load content"}
        description={labels.errorDescription}
      />
    );
  }

  return ready;
}
