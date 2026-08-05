/**
 * Cases / health API → Dashboard ViewModel adapter (TASK_003A).
 */

import type { CaseDto, HealthResponse } from "../models";
import {
  DASHBOARD_ANNOUNCEMENT,
  DASHBOARD_QUICK_ACTIONS,
  DASHBOARD_SHORTCUTS,
  type DashboardAnnouncement,
  type DashboardQuickAction,
  type DashboardRecentAnalysis,
  type DashboardShortcut,
  type DashboardStat,
} from "../screens/dashboard/mockData";

export type DashboardViewModel = {
  readonly quickActions: readonly DashboardQuickAction[];
  readonly stats: readonly DashboardStat[];
  readonly recent: readonly DashboardRecentAnalysis[];
  readonly shortcuts: readonly DashboardShortcut[];
  readonly announcement: DashboardAnnouncement;
};

function asString(value: unknown, fallback = ""): string {
  if (value === null || value === undefined) {
    return fallback;
  }
  return String(value);
}

function formatDate(iso: string): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso.slice(0, 10);
  }
  const dd = String(date.getDate()).padStart(2, "0");
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const yyyy = date.getFullYear();
  return `${yyyy}-${mm}-${dd}`;
}

function caseDisplayName(caseItem: CaseDto): string {
  const snapshot = caseItem.input_snapshot ?? {};
  const fullName = snapshot.full_name ?? snapshot.fullName ?? snapshot.name;
  if (fullName) {
    return asString(fullName);
  }
  return `Hồ sơ ${caseItem.case_id.slice(0, 8)}`;
}

function mapRecent(cases: readonly CaseDto[]): readonly DashboardRecentAnalysis[] {
  return [...cases]
    .sort((a, b) => asString(b.created_at).localeCompare(asString(a.created_at)))
    .slice(0, 8)
    .map((item) => ({
      id: item.case_id,
      fullName: caseDisplayName(item),
      createdAt: formatDate(asString(item.created_at)),
      status: "ready" as const,
      href: `/result?case_id=${encodeURIComponent(item.case_id)}`,
    }));
}

export type AdaptDashboardOptions = {
  readonly cases?: readonly CaseDto[];
  readonly caseCount?: number;
  readonly customerCount?: number;
  readonly reportCount?: number;
  readonly health?: HealthResponse | null;
};

/**
 * Build Dashboard ViewModel from backend list payloads.
 * Shortcuts / announcement stay static until CMS API exists (TODO).
 */
export function adaptDashboardViewModel(
  options: AdaptDashboardOptions = {},
): DashboardViewModel {
  const cases = options.cases ?? [];
  const caseCount = options.caseCount ?? cases.length;
  const customerCount = options.customerCount;
  const reportCount =
    options.reportCount ??
    cases.filter((item) => {
      const report = item.report_result;
      return report && Object.keys(report).length > 0;
    }).length;

  const healthHint =
    options.health?.status === "ok"
      ? `API ${options.health.version ?? "ok"}`
      : options.health
        ? `API ${options.health.status}`
        : undefined;

  const stats: DashboardStat[] = [
    {
      id: "charts",
      label: "Tổng số lá số",
      value: String(caseCount),
      hint: customerCount !== undefined ? `${customerCount} khách hàng` : healthHint,
    },
    {
      id: "analyses",
      label: "Số lần phân tích",
      value: String(caseCount),
      hint: healthHint,
    },
    {
      id: "reports",
      label: "Báo cáo đã tạo",
      value: String(reportCount),
    },
    {
      id: "activity",
      label: "Hoạt động gần đây",
      value: cases.length > 0 ? formatDate(asString(cases[0]?.created_at)) : "—",
      hint: healthHint,
    },
  ];

  return {
    quickActions: DASHBOARD_QUICK_ACTIONS,
    stats,
    recent: mapRecent(cases),
    shortcuts: DASHBOARD_SHORTCUTS,
    announcement: DASHBOARD_ANNOUNCEMENT,
  };
}
