import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { DashboardScreen } from "@portal/screens/DashboardScreen";
import { BaZiResultScreen } from "@portal/screens/bazi/BaZiResultScreen";
import { ExecutiveSummaryCard } from "@portal/screens/bazi/ExecutiveSummaryCard";
import { BAZI_RESULT_MOCK } from "@portal/screens/bazi/mockData";
import { S00DesktopScreen } from "@portal/screens/s00/S00DesktopScreen";
import { AuthLayout } from "@portal/layouts/AuthLayout";
import { BlankLayout } from "@portal/layouts/BlankLayout";
import { AppLayout } from "@portal/layouts/AppLayout";
import { AppProviders } from "@portal/app/AppProviders";
import { Dialog } from "@portal/components/feedback/Dialog";
import { Drawer } from "@portal/components/feedback/Drawer";
import { Toast } from "@portal/components/feedback/Toast";
import { EmptyState } from "@portal/components/feedback/EmptyState";
import { Skeleton } from "@portal/components/feedback/Skeleton";
import { BaseTooltip } from "@portal/components/base/BaseTooltip";
import { Button } from "@portal/components/base/Button";
import { Card } from "@portal/components/base/Card";
import { Stack } from "@portal/components/layout/Stack";
import "@portal/styles/index.css";

type ReviewPage =
  | "dashboard"
  | "bazi"
  | "s00"
  | "executive"
  | "bazi-loading"
  | "bazi-empty"
  | "bazi-error"
  | "patterns"
  | "drawer"
  | "auth";

function readPage(): ReviewPage {
  const value = new URLSearchParams(window.location.search).get("page") ?? "dashboard";
  switch (value) {
    case "bazi":
    case "s00":
    case "executive":
    case "bazi-loading":
    case "bazi-empty":
    case "bazi-error":
    case "patterns":
    case "drawer":
    case "auth":
      return value;
    default:
      return "dashboard";
  }
}

function PatternsGallery() {
  return (
    <AppProviders>
      <BlankLayout>
        <div className="cui-review-gallery">
          <Stack gap="section">
            <Card title="Empty / Skeleton / Toast / Tooltip / Dialog">
              <Stack gap="paragraph">
                <EmptyState
                  title="Empty State"
                  description="Không có dữ liệu để hiển thị."
                />
                <div aria-label="Skeleton samples">
                  <Skeleton width="100%" height="48px" />
                  <Skeleton width="80%" height="16px" />
                  <Skeleton width="60%" height="16px" />
                </div>
                <Toast open tone="info" title="Toast">
                  Thông báo tạm thời (placeholder).
                </Toast>
                <BaseTooltip content="Tooltip nội dung giải thích">
                  <Button variant="secondary">Hover / Focus Tooltip</Button>
                </BaseTooltip>
              </Stack>
            </Card>
            <Dialog open title="Dialog mẫu" onClose={() => undefined} closeLabel="Đóng">
              Nội dung dialog để review hierarchy và spacing.
            </Dialog>
          </Stack>
        </div>
      </BlankLayout>
    </AppProviders>
  );
}

function DrawerGallery() {
  return (
    <AppProviders>
      <BlankLayout>
        <div className="cui-review-gallery">
          <Card title="Drawer pattern">
            <p>Drawer đang mở bên phải để review.</p>
          </Card>
          <Drawer open side="end" title="Drawer mẫu" onClose={() => undefined} closeLabel="Đóng">
            Nội dung drawer (slide-over) để review.
          </Drawer>
        </div>
      </BlankLayout>
    </AppProviders>
  );
}

function App() {
  const page = readPage();
  if (page === "dashboard") {
    return <DashboardScreen userName="Nguyễn Văn Minh" />;
  }
  if (page === "s00") {
    return <S00DesktopScreen />;
  }
  if (page === "executive") {
    return (
      <AppProviders>
        <AppLayout pathname="/result" userLabel="Nguyễn Văn Minh" tocActiveId="summary">
          <div className="cui-review-executive-zoom">
            <ExecutiveSummaryCard
              status="ready"
              labels={BAZI_RESULT_MOCK.labels}
              executive={BAZI_RESULT_MOCK.executive}
            />
          </div>
        </AppLayout>
      </AppProviders>
    );
  }
  if (page === "bazi") {
    return <BaZiResultScreen userName="Nguyễn Văn Minh" />;
  }
  if (page === "bazi-loading") {
    return <BaZiResultScreen status="loading" />;
  }
  if (page === "bazi-empty") {
    return <BaZiResultScreen status="empty" />;
  }
  if (page === "bazi-error") {
    return (
      <BaZiResultScreen
        status="error"
        data={{
          ...BAZI_RESULT_MOCK,
          status: "error",
          errorMessage: "Mock error — không kết nối được Analysis Engine.",
        }}
      />
    );
  }
  if (page === "auth") {
    return (
      <AppProviders>
        <AuthLayout title="Đăng nhập BTE">
          <p>Auth layout placeholder — review shell only.</p>
        </AuthLayout>
      </AppProviders>
    );
  }
  if (page === "drawer") {
    return <DrawerGallery />;
  }
  return <PatternsGallery />;
}

const style = document.createElement("style");
style.textContent = `
  .cui-review-gallery {
    padding: calc(var(--space-block, 24px));
    max-width: 960px;
    margin: 0 auto;
  }
  .cui-review-executive-zoom,
  .cui-review-s00-zoom {
    max-width: 72rem;
    margin: 0 auto;
    padding: calc(var(--space-block, 24px));
  }
  .cui-review-s00-layout {
    max-width: 72rem;
    margin: 0 auto;
    padding: calc(var(--space-5, 24px));
  }
  .cui-review-s00-zoom__title {
    margin: 0 0 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-secondary, #555);
  }
`;
document.head.appendChild(style);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
