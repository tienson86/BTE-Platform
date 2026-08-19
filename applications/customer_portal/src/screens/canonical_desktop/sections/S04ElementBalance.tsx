/**
 * S04 — PHÂN BỐ NGŨ HÀNH
 * Structural occurrence bars. Count is the fact; no strength/balance labels.
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

const ELEMENT_CLASS: Record<string, string> = {
  wood: "cd-s04__bar-fill--wood",
  fire: "cd-s04__bar-fill--fire",
  earth: "cd-s04__bar-fill--earth",
  metal: "cd-s04__bar-fill--metal",
  water: "cd-s04__bar-fill--water",
};

/**
 * S04 Five Elements distribution — five count rows + provenance.
 */
export function S04ElementBalance(): ReactNode {
  const data = useCanonicalDesktop().s04;
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
                aria-label={`${row.name} ${row.count}${row.status ? ` — ${row.status}` : ""}`}
                aria-valuenow={row.count}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <span
                  className={`cd-s04__bar-fill ${ELEMENT_CLASS[row.element] ?? ""}`}
                  style={{ width: `${row.pct}%` }}
                />
              </div>
              <span className="cd-s04__pct">{row.count}</span>
              {row.status ? <span className="cd-s04__status">{row.status}</span> : null}
            </li>
          ))}
        </ul>

        {data.summary ? <p className="cd-s04__summary">{data.summary}</p> : null}
      </div>
    </section>
  );
}
