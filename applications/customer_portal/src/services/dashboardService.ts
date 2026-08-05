/**
 * Dashboard data service (TASK_003A).
 */

import { ApiClient, API_ENDPOINTS, getApiClient } from "../api";
import { adaptDashboardViewModel, type DashboardViewModel } from "../adapters";
import { isMockDataSource } from "../config/api";
import type {
  CasesListData,
  CustomersListData,
  HealthResponse,
} from "../models";
import {
  DASHBOARD_ANNOUNCEMENT,
  DASHBOARD_QUICK_ACTIONS,
  DASHBOARD_RECENT,
  DASHBOARD_SHORTCUTS,
  DASHBOARD_STATS,
} from "../screens/dashboard/mockData";

export type DashboardServiceOptions = {
  readonly client?: ApiClient;
};

export class DashboardService {
  private readonly client: ApiClient;

  constructor(options: DashboardServiceOptions = {}) {
    this.client = options.client ?? getApiClient();
  }

  async getHealth(): Promise<HealthResponse> {
    return this.client.get<HealthResponse>(API_ENDPOINTS.health, { skipAuth: true });
  }

  async listCases(): Promise<CasesListData> {
    const envelope = await this.client.get<{
      success: boolean;
      message: string;
      data: CasesListData;
    }>(API_ENDPOINTS.cases);
    return envelope.data;
  }

  async listCustomers(): Promise<CustomersListData> {
    const envelope = await this.client.get<{
      success: boolean;
      message: string;
      data: CustomersListData;
    }>(API_ENDPOINTS.customers);
    return envelope.data;
  }

  /**
   * Load Dashboard ViewModel from Cases (+ optional Customers / Health).
   */
  async getViewModel(): Promise<DashboardViewModel> {
    if (isMockDataSource()) {
      return {
        quickActions: DASHBOARD_QUICK_ACTIONS,
        stats: DASHBOARD_STATS,
        recent: DASHBOARD_RECENT,
        shortcuts: DASHBOARD_SHORTCUTS,
        announcement: DASHBOARD_ANNOUNCEMENT,
      };
    }

    const [casesResult, customersResult, healthResult] = await Promise.allSettled([
      this.listCases(),
      this.listCustomers(),
      this.getHealth(),
    ]);

    const casesData =
      casesResult.status === "fulfilled"
        ? casesResult.value
        : { cases: [], count: 0 };
    const customerCount =
      customersResult.status === "fulfilled" ? customersResult.value.count : undefined;
    const health = healthResult.status === "fulfilled" ? healthResult.value : null;

    return adaptDashboardViewModel({
      cases: casesData.cases,
      caseCount: casesData.count,
      customerCount,
      health,
    });
  }
}

let sharedDashboardService: DashboardService | null = null;

export function getDashboardService(): DashboardService {
  if (!sharedDashboardService) {
    sharedDashboardService = new DashboardService();
  }
  return sharedDashboardService;
}

export function resetDashboardService(): void {
  sharedDashboardService = null;
}
