import type {
  ApiEnvelope,
  CreateAssetPayload,
  DiffResult,
  HistoryEntry,
  KnowledgeAsset,
  PreviewResult,
  UpdateAssetPayload,
  ValidationResult,
  VersionSnapshot,
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
    detail?: { message?: string; issues?: unknown };
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

  listAssets: (params?: { asset_type?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.asset_type) query.set("asset_type", params.asset_type);
    if (params?.status) query.set("status", params.status);
    const suffix = query.toString() ? `?${query}` : "";
    return request<KnowledgeAsset[]>(`/api/v1/assets${suffix}`);
  },

  getAsset: (assetId: string) =>
    request<KnowledgeAsset>(`/api/v1/assets/${assetId}`),

  createAsset: (body: CreateAssetPayload) =>
    request<KnowledgeAsset>("/api/v1/assets", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  updateAsset: (assetId: string, body: UpdateAssetPayload) =>
    request<KnowledgeAsset>(`/api/v1/assets/${assetId}`, {
      method: "PUT",
      body: JSON.stringify(body),
    }),

  validate: (assetId: string) =>
    request<ValidationResult>(`/api/v1/assets/${assetId}/validate`, {
      method: "POST",
    }),

  preview: (assetId: string) =>
    request<PreviewResult>(`/api/v1/assets/${assetId}/preview`),

  history: (assetId: string) =>
    request<HistoryEntry[]>(`/api/v1/assets/${assetId}/history`),

  versions: (assetId: string) =>
    request<VersionSnapshot[]>(`/api/v1/assets/${assetId}/versions`),

  diff: (assetId: string, fromVersion: string, toVersion?: string) => {
    const query = new URLSearchParams({ from_version: fromVersion });
    if (toVersion) query.set("to_version", toVersion);
    return request<DiffResult>(
      `/api/v1/assets/${assetId}/diff?${query.toString()}`,
    );
  },

  approvalQueue: () =>
    request<KnowledgeAsset[]>("/api/v1/workflow/queue"),

  workflow: (
    assetId: string,
    action: WorkflowAction,
    actor = "reviewer",
    message = "",
  ) =>
    request<KnowledgeAsset>(`/api/v1/workflow/${assetId}`, {
      method: "POST",
      body: JSON.stringify({ action, actor, message }),
    }),
};
