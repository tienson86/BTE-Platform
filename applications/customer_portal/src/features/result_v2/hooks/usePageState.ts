/**
 * Page state overlay (printing / exporting reserved) over adapter output.
 */

import { useMemo } from "react";
import type { PageState, PortalResultModel } from "../adapter/PortalResultModel";

export function usePageState(
  model: PortalResultModel,
  overlay: { printing?: boolean; exporting?: boolean } = {},
): PageState {
  return useMemo(() => {
    if (overlay.printing) return "printing";
    if (overlay.exporting) return "exporting";
    return model.page.state;
  }, [model.page.state, overlay.printing, overlay.exporting]);
}
