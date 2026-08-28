import type { ReactNode } from "react";

import { PREVIEW_LUCK } from "../previewFixture";
import { SlotValue } from "./slots";

/**
 * Đại Vận / Lưu Niên — timeline shell only. No luck or year calculation.
 */
export function LuckCyclesPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="luck-cycles">
      <div className="bte-rw-stat" data-slot="luck-current">
        <span className="bte-rw-label">Đại vận hiện tại</span>
        <p className="bte-rw-primary">
          <SlotValue preview={preview} value={PREVIEW_LUCK.current} />
        </p>
      </div>
      <dl className="bte-rw-meta-grid">
        <div data-slot="luck-age">
          <dt className="bte-rw-label">Tuổi</dt>
          <dd className="bte-rw-secondary">
            <SlotValue preview={preview} value={PREVIEW_LUCK.ageRange} />
          </dd>
        </div>
        <div data-slot="luck-ganzhi">
          <dt className="bte-rw-label">Can Chi</dt>
          <dd className="bte-rw-secondary">
            <SlotValue preview={preview} value={PREVIEW_LUCK.ganzhi} />
          </dd>
        </div>
        <div data-slot="luck-year">
          <dt className="bte-rw-label">Năm hiện tại</dt>
          <dd className="bte-rw-secondary">
            <SlotValue preview={preview} value={PREVIEW_LUCK.year} />
          </dd>
        </div>
      </dl>
      <ol className="bte-rw-timeline" data-slot="luck-timeline" aria-label="Mốc đại vận">
        {["trước", "hiện tại", "sau"].map((point, index) => (
          <li
            key={point}
            className={index === 1 ? "bte-rw-timeline__node bte-rw-timeline__node--now" : "bte-rw-timeline__node"}
          >
            <span className="bte-rw-caption">{point}</span>
          </li>
        ))}
      </ol>
      <p className="bte-rw-caption" data-slot="luck-note">
        <SlotValue preview={preview} value={PREVIEW_LUCK.observation} />
      </p>
    </div>
  );
}
