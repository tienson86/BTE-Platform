/**
 * Reports/export entry — exposes the canonical FullReportViewModel composer.
 */

import {
  buildFullReportViewModel,
  renderFullReportHtml,
  type BuildFullReportOptions,
} from "../report/fullReportViewModel";
import type { AnalysisDataDto } from "../models";

declare global {
  interface Window {
    BteFullReport?: {
      build: typeof buildFullReportViewModel;
      render: typeof renderFullReportHtml;
    };
  }
}

window.BteFullReport = {
  build: (data: AnalysisDataDto, options?: BuildFullReportOptions) =>
    buildFullReportViewModel(data, options),
  render: renderFullReportHtml,
};
