/**
 * Print appendix plus archive signature. No Narrative composition.
 */

import type { ReactNode } from "react";
import { ReportAppendix } from "../components/ReportAppendix";
import { REPORT_APPENDIX_LABEL } from "../copy";
import type { ReportAppendixView } from "../reportModel";
import { PRINT_PREPARED_BY, PRINT_PREPARED_ORG } from "./copy";
import { PrintSection } from "./PrintSection";

type PrintAppendixProps = {
  readonly model: ReportAppendixView;
};

/**
 * Level 4 appendix on a new print section, with archive signature.
 */
export function PrintAppendix({ model }: PrintAppendixProps): ReactNode {
  return (
    <PrintSection breakBefore>
      <div data-print="appendix">
        <ReportAppendix model={model} />
        <footer className="bte-print__signature" data-print="signature">
          <p className="bte-print__signature-label">{PRINT_PREPARED_BY}</p>
          <p className="bte-print__signature-org">{PRINT_PREPARED_ORG}</p>
          {model.presentationVersion ? (
            <p className="bte-print__signature-meta">
              {REPORT_APPENDIX_LABEL.presentationVersion}: {model.presentationVersion}
            </p>
          ) : null}
          {model.analysisDate ? (
            <p className="bte-print__signature-meta">
              {REPORT_APPENDIX_LABEL.analysisDate}: {model.analysisDate}
            </p>
          ) : null}
        </footer>
      </div>
    </PrintSection>
  );
}
