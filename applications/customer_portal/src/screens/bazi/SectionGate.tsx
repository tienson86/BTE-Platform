import type { ReactNode } from "react";
import { EmptyState } from "../../components/feedback/EmptyState";
import { ErrorState } from "../../components/feedback/ErrorState";
import { Skeleton } from "../../components/feedback/Skeleton";
import { Stack } from "../../components/layout/Stack";
import type { PresentationStatus } from "./mockData";

export type SectionGateProps = {
  status: PresentationStatus;
  loadingLabel: string;
  emptyTitle: string;
  emptyDescription?: string;
  errorTitle: string;
  errorDescription?: string;
  children: ReactNode;
};

/** Shared loading / empty / error gate for BaZi Result sections. */
export function SectionGate({
  status,
  loadingLabel,
  emptyTitle,
  emptyDescription,
  errorTitle,
  errorDescription,
  children,
}: SectionGateProps): ReactNode {
  if (status === "loading") {
    return (
      <div className="cui-bazi-skeleton" aria-busy="true" aria-label={loadingLabel}>
        <Stack gap="list">
          <Skeleton height="1.5rem" width="40%" />
          <Skeleton height="6rem" width="100%" />
          <Skeleton height="4rem" width="100%" />
        </Stack>
      </div>
    );
  }
  if (status === "empty") {
    return <EmptyState title={emptyTitle} description={emptyDescription} />;
  }
  if (status === "error") {
    return <ErrorState title={errorTitle} description={errorDescription} />;
  }
  return children;
}
