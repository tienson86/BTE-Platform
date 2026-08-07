/**
 * LP-004 / Visualization Zone cards.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import type { LuckTimelineViewModel, RadarChartViewModel } from "../viewModels";
import { ResultCardShell } from "./ResultCardShell";

const ELEMENT_COLOR: Record<string, string> = {
  wood: "#2f6b3a",
  fire: "#b42318",
  earth: "#b8860b",
  metal: "#6b7280",
  water: "#1d4f91",
};

function polarPoint(cx: number, cy: number, radius: number, angleDeg: number): string {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return `${cx + radius * Math.cos(rad)},${cy + radius * Math.sin(rad)}`;
}

/**
 * Fixed-size radar from five-element percentages (presentation only).
 */
function FiveElementRadar({
  axes,
}: {
  axes: RadarChartViewModel["axes"];
}): ReactNode {
  const size = 200;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = 78;
  const step = 360 / Math.max(axes.length, 1);

  const rings = [0.25, 0.5, 0.75, 1].map((scale) =>
    axes
      .map((_, i) => polarPoint(cx, cy, maxR * scale, i * step))
      .join(" "),
  );

  const polygon = axes
    .map((axis, i) => polarPoint(cx, cy, maxR * (axis.pct / 100), i * step))
    .join(" ");

  return (
    <svg
      className="rp-radar__svg"
      viewBox={`0 0 ${size} ${size}`}
      width={size}
      height={size}
      role="img"
      aria-label="Radar ngũ hành"
    >
      {rings.map((points) => (
        <polygon
          key={points}
          points={points}
          className="rp-radar__ring"
          fill="none"
        />
      ))}
      {axes.map((axis, i) => (
        <line
          key={axis.name}
          x1={cx}
          y1={cy}
          x2={polarPoint(cx, cy, maxR, i * step).split(",")[0]}
          y2={polarPoint(cx, cy, maxR, i * step).split(",")[1]}
          className="rp-radar__axis"
        />
      ))}
      <polygon points={polygon} className="rp-radar__area" />
      {axes.map((axis, i) => {
        const [x, y] = polarPoint(cx, cy, maxR + 16, i * step).split(",");
        return (
          <text
            key={`label-${axis.name}`}
            x={x}
            y={y}
            className="rp-radar__label"
            fill={ELEMENT_COLOR[axis.element] ?? "#1c1c1c"}
            textAnchor="middle"
            dominantBaseline="middle"
          >
            {axis.name}
          </text>
        );
      })}
    </svg>
  );
}

export function RadarChartCard({ model }: { model: RadarChartViewModel }): ReactNode {
  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-radar-title"
      hasMore={model.hasMore}
      data-card="radar-chart"
    >
      <div className="rp-radar">
        <FiveElementRadar axes={model.axes} />
        <PresentationText
          typeRole="summary"
          preview={model.summary}
          className="rp-card__summary"
          as="p"
        />
      </div>
    </ResultCardShell>
  );
}

export function LuckTimelineCard({
  model,
}: {
  model: LuckTimelineViewModel;
}): ReactNode {
  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-timeline-title"
      hasMore={model.hasMore}
      data-card="luck-timeline"
    >
      <ol className="rp-timeline">
        {model.stages.items.map((stage, index) => (
          <li key={stage.label} className="rp-timeline__item">
            <span className="rp-timeline__marker" aria-hidden="true">
              {index + 1}
            </span>
            <div className="rp-timeline__content">
              <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
                {stage.label}
              </PresentationText>
              <PresentationText typeRole="summary" preview={stage.detail} as="p" />
            </div>
          </li>
        ))}
      </ol>
      <PresentationText
        typeRole="summary"
        preview={model.summary}
        className="rp-card__summary"
        as="p"
      />
    </ResultCardShell>
  );
}
