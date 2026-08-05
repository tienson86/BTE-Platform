/**
 * Dashboard data hook (TASK_003A).
 */

import { useMemo } from "react";
import { adaptDashboardViewModel, type DashboardViewModel } from "../adapters";
import { getDashboardService } from "../services";
import { useAsyncResource } from "./useAsyncResource";

export type UseDashboardOptions = {
  readonly enabled?: boolean;
  readonly initialData?: DashboardViewModel;
};

export type UseDashboardResult = {
  readonly viewModel: DashboardViewModel;
  readonly loading: boolean;
  readonly errorMessage: string | null;
  readonly reload: () => void;
};

/**
 * Load Dashboard ViewModel via DashboardService.
 */
export function useDashboard(options: UseDashboardOptions = {}): UseDashboardResult {
  const { enabled = true, initialData } = options;

  const asyncState = useAsyncResource(() => getDashboardService().getViewModel(), {
    enabled: enabled && !initialData,
    dependencyKey: "dashboard",
  });

  const viewModel = useMemo((): DashboardViewModel => {
    if (initialData) {
      return initialData;
    }
    if (asyncState.data) {
      return asyncState.data;
    }
    return adaptDashboardViewModel({});
  }, [initialData, asyncState.data]);

  return {
    viewModel,
    loading: !initialData && asyncState.status === "loading",
    errorMessage: asyncState.errorMessage,
    reload: asyncState.reload,
  };
}
