/**
 * Row03 — S03 | S04 | S05 | S10 (4 | 4 | 2 | 2).
 * S05/S10 are Dashboard Preview Cards. Natural height, top-aligned.
 */

import type { ReactNode } from "react";
import {
  S03FourPillars,
  S04ElementBalance,
  S05Strength,
  S10CanXuong,
} from "../sections/Sections";
import { RowGridCell } from "./RowGridCell";

/**
 * Row 3 — FourPillars | ElementBalance | Strength | BoneWeight.
 */
export function Row03(): ReactNode {
  return (
    <section
      className="cd-row-container cd-row-container--03 cd-row-container--natural-height"
      data-row="3"
      data-row-container="Row03"
      data-section-group="AnalysisSection"
      aria-label="Row 3 — Phân tích cốt lõi"
    >
      <div className="cd-row-grid">
        <RowGridCell span={4} mapping="FourPillarsCard">
          <S03FourPillars />
        </RowGridCell>
        <RowGridCell span={4} mapping="ElementBalanceCard">
          <S04ElementBalance />
        </RowGridCell>
        <RowGridCell span={2} mapping="StrengthCard">
          <S05Strength />
        </RowGridCell>
        <RowGridCell span={2} mapping="BoneWeightCard">
          <S10CanXuong />
        </RowGridCell>
      </div>
    </section>
  );
}
