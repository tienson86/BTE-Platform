import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { DashboardPage } from "./pages/DashboardPage";

const DatasetsPage = lazy(() =>
  import("./pages/DatasetsPage").then((m) => ({ default: m.DatasetsPage })),
);
const CreateDatasetPage = lazy(() =>
  import("./pages/CreateDatasetPage").then((m) => ({
    default: m.CreateDatasetPage,
  })),
);
const ImportDatasetPage = lazy(() =>
  import("./pages/ImportDatasetPage").then((m) => ({
    default: m.ImportDatasetPage,
  })),
);
const DatasetDetailPage = lazy(() =>
  import("./pages/DatasetDetailPage").then((m) => ({
    default: m.DatasetDetailPage,
  })),
);
const ApprovalQueuePage = lazy(() =>
  import("./pages/ApprovalQueuePage").then((m) => ({
    default: m.ApprovalQueuePage,
  })),
);

function Fallback() {
  return (
    <div className="py-16 text-center text-sm text-[var(--muted)]" role="status">
      Loading…
    </div>
  );
}

export default function App() {
  return (
    <AppShell>
      <Suspense fallback={<Fallback />}>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/datasets/:datasetId" element={<DatasetDetailPage />} />
          <Route path="/create" element={<CreateDatasetPage />} />
          <Route path="/import" element={<ImportDatasetPage />} />
          <Route path="/approval" element={<ApprovalQueuePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </AppShell>
  );
}
