/**
 * Low-level API client types (TASK_003A).
 */

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type ApiRequestOptions = {
  readonly method?: HttpMethod;
  readonly body?: unknown;
  readonly headers?: Readonly<Record<string, string>>;
  readonly signal?: AbortSignal;
  /** Override client timeout for one call (ms). */
  readonly timeoutMs?: number;
  /** Override retry count for one call. */
  readonly retries?: number;
  /** Skip Authorization header when true. */
  readonly skipAuth?: boolean;
};

export type ApiEnvelope<TData> = {
  readonly success: boolean;
  readonly message: string;
  readonly data: TData;
  readonly request_id?: string | null;
  readonly code?: string;
  readonly details?: unknown;
  readonly errors?: readonly unknown[];
};

export type ApiClientConfig = {
  readonly baseUrl: string;
  readonly timeoutMs: number;
  readonly retries: number;
  readonly getAccessToken?: () => string | null | undefined;
};

export type BlobDownload = {
  readonly blob: Blob;
  readonly filename: string;
  readonly analysisId: string;
  readonly mediaType: string;
};

export function filenameFromDisposition(header: string | null, fallback: string): string {
  if (!header) return fallback;
  const utf = /filename\*=UTF-8''([^;]+)/i.exec(header);
  if (utf?.[1]) {
    try {
      return decodeURIComponent(utf[1]);
    } catch {
      return utf[1];
    }
  }
  const ascii = /filename="?([^";]+)"?/i.exec(header);
  return ascii?.[1]?.trim() || fallback;
}
