/**
 * Health probe service (TASK_003A).
 */

import { ApiClient, API_ENDPOINTS, getApiClient } from "../api";
import type { HealthResponse } from "../models";

export class HealthService {
  private readonly client: ApiClient;

  constructor(client?: ApiClient) {
    this.client = client ?? getApiClient();
  }

  async check(): Promise<HealthResponse> {
    return this.client.get<HealthResponse>(API_ENDPOINTS.health, { skipAuth: true });
  }
}

let sharedHealthService: HealthService | null = null;

export function getHealthService(): HealthService {
  if (!sharedHealthService) {
    sharedHealthService = new HealthService();
  }
  return sharedHealthService;
}

export function resetHealthService(): void {
  sharedHealthService = null;
}
