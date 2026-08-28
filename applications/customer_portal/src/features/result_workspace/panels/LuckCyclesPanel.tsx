import type { ReactNode } from "react";

import type { WorkspaceLuckView } from "../adapter/types";
import { PREVIEW_LUCK } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Đại Vận / Lưu Niên — published luck cycles in engine order.
 */
export function LuckCyclesPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceLuckView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const cycles = model?.cycles ?? [];
  const timeline = preview
    ? ["trước", "hiện tại", "sau"]
    : cycles.length > 0
      ? cycles.map((cycle) => cycle.ganZhi)
      : ["trước", "hiện tại", "sau"];
  const currentIndex = preview
    ? 1
    : cycles.findIndex((cycle) => cycle.current);
  return (
    <div className="bte-rw-panel" data-shell="luck-cycles">
      <div className="bte-rw-stat" data-slot="luck-current">
        <span className="bte-rw-label">Đại vận hiện tại</span>
        <p className="bte-rw-primary">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? PREVIEW_LUCK.current : model?.current.value}
          />
        </p>
      </div>
      <dl className="bte-rw-meta-grid">
        <div data-slot="luck-age">
          <dt className="bte-rw-label">Tuổi</dt>
          <dd className="bte-rw-secondary">
            <SlotValue
              preview={preview}
              bound={bound}
              value={preview ? PREVIEW_LUCK.ageRange : model?.ageRange.value}
            />
          </dd>
        </div>
        <div data-slot="luck-ganzhi">
          <dt className="bte-rw-label">Can Chi</dt>
          <dd className="bte-rw-secondary">
            <SlotValue
              preview={preview}
              bound={bound}
              value={preview ? PREVIEW_LUCK.ganzhi : model?.ganZhi.value}
            />
          </dd>
        </div>
        <div data-slot="luck-year">
          <dt className="bte-rw-label">Năm hiện tại</dt>
          <dd className="bte-rw-secondary">
            <SlotValue
              preview={preview}
              bound={bound}
              value={preview ? PREVIEW_LUCK.year : model?.currentYear.value}
            />
          </dd>
        </div>
      </dl>
      <div className="bte-rw-stat bte-rw-stat--secondary" data-slot="luck-liunian">
        <span className="bte-rw-label">Lưu niên</span>
        <p className="bte-rw-secondary">
          <SlotValue
            preview={preview}
            bound={bound}
            value={preview ? "" : model?.currentLiunian.value}
          />
        </p>
      </div>
      <ol className="bte-rw-timeline" data-slot="luck-timeline" aria-label="Mốc đại vận">
        {timeline.map((point, index) => (
          <li
            key={`${point}-${index}`}
            className={
              index === currentIndex
                ? "bte-rw-timeline__node bte-rw-timeline__node--now"
                : "bte-rw-timeline__node"
            }
          >
            <span className="bte-rw-caption">{point}</span>
          </li>
        ))}
      </ol>
      <p className="bte-rw-caption" data-slot="luck-note">
        <SlotValue
          preview={preview}
          bound={bound}
          value={preview ? PREVIEW_LUCK.observation : model?.observation.value}
        />
      </p>
    </div>
  );
}
