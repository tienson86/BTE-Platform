import { CommercialRail, type ReportMode } from "../components/CommercialRail";
import { ResultPageV2 } from "../../result_v2/pages/ResultPageV2";
import { portalDemoReport } from "../fixtures/demoReport";

export type ResultViewerPageProps = {
  mode?: ReportMode;
  saved?: boolean;
  onSave?: () => void;
  onPdf?: () => void;
  onPrint?: () => void;
  onShare?: () => void;
  onKnowledge?: () => void;
  onPremium?: () => void;
};

export default function ResultViewerPage({
  mode = "reading",
  saved = false,
  onSave,
  onPdf,
  onPrint,
  onShare,
  onKnowledge,
  onPremium,
}: ResultViewerPageProps) {
  return (
    <div className="pv-result-viewer" data-report-mode={mode}>
      <ResultPageV2 report={portalDemoReport} />
      <CommercialRail
        saved={saved}
        onSave={() => onSave?.()}
        onPdf={() => onPdf?.()}
        onPrint={() => onPrint?.()}
        onShare={() => onShare?.()}
        onKnowledge={() => onKnowledge?.()}
        onPremium={() => onPremium?.()}
      />
    </div>
  );
}
