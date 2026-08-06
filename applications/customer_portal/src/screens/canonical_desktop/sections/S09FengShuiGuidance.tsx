/**
 * S09 — CUNG PHÍ / QUÁI MỆNH & NHÓM TRẠCH
 * Uses approved canonical Later Heaven Bagua SVG.
 * knowledge/ui_master/sections/S09_FENG_SHUI_GUIDANCE/assets/bagua/Bagua_HauThien.svg
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
 * Approved Bagua asset with dynamic center overlay (SVG unchanged).
 */
function BaguaDiagram({ center, number }: { center: string; number: string }): ReactNode {
  return (
    <div
      className="cd-s09__bagua"
      aria-hidden="true"
      style={{ position: "relative" }}
    >
      <img
        className="cd-s09__bagua-img"
        src={baguaHauThienUrl}
        alt=""
        width={88}
        height={88}
        draggable={false}
        style={{ display: "block", width: "100%", height: "100%" }}
      />
      <div
        className="cd-s09__bagua-center"
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          textAlign: "center",
          pointerEvents: "none",
          lineHeight: 1.15,
        }}
      >
        <span
          style={{
            color: "#a60000",
            fontSize: 11,
            fontWeight: 700,
          }}
        >
          {center}
        </span>
        <span
          style={{
            color: "#a60000",
            fontSize: 14,
            fontWeight: 700,
          }}
        >
          {number}
        </span>
      </div>
    </div>
  );
}

/**
 * S09 Feng Shui / Cung Phí section — Desktop Canonical V1.
 */
export function S09FengShuiGuidance(): ReactNode {
  const icons = {
    home: <IconHome size={18} color="#fff" />,
    briefcase: <IconBriefcase />,
    compass: <IconCompass size={18} color="#fff" />,
    palette: <IconPalette />,
    grid: <IconGrid />,
  } as const;

  return (
    <section className="cd-card cd-card--fill" aria-labelledby="cd-s09-title">
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
