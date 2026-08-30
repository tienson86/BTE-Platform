/**
 * Executive summary from NarrativeV2Presentation.overview. Copy only.
 */

import type { ReactNode } from "react";
import type { NarrativeV2OverviewView } from "../../../adapters/narrativeV2PresentationAdapter";
import { REPORT_SECTION } from "../copy";
import { ReportSectionHeader } from "./ReportPrimitives";

type ExecutiveSummarySectionProps = {
  readonly overview: NarrativeV2OverviewView | null;
};

/**
 * Level A summary. Renders published overview fields only.
 */
export function ExecutiveSummarySection({ overview }: ExecutiveSummarySectionProps): ReactNode {
  if (!overview) return null;
  const { headline, summary, identity, balance, conclusion } = overview;
  if (!headline && !summary && !identity && !balance && !conclusion) return null;
  return (
    <section
      className="bte-er__section bte-er__summary"
      data-report-section="executive-summary"
      data-report-level="executive"
    >
      <ReportSectionHeader title={REPORT_SECTION.summary} level="executive" />
      {headline ? (
        <p className="bte-er__insight" data-report-overview="headline">
          {headline}
        </p>
      ) : null}
      {summary ? (
        <p className="bte-er__lead" data-report-overview="summary">
          {summary}
        </p>
      ) : null}
      {identity ? (
        <p className="bte-er__body" data-report-overview="identity">
          {identity}
        </p>
      ) : null}
      {balance ? (
        <p className="bte-er__body" data-report-overview="balance">
          {balance}
        </p>
      ) : null}
      {conclusion ? (
        <p className="bte-er__conclusion" data-report-overview="conclusion">
          {conclusion}
        </p>
      ) : null}
    </section>
  );
}
