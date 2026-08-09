/**
 * Result Page V2 — PX-1 reading order + PX-2 UI Contract.
 */

import "../styles/result_v2.css";
import "../../../styles/themes/light.css";

import type { CanonicalReportInput } from "../adapter/reportInput";
import { ResultPage } from "../components/ResultPage";
import { useResultPage } from "../hooks/useResultPage";

export type ResultPageV2Props = {
  report?: CanonicalReportInput | null;
  loading?: boolean;
  offline?: boolean;
  printing?: boolean;
  exporting?: boolean;
  onRetry?: () => void;
  onPrimaryCta?: () => void;
  onSecondaryCta?: () => void;
};

export function ResultPageV2({
  report = null,
  loading = false,
  offline = false,
  printing = false,
  exporting = false,
  onRetry,
  onPrimaryCta,
  onSecondaryCta,
}: ResultPageV2Props) {
  const { model, pageState, expand, onNavigate } = useResultPage({
    report,
    loading,
    offline,
    printing,
    exporting,
  });

  return (
    <ResultPage
      model={model}
      pageState={pageState}
      isExpanded={expand.isExpanded}
      onToggle={expand.toggle}
      onNavigate={onNavigate}
      onRetry={onRetry}
      onPrimaryCta={onPrimaryCta}
      onSecondaryCta={onSecondaryCta}
    />
  );
}

export default ResultPageV2;
