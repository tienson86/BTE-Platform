/**
 * Compact chart snapshot. Canonical structure only. Not the full evidence tables.
 */

import type { ReactNode } from "react";
import type {
  BaziStructureView,
  FiveElementsView,
  LuckView,
  PatternView,
} from "../../commercial_dashboard/types";
import { REPORT_SECTION } from "../copy";
import { ReportSectionHeader } from "./ReportPrimitives";

type ChartSnapshotSectionProps = {
  readonly bazi: BaziStructureView;
  readonly fiveElements: FiveElementsView;
  readonly pattern: PatternView;
  readonly luck: LuckView;
};

function barPercent(count: number | null, peak: number): number {
  if (count == null || peak <= 0) return 0;
  return Math.max(0, Math.min(100, (count / peak) * 100));
}

/**
 * One-page structural evidence behind the executive summary.
 */
export function ChartSnapshotSection({
  bazi,
  fiveElements,
  pattern,
  luck,
}: ChartSnapshotSectionProps): ReactNode {
  const hasPillars = bazi.available && bazi.pillars.length > 0;
  const hasElements = fiveElements.available && fiveElements.rows.length > 0;
  const hasPattern = Boolean(pattern.primary);
  const hasLuck = Boolean(luck.current?.ganZhi);
  if (!hasPillars && !hasElements && !hasPattern && !hasLuck) return null;
  const peak = Math.max(0, ...fiveElements.rows.map((row) => row.count ?? 0));
  return (
    <section
      className="bte-er__section bte-er__snapshot"
      data-report-section="chart-snapshot"
      data-report-level="primary"
    >
      <ReportSectionHeader title={REPORT_SECTION.snapshot} level="primary" />
      {hasPillars ? (
        <ol className="bte-er__tutru" data-viz="structure" data-viz-chart="structure">
          {bazi.pillars.map((pillar) => (
            <li key={pillar.key} className="bte-er__tutru-col" data-pillar={pillar.key}>
              <span className="bte-er__tutru-label">{pillar.label}</span>
              <span className="bte-er__tutru-stem">{pillar.stem}</span>
              <span className="bte-er__tutru-branch">{pillar.branch}</span>
            </li>
          ))}
        </ol>
      ) : null}
      {hasElements ? (
        <ul className="bte-er__bars" data-viz="balance-bars" data-viz-chart="balance-bars">
          {fiveElements.rows.map((row) => (
            <li key={row.key} data-element={row.key}>
              <span className="bte-er__bar-name">{row.label}</span>
              <span className="bte-er__bar-track">
                <span
                  className={`bte-er__bar-fill bte-er__bar-fill--${row.key}`}
                  style={{ width: `${barPercent(row.count, peak)}%` }}
                />
              </span>
              <span className="bte-er__bar-count">{row.count == null ? "" : String(row.count)}</span>
            </li>
          ))}
        </ul>
      ) : null}
      <div className="bte-er__snapshot-facts">
        {hasPattern ? (
          <p className="bte-er__snapshot-fact" data-viz="formation-flow">
            <span className="bte-er__caption">Mệnh Cục</span>
            <span>{pattern.primary}</span>
          </p>
        ) : null}
        {hasLuck ? (
          <p className="bte-er__snapshot-fact">
            <span className="bte-er__caption">Đại Vận hiện tại</span>
            <span>
              {luck.current?.ganZhi}
              {luck.current?.yearRange ? ` · ${luck.current.yearRange}` : ""}
            </span>
          </p>
        ) : null}
      </div>
    </section>
  );
}
