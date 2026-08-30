/**
 * Reference appendix. Product chrome plus published versions. No internal ids.
 */

import type { ReactNode } from "react";
import {
  REPORT_APPENDIX_LABEL,
  REPORT_DISCLAIMER,
  REPORT_METHODOLOGY,
  REPORT_SECTION,
} from "../copy";
import type { ReportAppendixView } from "../reportModel";
import { ReportSectionHeader } from "./ReportPrimitives";

type ReportAppendixProps = {
  readonly model: ReportAppendixView;
};

/**
 * Level 4 reference. Omits unpublished metadata fields.
 */
export function ReportAppendix({ model }: ReportAppendixProps): ReactNode {
  return (
    <section
      className="bte-er__section bte-er__appendix"
      data-report-section="appendix"
      data-report-level="reference"
    >
      <ReportSectionHeader title={REPORT_SECTION.appendix} level="reference" />
      <div className="bte-er__appendix-block">
        <h3 className="bte-er__subhead">{REPORT_APPENDIX_LABEL.method}</h3>
        <p className="bte-er__caption">{REPORT_METHODOLOGY}</p>
      </div>
      <div className="bte-er__appendix-block">
        <h3 className="bte-er__subhead">{REPORT_APPENDIX_LABEL.disclaimer}</h3>
        <p className="bte-er__caption">{REPORT_DISCLAIMER}</p>
      </div>
      <dl className="bte-er__appendix-meta">
        {model.reportVersion ? (
          <div>
            <dt>{REPORT_APPENDIX_LABEL.reportVersion}</dt>
            <dd>{model.reportVersion}</dd>
          </div>
        ) : null}
        {model.presentationVersion ? (
          <div>
            <dt>{REPORT_APPENDIX_LABEL.presentationVersion}</dt>
            <dd data-presentation-version="true">{model.presentationVersion}</dd>
          </div>
        ) : null}
        {model.analysisDate ? (
          <div>
            <dt>{REPORT_APPENDIX_LABEL.analysisDate}</dt>
            <dd>{model.analysisDate}</dd>
          </div>
        ) : null}
      </dl>
    </section>
  );
}
