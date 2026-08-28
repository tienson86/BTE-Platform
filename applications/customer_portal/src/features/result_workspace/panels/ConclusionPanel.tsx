import type { ReactNode } from "react";

import { Chip } from "../../../components/base/Chip";
import type { WorkspaceConclusionView } from "../adapter/types";
import { ACTION_CHIPS } from "../catalog";
import { PREVIEW_CONCLUSION } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Kết Luận & Hành Động — canonical conclusion only. Action chips stay unpublished.
 */
export function ConclusionPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceConclusionView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const chips = preview
    ? ACTION_CHIPS.map((chip) => ({ ...chip, available: true }))
    : model?.actions ?? ACTION_CHIPS.map((chip) => ({ ...chip, available: false }));
  return (
    <div className="bte-rw-panel" data-shell="conclusion">
      <div className="bte-rw-stat" data-slot="conclusion-overall">
        <span className="bte-rw-label">Kết luận</span>
        <p className="bte-rw-prose bte-rw-prose--lead">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? PREVIEW_CONCLUSION.overall : model?.overall.value}
          />
        </p>
      </div>
      <div className="bte-rw-stat" data-slot="conclusion-action">
        <span className="bte-rw-label">Hành động</span>
        <p className="bte-rw-caption">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? "" : model?.action.value}
          />
        </p>
      </div>
      <div data-slot="conclusion-actions">
        <span className="bte-rw-label">Ưu tiên hành động</span>
        <div className="bte-rw-chips">
          {chips.map((chip) => (
            <Chip
              key={chip.id}
              className="bte-rw-chip"
              data-slot="action-chip"
              data-action={chip.id}
              data-unavailable={chip.available ? "false" : "true"}
            >
              {chip.label}
            </Chip>
          ))}
        </div>
      </div>
    </div>
  );
}
