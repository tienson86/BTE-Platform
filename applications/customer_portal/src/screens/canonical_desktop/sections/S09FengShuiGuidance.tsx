/**
 * S09 — CUNG PHÍ / QUÁI MỆNH & NHÓM TRẠCH
 * Canonical Final layout (SSOT: S09_CANONICAL_FINAL*.png).
 * Bagua asset: Bagua_HauThien.svg (unchanged).
 */

import type { ReactNode } from "react";
import { CANONICAL_DESKTOP_MOCK } from "../mockData";
import {
  IconBriefcase,
  IconCompass,
  IconGrid,
  IconHome,
  IconPalette,
} from "../icons";
import baguaHauThienUrl from "../assets/Bagua_HauThien.svg";

const data = CANONICAL_DESKTOP_MOCK.s09;

/**
 * Approved Bagua asset with dynamic center as SVG <text> (asset file unchanged).
 * Center circle in Bagua_HauThien.svg: r≈157 @ 1024 → optically centered overlay.
 */
function BaguaDiagram({ center, number }: { center: string; number: string }): ReactNode {
  return (
    <svg
      className="cd-s09__bagua"
      viewBox="0 0 168 168"
      width={168}
      height={168}
      aria-hidden="true"
    >
      <image
        href={baguaHauThienUrl}
        width={168}
        height={168}
        preserveAspectRatio="xMidYMid meet"
      />
      {/* Title ~−25% vs prior 16px; SemiBold; sits above optical center */}
      <text
        x={84}
        y={72}
        textAnchor="middle"
        dominantBaseline="central"
        fill="#a60000"
        fontFamily="Inter, Arial, Helvetica, sans-serif"
        fontSize={12}
        fontWeight={600}
      >
        {center}
      </text>
      {/* Number ~+25% vs prior 24px; Bold; primary focal point */}
      <text
        x={84}
        y={96}
        textAnchor="middle"
        dominantBaseline="central"
        fill="#a60000"
        fontFamily="Inter, Arial, Helvetica, sans-serif"
        fontSize={30}
        fontWeight={700}
      >
        {number}
      </text>
    </svg>
  );
}

/**
 * S09 Feng Shui / Cung Phí — Desktop Canonical Final.
 */
export function S09FengShuiGuidance(): ReactNode {
  const icons = {
    home: <IconHome size={28} color="#fff" />,
    briefcase: <IconBriefcase size={28} color="#fff" />,
    compass: <IconCompass size={28} color="#fff" />,
    palette: <IconPalette size={28} color="#fff" />,
    grid: <IconGrid size={28} color="#fff" />,
  } as const;

  return (
    <section className="cd-s09 cd-card cd-card--fill" aria-labelledby="cd-s09-title">
      <h2 id="cd-s09-title" className="cd-section-title">
        {data.title}
      </h2>
      <div className="cd-s09__quai">
        <BaguaDiagram center={data.quai.center} number={data.quai.number} />
        <ul className="cd-s09__bullets">
          {data.quai.bullets.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      </div>
      <h3 className="cd-s09__nhom-title">{data.nhomTrachTitle}</h3>
      <div className="cd-s09__icons">
        {data.nhomTrach.map((item) => (
          <div key={item.label} className="cd-s09__icon-btn">
            <div className={`cd-s09__icon-tile cd-s09__icon-tile--${item.color}`}>
              {icons[item.icon]}
            </div>
            <span className="cd-s09__icon-label">{item.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

/** Portal export alias — same component tree entry as before. */
export const S09CungPhi = S09FengShuiGuidance;
