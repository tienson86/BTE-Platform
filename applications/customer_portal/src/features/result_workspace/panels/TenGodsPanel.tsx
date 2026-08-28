import type { ReactNode } from "react";

import { TEN_GODS } from "../catalog";
import { PREVIEW_TEN_GODS } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

/**
 * Thập Thần — ten canonical rows with compact bar/value slots.
 */
export function TenGodsPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="ten-gods">
      <ul className="bte-rw-list bte-rw-list--compact">
        {TEN_GODS.map((name) => (
          <li key={name} className="bte-rw-row" data-slot="ten-god" data-god={name}>
            <span className="bte-rw-label">{name}</span>
            <VisualMeter label={name} preview={preview} value={PREVIEW_TEN_GODS[name]} />
            <span className="bte-rw-secondary">
              <SlotValue preview={preview} value={PREVIEW_TEN_GODS[name]} />
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
