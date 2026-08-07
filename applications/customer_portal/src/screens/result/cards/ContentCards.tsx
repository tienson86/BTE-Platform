/**
 * LP-005 / LP-006 / LP-007 content cards — Sprint B content, Sprint C a11y/perf.
 */

import { memo, useId, useState, type ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import type {
  InterpretationBlockViewModel,
  InterpretationZoneViewModel,
  KnowledgeSectionViewModel,
  KnowledgeZoneViewModel,
  RecommendationItemViewModel,
  RecommendationZoneViewModel,
} from "../viewModels";

function PriorityBadge({
  priority,
  label,
}: {
  priority: RecommendationItemViewModel["priority"];
  label: string;
}): ReactNode {
  return (
    <span className="rp-priority" data-priority={priority}>
      {label}
    </span>
  );
}

function RecommendationItem({
  item,
}: {
  item: RecommendationItemViewModel;
}): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const detailId = useId();

  return (
    <article
      className="rp-rec-item"
      data-priority={item.priority}
      data-expanded={expanded ? "true" : "false"}
    >
      <div className="rp-rec-item__head">
        <PriorityBadge priority={item.priority} label={item.priorityLabel} />
        <PresentationText
          typeRole="subtitle"
          preview={item.action}
          className="rp-rec-item__action"
          as="h3"
        />
      </div>
      <PresentationText
        typeRole="summary"
        preview={item.reason}
        className="rp-rec-item__reason"
        as="p"
      />
      <PresentationText
        typeRole="summary"
        preview={item.benefit}
        className="rp-rec-item__benefit"
        as="p"
      />
      {expanded ? (
        <div id={detailId}>
          <PresentationText
            typeRole="body"
            preview={item.detail}
            className="rp-rec-item__detail"
            as="p"
          />
        </div>
      ) : null}
      {item.hasMore ? (
        <button
          type="button"
          className="rp-expand-btn"
          aria-expanded={expanded}
          aria-controls={detailId}
          aria-label={`${expanded ? "Thu gọn" : "Xem thêm"}: ${item.action.text}`}
          onClick={() => setExpanded((value) => !value)}
        >
          {expanded ? "Thu gọn" : "Xem thêm"}
        </button>
      ) : null}
    </article>
  );
}

/**
 * LP-005 Recommendation card — priority list, max 5 primary.
 */
export const RecommendationCard = memo(function RecommendationCard({
  model,
}: {
  model: RecommendationZoneViewModel;
}): ReactNode {
  return (
    <article
      className="rp-card rp-card--recommendation"
      data-card="recommendation"
      data-pattern="LP-005"
      aria-labelledby="rp-recommendation-title"
    >
      <PresentationText
        as="h2"
        id="rp-recommendation-title"
        typeRole="title"
        clamp="title"
        className="rp-card__title"
      >
        {model.title}
      </PresentationText>
      <div className="rp-card__body rp-rec-list" role="list">
        {model.items.map((item) => (
          <div key={item.id} role="listitem">
            <RecommendationItem item={item} />
          </div>
        ))}
      </div>
      {model.hasMore ? (
        <div className="rp-card__footer">
          <button
            type="button"
            className="rp-card__cta rp-card__cta--text"
            aria-label={model.viewAllLabel}
          >
            {model.viewAllLabel}
          </button>
        </div>
      ) : null}
    </article>
  );
});

function InterpretationBlock({
  block,
  expandLabel,
  collapseLabel,
}: {
  block: InterpretationBlockViewModel;
  expandLabel: string;
  collapseLabel: string;
}): ReactNode {
  const [expanded, setExpanded] = useState(false);
  const detailId = useId();

  return (
    <article
      className="rp-interp-block"
      data-expanded={expanded ? "true" : "false"}
      aria-labelledby={`rp-interp-${block.id}`}
    >
      <PresentationText
        as="h3"
        id={`rp-interp-${block.id}`}
        typeRole="subtitle"
        clamp="title"
        className="rp-interp-block__title"
      >
        {block.title}
      </PresentationText>

      <div className="rp-interp-step" data-step="observation">
        <span className="rp-interp-step__label" id={`${detailId}-obs`}>
          Observation
        </span>
        <PresentationText
          typeRole="summary"
          preview={block.observation}
          as="p"
          aria-labelledby={`${detailId}-obs`}
        />
      </div>

      {expanded ? (
        <div id={detailId}>
          <div className="rp-interp-step" data-step="explanation">
            <span className="rp-interp-step__label">Explanation</span>
            <PresentationText typeRole="body" preview={block.explanation} as="p" />
          </div>
          <div className="rp-interp-step" data-step="impact">
            <span className="rp-interp-step__label">Impact</span>
            <PresentationText typeRole="body" preview={block.impact} as="p" />
          </div>
          <div className="rp-interp-step" data-step="suggestion">
            <span className="rp-interp-step__label">Suggestion</span>
            <PresentationText typeRole="body" preview={block.suggestion} as="p" />
          </div>
        </div>
      ) : (
        <div className="rp-interp-step rp-interp-step--preview" data-step="explanation-preview">
          <span className="rp-interp-step__label">Explanation</span>
          <PresentationText typeRole="summary" preview={block.explanation} as="p" />
        </div>
      )}

      <button
        type="button"
        className="rp-expand-btn"
        aria-expanded={expanded}
        aria-controls={detailId}
        aria-label={`${expanded ? collapseLabel : expandLabel}: ${block.title}`}
        onClick={() => setExpanded((value) => !value)}
      >
        {expanded ? collapseLabel : expandLabel}
      </button>
    </article>
  );
}

/**
 * LP-006 Interpretation card — preview / expand / collapse reading layout.
 */
export const InterpretationCard = memo(function InterpretationCard({
  model,
}: {
  model: InterpretationZoneViewModel;
}): ReactNode {
  return (
    <article
      className="rp-card rp-card--auto rp-card--interpretation"
      data-card="interpretation"
      data-pattern="LP-006"
      aria-labelledby="rp-interpretation-title"
    >
      <PresentationText
        as="h2"
        id="rp-interpretation-title"
        typeRole="title"
        clamp="title"
        className="rp-card__title"
      >
        {model.title}
      </PresentationText>
      <div className="rp-card__body rp-interp-list">
        {model.blocks.map((block) => (
          <InterpretationBlock
            key={block.id}
            block={block}
            expandLabel={model.expandLabel}
            collapseLabel={model.collapseLabel}
          />
        ))}
      </div>
    </article>
  );
});

function KnowledgeSection({
  section,
}: {
  section: KnowledgeSectionViewModel;
}): ReactNode {
  const [open, setOpen] = useState(section.defaultOpen);
  const panelId = useId();

  return (
    <div
      className="rp-know-section"
      data-kind={section.kind}
      data-open={open ? "true" : "false"}
    >
      <button
        type="button"
        className="rp-know-section__trigger"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((value) => !value)}
      >
        <PresentationText typeRole="subtitle" clamp="title" as="span">
          {section.title}
        </PresentationText>
        <span className="rp-know-section__chevron" aria-hidden="true">
          {open ? "−" : "+"}
        </span>
      </button>
      {open ? (
        <div
          id={panelId}
          className="rp-know-section__panel"
          role="region"
          aria-label={section.title}
        >
          <PresentationText typeRole="summary" preview={section.definition} as="p" />
          <PresentationText
            typeRole="caption"
            preview={section.reference}
            className="rp-know-section__ref"
            as="p"
          />
          {section.hasMore ? (
            <PresentationText typeRole="body" preview={section.detail} as="p" />
          ) : null}
        </div>
      ) : (
        <PresentationText
          typeRole="summary"
          preview={section.definition}
          className="rp-know-section__teaser"
          as="p"
          id={panelId}
        />
      )}
    </div>
  );
}

/**
 * LP-007 Knowledge card — terminology / references / theory / appendix accordion.
 */
export const KnowledgeCard = memo(function KnowledgeCard({
  model,
}: {
  model: KnowledgeZoneViewModel;
}): ReactNode {
  return (
    <article
      className="rp-card rp-card--auto rp-card--knowledge"
      data-card="knowledge"
      data-pattern="LP-007"
      aria-labelledby="rp-knowledge-title"
    >
      <PresentationText
        as="h2"
        id="rp-knowledge-title"
        typeRole="title"
        clamp="title"
        className="rp-card__title"
      >
        {model.title}
      </PresentationText>
      <div className="rp-card__body rp-know-list">
        {model.sections.map((section) => (
          <KnowledgeSection key={section.id} section={section} />
        ))}
      </div>
    </article>
  );
});
