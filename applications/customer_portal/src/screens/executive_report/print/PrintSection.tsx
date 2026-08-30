/**
 * Print section wrapper. Page-break chrome only. Does not compose content.
 */

import type { ReactNode } from "react";

type PrintSectionProps = {
  readonly children: ReactNode;
  readonly breakBefore?: boolean;
  readonly keepTogether?: boolean;
};

/**
 * Apply print page-break policy around an existing report section.
 */
export function PrintSection({
  children,
  breakBefore = false,
  keepTogether = false,
}: PrintSectionProps): ReactNode {
  const mods = [
    "bte-print__section",
    breakBefore ? "bte-print__section--break-before" : "",
    keepTogether ? "bte-print__section--keep" : "",
  ]
    .filter(Boolean)
    .join(" ");
  return (
    <div
      className={mods}
      data-print-section="true"
      data-print-break-before={breakBefore ? "true" : undefined}
      data-print-keep={keepTogether ? "true" : undefined}
    >
      {children}
    </div>
  );
}
