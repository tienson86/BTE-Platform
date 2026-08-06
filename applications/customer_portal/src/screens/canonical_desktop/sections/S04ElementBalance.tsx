/**
 * S04 — CÂN BẰNG NGŨ HÀNH
 * Isolated rebuild from CANONICAL_PORTAL_UI_DESKTOP_V1.png
 * + knowledge/ui_master/master_sections/S04_ELEMENT_BALANCE/
 *
 * Horizontal bars only. No pie / donut / gauge.
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s04;

const ELEMENT_CLASS: Record<string, string> = {
  wood: "cd-s04__bar-fill--wood",
  fire: "cd-s04__bar-fill--fire",
  earth: "cd-s04__bar-fill--earth",
  metal: "cd-s04__bar-fill--metal",
  water: "cd-s04__bar-fill--water",
};

/**
 * Map status label to semantic color modifier.
 */
function statusModifier(status: string): string {
  if (status === "Rất mạnh" || status === "Mạnh") return "cd-s04__status--strong";
  if (status === "Trung bình") return "cd-s04__status--medium";
  if (status === "Yếu") return "cd-s04__status--weak";
  if (status === "Rất yếu") return "cd-s04__status--very-weak";
  return "";
}

/**
 * S04 Element Balance — five proportional rows + one summary line.
 */
export function S04ElementBalance(): ReactNode {
  return (
    <section className="cd-s04" aria-labelledby="cd-s04-title">
      <div className="cd-s04__card">
        <h2 id="cd-s04-title" className="cd-s04__title">
          {data.title}
        </h2>

        <ul className="cd-s04__list">
          {data.rows.map((row) => (
            <li key={row.name} className="cd-s04__row">
              <span className="cd-s04__name">{row.name}</span>
              <div
                className="cd-s04__track"
                role="meter"
                aria-label={`${row.name} ${row.pct}% — ${row.status}`}
                aria-valuenow={row.pct}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <span
                  className={`cd-s04__bar-fill ${ELEMENT_CLASS[row.element] ?? ""}`}
                  style={{ width: `${row.pct}%` }}
                />
              </div>
              <span className="cd-s04__pct">{row.pct}%</span>
              <span className={`cd-s04__status ${statusModifier(row.status)}`}>
                {row.status}
              </span>
            </li>
          ))}
        </ul>

        <p className="cd-s04__summary">{data.summary}</p>
      </div>
    </section>
  );
}
