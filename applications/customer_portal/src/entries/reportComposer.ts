/**
 * Reports/export entry — exposes the canonical FullReportViewModel composer.
 */

import {
  buildFullReportViewModel,
  renderFullReportHtml,
  type BuildFullReportOptions,
} from "../report/fullReportViewModel";
import type { AnalysisDataDto } from "../models";
import {
  CUSTOMER_USEFUL_GOD_CONTRACT,
  customerContractMessage,
  customerContractStatus,
} from "../resultState/customerContract";

declare global {
  interface Window {
    BteFullReport?: {
      build: typeof buildFullReportViewModel;
      render: typeof renderFullReportHtml;
      contractStatus: typeof customerContractStatus;
      contractMessage: typeof customerContractMessage;
      customerContract: string;
    };
  }
}

window.BteFullReport = {
  build: (data: AnalysisDataDto, options?: BuildFullReportOptions) =>
    buildFullReportViewModel(data, options),
  render: renderFullReportHtml,
  contractStatus: customerContractStatus,
  contractMessage: customerContractMessage,
  customerContract: CUSTOMER_USEFUL_GOD_CONTRACT,
};
