import type { ReactNode } from "react";

import type { WorkspaceFiveElementsView } from "../adapter/types";
import { FIVE_ELEMENTS } from "../catalog";
import { PREVIEW_FIVE_ELEMENTS } from "../previewFixture";
import { SlotValue, VisualMeter } from "./slots";

/**
 * Ngũ Hành — analytical five_elements counts. Percents are presentation-only.
 */
export function FiveElementsPanel({
  preview,
  model,
}: {
  preview: boolean;
  model?: WorkspaceFiveElementsView;
}): ReactNode {
  const bound = Boolean(model) && !preview;
  const publishedPercents = (model?.rows ?? [])
    .map((row) => row.percent.value)
    .filter((value): value is number => typeof value === "number");
  const peak = publishedPercents.length ? Math.max(...publishedPercents) : null;
  return (
    <div className="bte-rw-panel" data-shell="five-elements">
      <div className="bte-rw-chart" data-slot="five-elements-chart" aria-hidden="true">
        {FIVE_ELEMENTS.map((el, index) => {
          const pct = preview
            ? PREVIEW_FIVE_ELEMENTS[el.id]
            : model?.rows[index]?.percent.value ?? 0;
          const ready = preview || model?.rows[index]?.percent.available;
          return (
            <span
              key={el.id}
              className={`bte-rw-chart__col bte-rw-chart__col--${el.id}`}
              style={{ height: ready ? `${pct}%` : "8px" }}
              title={el.name}
            />
          );
        })}
      </div>
      <ul className="bte-rw-list">
        {FIVE_ELEMENTS.map((el, index) => {
          const row = model?.rows[index];
          const pct = preview ? PREVIEW_FIVE_ELEMENTS[el.id] : row?.percent.value;
          const emphasize =
            !preview && peak != null && typeof pct === "number" && pct === peak && peak > 0;
          return (
            <li
              key={el.id}
              className="bte-rw-row"
              data-slot="five-element"
              data-element={el.id}
              data-emphasis={emphasize ? "high" : undefined}
            >
              <span className={`bte-rw-swatch bte-rw-swatch--${el.id}`} aria-hidden="true" />
              <span className="bte-rw-label">{el.name}</span>
              <VisualMeter
                label={`${el.name} tỷ lệ`}
                preview={preview}
                bound={bound}
                value={pct}
                tone={el.id}
              />
              <span className="bte-rw-secondary">
                <SlotValue
                  preview={preview}
                  bound={bound}
                  value={typeof pct === "number" ? `${pct}%` : null}
                />
              </span>
            </li>
          );
        })}
      </ul>
      <p className="bte-rw-caption" data-slot="five-elements-note">
        <SlotValue
          preview={preview}
          bound={bound}
          value={preview ? PREVIEW_FIVE_ELEMENTS.observation : model?.observation.value}
        />
      </p>
    </div>
  );
}
