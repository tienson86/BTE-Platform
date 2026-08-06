/**
 * S06 — THẬP THẦN
 * Isolated rebuild: Quick Recognition Panel (2×5 grid).
 * PATTERN_03_DATA_COLUMNS + PATTERN_06_INFORMATION_LIST
 * + CANONICAL_PORTAL_UI_DESKTOP_V1.png
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s06;

/**
 * S06 Ten Gods — 10 equal cells, fixed order, scan in under 5 seconds.
 */
export function S06TenGods(): ReactNode {
  return (
    <section className="cd-s06" aria-labelledby="cd-s06-title">
      <div className="cd-s06__card">
        <h2 id="cd-s06-title" className="cd-s06__title">
          {data.title}
        </h2>

        <div className="cd-s06__scroll">
          <ul className="cd-s06__grid">
            {data.gods.map((god) => (
              <li key={god.name} className="cd-s06__cell" aria-label={`${god.name} ${god.score}`}>
                <span
                  className="cd-s06__dot"
                  style={{ background: god.color }}
                  aria-hidden="true"
                />
                <span className="cd-s06__short">{god.name}</span>
                <span className="cd-s06__score">{god.score}</span>
              </li>
            ))}
          </ul>
        </div>

        <a className="cd-s06__link" href="#s06-detail">
          {data.link}
        </a>
      </div>
    </section>
  );
}
