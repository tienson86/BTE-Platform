import type { ReactNode } from "react";

import type { WorkspaceShenShaView } from "../adapter/types";
import { SHEN_SHA_NAMES } from "../catalog";
import { PREVIEW_SHEN_SHA } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Thần Sát — published matches only. Catalog gaps stay empty, never fabricated.
 */
export function ShenShaPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceShenShaView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const rows = model?.rows ?? SHEN_SHA_NAMES.map((name) => ({
    name,
    presence: { value: null, available: false, source: "" },
    catalog: true,
  }));
  return (
    <div className="bte-rw-panel" data-shell="shen-sha">
      <ul className="bte-rw-list bte-rw-list--compact">
        {rows.map((row) => (
          <li key={row.name} className="bte-rw-row" data-slot="shen-sha-row" data-name={row.name}>
            <span className="bte-rw-mark" aria-hidden="true">
              ✦
            </span>
            <span className="bte-rw-label">{row.name}</span>
            <span className="bte-rw-secondary">
              <SlotValue
                preview={preview}
                bound={bound}
                value={preview ? PREVIEW_SHEN_SHA[row.name] : row.presence.value}
              />
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
