/**
 * S10 — Dashboard Preview Card: CÂN XƯƠNG ĐOÁN MỆNH
 * Bone-weight engine is not in the production pipeline; ViewModel shows unavailable copy.
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

/**
 * S10 Bone Weight Fortune — Dashboard preview card.
 */
export function S10BoneWeightFortune(): ReactNode {
  const data = useCanonicalDesktop().s10;
  return (
    <section className="cd-s10 cd-preview-card" aria-labelledby="cd-s10-title">
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

        <button type="button" className="cd-preview-cta">
          {data.link}
        </button>
      </div>
    </section>
  );
}

/** Portal export alias — keep S10CanXuong name for Desktop shell stability. */
export const S10CanXuong = S10BoneWeightFortune;
