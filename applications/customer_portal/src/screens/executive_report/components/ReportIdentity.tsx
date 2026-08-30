/**
 * Compact client profile. Published identity fields only.
 */

import type { ReactNode } from "react";
import { REPORT_SECTION } from "../copy";
import type { ReportIdentityRow } from "../reportModel";
import { ReportSectionHeader } from "./ReportPrimitives";

type ReportIdentityProps = {
  readonly rows: readonly ReportIdentityRow[];
};

/**
 * Identity section. Omits the block when no published fields exist.
 */
export function ReportIdentity({ rows }: ReportIdentityProps): ReactNode {
  if (!rows.length) return null;
  return (
    <section
      className="bte-er__section bte-er__identity"
      data-report-section="identity"
      data-report-level="primary"
    >
      <ReportSectionHeader title={REPORT_SECTION.identity} level="primary" />
      <dl className="bte-er__identity-grid">
        {rows.map((row) => (
          <div key={row.label} className="bte-er__identity-row">
            <dt>{row.label}</dt>
            <dd>{row.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
