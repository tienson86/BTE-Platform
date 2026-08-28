import type { ReactNode } from "react";

import { Chip } from "../../../components/base/Chip";
import { ACTION_CHIPS } from "../catalog";
import { PREVIEW_CONCLUSION } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Kết Luận & Hành Động — conclusion + category chips. No generated advice.
 */
export function ConclusionPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="conclusion">
      <div className="bte-rw-stat" data-slot="conclusion-overall">
        <span className="bte-rw-label">Kết luận</span>
        <p className="bte-rw-caption">
          <SlotValue preview={preview} value={PREVIEW_CONCLUSION.overall} />
        </p>
      </div>
      <div data-slot="conclusion-actions">
        <span className="bte-rw-label">Ưu tiên hành động</span>
        <div className="bte-rw-chips">
          {ACTION_CHIPS.map((chip) => (
            <Chip
              key={chip.id}
              className="bte-rw-chip"
              data-slot="action-chip"
              data-action={chip.id}
            >
              {chip.label}
            </Chip>
          ))}
        </div>
      </div>
    </div>
  );
}
