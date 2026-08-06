/**
 * S07 — THẦN SÁT
 * Isolated rebuild: Executive Summary of Shen Sha.
 * knowledge/ui_master/sections/S07_SHEN_SHA/
 * + CANONICAL_PORTAL_UI_DESKTOP_V1.png
 *
 * NOT a dashboard / KPI / chart / analytics panel.
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s07;

/**
 * S07 Shen Sha — Cát tinh / Hung tinh lists + footer summary + text link.
 */
export function S07ShenSha(): ReactNode {
  return (
    <section className="cd-s07" aria-labelledby="cd-s07-title">
      <div className="cd-s07__card">
        <h2 id="cd-s07-title" className="cd-s07__title">
          {data.title}
        </h2>

        <div className="cd-s07__exec">
          <p className="cd-s07__exec-line">{data.executive.line1}</p>
          <p className="cd-s07__exec-line">{data.executive.line2}</p>
        </div>

        <div className="cd-s07__group">
          <h3 className="cd-s07__group-title cd-s07__group-title--good">
            {data.good.title}
          </h3>
          <ul className="cd-s07__list">
            {data.good.items.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--good" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s07__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s07__divider" />

        <div className="cd-s07__group">
          <h3 className="cd-s07__group-title cd-s07__group-title--bad">
            {data.bad.title}
          </h3>
          <ul className="cd-s07__list">
            {data.bad.items.map((item) => (
              <li key={item} className="cd-s07__row">
                <span className="cd-s07__icon cd-s07__icon--bad" aria-hidden="true">
                  ✕
                </span>
                <span className="cd-s07__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s07__divider" />

        <div className="cd-s07__footer-summary">
          <p className="cd-s07__footer-line">{data.footerSummary.line1}</p>
          <p className="cd-s07__footer-line">{data.footerSummary.line2}</p>
        </div>

        <a className="cd-s07__link" href="#s07-detail">
          {data.link}
        </a>
      </div>
    </section>
  );
}
