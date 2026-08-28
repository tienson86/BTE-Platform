import type { ReactNode } from "react";

import { Badge } from "../../../components/base/Badge";
import type { WorkspaceOverviewView } from "../adapter/types";
import { OVERVIEW_SLOTS } from "../catalog";
import { PREVIEW_OVERVIEW } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

const PREVIEW_MAP = {
  strength: PREVIEW_OVERVIEW.strength,
  "useful-god": PREVIEW_OVERVIEW.usefulGod,
  "favorable-god": PREVIEW_OVERVIEW.favorableGod,
  "avoid-god": PREVIEW_OVERVIEW.avoidGod,
} as const;

const PILL_SLOTS = OVERVIEW_SLOTS.filter((slot) => slot.id !== "strength");

/**
 * Tổng quan lá số — Strength primary, Useful God / Hỷ / Kỵ as compact pills.
 */
export function OverviewPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceOverviewView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const values = {
    strength: preview ? PREVIEW_MAP.strength : model?.strength.value,
    "useful-god": preview ? PREVIEW_MAP["useful-god"] : model?.usefulGod.value,
    "favorable-god": preview ? PREVIEW_MAP["favorable-god"] : model?.favorableGod.value,
    "avoid-god": preview ? PREVIEW_MAP["avoid-god"] : model?.avoidGod.value,
  } as const;
  const score = preview ? PREVIEW_OVERVIEW.score : model?.overallScore.value;
  const scoreMax = preview ? PREVIEW_OVERVIEW.scoreMax : model?.overallScoreMax ?? 100;
  const scoreLabel =
    typeof score === "number" ? `${score} / ${scoreMax}` : undefined;
  const confidence = preview ? PREVIEW_OVERVIEW.confidence : model?.confidence.value;
  return (
    <div className="bte-rw-panel bte-rw-panel--overview" data-shell="overview">
      <div className="bte-rw-overview__hero" data-slot="strength">
        <span className="bte-rw-label">{OVERVIEW_SLOTS[0].label}</span>
        <p className="bte-rw-primary bte-rw-primary--xl">
          <SlotValue preview={preview} bound={bound} value={values.strength} />
        </p>
      </div>
      <ul className="bte-rw-pills">
        {PILL_SLOTS.map((slot) => (
          <li key={slot.id} className="bte-rw-stat" data-slot={slot.id}>
            <span className="bte-rw-label">{slot.label}</span>
            <span className="bte-rw-pill">
              <SlotValue preview={preview} bound={bound} value={values[slot.id]} />
            </span>
          </li>
        ))}
      </ul>
      <div className="bte-rw-score" data-slot="overview-score">
        <div className="bte-rw-score__head">
          <span className="bte-rw-label">Điểm tổng quan</span>
          <span className="bte-rw-secondary">
            <SlotValue preview={preview} bound={bound} value={scoreLabel} />
          </span>
        </div>
        <VisualMeter
          label="Điểm tổng quan"
          preview={preview}
          bound={bound}
          value={score}
          max={scoreMax}
        />
      </div>
      <div className="bte-rw-inline" data-slot="overview-confidence">
        <span className="bte-rw-label">Độ tin cậy</span>
        {confidence ? (
          <Badge tone="success">{confidence}</Badge>
        ) : (
          <SlotValue preview={false} bound={false} />
        )}
      </div>
    </div>
  );
}
