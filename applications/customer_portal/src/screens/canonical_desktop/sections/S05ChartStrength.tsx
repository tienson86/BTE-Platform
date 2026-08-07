/**
 * S05 — Dashboard Preview Card: SỨC MẠNH MỆNH CỤC
 */

import type { ReactNode } from "react";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";

const CHECK_TONE: Record<string, string> = {
  positive: "cd-s05__check--positive",
  neutral: "cd-s05__check--neutral",
  warning: "cd-s05__check--warning",
  negative: "cd-s05__check--negative",
};

function levelModifier(level: string): string {
  const key = level.trim().toLowerCase();
  if (key === "rất mạnh") return "cd-s05__level--very-strong";
  if (key === "mạnh") return "cd-s05__level--strong";
  if (key === "trung bình") return "cd-s05__level--medium";
  if (key === "yếu") return "cd-s05__level--weak";
  if (key === "rất yếu") return "cd-s05__level--very-weak";
  return "cd-s05__level--strong";
}

/**
 * S05 Chart Strength — Dashboard preview card.
 */
export function S05ChartStrength(): ReactNode {
  const data = useCanonicalDesktop().s05;
  const previewFactors = data.factors.slice(0, 4);
  const [scoreMain, scoreMax = "100"] = data.score.split(/\s*\/\s*/);

  return (
    <section className="cd-s05 cd-preview-card" aria-labelledby="cd-s05-title">
      <div className="cd-s05__card">
        <h2 id="cd-s05-title" className="cd-s05__title">
          {data.title}
        </h2>

        <div className="cd-s05__summary">
          <div className={`cd-s05__level ${levelModifier(data.level)}`}>
            {data.level}
          </div>
          <div className="cd-s05__score">
            <span className="cd-s05__score-main">{scoreMain}</span>
            <span className="cd-s05__score-max"> / {scoreMax}</span>
          </div>
        </div>

        <p className="cd-s05__insight">{data.insight}</p>

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
          {previewFactors.map((factor) => (
            <li key={factor.text} className="cd-s05__factor">
              <span
                className={`cd-s05__check ${CHECK_TONE[factor.tone] ?? ""}`}
                aria-hidden="true"
              >
                ✓
              </span>
              <span>{factor.text}</span>
            </li>
          ))}
        </ul>

        <button type="button" className="cd-s05__cta cd-preview-cta">
          {data.cta}
        </button>
      </div>
    </section>
  );
}

/** Portal wiring alias — same component. */
export const S05Strength = S05ChartStrength;
