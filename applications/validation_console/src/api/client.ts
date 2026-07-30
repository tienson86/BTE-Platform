import type {
  ApiEnvelope,
  CompareResponse,
  CoverageReport,
  GoldenCase,
  GoldenDataset,
  RegressionReport,
  Statistics,
  WorkflowAction,
} from "./types";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(message: string, status: number, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  const payload = (await response.json()) as ApiEnvelope<T> & {
    detail?: { message?: string };
  };
  if (!response.ok || !payload.success) {
    const detail = payload.detail ?? payload;
    const message =
      (typeof detail === "object" &&
        detail &&
        "message" in detail &&
        typeof detail.message === "string" &&
        detail.message) ||
      payload.message ||
      `Request failed (${response.status})`;
    throw new ApiError(message, response.status, detail);
  }
  return payload.data;
}

export const api = {
  health: () =>
    fetch("/health").then(async (r) => {
      if (!r.ok) throw new Error("API unavailable");
      return r.json() as Promise<{
        status: string;
        service: string;
        version: string;
      }>;
    }),

  listDatasets: (params?: { status?: string; module?: string }) => {
    const query = new URLSearchParams();
    if (params?.status) query.set("status", params.status);
    if (params?.module) query.set("module", params.module);
    const suffix = query.toString() ? `?${query}` : "";
    return request<GoldenDataset[]>(`/api/v1/datasets${suffix}`);
  },

  getDataset: (id: string) =>
    request<GoldenDataset>(`/api/v1/datasets/${id}`),

  createDataset: (body: {
    name: string;
    description?: string;
    module?: string;
    cases?: Partial<GoldenCase>[];
  }) =>
    request<GoldenDataset>("/api/v1/datasets", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  importDataset: (body: {
    name: string;
    cases: Partial<GoldenCase>[];
    description?: string;
    module?: string;
  }) =>
    request<GoldenDataset>("/api/v1/datasets/import", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  addCase: (datasetId: string, casePayload: Partial<GoldenCase>) =>
    request<GoldenDataset>(`/api/v1/datasets/${datasetId}/cases`, {
      method: "POST",
      body: JSON.stringify({ case: casePayload }),
    }),

  setActual: (
    datasetId: string,
    caseId: string,
    actual_output: Record<string, unknown>,
  ) =>
    request<GoldenDataset>(
      `/api/v1/datasets/${datasetId}/cases/${caseId}/actual`,
      {
        method: "PUT",
        body: JSON.stringify({ actual_output }),
      },
    ),

  compare: (datasetId: string, caseId?: string) => {
    const query = caseId ? `?case_id=${encodeURIComponent(caseId)}` : "";
    return request<CompareResponse>(
      `/api/v1/datasets/${datasetId}/compare${query}`,
    );
  },

  regression: (datasetId: string) =>
    request<RegressionReport>(`/api/v1/datasets/${datasetId}/regression`, {
      method: "POST",
      body: JSON.stringify({ actor: "validator" }),
    }),

  statistics: (datasetId: string) =>
    request<Statistics>(`/api/v1/datasets/${datasetId}/statistics`),

  coverage: (datasetId: string) =>
    request<CoverageReport>(`/api/v1/datasets/${datasetId}/coverage`),

  approvalQueue: () =>
    request<GoldenDataset[]>("/api/v1/workflow/queue"),

  workflow: (
    datasetId: string,
    action: WorkflowAction,
    actor = "reviewer",
    message = "",
  ) =>
    request<GoldenDataset>(`/api/v1/workflow/${datasetId}`, {
      method: "POST",
      body: JSON.stringify({ action, actor, message }),
    }),
};
