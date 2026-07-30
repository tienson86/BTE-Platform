import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type {
  AnalysisData,
  ChartData,
  InterpretationData,
  ReportData,
} from "../api/types";

type SessionState = {
  chart: ChartData | null;
  analysis: AnalysisData | null;
  interpretation: InterpretationData | null;
  report: ReportData | null;
  setChart: (value: ChartData | null) => void;
  setAnalysis: (value: AnalysisData | null) => void;
  setInterpretation: (value: InterpretationData | null) => void;
  setReport: (value: ReportData | null) => void;
  resetDownstreamFromChart: () => void;
};

const SessionContext = createContext<SessionState | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const [chart, setChart] = useState<ChartData | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [interpretation, setInterpretation] = useState<InterpretationData | null>(
    null,
  );
  const [report, setReport] = useState<ReportData | null>(null);

  const resetDownstreamFromChart = useCallback(() => {
    setAnalysis(null);
    setInterpretation(null);
    setReport(null);
  }, []);

  const value = useMemo(
    () => ({
      chart,
      analysis,
      interpretation,
      report,
      setChart,
      setAnalysis,
      setInterpretation,
      setReport,
      resetDownstreamFromChart,
    }),
    [chart, analysis, interpretation, report, resetDownstreamFromChart],
  );

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}

export function useSession() {
  const ctx = useContext(SessionContext);
  if (!ctx) {
    throw new Error("useSession must be used within SessionProvider");
  }
  return ctx;
}
