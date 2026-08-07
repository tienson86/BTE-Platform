/**
 * Shared module header for Desktop V2 cards (S01–S11 visual language).
 * Inside white card · 24px card padding · #B91C1C · uppercase.
 */

import type { ReactNode } from "react";

type ModuleHeaderProps = {
  id: string;
  children: ReactNode;
};

/**
 * Identical section title used across canonical desktop modules.
 */
export function ModuleHeader({ id, children }: ModuleHeaderProps): ReactNode {
  return (
    <h2 id={id} className="cd-module-header">
      {children}
    </h2>
  );
}
