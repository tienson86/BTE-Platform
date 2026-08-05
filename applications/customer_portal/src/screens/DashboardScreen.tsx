import type { ReactNode } from "react";
import { AppProviders } from "../app/AppProviders";
import { Stack } from "../components/layout/Stack";
import { AppLayout } from "../layouts/AppLayout";
import { PageWrapper } from "../layouts/PageWrapper";
import {
  AnnouncementSection,
  DASHBOARD_ANNOUNCEMENT,
  DASHBOARD_QUICK_ACTIONS,
  DASHBOARD_RECENT,
  DASHBOARD_SHORTCUTS,
  DASHBOARD_STATS,
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
};

/**
 * Portal Dashboard home screen (WP04).
 * Uses AppLayout from WP03 only — no alternate layout.
 */
export function DashboardScreen({
  userName,
  pathname = "/dashboard",
  loading = false,
  emptyRecent = false,
}: DashboardScreenProps): ReactNode {
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
          {loading ? (
            <DashboardSkeleton />
          ) : (
            <Stack gap="section" className="cui-dashboard">
              <WelcomeSection userName={userName} />
              <QuickActionsSection actions={DASHBOARD_QUICK_ACTIONS} />
              <StatisticsSection stats={DASHBOARD_STATS} />
              <RecentAnalysesSection
                items={emptyRecent ? [] : DASHBOARD_RECENT}
              />
              <ShortcutsSection shortcuts={DASHBOARD_SHORTCUTS} />
              <AnnouncementSection announcement={DASHBOARD_ANNOUNCEMENT} />
            </Stack>
          )}
        </PageWrapper>
      </AppLayout>
    </AppProviders>
  );
}
