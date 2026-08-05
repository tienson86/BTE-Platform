/**
 * Shared async resource hook (loading / error / retry) — TASK_003A.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { ApiError, apiErrorUserMessage, isApiError } from "../api";

export type AsyncStatus = "idle" | "loading" | "success" | "error";

export type AsyncResourceState<T> = {
  readonly status: AsyncStatus;
  readonly data: T | null;
  readonly error: ApiError | null;
  readonly errorMessage: string | null;
  readonly reload: () => void;
};

function toApiError(error: unknown): ApiError {
  if (isApiError(error)) {
    return error;
  }
  if (error instanceof Error) {
    return new ApiError(error.message, { kind: "unknown", cause: error });
  }
  return new ApiError("Unknown error", { kind: "unknown", cause: error });
}

/**
 * Load a resource with loading / error / retry semantics.
 */
export function useAsyncResource<T>(
  loader: () => Promise<T>,
  options: {
    readonly enabled?: boolean;
    /** Re-run when this key changes. */
    readonly dependencyKey?: string;
  } = {},
): AsyncResourceState<T> {
  const enabled = options.enabled ?? true;
  const dependencyKey = options.dependencyKey ?? "";
  const [status, setStatus] = useState<AsyncStatus>(enabled ? "loading" : "idle");
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [tick, setTick] = useState(0);
  const loaderRef = useRef(loader);
  loaderRef.current = loader;

  const reload = useCallback(() => {
    setTick((value) => value + 1);
  }, []);

  useEffect(() => {
    if (!enabled) {
      setStatus("idle");
      return;
    }

    let cancelled = false;
    setStatus("loading");
    setError(null);

    void loaderRef
      .current()
      .then((result) => {
        if (cancelled) return;
        setData(result);
        setStatus("success");
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        const apiError = toApiError(err);
        setError(apiError);
        setStatus("error");
      });

    return () => {
      cancelled = true;
    };
  }, [enabled, dependencyKey, tick]);

  return {
    status,
    data,
    error,
    errorMessage: error ? apiErrorUserMessage(error) : null,
    reload,
  };
}
