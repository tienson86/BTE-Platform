/**
 * Row02 — S01 | S02 | S09 (4 | 4 | 4).
 * PACK_04: equal-height independent cards (module / guidance).
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
      className="cd-row-container cd-row-container--02"
      data-row="2"
      data-row-container="Row02"
      data-section-group="LifeDirectionSection"
      data-presentation="pack04"
      data-equal-height="true"
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
