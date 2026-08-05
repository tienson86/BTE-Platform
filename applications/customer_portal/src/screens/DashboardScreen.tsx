import type { ReactNode } from "react";
import { AppProviders } from "../app/AppProviders";
import { Stack } from "../components/layout/Stack";
import { useDashboard } from "../hooks/useDashboard";
import { AppLayout } from "../layouts/AppLayout";
import { PageWrapper } from "../layouts/PageWrapper";
import type { DashboardViewModel } from "../adapters";
import {
  AnnouncementSection,
  DashboardSkeleton,
  QuickActionsSection,
  RecentAnalysesSection,
  ShortcutsSection,
  StatisticsSection,
  WelcomeSection,
} from "./dashboard";

export type DashboardScreenProps = {
  userName?: string;
  pathname?: string;
  loading?: boolean;
  /** When true, recent list is forced empty to demonstrate Empty State. */
  emptyRecent?: boolean;
  /**
   * Injected ViewModel (tests / story).
   * When omitted, loads via DashboardService → Adapter.
   */
  viewModel?: DashboardViewModel;
};

/**
 * Portal Dashboard home screen (WP04 + TASK_003A).
 * Uses AppLayout from WP03 only — no alternate layout.
 * Data: Service → Adapter → ViewModel (no fetch in presentational children).
 */
export function DashboardScreen({
  userName,
  pathname = "/dashboard",
  loading,
  emptyRecent = false,
  viewModel: viewModelProp,
}: DashboardScreenProps): ReactNode {
  const remote = useDashboard({
    enabled: viewModelProp === undefined,
    initialData: viewModelProp,
  });
  const viewModel = remote.viewModel;
  const isLoading = loading ?? remote.loading;
  const recentItems = emptyRecent ? [] : viewModel.recent;

  return (
    <AppProviders>
      <AppLayout pathname={pathname} userLabel={userName ?? "Người dùng"}>
        <PageWrapper
          title="Dashboard"
          description="Tổng quan hoạt động và lối vào chức năng chính."
          breadcrumb={[
            { id: "home", label: "Portal", href: "/dashboard" },
            { id: "dashboard", label: "Dashboard" },
          ]}
        >
          {isLoading ? (
            <DashboardSkeleton />
          ) : (
            <Stack gap="section" className="cui-dashboard">
              <WelcomeSection userName={userName} />
              <QuickActionsSection actions={viewModel.quickActions} />
              <StatisticsSection stats={viewModel.stats} />
              <RecentAnalysesSection items={recentItems} />
              <ShortcutsSection shortcuts={viewModel.shortcuts} />
              <AnnouncementSection announcement={viewModel.announcement} />
            </Stack>
          )}
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
