/**
 * Shared editorial chrome for the executive report. Layout only.
 */

import type { ReactNode } from "react";

type ReportSectionHeaderProps = {
  readonly eyebrow?: string;
  readonly title: string;
  readonly level?: "executive" | "primary" | "detailed" | "reference";
};

/**
 * Section title with optional editorial eyebrow.
 */
export function ReportSectionHeader({
  eyebrow,
  title,
  level,
}: ReportSectionHeaderProps): ReactNode {
  return (
    <header className="bte-er__section-head">
      {eyebrow ? <p className="bte-er__eyebrow">{eyebrow}</p> : null}
      <h2 className="bte-er__section-title" data-report-level={level}>
        {title}
      </h2>
    </header>
  );
}

type ReportCalloutProps = {
  readonly label?: string;
  readonly children: ReactNode;
  readonly tone?: "priority" | "insight" | "note";
};

/**
 * Controlled editorial callout. Does not invent copy.
 */
export function ReportCallout({ label, children, tone = "note" }: ReportCalloutProps): ReactNode {
  return (
    <aside className={`bte-er__callout bte-er__callout--${tone}`}>
      {label ? <p className="bte-er__callout-label">{label}</p> : null}
      <div className="bte-er__callout-body">{children}</div>
    </aside>
  );
}

type ReportMetricProps = {
  readonly label: string;
  readonly value: string;
};

/**
 * Compact labeled metric. Omits empty values at the call site.
 */
export function ReportMetric({ label, value }: ReportMetricProps): ReactNode {
  return (
    <div className="bte-er__metric">
      <dt className="bte-er__metric-label">{label}</dt>
      <dd className="bte-er__metric-value">{value}</dd>
    </div>
  );
}

/**
 * Controlled vertical divider between editorial blocks.
 */
export function ReportDivider(): ReactNode {
  return <hr className="bte-er__divider" />;
}
