/**
 * Report cover. Brand, analysis title, published identity, date, version.
 */

import type { ReactNode } from "react";
import type { ReportCoverView } from "../reportModel";

type ReportCoverProps = {
  readonly model: ReportCoverView;
};

/**
 * First-page cover. Omits unpublished fields. No scores or engine metadata.
 */
export function ReportCover({ model }: ReportCoverProps): ReactNode {
  return (
    <section
      className="bte-er__cover"
      data-report-section="cover"
      data-report-level="executive"
    >
      <div className="bte-er__cover-motif" aria-hidden="true" />
      <p className="bte-er__cover-brand">{model.productTitle}</p>
      <h1 className="bte-er__cover-title">{model.analysisTitle}</h1>
      {model.customerName ? (
        <p className="bte-er__cover-name" data-report-cover="name">
          {model.customerName}
        </p>
      ) : null}
      {model.birthLine ? (
        <p className="bte-er__cover-birth" data-report-cover="birth">
          {model.birthLine}
        </p>
      ) : null}
      <dl className="bte-er__cover-meta">
        {model.analysisDate ? (
          <div>
            <dt>Ngày phân tích</dt>
            <dd data-report-cover="date">{model.analysisDate}</dd>
          </div>
        ) : null}
        {model.reportVersion ? (
          <div>
            <dt>Phiên bản</dt>
            <dd data-report-cover="version">{model.reportVersion}</dd>
          </div>
        ) : null}
      </dl>
    </section>
  );
}
