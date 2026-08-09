import { memo } from "react";
import type { ChromeModel, WarningModel } from "../../adapter/PortalResultModel";
import { Card } from "../Shared/Card";
import { Expand } from "../Shared/Expand";
import { Notice } from "../Shared/Notice";
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
      className="rv2-section"
      id="rv2-Warnings"
      tabIndex={-1}
      aria-labelledby="rv2-warn-title"
    >
      <SectionHeader id="rv2-warn-title">{title}</SectionHeader>
      {items.map((item, index) => {
        const key = `warn:${index}`;
        const detailId = `rv2-warn-detail-${index}`;
        const expanded = isExpanded(key);
        const tone = item.severity === "critical" ? "danger" : "warning";
        return (
          <Card key={key} title={item.title} tone={tone}>
            <Notice tone={tone}>
              <p>{item.body}</p>
            </Notice>
            {item.mitigation ? (
              <>
                <Expand
                  expanded={expanded}
                  expandLabel={chrome.expand_more}
                  collapseLabel={chrome.expand_less}
                  controlsId={detailId}
                  onToggle={() => onToggleItem(key)}
                />
                {expanded ? <p id={detailId}>{item.mitigation}</p> : <div id={detailId} hidden />}
              </>
            ) : null}
          </Card>
        );
      })}
    </section>
  );
});
