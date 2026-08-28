import type { ReactNode } from "react";

import { EMPTY_COPY } from "../catalog";
import type { WorkspaceBoneWeightView } from "../adapter/types";
import { PREVIEW_BONE_WEIGHT } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Cân Xương Đoán Mệnh — published bone_weight only. No year/month/day lookup.
 */
export function BoneWeightPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceBoneWeightView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const stars = preview ? PREVIEW_BONE_WEIGHT.stars : 0;
  const rated = preview;
  return (
    <div className="bte-rw-panel" data-shell="bone-weight">
      <p className="bte-rw-primary bte-rw-primary--xl" data-slot="bone-amount">
        <SlotValue
          preview={preview}
          bound={bound}
          value={preview ? PREVIEW_BONE_WEIGHT.amount : model?.amount.value}
        />
      </p>
      <p
        className="bte-rw-stars"
        data-slot="bone-rating"
        aria-label={rated ? `${stars} trên 5` : EMPTY_COPY}
        data-empty={rated ? "false" : "true"}
      >
        {Array.from({ length: 5 }, (_, index) => (
          <span key={index} aria-hidden="true">
            {rated && index < stars ? "★" : "☆"}
          </span>
        ))}
      </p>
      <div className="bte-rw-stat" data-slot="bone-class">
        <span className="bte-rw-label">Phân loại</span>
        <p className="bte-rw-secondary">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? PREVIEW_BONE_WEIGHT.classification : model?.classification.value}
          />
        </p>
      </div>
      <p className="bte-rw-caption" data-slot="bone-preview">
        <SlotValue
          preview={preview}
          bound={bound}
          value={preview ? PREVIEW_BONE_WEIGHT.preview : model?.interpretation.value}
        />
      </p>
    </div>
  );
}
