/**
 * Row04 — S06 | S07 | S08 | S11 (4 | 2 | 3 | 3).
 * PACK_04: equal-height independent cards (list / preview).
 */

import type { ReactNode } from "react";
import {
  S06TenGods,
  S07ShenSha,
  S08Interpretation,
  S11ReportSummary,
} from "../sections/Sections";
import { RowGridCell } from "./RowGridCell";

/**
 * Row 4 — TenGod | ShenSha | Summary | FinalReport.
 */
export function Row04(): ReactNode {
  return (
    <section
      className="cd-row-container cd-row-container--04"
      data-row="4"
      data-row-container="Row04"
      data-section-group="InterpretationSection"
      data-presentation="pack04"
      data-equal-height="true"
      aria-label="Row 4 — Luận giải & báo cáo tổng kết"
    >
      <div className="cd-row-grid">
        <RowGridCell span={4} mapping="TenGodCard">
          <S06TenGods />
        </RowGridCell>
        <RowGridCell span={2} mapping="ShenShaCard">
          <S07ShenSha />
        </RowGridCell>
        <RowGridCell span={3} mapping="SummaryCard">
          <S08Interpretation />
        </RowGridCell>
        <RowGridCell span={3} mapping="FinalReportCard">
          <S11ReportSummary />
        </RowGridCell>
      </div>
    </section>
  );
}
