import type { ReactNode } from "react";

import { ErrorBoundary } from "../components/feedback";
import { ThemeProvider, type ThemePreference } from "../theme";

export type AppProvidersProps = {
  children: ReactNode;
  themePreference?: ThemePreference;
  themeRoot?: HTMLElement | null;
  errorFallback?: ReactNode;
};

/**
 * Application provider composition root.
 *
 * AppProviders → ThemeProvider → ErrorBoundary → Application
 *
 * Future providers plug in here. Do not add business providers yet.
 */
export function AppProviders({
  children,
  themePreference,
  themeRoot,
  errorFallback,
}: AppProvidersProps): ReactNode {
  return (
    <ThemeProvider initialPreference={themePreference} root={themeRoot}>
      <ErrorBoundary fallback={errorFallback}>{children}</ErrorBoundary>
    </ThemeProvider>
  );
}
