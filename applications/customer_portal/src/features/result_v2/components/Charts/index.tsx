import { memo } from "react";
import type { ChartModel, ChromeModel } from "../../adapter/PortalResultModel";
import { Card } from "../Shared/Card";
import { Expand } from "../Shared/Expand";
import { SectionHeader } from "../Shared/SectionHeader";

export type ChartsProps = {
  title: string;
  items: ChartModel[];
  chrome: ChromeModel;
  isExpanded: (id: string) => boolean;
  onToggleTable: (index: number) => void;
};

export const Charts = memo(function Charts({
  title,
  items,
  chrome,
  isExpanded,
  onToggleTable,
}: ChartsProps) {
  if (items.length === 0) return null;
  return (
    <section className="rv2-section" id="rv2-Charts" tabIndex={-1} aria-labelledby="rv2-charts-title">
      <SectionHeader id="rv2-charts-title">{title}</SectionHeader>
      {items.map((item, index) => {
        const tableId = `rv2-chart-table-${index}`;
        const expanded = isExpanded(`chart:${index}`);
        return (
          <Card key={`${item.asset_ref}-${index}`} title={item.title}>
            <figure className="rv2-chart" aria-label={item.title}>
              <figcaption className="rv2-chart-caption">{item.caption}</figcaption>
            </figure>
            {item.table ? (
              <>
                <Expand
                  expanded={expanded}
                  expandLabel={chrome.expand_table}
                  collapseLabel={chrome.expand_table_less}
                  controlsId={tableId}
                  onToggle={() => onToggleTable(index)}
                />
                {expanded ? (
                  <div className="rv2-table-wrap">
                    <table id={tableId} className="rv2-table">
                      <thead>
                        <tr>
                          {item.table.headers.map((header) => (
                            <th key={header}>{header}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {item.table.rows.map((row, rowIndex) => (
                          <tr key={rowIndex}>
                            {row.map((cell, cellIndex) => (
                              <td key={cellIndex}>{cell}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div id={tableId} hidden />
                )}
              </>
            ) : null}
          </Card>
        );
      })}
    </section>
  );
});
