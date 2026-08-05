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
