/**
 * Single HTTP client for Portal → FastAPI (TASK_003A).
 * Screens must not call fetch() directly.
 */

import { getApiRuntimeConfig } from "../config/api";
import { ApiError, kindFromStatus, type ApiErrorPayload } from "./errors";
import type { ApiClientConfig, ApiEnvelope, ApiRequestOptions, BlobDownload } from "./types";
import { filenameFromDisposition } from "./types";

const RETRYABLE_KINDS = new Set(["timeout", "network", "server"]);

function joinUrl(baseUrl: string, path: string): string {
  const base = baseUrl.replace(/\/+$/, "");
  const suffix = path.startsWith("/") ? path : `/${path}`;
  return `${base}${suffix}`;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function parseJsonSafe(text: string): unknown {
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return { raw: text };
  }
}

function messageFromPayload(payload: ApiErrorPayload | null, fallback: string): string {
  if (!payload) {
    return fallback;
  }
  if (typeof payload.message === "string" && payload.message) {
    return payload.message;
  }
  if (typeof payload.detail === "string" && payload.detail) {
    return payload.detail;
  }
  return fallback;
}

function createTimeoutSignal(
  timeoutMs: number,
  external?: AbortSignal,
): { signal: AbortSignal; clear: () => void } {
  const controller = new AbortController();
  const timer = setTimeout(() => {
    controller.abort();
  }, timeoutMs);

  const onExternalAbort = (): void => {
    controller.abort();
  };

  if (external) {
    if (external.aborted) {
      controller.abort();
    } else {
      external.addEventListener("abort", onExternalAbort, { once: true });
    }
  }

  return {
    signal: controller.signal,
    clear: () => {
      clearTimeout(timer);
      if (external) {
        external.removeEventListener("abort", onExternalAbort);
      }
    },
  };
}

/**
 * API Client — one instance per app (factory for tests).
 */
export class ApiClient {
  private readonly config: ApiClientConfig;

  constructor(config?: Partial<ApiClientConfig>) {
    const runtime = getApiRuntimeConfig();
    this.config = {
      baseUrl: config?.baseUrl ?? runtime.baseUrl,
      timeoutMs: config?.timeoutMs ?? runtime.timeoutMs,
      retries: config?.retries ?? runtime.retries,
      getAccessToken: config?.getAccessToken,
    };
  }

  get baseUrl(): string {
    return this.config.baseUrl;
  }

  /**
   * Perform a JSON request with timeout + retry for transient failures.
   */
  async request<TData>(path: string, options: ApiRequestOptions = {}): Promise<TData> {
    const method = options.method ?? (options.body !== undefined ? "POST" : "GET");
    const retries = options.retries ?? this.config.retries;
    const timeoutMs = options.timeoutMs ?? this.config.timeoutMs;
    let attempt = 0;
    let lastError: ApiError | undefined;

    while (attempt <= retries) {
      try {
        return await this.requestOnce<TData>(path, method, options, timeoutMs);
      } catch (error) {
        const apiError =
          error instanceof ApiError
            ? error
            : new ApiError("Unknown client error", {
                kind: "unknown",
                cause: error,
              });
        lastError = apiError;
        const canRetry =
          attempt < retries && RETRYABLE_KINDS.has(apiError.kind) && method === "GET";
        // Also retry idempotent-safe analyze POST on network/timeout only.
        const canRetryPost =
          attempt < retries &&
          (apiError.kind === "network" || apiError.kind === "timeout") &&
          method === "POST";
        if (!canRetry && !canRetryPost) {
          throw apiError;
        }
        attempt += 1;
        await sleep(Math.min(1000 * 2 ** (attempt - 1), 4000));
      }
    }

    throw lastError ?? new ApiError("Request failed", { kind: "unknown" });
  }

  async get<TData>(path: string, options?: Omit<ApiRequestOptions, "method" | "body">): Promise<TData> {
    return this.request<TData>(path, { ...options, method: "GET" });
  }

  async post<TData>(
    path: string,
    body?: unknown,
    options?: Omit<ApiRequestOptions, "method" | "body">,
  ): Promise<TData> {
    return this.request<TData>(path, { ...options, method: "POST", body });
  }

  /**
   * POST that returns a file blob (official PDF/DOCX). Does not parse JSON on success.
   */
  async requestBlob(
    path: string,
    body: unknown,
    options: Omit<ApiRequestOptions, "method"> & { fallbackFilename: string } = {
      fallbackFilename: "BTE_BaoCao_V1.bin",
    },
  ): Promise<BlobDownload> {
    const timeoutMs = options.timeoutMs ?? 120_000;
    const headers: Record<string, string> = {
      Accept: "application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/json",
      ...(options.headers ?? {}),
    };
    if (headers["Content-Type"] === undefined) {
      headers["Content-Type"] = "application/json";
    }
    if (!options.skipAuth) {
      const token = this.config.getAccessToken?.();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }
    const { signal, clear } = createTimeoutSignal(timeoutMs, options.signal);
    let response: Response;
    try {
      response = await fetch(joinUrl(this.config.baseUrl, path), {
        method: "POST",
        headers,
        body: JSON.stringify(body),
        signal,
      });
    } catch (error) {
      clear();
      const aborted =
        (error instanceof DOMException && error.name === "AbortError") ||
        (error instanceof Error && error.name === "AbortError");
      if (aborted) {
        throw new ApiError("Request timed out", {
          kind: "timeout",
          status: 408,
          code: "timeout",
          cause: error,
        });
      }
      throw new ApiError("Network error", {
        kind: "network",
        code: "network_error",
        cause: error,
      });
    }
    clear();
    if (!response.ok) {
      const text = await response.text();
      const parsed = parseJsonSafe(text);
      const payload =
        parsed && typeof parsed === "object" ? (parsed as ApiErrorPayload) : null;
      throw new ApiError(messageFromPayload(payload, response.statusText || "Request failed"), {
        kind: kindFromStatus(response.status),
        status: response.status,
        code: payload?.code ?? kindFromStatus(response.status),
        details: payload?.details ?? payload?.errors ?? null,
        requestId: payload?.request_id ?? null,
        payload,
      });
    }
    const blob = await response.blob();
    if (!blob.size) {
      throw new ApiError("Không tạo được tệp xuất. Vui lòng thử lại.", {
        kind: "server",
        status: response.status,
        code: "export_empty_file",
      });
    }
    return {
      blob,
      filename: filenameFromDisposition(
        response.headers.get("Content-Disposition"),
        options.fallbackFilename,
      ),
      analysisId: response.headers.get("X-BTE-Analysis-Id") || "",
      mediaType: response.headers.get("Content-Type") || blob.type,
    };
  }

  private async requestOnce<TData>(
    path: string,
    method: string,
    options: ApiRequestOptions,
    timeoutMs: number,
  ): Promise<TData> {
    const headers: Record<string, string> = {
      Accept: "application/json",
      ...(options.headers ?? {}),
    };

    if (options.body !== undefined && headers["Content-Type"] === undefined) {
      headers["Content-Type"] = "application/json";
    }

    if (!options.skipAuth) {
      const token = this.config.getAccessToken?.();
      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }
    }

    const { signal, clear } = createTimeoutSignal(timeoutMs, options.signal);
    let response: Response;

    try {
      response = await fetch(joinUrl(this.config.baseUrl, path), {
        method,
        headers,
        body: options.body === undefined ? undefined : JSON.stringify(options.body),
        signal,
      });
    } catch (error) {
      clear();
      const aborted =
        (error instanceof DOMException && error.name === "AbortError") ||
        (error instanceof Error && error.name === "AbortError");
      if (aborted) {
        throw new ApiError("Request timed out", {
          kind: "timeout",
          status: 408,
          code: "timeout",
          cause: error,
        });
      }
      throw new ApiError("Network error", {
        kind: "network",
        code: "network_error",
        cause: error,
      });
    }
    clear();

    const text = await response.text();
    const parsed = parseJsonSafe(text);
    const payload =
      parsed && typeof parsed === "object" ? (parsed as ApiErrorPayload & ApiEnvelope<TData>) : null;

    if (!response.ok) {
      const kind = kindFromStatus(response.status);
      throw new ApiError(messageFromPayload(payload, response.statusText || "Request failed"), {
        kind,
        status: response.status,
        code: payload?.code ?? kind,
        details: payload?.details ?? payload?.errors ?? null,
        requestId: payload?.request_id ?? null,
        payload,
      });
    }

    // Health endpoint returns a flat object (no envelope).
    if (payload && typeof payload.success === "boolean") {
      if (payload.success === false) {
        throw new ApiError(messageFromPayload(payload, "Request failed"), {
          kind: "server",
          status: response.status,
          code: payload.code ?? "api_error",
          details: payload.details ?? payload.errors ?? null,
          requestId: payload.request_id ?? null,
          payload,
        });
      }
      return payload as TData;
    }

    return (parsed as TData) ?? ({} as TData);
  }
}

let sharedClient: ApiClient | null = null;

/** Shared singleton client (lazy). Prefer DI in services for tests. */
export function getApiClient(): ApiClient {
  if (!sharedClient) {
    sharedClient = new ApiClient({
      getAccessToken: () => {
        if (typeof sessionStorage === "undefined") {
          return null;
        }
        try {
          return sessionStorage.getItem("bte_portal_token");
        } catch {
          return null;
        }
      },
    });
  }
  return sharedClient;
}

/** Reset shared client (tests). */
export function resetApiClient(): void {
  sharedClient = null;
}
