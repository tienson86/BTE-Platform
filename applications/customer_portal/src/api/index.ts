/**
 * API layer barrel (TASK_003A).
 */

export { ApiClient, getApiClient, resetApiClient } from "./client";
export { API_ENDPOINTS } from "./endpoints";
export type { ApiEndpointKey } from "./endpoints";
export {
  ApiError,
  apiErrorUserMessage,
  isApiError,
  kindFromStatus,
} from "./errors";
export type { ApiErrorKind, ApiErrorPayload } from "./errors";
export type {
  ApiClientConfig,
  ApiEnvelope,
  ApiRequestOptions,
  HttpMethod,
} from "./types";
