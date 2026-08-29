/**
 * BaZi Structure Card — BÁT TỰ. Presentation only. No interpretation.
 */

import { useState, type ReactNode } from "react";
import type { BaziPillarView, BaziStructureView, DashboardCardSpec } from "./types";

type BaziCardProps = {
  readonly card: DashboardCardSpec;
  readonly model: BaziStructureView;
};

function cellMeta(primary: string, secondary: string): ReactNode {
  if (!primary) return null;
  return (
    <>
      <span className="bte-bazi__value">{primary}</span>
      {secondary ? <span className="bte-bazi__meta">{secondary}</span> : null}
    </>
  );
}

function HiddenCell({ items }: { readonly items: BaziPillarView["hiddenStems"] }): ReactNode {
  if (!items.length) return null;
  return (
    <ul className="bte-bazi__hidden">
      {items.map((item) => (
        <li key={item.stem}>
          <span>{item.stem}</span>
          {item.tenGod ? <span className="bte-bazi__meta">{item.tenGod}</span> : null}
        </li>
      ))}
    </ul>
  );
}

function hasRow(pillars: readonly BaziPillarView[], read: (pillar: BaziPillarView) => boolean): boolean {
  return pillars.some(read);
}

/**
 * Four-pillar BaZi evidence table with progressive disclosure.
 */
export function BaziCard({ card, model }: BaziCardProps): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const pillars = model.pillars;
  const showNapAm = hasRow(pillars, (pillar) => Boolean(pillar.napAm));
  const showTenGod = hasRow(pillars, (pillar) => Boolean(pillar.tenGod));
  const showHidden = hasRow(pillars, (pillar) => pillar.hiddenStems.length > 0);
  const showStage = hasRow(pillars, (pillar) => Boolean(pillar.truongSinh));
  const canExpand = showHidden || showStage || showTenGod;

  return (
    <article
      className={`bte-cdash__card bte-cdash__card--span-${card.span} bte-bazi`}
      data-card={card.id}
      data-span={card.span}
      data-implemented="bazi"
      data-expanded={expanded ? "true" : "false"}
      aria-label={model.title}
    >
      <header className="bte-bazi__header">
        <h2 className="bte-cdash__card-title">{model.title}</h2>
        {canExpand ? (
          <button
            type="button"
            className="bte-bazi__toggle"
            aria-expanded={expanded}
            onClick={() => setExpanded((value) => !value)}
          >
            {expanded ? "Thu gọn" : "Xem chi tiết"}
          </button>
        ) : null}
      </header>
      {!model.available ? (
        <p className="bte-bazi__empty" data-bazi-empty="true">
          Chưa đủ dữ liệu Bát Tự.
        </p>
      ) : (
        <div className="bte-bazi__scroll">
          <table className="bte-bazi__table">
            <thead>
              <tr>
                <th scope="col" className="bte-bazi__corner" />
                {pillars.map((pillar) => (
                  <th
                    key={pillar.key}
                    scope="col"
                    data-pillar={pillar.key}
                    data-day-master={pillar.isDayMaster ? "true" : undefined}
                  >
                    {pillar.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr data-bazi-row="stem">
                <th scope="row">Thiên Can</th>
                {pillars.map((pillar) => (
                  <td
                    key={`stem-${pillar.key}`}
                    data-pillar={pillar.key}
                    data-bazi-field="stem"
                    data-day-master={pillar.isDayMaster ? "true" : undefined}
                  >
                    {cellMeta(
                      pillar.stem,
                      [pillar.stemElement, pillar.stemYinYang].filter(Boolean).join(" · "),
                    )}
                  </td>
                ))}
              </tr>
              <tr data-bazi-row="branch">
                <th scope="row">Địa Chi</th>
                {pillars.map((pillar) => (
                  <td key={`branch-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="branch">
                    {cellMeta(pillar.branch, pillar.branchElement)}
                  </td>
                ))}
              </tr>
              {showNapAm ? (
                <tr data-bazi-row="nap-am">
                  <th scope="row">Nạp Âm</th>
                  {pillars.map((pillar) => (
                    <td key={`nap-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="nap-am">
                      {pillar.napAm}
                    </td>
                  ))}
                </tr>
              ) : null}
              {showTenGod ? (
                <tr data-bazi-row="ten-god">
                  <th scope="row">Thập Thần</th>
                  {pillars.map((pillar) => (
                    <td key={`god-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="ten-god">
                      {pillar.tenGod}
                    </td>
                  ))}
                </tr>
              ) : null}
              {expanded && showHidden ? (
                <tr data-bazi-row="hidden">
                  <th scope="row">Tàng Can</th>
                  {pillars.map((pillar) => (
                    <td key={`hidden-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="hidden">
                      <HiddenCell items={pillar.hiddenStems} />
                    </td>
                  ))}
                </tr>
              ) : null}
              {expanded && showStage ? (
                <tr data-bazi-row="stage">
                  <th scope="row">Trường Sinh</th>
                  {pillars.map((pillar) => (
                    <td key={`stage-${pillar.key}`} data-pillar={pillar.key} data-bazi-field="stage">
                      {pillar.truongSinh}
                    </td>
                  ))}
                </tr>
              ) : null}
            </tbody>
          </table>
        </div>
      )}
    </article>
  );
}
