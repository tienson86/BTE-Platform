/**
 * LP-001 / Summary Zone cards.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
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
  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-executive-title"
      hasMore={model.hasMore}
      data-card="executive-summary"
    >
      <PresentationText
        typeRole="body"
        preview={model.headline}
        className="rp-card__headline"
        as="p"
      />
      <ul className="rp-card__bullets">
        {model.points.items.map((point) => (
          <li key={point} className="rp-card__bullet">
            <PresentationText typeRole="summary" clamp="summary" as="span">
              {point}
            </PresentationText>
          </li>
        ))}
      </ul>
    </ResultCardShell>
  );
}

export function CoreIndicatorsCard({
  model,
}: {
  model: CoreIndicatorsViewModel;
}): ReactNode {
  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-indicators-title"
      hasMore={model.hasMore}
      data-card="core-indicators"
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
    </ResultCardShell>
  );
}

export function DestinyDirectionCard({
  model,
}: {
  model: DestinyDirectionViewModel;
}): ReactNode {
  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-destiny-title"
      hasMore={model.hasMore}
      data-card="destiny-direction"
      footer={
        <button type="button" className="rp-card__cta" data-has-more={model.hasMore ? "true" : "false"}>
          {model.cta}
        </button>
      }
    >
      <ul className="rp-destiny">
        {model.items.items.map((item) => (
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
