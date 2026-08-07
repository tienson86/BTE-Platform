/**
 * Row02 — S01 | S02 | S09 (4 | 4 | 4). Natural height, top-aligned.
 */

import type { ReactNode } from "react";
import {
  S01IdentityDecision,
  S02OverviewActions,
  S09CungPhi,
} from "../sections/Sections";
import { RowGridCell } from "./RowGridCell";

/**
 * Row 2 — LifeProfile | Overview | Bagua.
 */
export function Row02(): ReactNode {
  return (
    <section
      className="cd-row-container cd-row-container--02 cd-row-container--natural-height"
      data-row="2"
      data-row-container="Row02"
      data-section-group="LifeDirectionSection"
      aria-label="Row 2 — Thông tin & tổng quan"
    >
      <div className="cd-row-grid">
        <RowGridCell span={4} mapping="LifeProfileCard">
          <S01IdentityDecision />
        </RowGridCell>
        <RowGridCell span={4} mapping="OverviewCard">
          <S02OverviewActions />
        </RowGridCell>
        <RowGridCell span={4} mapping="BaguaCard">
          <S09CungPhi />
        </RowGridCell>
      </div>
    </section>
  );
}
