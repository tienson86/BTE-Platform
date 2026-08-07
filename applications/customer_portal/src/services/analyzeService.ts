/**
 * Analyze / chart services — Component → Service → API Client (TASK_003A).
 */

import { ApiClient, API_ENDPOINTS, getApiClient } from "../api";
import {
  adaptAnalysisToBaZiResult,
  adaptAnalysisToCanonicalDesktop,
  createBaZiResultGateViewModel,
  createCanonicalDesktopMockViewModel,
  type BaZiResultViewModel,
  type CanonicalDesktopViewModel,
} from "../adapters";
import { isMockDataSource } from "../config/api";
import type { AnalysisResponse, AnalyzeChartRequest, ChartResponse } from "../models";
import { BAZI_RESULT_MOCK } from "../screens/bazi/mockData";

export type AnalyzeServiceOptions = {
  readonly client?: ApiClient;
};

export class AnalyzeService {
  private readonly client: ApiClient;

  constructor(options: AnalyzeServiceOptions = {}) {
    this.client = options.client ?? getApiClient();
  }

  /** POST /analyze — full pipeline envelope. */
  async analyze(request: AnalyzeChartRequest): Promise<AnalysisResponse> {
    return this.client.post<AnalysisResponse>(API_ENDPOINTS.analyze, request);
  }

  /** POST /bazi — chart slice (same birth request). */
  async createChart(request: AnalyzeChartRequest): Promise<ChartResponse> {
    return this.client.post<ChartResponse>(API_ENDPOINTS.bazi, request);
  }

  /**
   * Analyze and adapt to BaZi Result ViewModel.
   * Uses mock adapter when `BTE_DATA_SOURCE=mock` (tests).
   */
  async getBaZiResultViewModel(request: AnalyzeChartRequest): Promise<BaZiResultViewModel> {
    if (isMockDataSource()) {
      return {
        ...BAZI_RESULT_MOCK,
        status: "ready",
        profile: {
          ...BAZI_RESULT_MOCK.profile,
          fullName: request.full_name ?? BAZI_RESULT_MOCK.profile.fullName,
          birthPlace: request.birth_place ?? BAZI_RESULT_MOCK.profile.birthPlace,
        },
      };
    }

    const response = await this.analyze(request);
    return adaptAnalysisToBaZiResult(response.data, {
      request,
      requestId: response.request_id,
      status: "ready",
    });
  }

  /**
   * Analyze and adapt to Canonical Desktop ViewModel (S00–S11).
   * Calendar → BaZi → Pattern/Score/Strength → Interpretation → Report via orchestrator.
   */
  async getCanonicalDesktopViewModel(
    request: AnalyzeChartRequest,
  ): Promise<CanonicalDesktopViewModel> {
    if (isMockDataSource()) {
      const fixture = createCanonicalDesktopMockViewModel();
      return {
        ...fixture,
        header: {
          ...fixture.header,
          user: {
            ...fixture.header.user,
            name: request.full_name ?? fixture.header.user.name,
          },
        },
        s00: {
          ...fixture.s00,
          profile: {
            ...fixture.s00.profile,
            name: request.full_name ?? fixture.s00.profile.name,
          },
        },
        source: "mock",
        status: "ready",
      };
    }

    const response = await this.analyze(request);
    return adaptAnalysisToCanonicalDesktop(response.data, {
      request,
      requestId: response.request_id,
      status: "ready",
      source: "api",
    });
  }

  /** Loading gate ViewModel helper. */
  loadingViewModel(): BaZiResultViewModel {
    return createBaZiResultGateViewModel("loading");
  }
}

let sharedAnalyzeService: AnalyzeService | null = null;

export function getAnalyzeService(): AnalyzeService {
  if (!sharedAnalyzeService) {
    sharedAnalyzeService = new AnalyzeService();
  }
  return sharedAnalyzeService;
}

export function resetAnalyzeService(): void {
  sharedAnalyzeService = null;
}
