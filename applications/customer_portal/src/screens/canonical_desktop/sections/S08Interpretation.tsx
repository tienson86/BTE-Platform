/**
 * S08 — LUẬN GIẢI TỔNG HỢP
 * Isolated rebuild: Executive Interpretation Brief.
 * knowledge/ui_master/sections/S08_INTERPRETATION/
 * + CANONICAL_PORTAL_UI_DESKTOP_V1.png
 *
 * NOT a dashboard / KPI / analytics / rule viewer.
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s08;

/**
 * S08 Interpretation — executive summary + strengths + warnings + actions + link.
 */
export function S08Interpretation(): ReactNode {
  return (
    <section className="cd-s08" aria-labelledby="cd-s08-title">
      <div className="cd-s08__card">
        <h2 id="cd-s08-title" className="cd-s08__title">
          {data.title}
        </h2>

        <div className="cd-s08__exec">
          <h3 className="cd-s08__exec-title">{data.executive.title}</h3>
          <p className="cd-s08__exec-caption">
            Kết luận quan trọng nhất từ toàn bộ quá trình phân tích.
          </p>
          <p className="cd-s08__exec-body">{data.executive.body}</p>
        </div>

        <hr className="cd-s08__divider" />

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s08__list">
            {data.strengths.items.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s08__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s08__divider" />

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--warning">
            {data.warnings.title}
          </h3>
          <ul className="cd-s08__list">
            {data.warnings.items.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--warning" aria-hidden="true">
                  •
                </span>
                <span className="cd-s08__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s08__divider" />

        <div className="cd-s08__block">
          <h3 className="cd-s08__block-title cd-s08__block-title--action">
            {data.actions.title}
          </h3>
          <ul className="cd-s08__list">
            {data.actions.items.map((item) => (
              <li key={item} className="cd-s08__row">
                <span className="cd-s08__icon cd-s08__icon--action" aria-hidden="true">
                  →
                </span>
                <span className="cd-s08__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s08__divider" />

        <a className="cd-s08__link" href="#s08-detail">
          {data.link}
        </a>
      </div>
    </section>
  );
}
