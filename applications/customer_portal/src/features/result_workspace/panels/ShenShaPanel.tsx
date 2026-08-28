import type { ReactNode } from "react";

import type { WorkspaceShenShaView } from "../adapter/types";
import { SHEN_SHA_NAMES } from "../catalog";
import { PREVIEW_SHEN_SHA } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Thần Sát — published matches as tags. Catalog gaps stay empty, never "Không".
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
      <ul className="bte-rw-tags">
        {rows.map((row) => {
          const previewValue = PREVIEW_SHEN_SHA[row.name];
          const liveValue =
            row.presence.value && row.presence.value !== "Không" ? row.presence.value : null;
          const present = preview ? previewValue === "Có" : Boolean(liveValue);
          return (
            <li
              key={row.name}
              className="bte-rw-tag"
              data-slot="shen-sha-row"
              data-name={row.name}
              data-present={present ? "true" : "false"}
            >
              <span className="bte-rw-tag__name">{row.name}</span>
              <span className="bte-rw-tag__value">
                <SlotValue
                  preview={preview}
                  bound={bound}
                  value={preview ? (previewValue === "Không" ? null : previewValue) : liveValue}
                />
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
