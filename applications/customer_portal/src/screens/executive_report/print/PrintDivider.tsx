/**
 * Print section divider. Editorial rule, not a dashboard border.
 */

import type { ReactNode } from "react";

/**
 * Controlled print divider.
 */
export function PrintDivider(): ReactNode {
  return <hr className="bte-er__divider bte-print__divider" data-print="divider" />;
}
