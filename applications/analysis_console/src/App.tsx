import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { AnalysisViewerPage } from "./pages/AnalysisViewerPage";
import { ChartInputPage } from "./pages/ChartInputPage";
import { ChartViewerPage } from "./pages/ChartViewerPage";
import { DashboardPage } from "./pages/DashboardPage";
import { InterpretationViewerPage } from "./pages/InterpretationViewerPage";
import { LuckViewerPage } from "./pages/LuckViewerPage";
import { SessionProvider } from "./state/session";

export default function App() {
  return (
    <SessionProvider>
      <AppShell>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/chart/input" element={<ChartInputPage />} />
          <Route path="/chart" element={<ChartViewerPage />} />
          <Route path="/analysis" element={<AnalysisViewerPage />} />
          <Route
            path="/interpretation"
            element={<InterpretationViewerPage />}
          />
          <Route path="/luck" element={<LuckViewerPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </SessionProvider>
  );
}
