import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  UnavailableState,
} from "../shared";
import type { PresentationStatus } from "../../view_models/executive_summary";

type GateLabels = {
  loadingTitle?: string;
  emptyTitle?: string;
  unavailableTitle?: string;
  errorTitle?: string;
  errorDescription?: string;
};

/** Presentation-state gate for navigation components — Shared states only. */
export function renderNavigationGate(
  status: PresentationStatus | undefined,
  labels: GateLabels,
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
