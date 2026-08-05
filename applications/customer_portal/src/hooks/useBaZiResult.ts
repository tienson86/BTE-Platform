/**
 * BaZi Result data hook — Service → Adapter → ViewModel (TASK_003A).
 */

import { useMemo } from "react";
import {
  createBaZiResultGateViewModel,
  type BaZiResultViewModel,
} from "../adapters";
import type { AnalyzeChartRequest } from "../models";
import { getAnalyzeService } from "../services";
import { useAsyncResource } from "./useAsyncResource";

export type UseBaZiResultOptions = {
  readonly request?: AnalyzeChartRequest | null;
  readonly enabled?: boolean;
  /** Injected ViewModel skips network (tests / story). */
  readonly initialData?: BaZiResultViewModel;
};

export type UseBaZiResultResult = {
  readonly viewModel: BaZiResultViewModel;
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
 * Load BaZi Result ViewModel via AnalyzeService.
 */
export function useBaZiResult(options: UseBaZiResultOptions = {}): UseBaZiResultResult {
  const { request = null, enabled = true, initialData } = options;

  const asyncState = useAsyncResource(
    () => {
      if (!request) {
        return Promise.reject(new Error("Thiếu thông tin ngày giờ sinh để phân tích."));
      }
      return getAnalyzeService().getBaZiResultViewModel(request);
    },
    {
      enabled: enabled && !initialData && Boolean(request),
      dependencyKey: requestKey(request),
    },
  );

  const viewModel = useMemo((): BaZiResultViewModel => {
    if (initialData) {
      return initialData;
    }
    if (asyncState.status === "loading" || asyncState.status === "idle") {
      if (!request && enabled) {
        return createBaZiResultGateViewModel(
          "empty",
          "Nhập thông tin ngày giờ sinh để xem kết quả phân tích.",
        );
      }
      return createBaZiResultGateViewModel("loading");
    }
    if (asyncState.status === "error") {
      return createBaZiResultGateViewModel(
        "error",
        asyncState.errorMessage ?? "Không tải được kết quả.",
      );
    }
    return asyncState.data ?? createBaZiResultGateViewModel("empty");
  }, [
    initialData,
    asyncState.status,
    asyncState.data,
    asyncState.errorMessage,
    request,
    enabled,
  ]);

  return {
    viewModel,
    loading: !initialData && asyncState.status === "loading",
    errorMessage: asyncState.errorMessage,
    reload: asyncState.reload,
  };
}
