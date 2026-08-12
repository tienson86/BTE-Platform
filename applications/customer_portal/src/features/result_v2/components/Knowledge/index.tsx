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

/** Split stored prose into readable paragraphs without inventing content. */
export function splitProseParagraphs(text: string): string[] {
  return text
    .split(/\n\s*\n/)
    .map((part) => part.trim())
    .filter((part) => part.length > 0);
}

function knowledgeParagraphs(item: KnowledgeModel): string[] {
  const body = (item.body ?? "").trim();
  const teaser = (item.teaser ?? "").trim();
  if (body) return splitProseParagraphs(body);
  if (teaser) return [teaser];
  return [];
}

/**
 * Narrative sections: full prose is visible when the section is open.
 * Section-level expand preserves hierarchy; no teaser/body duplication.
 */
export function Knowledge({
  title,
  items,
  chrome,
  sectionCollapsed,
  onToggleSection,
}: KnowledgeProps) {
  if (items.length === 0) return null;
  const panelId = "rv2-knowledge-panel";
  return (
    <section
      className="rv2-section rv2-section--reference rv2-section--knowledge"
      id="rv2-Knowledge"
      tabIndex={-1}
      aria-labelledby="rv2-know-title"
      data-narrative-sections="true"
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
        <div id={panelId} className="rv2-expand-panel rv2-knowledge-list">
          {items.map((item, index) => {
            const paragraphs = knowledgeParagraphs(item);
            return (
              <Card
                key={`${item.title}-${index}`}
                className="rv2-knowledge-card"
                title={item.title}
              >
                <div
                  className="rv2-article rv2-knowledge-body"
                  data-knowledge-index={index}
                >
                  {paragraphs.map((paragraph, paragraphIndex) => (
                    <p key={`know-${index}-p-${paragraphIndex}`}>{paragraph}</p>
                  ))}
                </div>
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
