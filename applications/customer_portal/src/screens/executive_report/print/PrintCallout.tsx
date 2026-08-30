/**
 * Print callout. Executive Summary insight and Top Priority only.
 */

import type { ReactNode } from "react";

type PrintCalloutProps = {
  readonly label?: string;
  readonly children: ReactNode;
  readonly tone: "insight" | "priority";
};

/**
 * Restrained print callout. Does not invent copy.
 */
export function PrintCallout({ label, children, tone }: PrintCalloutProps): ReactNode {
  return (
    <aside
      className={`bte-er__callout bte-print__callout bte-print__callout--${tone}`}
      data-print="callout"
      data-print-callout={tone}
    >
      {label ? <p className="bte-er__callout-label">{label}</p> : null}
      <div className="bte-print__callout-body">{children}</div>
    </aside>
  );
}
