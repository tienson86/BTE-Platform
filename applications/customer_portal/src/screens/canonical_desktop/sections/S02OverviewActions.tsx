/**
 * S02 — TỔNG QUAN LÁ SỐ
 * Isolated rebuild from CANONICAL_PORTAL_UI_DESKTOP_V1.png
 * + knowledge/ui_master/master_sections/S02_OVERVIEW_ACTIONS/
 */

import type { ReactNode } from "react";
import { ModuleHeader } from "../ModuleHeader";
import { useCanonicalDesktop } from "../CanonicalDesktopContext";
import {
  IconDrop,
  IconFire,
  IconLeaf,
  IconScale,
  IconSpark,
  IconYinYang,
} from "../icons";

const ICON_COLOR: Record<string, string> = {
  fire: "#b42318",
  water: "#1d4f91",
  wood: "#2f6b3a",
  metal: "#6b7280",
  earth: "#b8860b",
};

/**
 * S02 Overview — title inside card; 3×2 tiles as primary content.
 */
export function S02OverviewActions(): ReactNode {
  const data = useCanonicalDesktop().s02;
  return (
    <section className="cd-s02" aria-labelledby="cd-s02-title">
      <div className="cd-s02__card">
        <ModuleHeader id="cd-s02-title">{data.title}</ModuleHeader>
        <div className="cd-s02__grid">
          {data.items.map((item) => {
            const color = ICON_COLOR[item.color] ?? ICON_COLOR.metal;
            return (
              <article key={item.label} className="cd-s02__tile">
                <div className="cd-s02__tile-icon" aria-hidden="true">
                  {item.icon === "fire" && <IconFire size={32} color={color} />}
                  {item.icon === "yinyang" && <IconYinYang size={32} color={color} />}
                  {item.icon === "scale" && <IconScale size={32} color={color} />}
                  {item.icon === "drop" && <IconDrop size={32} color={color} />}
                  {item.icon === "spark" && <IconSpark size={32} color={color} />}
                  {item.icon === "leaf" && <IconLeaf size={32} color={color} />}
                </div>
                <div className="cd-s02__tile-title">{item.label}</div>
                <div className="cd-s02__tile-value" style={{ color }}>
                  {item.value}
                </div>
              </article>
            );
          })}
        </div>
        {data.dungReason ? (
          <p className="cd-s02__reason">
            <span className="cd-s02__reason-label">Căn cứ chọn Dụng</span>
            {data.dungReason}
          </p>
        ) : null}
      </div>
    </section>
  );
}
