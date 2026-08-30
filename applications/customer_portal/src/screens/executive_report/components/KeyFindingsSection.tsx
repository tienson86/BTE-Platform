/**
 * Compact key findings from already-published Presentation and canonical facts.
 */

import type { ReactNode } from "react";
import { REPORT_SECTION } from "../copy";
import type { ReportFinding } from "../reportModel";
import { ReportSectionHeader } from "./ReportPrimitives";

type KeyFindingsSectionProps = {
  readonly findings: readonly ReportFinding[];
};

/**
 * 3–5 finding cards. No new prose. Top Priority may appear as a highlight.
 */
export function KeyFindingsSection({ findings }: KeyFindingsSectionProps): ReactNode {
  if (!findings.length) return null;
  return (
    <section
      className="bte-er__section bte-er__findings"
      data-report-section="key-findings"
      data-report-level="primary"
    >
      <ReportSectionHeader title={REPORT_SECTION.findings} level="primary" />
      <ul className="bte-er__finding-list">
        {findings.map((finding) => (
          <li
            key={finding.id}
            className="bte-er__finding"
            data-finding={finding.id}
            data-report-level={finding.id === "priority" ? "executive" : "primary"}
          >
            <p className="bte-er__finding-label">{finding.label}</p>
            <p className="bte-er__finding-value">{finding.value}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
