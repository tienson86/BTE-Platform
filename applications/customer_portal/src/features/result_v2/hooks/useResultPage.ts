/**
 * Receive Report → adapter → PortalResultModel + expand helpers.
 */

import { useCallback, useMemo } from "react";
import { adaptPortalResult } from "../adapter/portalPresentationAdapter";
import type { PortalResultModel } from "../adapter/PortalResultModel";
import type { AdapterOptions, CanonicalReportInput } from "../adapter/reportInput";
import { useExpand } from "./useExpand";
import { usePageState } from "./usePageState";

export type UseResultPageArgs = {
  report?: CanonicalReportInput | null;
  loading?: boolean;
  offline?: boolean;
  printing?: boolean;
  exporting?: boolean;
};

export function useResultPage(args: UseResultPageArgs) {
  const options: AdapterOptions = {
    loading: args.loading === true,
    offline: args.offline === true,
    printing: args.printing === true,
    exporting: args.exporting === true,
  };

  const model: PortalResultModel = useMemo(
    () => adaptPortalResult(args.report ?? null, options),
    [args.report, options.loading, options.offline, options.printing, options.exporting],
  );

  const pageState = usePageState(model, {
    printing: args.printing,
    exporting: args.exporting,
  });

  // Expand chart fundamentals (and narrative sections) on first paint.
  const expand = useExpand({
    "section:technical": true,
    "section:knowledge": true,
  });

  const onNavigate = useCallback((targetUiId: string) => {
    const node = document.getElementById(`rv2-${targetUiId}`);
    node?.focus?.();
    node?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, []);

  return { model, pageState, expand, onNavigate };
}
