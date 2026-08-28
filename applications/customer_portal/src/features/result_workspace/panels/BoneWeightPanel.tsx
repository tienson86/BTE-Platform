import type { ReactNode } from "react";

import { EMPTY_COPY } from "../catalog";
import { PREVIEW_BONE_WEIGHT } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Cân Xương Đoán Mệnh — amount, rating, classification, preview text.
 */
export function BoneWeightPanel({ preview }: { preview: boolean }): ReactNode {
  const stars = preview ? PREVIEW_BONE_WEIGHT.stars : 0;
  return (
    <div className="bte-rw-panel" data-shell="bone-weight">
      <p className="bte-rw-primary bte-rw-primary--xl" data-slot="bone-amount">
        <SlotValue preview={preview} value={PREVIEW_BONE_WEIGHT.amount} />
      </p>
      <p
        className="bte-rw-stars"
        data-slot="bone-rating"
        aria-label={preview ? `${stars} trên 5` : EMPTY_COPY}
      >
        {Array.from({ length: 5 }, (_, index) => (
          <span key={index} aria-hidden="true">
            {index < stars ? "★" : "☆"}
          </span>
        ))}
      </p>
      <div className="bte-rw-stat" data-slot="bone-class">
        <span className="bte-rw-label">Phân loại</span>
        <p className="bte-rw-secondary">
          <SlotValue preview={preview} value={PREVIEW_BONE_WEIGHT.classification} />
        </p>
      </div>
      <p className="bte-rw-caption" data-slot="bone-preview">
        <SlotValue preview={preview} value={PREVIEW_BONE_WEIGHT.preview} />
      </p>
    </div>
  );
}
