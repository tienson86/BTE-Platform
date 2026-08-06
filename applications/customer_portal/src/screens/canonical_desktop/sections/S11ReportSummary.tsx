/**
 * S11 — BÁO CÁO TỔNG KẾT
 * Isolated rebuild: Executive Closing Report.
 * knowledge/ui_master/sections/S11_REPORT_SUMMARY/
 *
 * Reading flow:
 * Header → Executive Summary → Strength → Attention → Recommendation → Link
 *
 * NOT a dashboard / KPI / chart / learning panel.
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s11;

/**
 * S11 Report Summary — executive closing card for Desktop Canonical V1.
 */
export function S11ReportSummary(): ReactNode {
  return (
    <section className="cd-s11" aria-labelledby="cd-s11-title">
      <div className="cd-s11__card">
        <h2 id="cd-s11-title" className="cd-s11__title">
          {data.title}
        </h2>

        <div className="cd-s11__exec">
          <h3 className="cd-s11__exec-title">{data.executive.title}</h3>
          <p className="cd-s11__exec-body">{data.executive.body}</p>
        </div>

        <hr className="cd-s11__divider" />

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--strength">
            {data.strengths.title}
          </h3>
          <ul className="cd-s11__list">
            {data.strengths.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--strength" aria-hidden="true">
                  ✓
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s11__divider" />

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--attention">
            {data.attention.title}
          </h3>
          <ul className="cd-s11__list">
            {data.attention.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--attention" aria-hidden="true">
                  •
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s11__divider" />

        <div className="cd-s11__block">
          <h3 className="cd-s11__block-title cd-s11__block-title--recommend">
            {data.recommendations.title}
          </h3>
          <ul className="cd-s11__list">
            {data.recommendations.items.map((item) => (
              <li key={item} className="cd-s11__row">
                <span className="cd-s11__icon cd-s11__icon--recommend" aria-hidden="true">
                  →
                </span>
                <span className="cd-s11__text">{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <hr className="cd-s11__divider cd-s11__divider--footer" />

        <a className="cd-s11__link" href="#s11-report">
          {data.link}
        </a>
      </div>
    </section>
  );
}

/** Portal export alias — keep S11LearningPanel name for shell stability. */
export const S11LearningPanel = S11ReportSummary;
