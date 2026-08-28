import type { ReactNode } from "react";

import { SHEN_SHA_NAMES } from "../catalog";
import { PREVIEW_SHEN_SHA } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Thần Sát — compact name + presence list. No calculation.
 */
export function ShenShaPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="shen-sha">
      <ul className="bte-rw-list bte-rw-list--compact">
        {SHEN_SHA_NAMES.map((name) => (
          <li key={name} className="bte-rw-row" data-slot="shen-sha-row" data-name={name}>
            <span className="bte-rw-mark" aria-hidden="true">
              ✦
            </span>
            <span className="bte-rw-label">{name}</span>
            <span className="bte-rw-secondary">
              <SlotValue preview={preview} value={PREVIEW_SHEN_SHA[name]} />
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
