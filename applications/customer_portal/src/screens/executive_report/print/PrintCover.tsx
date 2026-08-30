/**
 * Print cover wrapper. Does not redesign cover content.
 */

import type { ReactNode } from "react";
import { ReportCover } from "../components/ReportCover";
import type { ReportCoverView } from "../reportModel";

type PrintCoverProps = {
  readonly model: ReportCoverView;
};

/**
 * Cover as print page 1. Reuses ReportCover fields only.
 */
export function PrintCover({ model }: PrintCoverProps): ReactNode {
  return (
    <div className="bte-print__cover" data-print="cover">
      <ReportCover model={model} />
    </div>
  );
}
