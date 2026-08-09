import { memo } from "react";
import type { ChromeModel, WarningModel } from "../../adapter/PortalResultModel";
import { Card } from "../Shared/Card";
import { Expand } from "../Shared/Expand";
import { ResultIcon } from "../Shared/Icon";
import { SectionHeader } from "../Shared/SectionHeader";

export type ImportantWarningsProps = {
  title: string;
  items: WarningModel[];
  chrome: ChromeModel;
  isExpanded: (id: string) => boolean;
  onToggleItem: (id: string) => void;
};

export const ImportantWarnings = memo(function ImportantWarnings({
  title,
  items,
  chrome,
  isExpanded,
  onToggleItem,
}: ImportantWarningsProps) {
  if (items.length === 0) return null;
  return (
    <section
      className="rv2-section rv2-section--attention"
      id="rv2-Warnings"
      tabIndex={-1}
      aria-labelledby="rv2-warn-title"
    >
      <SectionHeader id="rv2-warn-title" icon="warning">
        {title}
      </SectionHeader>
      {items.map((item, index) => {
        const key = `warn:${index}`;
        const detailId = `rv2-warn-detail-${index}`;
        const expanded = isExpanded(key);
        const tone = item.severity === "critical" ? "danger" : "warning";
        return (
          <Card
            key={key}
            className="rv2-attention-card"
            tone={tone}
            title={
              <>
                <div className="rv2-rec-card__meta">
                  <ResultIcon name="warning" />
                  <h3 className="rv2-card__title">{item.title}</h3>
                </div>
              </>
            }
          >
            <p className="rv2-prose">{item.body}</p>
            {item.mitigation ? (
              <div className="rv2-card__footer">
                <Expand
                  expanded={expanded}
                  expandLabel={chrome.expand_more}
                  collapseLabel={chrome.expand_less}
                  controlsId={detailId}
                  onToggle={() => onToggleItem(key)}
                />
                {expanded ? (
                  <p id={detailId} className="rv2-prose rv2-expand-panel">
                    {item.mitigation}
                  </p>
                ) : (
                  <div id={detailId} hidden />
                )}
              </div>
            ) : null}
          </Card>
        );
      })}
    </section>
  );
});
