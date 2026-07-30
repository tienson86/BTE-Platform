import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { DashboardPage } from "./pages/DashboardPage";

const LibraryPage = lazy(() =>
  import("./pages/LibraryPage").then((m) => ({ default: m.LibraryPage })),
);
const CreateAssetPage = lazy(() =>
  import("./pages/CreateAssetPage").then((m) => ({
    default: m.CreateAssetPage,
  })),
);
const EditorPage = lazy(() =>
  import("./pages/EditorPage").then((m) => ({ default: m.EditorPage })),
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
          <Route path="/library" element={<LibraryPage />} />
          <Route path="/create" element={<CreateAssetPage />} />
          <Route path="/editor/:assetId" element={<EditorPage />} />
          <Route path="/approval" element={<ApprovalQueuePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </AppShell>
  );
}
