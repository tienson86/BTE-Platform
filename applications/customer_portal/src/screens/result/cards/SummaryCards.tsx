/**
 * LP-001 / Summary Zone cards — Product Polish V1 consulting presentation.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import { scrollToResultZone } from "../presentation/scrollToZone";
import type {
  CoreIndicatorsViewModel,
  DestinyDirectionViewModel,
  ExecutiveSummaryViewModel,
} from "../viewModels";
import { ResultCardShell } from "./ResultCardShell";

export function ExecutiveSummaryCard({
  model,
}: {
  model: ExecutiveSummaryViewModel;
}): ReactNode {
  const usablePoints = model.points.items.filter(Boolean).slice(0, 4);

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-executive-title"
      hasMore={model.hasMore}
      data-card="executive-summary"
      data-question="what-is-my-situation"
      data-priority="1"
      className="rp-card--hero-exec"
      footer={
        <div className="rp-cta-row">
          <button
            type="button"
            className="rp-card__cta rp-card__cta--primary"
            onClick={() => scrollToResultZone("recommendation")}
          >
            {model.primaryCtaLabel}
          </button>
          <button
            type="button"
            className="rp-card__cta rp-card__cta--secondary"
            onClick={() => scrollToResultZone("analysis")}
          >
            {model.secondaryCtaLabel}
          </button>
        </div>
      }
    >
      <PresentationText
        typeRole="body"
        preview={model.headline}
        className="rp-card__headline"
        as="p"
      />
      {usablePoints.length > 0 ? (
        <ul className="rp-card__bullets">
          {usablePoints.map((point) => (
            <li key={point} className="rp-card__bullet">
              <PresentationText typeRole="summary" clamp="summary" as="span">
                {point}
              </PresentationText>
            </li>
          ))}
        </ul>
      ) : null}
      {model.conclusion ? (
        <PresentationText
          typeRole="subtitle"
          preview={model.conclusion}
          className="rp-card__conclusion"
          as="p"
        />
      ) : null}
    </ResultCardShell>
  );
}

export function CoreIndicatorsCard({
  model,
}: {
  model: CoreIndicatorsViewModel;
}): ReactNode {
  if (!model.visible || model.items.items.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-indicators-title"
      hasMore={model.hasMore}
      data-card="core-indicators"
      data-priority="3"
    >
      <ul className="rp-indicators">
        {model.items.items.map((item) => (
          <li key={item.label} className="rp-indicators__row" data-tone={item.color}>
            <PresentationText typeRole="caption" clamp="subtitle" as="span">
              {item.label}
            </PresentationText>
            <PresentationText typeRole="subtitle" clamp="subtitle" as="span">
              {item.value}
            </PresentationText>
          </li>
        ))}
      </ul>
      {model.reason ? (
        <p className="rp-indicators__reason">
          <span className="rp-indicators__reason-label">{model.reasonLabel}</span>
          {model.reason}
        </p>
      ) : null}
    </ResultCardShell>
  );
}

export function DestinyDirectionCard({
  model,
}: {
  model: DestinyDirectionViewModel;
}): ReactNode {
  if (!model.visible || model.items.items.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-destiny-title"
      hasMore={model.hasMore}
      data-card="destiny-direction"
      data-question="career-direction"
      data-priority="1"
      footer={
        <button
          type="button"
          className="rp-card__cta rp-card__cta--text"
          onClick={() => scrollToResultZone("recommendation")}
        >
          {model.cta || "Xem khuyến nghị nghề nghiệp"}
        </button>
      }
    >
      <PresentationText typeRole="caption" as="p" className="rp-destiny__question">
        {model.questionLabel}
      </PresentationText>
      <ul className="rp-destiny">
        {model.items.items.slice(0, 3).map((item) => (
          <li key={item.question} className="rp-destiny__item">
            <PresentationText typeRole="subtitle" clamp="subtitle" as="div">
              {item.question}
            </PresentationText>
            <PresentationText typeRole="summary" preview={item.answer} as="p" />
          </li>
        ))}
      </ul>
    </ResultCardShell>
  );
}
