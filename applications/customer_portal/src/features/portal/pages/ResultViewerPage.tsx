import { ResultPageV2 } from "../../result_v2/pages/ResultPageV2";
import { portalDemoReport } from "../fixtures/demoReport";

export default function ResultViewerPage() {
  return (
    <div className="pv-result-viewer">
      <ResultPageV2 report={portalDemoReport} />
    </div>
  );
}
