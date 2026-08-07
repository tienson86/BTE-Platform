/**
 * Row01 — Context (S00). Natural height.
 */

import type { ReactNode } from "react";
import { S00ContextHeader } from "../sections/Sections";
import { RowGridCell } from "./RowGridCell";

/**
 * Row 1 — full-width ContextHeader.
 */
export function Row01(): ReactNode {
  return (
    <section
      className="cd-row-container cd-row-container--01 cd-row-container--natural-height"
      data-row="1"
      data-row-container="Row01"
      aria-label="Row 1 — Thông tin bối cảnh"
    >
      <div className="cd-row-grid">
        <RowGridCell span={12} mapping="ContextHeader">
          <S00ContextHeader />
        </RowGridCell>
      </div>
    </section>
  );
}
