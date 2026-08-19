/**
 * S05 — Dashboard Preview Card: SỨC MẠNH MỆNH CỤC
 * PACK_04: Presentation Adapter preview + hasMore (fixed height).
 */

import type { ReactNode } from "react";
import { adaptStrengthPreview } from "../../../presentation";
import { PresentationText } from "../../../components/shared/PresentationText";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

const CHECK_TONE: Record<string, string> = {
  positive: "cd-s05__check--positive",
  neutral: "cd-s05__check--neutral",
  warning: "cd-s05__check--warning",
  negative: "cd-s05__check--negative",
};

function levelModifier(level: string): string {
  const key = level.trim().toLowerCase();
  if (key.includes("vượng") || key.includes("vuong") || key === "mạnh") {
    return "cd-s05__level--strong";
  }
  if (key.includes("nhược") || key.includes("nhuoc") || key === "yếu") {
    return "cd-s05__level--weak";
  }
  if (key.includes("cân") || key.includes("trung")) {
    return "cd-s05__level--medium";
  }
  if (key === "rất mạnh") return "cd-s05__level--very-strong";
  if (key === "rất yếu") return "cd-s05__level--very-weak";
  return "cd-s05__level--strong";
}

/**
 * S05 Chart Strength — Dashboard preview card.
 */
export function S05ChartStrength(): ReactNode {
  const data = useCanonicalDesktop().s05;
  const preview = adaptStrengthPreview({
    insight: data.insight,
    factors: data.factors,
    cardType: "preview",
  });
  const hasScale = data.score.includes("/");
  const [scoreMain, scoreMax] = hasScale
    ? data.score.split(/\s*\/\s*/)
    : [data.score, ""];

  return (
    <section
      className="cd-s05 cd-preview-card"
      data-card-type="preview"
      data-has-more={preview.hasMore ? "true" : "false"}
      aria-labelledby="cd-s05-title"
    >
      <div className="cd-s05__card">
        <h2 id="cd-s05-title" className="cd-s05__title ui-line-clamp-2">
          {data.title}
        </h2>

        <div className="cd-s05__summary">
          <div className={`cd-s05__level ${levelModifier(data.level)}`}>
            {data.level}
          </div>
          <div className="cd-s05__score">
            <span className="cd-s05__score-main">{scoreMain}</span>
            {scoreMax ? (
              <span className="cd-s05__score-max"> / {scoreMax}</span>
            ) : null}
          </div>
        </div>

        <PresentationText
          className="cd-s05__insight"
          typeRole="summary"
          preview={preview.insight}
          as="p"
        />

        <div
          className="cd-s05__track"
          role="meter"
          aria-label={`Sức mạnh mệnh cục ${data.percent} trên 100 — ${data.level}`}
          aria-valuenow={data.percent}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <span
            className="cd-s05__bar-fill"
            style={{ width: `${data.percent}%` }}
          />
        </div>

        <ul className="cd-s05__factors">
          {preview.factors.items.map((factor) => (
            <li key={factor.text} className="cd-s05__factor">
              <span
                className={`cd-s05__check ${CHECK_TONE[factor.tone] ?? ""}`}
                aria-hidden="true"
              >
                ✓
              </span>
              <span className="ui-line-clamp-2">{factor.text}</span>
            </li>
          ))}
        </ul>

        <button
          type="button"
          className="cd-s05__cta cd-preview-cta"
          data-has-more={preview.hasMore ? "true" : "false"}
          aria-label={
            preview.hasMore ? `${data.cta} — còn nội dung đầy đủ` : data.cta
          }
        >
          {data.cta}
        </button>
      </div>
    </section>
  );
}

/** Portal wiring alias — same component. */
export const S05Strength = S05ChartStrength;
