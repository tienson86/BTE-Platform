/**
 * S10 — CÂN XƯƠNG ĐOÁN MỆNH
 * Isolated rebuild: Executive Bone Weight Fortune Card.
 * knowledge/ui_master/sections/S10_BONE_WEIGHT_FORTUNE/
 *
 * Reading flow: Header → Decision → Verse → Interpretation → Link
 * NOT a dashboard / KPI / calculator / rule viewer.
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";

const data = CANONICAL_DESKTOP_MOCK.s10;

/**
 * S10 Bone Weight Fortune — decision card + verse + interpretation + link.
 */
export function S10BoneWeightFortune(): ReactNode {
  return (
    <section className="cd-s10" aria-labelledby="cd-s10-title">
      <div className="cd-s10__card">
        <h2 id="cd-s10-title" className="cd-s10__title">
          {data.title}
        </h2>

        <div className="cd-s10__decision">
          <div className="cd-s10__stars" aria-label={`${data.stars} sao`}>
            {"★".repeat(data.stars)}
          </div>
          <p className="cd-s10__weight">{data.weight}</p>
          <p className="cd-s10__grade">{data.grade}</p>
          <p className="cd-s10__insight">{data.insight}</p>
        </div>

        <hr className="cd-s10__divider" />

        <div className="cd-s10__block">
          <h3 className="cd-s10__block-title">{data.verse.title}</h3>
          <div className="cd-s10__verse">
            {data.verse.lines.map((line) => (
              <p key={line} className="cd-s10__verse-line">
                {line}
              </p>
            ))}
          </div>
        </div>

        <hr className="cd-s10__divider" />

        <div className="cd-s10__block">
          <h3 className="cd-s10__block-title">{data.interpretation.title}</h3>
          <p className="cd-s10__interp-body">{data.interpretation.body}</p>
        </div>

        <hr className="cd-s10__divider" />

        <a className="cd-s10__link" href="#s10-detail">
          {data.link}
        </a>
      </div>
    </section>
  );
}

/** Portal export alias — keep S10CanXuong name for Desktop shell stability. */
export const S10CanXuong = S10BoneWeightFortune;
