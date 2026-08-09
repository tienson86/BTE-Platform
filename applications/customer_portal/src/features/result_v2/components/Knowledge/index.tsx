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
      className="rv2-section rv2-section--reference rv2-section--knowledge"
      id="rv2-Knowledge"
      tabIndex={-1}
      aria-labelledby="rv2-know-title"
    >
      <SectionHeader id="rv2-know-title" icon="knowledge">
        {title}
      </SectionHeader>
      <Expand
        expanded={!sectionCollapsed}
        expandLabel={chrome.expand_knowledge}
        collapseLabel={chrome.expand_knowledge_less}
        controlsId={panelId}
        onToggle={onToggleSection}
      />
      {!sectionCollapsed ? (
        <div id={panelId} className="rv2-expand-panel">
          {items.map((item, index) => {
            const itemId = `rv2-know-item-${index}`;
            const expanded = isItemExpanded(index);
            return (
              <Card key={`${item.title}-${index}`} className="rv2-knowledge-card" title={item.title}>
                <p className="rv2-prose rv2-knowledge-teaser">{item.teaser}</p>
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
                      <div id={itemId} className="rv2-article rv2-expand-panel">
                        <p>{item.body}</p>
                      </div>
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
