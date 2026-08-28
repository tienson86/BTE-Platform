import type { ReactNode } from "react";

import type { WorkspaceTenGodsView } from "../adapter/types";
import { TEN_GODS } from "../catalog";
import { PREVIEW_TEN_GODS } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

/**
 * Thập Thần — counts of published canonical labels. No score-engine series.
 */
export function TenGodsPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceTenGodsView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const maxBound = Math.max(
    1,
    ...(model?.rows ?? []).map((row) => row.count.value ?? 0),
  );
  return (
    <div className="bte-rw-panel" data-shell="ten-gods">
      <ul className="bte-rw-list bte-rw-list--compact">
        {TEN_GODS.map((name, index) => {
          const count = preview ? PREVIEW_TEN_GODS[name] : model?.rows[index]?.count.value;
          const meterMax = preview ? 100 : maxBound;
          return (
            <li key={name} className="bte-rw-row" data-slot="ten-god" data-god={name}>
              <span className="bte-rw-label">{name}</span>
              <VisualMeter
                label={name}
                preview={preview}
                bound={bound}
                value={count}
                max={meterMax}
              />
              <span className="bte-rw-secondary">
                <SlotValue preview={preview} bound={bound} value={count} />
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
