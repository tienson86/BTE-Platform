import { memo } from "react";
import type { ChromeModel, KnowledgeModel } from "../../adapter/PortalResultModel";
import { Card } from "../Shared/Card";
import { Expand } from "../Shared/Expand";
import { SectionHeader } from "../Shared/SectionHeader";

export type KnowledgeProps = {
  title: string;
  items: KnowledgeModel[];
  chrome: ChromeModel;
  sectionCollapsed: boolean;
  isItemExpanded: (index: number) => boolean;
  onToggleSection: () => void;
  onToggleItem: (index: number) => void;
};

export function Knowledge({
  title,
  items,
  chrome,
  sectionCollapsed,
  isItemExpanded,
  onToggleSection,
  onToggleItem,
}: KnowledgeProps) {
  if (items.length === 0) return null;
  const panelId = "rv2-knowledge-panel";
  return (
    <section
      className="rv2-section"
      id="rv2-Knowledge"
      tabIndex={-1}
      aria-labelledby="rv2-know-title"
    >
      <SectionHeader id="rv2-know-title">{title}</SectionHeader>
      <Expand
        expanded={!sectionCollapsed}
        expandLabel={chrome.expand_knowledge}
        collapseLabel={chrome.expand_knowledge_less}
        controlsId={panelId}
        onToggle={onToggleSection}
      />
      {!sectionCollapsed ? (
        <div id={panelId}>
          {items.map((item, index) => {
            const itemId = `rv2-know-item-${index}`;
            const expanded = isItemExpanded(index);
            return (
              <Card key={`${item.title}-${index}`} title={item.title}>
                <p className="rv2-prose">{item.teaser}</p>
                {item.body ? (
                  <>
                    <Expand
                      expanded={expanded}
                      expandLabel={chrome.expand_knowledge_item}
                      collapseLabel={chrome.expand_less}
                      controlsId={itemId}
                      onToggle={() => onToggleItem(index)}
                    />
                    {expanded ? (
                      <p id={itemId} className="rv2-prose">
                        {item.body}
                      </p>
                    ) : (
                      <div id={itemId} hidden />
                    )}
                  </>
                ) : null}
              </Card>
            );
          })}
        </div>
      ) : (
        <div id={panelId} hidden />
      )}
    </section>
  );
}

export default memo(Knowledge);
