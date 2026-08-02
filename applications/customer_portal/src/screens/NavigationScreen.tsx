import type { ReactNode } from "react";
import {
  EmptyState,
  ErrorState,
  LoadingState,
  SectionContainer,
  UnavailableState,
} from "../components/shared";
import type { NavigationViewModel } from "../view_models/navigation";
import { cx } from "../utils";
import { ReadingNavigation } from "../components/navigation";

export type NavigationScreenProps = {
  data: NavigationViewModel;
  children?: ReactNode;
  className?: string;
};

/**
 * Navigation Screen — Pack 06 WP-0011.
 * Wraps frozen report content with reading navigation chrome.
 * Does not modify frozen screens.
 */
export function NavigationScreen({
  data,
  children,
  className,
}: NavigationScreenProps) {
  if (data.status !== "ready") {
    return (
      <SectionContainer
        className={cx("cui-nav-navigation-screen", className)}
        aria-label="Reading Navigation"
      >
        {data.status === "loading" ? (
          <LoadingState title="Loading navigation" />
        ) : null}
        {data.status === "empty" ? (
          <EmptyState title="No navigation available" />
        ) : null}
        {data.status === "unavailable" ? (
          <UnavailableState title="Navigation unavailable" />
        ) : null}
        {data.status === "error" ? (
          <ErrorState
            title="Unable to load navigation"
            description={data.errorMessage}
          />
        ) : null}
      </SectionContainer>
    );
  }

  return (
    <NavigationScreenReady className={className} data={data}>
      {children}
    </NavigationScreenReady>
  );
}

function NavigationScreenReady({
  data,
  children,
  className,
}: {
  data: Extract<NavigationViewModel, { status: "ready" }>;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <ReadingNavigation data={data} className={cx("cui-nav-navigation-screen", className)}>
      {children}
    </ReadingNavigation>
  );
}
