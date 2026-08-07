/**
 * Result Page ViewModel context — Sprint A zones consume this only.
 */

import { createContext, useContext, type ReactNode } from "react";
import type { ResultPageViewModel } from "./viewModels";

const ResultPageContext = createContext<ResultPageViewModel | null>(null);

/**
 * Provides Sprint A Result Page ViewModels to zones/cards.
 */
export function ResultPageProvider({
  value,
  children,
}: {
  value: ResultPageViewModel;
  children: ReactNode;
}): ReactNode {
  return (
    <ResultPageContext.Provider value={value}>{children}</ResultPageContext.Provider>
  );
}

/**
 * Read Result Page ViewModel — throws if used outside provider.
 */
export function useResultPageViewModel(): ResultPageViewModel {
  const value = useContext(ResultPageContext);
  if (!value) {
    throw new Error("useResultPageViewModel requires ResultPageProvider");
  }
  return value;
}
