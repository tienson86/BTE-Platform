/**
 * Canonical Desktop data context — sections read ViewModel, never raw API/mock imports.
 */

import {
  createContext,
  useContext,
  type ReactNode,
} from "react";
import {
  createCanonicalDesktopMockViewModel,
  type CanonicalDesktopViewModel,
} from "../../adapters/canonicalDesktopAdapter";

const CanonicalDesktopContext = createContext<CanonicalDesktopViewModel | null>(null);

/**
 * Provide desktop ViewModel to shell + S00–S11.
 */
export function CanonicalDesktopProvider({
  value,
  children,
}: {
  value: CanonicalDesktopViewModel;
  children: ReactNode;
}): ReactNode {
  return (
    <CanonicalDesktopContext.Provider value={value}>
      {children}
    </CanonicalDesktopContext.Provider>
  );
}

/**
 * Active Canonical Desktop ViewModel (fixture fallback outside provider for tests).
 */
export function useCanonicalDesktop(): CanonicalDesktopViewModel {
  return useContext(CanonicalDesktopContext) ?? createCanonicalDesktopMockViewModel();
}
