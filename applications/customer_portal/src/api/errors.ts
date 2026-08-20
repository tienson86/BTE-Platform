/**
 * Typed API errors for Portal ↔ FastAPI (TASK_003A).
 */

export type ApiErrorKind =
  | "validation"
  | "unauthorized"
  | "forbidden"
  | "not_found"
  | "server"
  | "timeout"
  | "network"
  | "unknown";

export type ApiErrorPayload = {
  readonly success?: boolean;
  readonly message?: string;
  readonly code?: string;
  readonly details?: unknown;
  readonly errors?: readonly unknown[];
  readonly request_id?: string | null;
  readonly detail?: unknown;
};

/**
 * Normalized error thrown by the API client.
 */
export class ApiError extends Error {
  readonly kind: ApiErrorKind;
  readonly status: number | null;
  readonly code: string | null;
  readonly details: unknown;
  readonly requestId: string | null;
  readonly payload: ApiErrorPayload | null;

  constructor(
    message: string,
    options: {
      kind: ApiErrorKind;
      status?: number | null;
      code?: string | null;
      details?: unknown;
      requestId?: string | null;
      payload?: ApiErrorPayload | null;
      cause?: unknown;
    },
  ) {
    super(message, options.cause !== undefined ? { cause: options.cause } : undefined);
    this.name = "ApiError";
    this.kind = options.kind;
    this.status = options.status ?? null;
    this.code = options.code ?? null;
    this.details = options.details ?? null;
    this.requestId = options.requestId ?? null;
    this.payload = options.payload ?? null;
  }
}

/** Map HTTP status to a stable error kind. */
export function kindFromStatus(status: number): ApiErrorKind {
  if (status === 401) return "unauthorized";
  if (status === 403) return "forbidden";
  if (status === 404) return "not_found";
  if (status === 408 || status === 504) return "timeout";
  if (status === 400 || status === 409 || status === 422) return "validation";
  if (status >= 500) return "server";
  return "unknown";
}

/** User-facing Vietnamese message for UI gates. */
export function apiErrorUserMessage(error: ApiError): string {
  switch (error.kind) {
    case "validation":
      return error.message || "Dữ liệu không hợp lệ.";
    case "unauthorized":
      return "Phiên đăng nhập hết hạn hoặc chưa xác thực.";
    case "forbidden":
      return "Bạn không có quyền thực hiện thao tác này.";
    case "not_found":
      return "Không tìm thấy dữ liệu yêu cầu.";
    case "timeout":
      return "Yêu cầu hết thời gian chờ. Vui lòng thử lại.";
    case "network":
      return "Không kết nối được máy chủ. Kiểm tra mạng và thử lại.";
    case "server":
      return error.message || "Lỗi máy chủ. Vui lòng thử lại sau.";
    default:
      return error.message || "Đã xảy ra lỗi không xác định.";
  }
}

export function isApiError(value: unknown): value is ApiError {
  return value instanceof ApiError;
}
