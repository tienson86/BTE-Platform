import type { ReactNode } from "react";

import { FIVE_ELEMENTS } from "../catalog";
import { PREVIEW_FIVE_ELEMENTS } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

/**
 * Ngũ Hành — chart area + five labeled meters. No engine values.
 */
export function FiveElementsPanel({ preview }: { preview: boolean }): ReactNode {
  return (
    <div className="bte-rw-panel" data-shell="five-elements">
      <div className="bte-rw-chart" data-slot="five-elements-chart" aria-hidden="true">
        {FIVE_ELEMENTS.map((el) => {
          const pct = preview ? PREVIEW_FIVE_ELEMENTS[el.id] : 12;
          return (
            <span
              key={el.id}
              className={`bte-rw-chart__col bte-rw-chart__col--${el.id}`}
              style={{ height: `${preview ? pct : 18}%` }}
              title={el.name}
            />
          );
        })}
      </div>
      <ul className="bte-rw-list">
        {FIVE_ELEMENTS.map((el) => (
          <li
            key={el.id}
            className="bte-rw-row"
            data-slot="five-element"
            data-element={el.id}
          >
            <span className={`bte-rw-swatch bte-rw-swatch--${el.id}`} aria-hidden="true" />
            <span className="bte-rw-label">{el.name}</span>
            <VisualMeter
              label={`${el.name} tỷ lệ`}
              preview={preview}
              value={PREVIEW_FIVE_ELEMENTS[el.id]}
              tone={el.id}
            />
            <span className="bte-rw-secondary">
              <SlotValue
                preview={preview}
                value={`${PREVIEW_FIVE_ELEMENTS[el.id]}%`}
              />
            </span>
          </li>
        ))}
      </ul>
      <p className="bte-rw-caption" data-slot="five-elements-note">
        <SlotValue preview={preview} value={PREVIEW_FIVE_ELEMENTS.observation} />
      </p>
    </div>
  );
}
