/**
 * Supporting analysis evidence. UI-15 visualization kinds. Not executive prose.
 */

import type { ReactNode } from "react";
import type {
  BaziStructureView,
  FiveElementsView,
  PatternView,
  ShenShaView,
  TenGodsView,
} from "../../commercial_dashboard/types";
import { REPORT_SECTION, REPORT_SUPPORT_LABEL } from "../copy";
import { ReportSectionHeader } from "./ReportPrimitives";

type SupportingAnalysisSectionProps = {
  readonly bazi: BaziStructureView;
  readonly fiveElements: FiveElementsView;
  readonly tenGods: TenGodsView;
  readonly pattern: PatternView;
  readonly shenSha: ShenShaView;
};

function barPercent(count: number | null, peak: number): number {
  if (count == null || peak <= 0) return 0;
  return Math.max(0, Math.min(100, (count / peak) * 100));
}

/**
 * Level 3 evidence. Omits empty modules. Does not compete with executive type.
 */
export function SupportingAnalysisSection({
  bazi,
  fiveElements,
  tenGods,
  pattern,
  shenSha,
}: SupportingAnalysisSectionProps): ReactNode {
  const peak = Math.max(0, ...fiveElements.rows.map((row) => row.count ?? 0));
  const godNames = tenGods.featured.length
    ? tenGods.featured
    : tenGods.visible.map((item) => item.tenGod).filter(Boolean);
  const shenShaItems = shenSha.items.length
    ? shenSha.items
    : shenSha.groups.flatMap((group) => group.items);
  const hasAny =
    bazi.available ||
    fiveElements.available ||
    tenGods.available ||
    pattern.available ||
    shenSha.available;
  if (!hasAny) return null;
  return (
    <section
      className="bte-er__section bte-er__support"
      data-report-section="supporting"
      data-report-level="detailed"
    >
      <ReportSectionHeader title={REPORT_SECTION.supporting} level="detailed" />
      {bazi.available ? (
        <div className="bte-er__support-block" data-viz="structure">
          <h3 className="bte-er__subhead">{REPORT_SUPPORT_LABEL.bazi}</h3>
          <div className="bte-er__table-wrap" data-viz-chart="structure">
            <table className="bte-er__table">
              <thead>
                <tr>
                  <th scope="col" />
                  {bazi.pillars.map((pillar) => (
                    <th key={pillar.key} scope="col">
                      {pillar.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">Thiên Can</th>
                  {bazi.pillars.map((pillar) => (
                    <td key={`stem-${pillar.key}`}>{pillar.stem}</td>
                  ))}
                </tr>
                <tr>
                  <th scope="row">Địa Chi</th>
                  {bazi.pillars.map((pillar) => (
                    <td key={`branch-${pillar.key}`}>{pillar.branch}</td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      ) : null}
      {fiveElements.available ? (
        <div className="bte-er__support-block" data-viz="balance-bars">
          <h3 className="bte-er__subhead">{REPORT_SUPPORT_LABEL.fiveElements}</h3>
          <ul className="bte-er__bars" data-viz-chart="balance-bars">
            {fiveElements.rows.map((row) => (
              <li key={row.key} data-element={row.key}>
                <span className="bte-er__bar-name">{row.label}</span>
                <span className="bte-er__bar-track">
                  <span
                    className={`bte-er__bar-fill bte-er__bar-fill--${row.key}`}
                    style={{ width: `${barPercent(row.count, peak)}%` }}
                  />
                </span>
                <span className="bte-er__bar-count">
                  {row.count == null ? "" : String(row.count)}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      {godNames.length ? (
        <div className="bte-er__support-block" data-viz="relationship">
          <h3 className="bte-er__subhead">{REPORT_SUPPORT_LABEL.tenGods}</h3>
          <ul className="bte-er__chips" data-viz-chart="relationship">
            {godNames.map((name, index) => (
              <li key={`${name}-${index}`} className="bte-er__chip">
                {name}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
      {pattern.available ? (
        <div className="bte-er__support-block" data-viz="formation-flow">
          <h3 className="bte-er__subhead">{REPORT_SUPPORT_LABEL.pattern}</h3>
          {pattern.primary ? <p className="bte-er__body">{pattern.primary}</p> : null}
          {pattern.formation.length ? (
            <ol className="bte-er__flow" data-viz-chart="formation-flow">
              {pattern.formation.map((step, index) => (
                <li key={`${step}-${index}`}>{step}</li>
              ))}
            </ol>
          ) : null}
        </div>
      ) : null}
      {shenShaItems.length ? (
        <div className="bte-er__support-block" data-viz="grouped-chips">
          <h3 className="bte-er__subhead">{REPORT_SUPPORT_LABEL.shenSha}</h3>
          <ul className="bte-er__chips" data-viz-chart="grouped-chips">
            {shenShaItems.map((item, index) => (
              <li key={`${item.name}-${index}`} className="bte-er__chip">
                {item.name}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
