import type { ReactNode } from "react";
import { AppProviders } from "../app/AppProviders";
import { Stack } from "../components/layout/Stack";
import { AppLayout } from "../layouts/AppLayout";
import { DASHBOARD_TOC_ITEMS } from "../layouts/Navigation/navItems";
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
import {
  DASHBOARD_ANNOUNCEMENT,
  DASHBOARD_QUICK_ACTIONS,
  DASHBOARD_RECENT,
  DASHBOARD_SHORTCUTS,
  DASHBOARD_STATS,
} from "./dashboard/mockData";

export type DashboardScreenProps = {
  userName?: string;
  pathname?: string;
  loading?: boolean;
  emptyRecent?: boolean;
  viewModel?: DashboardViewModel;
};

const DASHBOARD_MOCK_VIEW_MODEL: DashboardViewModel = {
  quickActions: DASHBOARD_QUICK_ACTIONS,
  stats: DASHBOARD_STATS,
  recent: DASHBOARD_RECENT,
  shortcuts: DASHBOARD_SHORTCUTS,
  announcement: DASHBOARD_ANNOUNCEMENT,
};

/**
 * Canonical Portal Dashboard.
 * Same data; shell = top primary nav + TOC; content tiers preserved.
 */
export function DashboardScreen({
  userName,
  pathname = "/dashboard",
  loading = false,
  emptyRecent = false,
  viewModel = DASHBOARD_MOCK_VIEW_MODEL,
}: DashboardScreenProps): ReactNode {
  const recentItems = emptyRecent ? [] : viewModel.recent;

  return (
    <AppProviders>
      <AppLayout
        pathname={pathname}
        userLabel={userName ?? "Người dùng"}
        tocItems={DASHBOARD_TOC_ITEMS}
        tocTitle="MỤC LỤC"
        tocActiveId="welcome"
      >
        <PageWrapper
          title="Dashboard"
          description="Tổng quan hoạt động và lối vào chức năng chính."
          className="cui-dashboard-page"
        >
          {loading ? (
            <DashboardSkeleton />
          ) : (
            <Stack gap="section" className="cui-dashboard cui-dashboard--canonical">
              <section
                id="tong-quan"
                className="cui-dashboard__tier cui-dashboard__tier--hero"
                aria-label="Chào mừng"
              >
                <WelcomeSection userName={userName} />
              </section>

              <section
                id="thao-tac"
                className="cui-dashboard__tier"
                aria-label="Thao tác nhanh"
              >
                <QuickActionsSection actions={viewModel.quickActions} />
              </section>

              <section
                id="chi-so"
                className="cui-dashboard__tier cui-dashboard__tier--metrics"
                aria-label="Chỉ số"
              >
                <StatisticsSection stats={viewModel.stats} />
              </section>

              <section
                id="gan-day"
                className="cui-dashboard__tier cui-dashboard__tier--primary"
                aria-label="Công việc gần đây"
              >
                <RecentAnalysesSection items={recentItems} />
              </section>

              <section
                id="tien-ich"
                className="cui-dashboard__tier cui-dashboard__tier--utility"
                aria-label="Tiện ích"
              >
                <ShortcutsSection shortcuts={viewModel.shortcuts} />
                <AnnouncementSection announcement={viewModel.announcement} />
              </section>
            </Stack>
          )}
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
