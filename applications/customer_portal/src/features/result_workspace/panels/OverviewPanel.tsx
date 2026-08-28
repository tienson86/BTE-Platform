import type { ReactNode } from "react";

import { Badge } from "../../../components/base/Badge";
import { OVERVIEW_SLOTS } from "../catalog";
import { PREVIEW_OVERVIEW } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

const PREVIEW_MAP = {
  strength: PREVIEW_OVERVIEW.strength,
  "useful-god": PREVIEW_OVERVIEW.usefulGod,
  "favorable-god": PREVIEW_OVERVIEW.favorableGod,
  "avoid-god": PREVIEW_OVERVIEW.avoidGod,
} as const;

/**
 * Tổng quan lá số — visual shell for strength / useful / hỷ / kỵ / score.
 */
export function OverviewPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="overview">
      <ul className="bte-rw-stat-grid">
        {OVERVIEW_SLOTS.map((slot) => (
          <li key={slot.id} className="bte-rw-stat" data-slot={slot.id}>
            <span className="bte-rw-label">{slot.label}</span>
            <span className="bte-rw-primary">
              <SlotValue preview={preview} value={PREVIEW_MAP[slot.id]} />
            </span>
          </li>
        ))}
      </ul>
      <div className="bte-rw-score" data-slot="overview-score">
        <div className="bte-rw-score__head">
          <span className="bte-rw-label">Điểm tổng quan</span>
          <span className="bte-rw-primary">
            <SlotValue
              preview={preview}
              value={`${PREVIEW_OVERVIEW.score} / ${PREVIEW_OVERVIEW.scoreMax}`}
            />
          </span>
        </div>
        <VisualMeter
          label="Điểm tổng quan"
          preview={preview}
          value={PREVIEW_OVERVIEW.score}
          max={PREVIEW_OVERVIEW.scoreMax}
        />
      </div>
      <div className="bte-rw-inline" data-slot="overview-confidence">
        <span className="bte-rw-label">Độ tin cậy</span>
        {preview ? (
          <Badge tone="success">{PREVIEW_OVERVIEW.confidence}</Badge>
        ) : (
          <SlotValue preview={false} />
        )}
      </div>
    </div>
  );
}
