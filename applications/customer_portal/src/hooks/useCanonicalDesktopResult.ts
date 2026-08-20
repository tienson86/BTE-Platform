/**
 * Canonical Desktop data hook — AnalyzeService → adapter → ViewModel.
 */

import { useMemo } from "react";
import {
  createCanonicalDesktopGateViewModel,
  createCanonicalDesktopMockViewModel,
  type CanonicalDesktopViewModel,
} from "../adapters";
import type { AnalyzeChartRequest } from "../models";
import { getAnalyzeService } from "../services";
import { useAsyncResource } from "./useAsyncResource";

export type UseCanonicalDesktopResultOptions = {
  readonly request?: AnalyzeChartRequest | null;
  readonly enabled?: boolean;
  /** Injected ViewModel skips network (tests / frozen preview). */
  readonly initialData?: CanonicalDesktopViewModel;
  /** When no request: use fixture preview instead of empty gate. */
  readonly previewFallback?: boolean;
};

export type UseCanonicalDesktopResultResult = {
  readonly viewModel: CanonicalDesktopViewModel;
  readonly loading: boolean;
  readonly errorMessage: string | null;
  readonly reload: () => void;
};

function requestKey(request: AnalyzeChartRequest | null | undefined): string {
  if (!request) return "";
  return [
    request.year,
    request.month,
    request.day,
    request.hour ?? 0,
    request.minute ?? 0,
    request.gender ?? "",
    request.full_name ?? "",
    request.customer_id ?? "",
  ].join("|");
}

/**
 * Load Canonical Desktop ViewModel from Orchestrator POST /analyze.
 */
export function useCanonicalDesktopResult(
  options: UseCanonicalDesktopResultOptions = {},
): UseCanonicalDesktopResultResult {
  const {
    request = null,
    enabled = true,
    initialData,
    previewFallback = false,
  } = options;

  const asyncState = useAsyncResource(
    () => {
      if (!request) {
        return Promise.reject(new Error("Thiếu thông tin ngày giờ sinh để phân tích."));
      }
      return getAnalyzeService().getCanonicalDesktopViewModel(request);
    },
    {
      enabled: enabled && !initialData && Boolean(request),
      dependencyKey: requestKey(request),
    },
  );

  const viewModel = useMemo((): CanonicalDesktopViewModel => {
    if (initialData) {
      return initialData;
    }
    if (!request) {
      return previewFallback
        ? createCanonicalDesktopMockViewModel()
        : createCanonicalDesktopGateViewModel(
            "empty",
            "Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.",
          );
    }
    if (asyncState.status === "loading" || asyncState.status === "idle") {
      return createCanonicalDesktopGateViewModel("loading");
    }
    if (asyncState.status === "error") {
      return createCanonicalDesktopGateViewModel(
        "error",
        asyncState.errorMessage ?? "Không tải được kết quả.",
      );
    }
    return asyncState.data ?? createCanonicalDesktopGateViewModel(
      "error",
      asyncState.errorMessage ?? "Không tải được kết quả.",
    );
  }, [
    initialData,
    request,
    previewFallback,
    asyncState.status,
    asyncState.data,
    asyncState.errorMessage,
  ]);

  return {
    viewModel,
    loading: Boolean(request) && !initialData && asyncState.status === "loading",
    errorMessage: asyncState.errorMessage,
    reload: asyncState.reload,
  };
}
