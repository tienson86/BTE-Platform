/**
 * LP-003 / Analysis Zone cards.
 */

import type { ReactNode } from "react";
import { PresentationText } from "../../../components/shared/PresentationText";
import type {
  FiveElementsViewModel,
  StrengthAnalysisViewModel,
  TenGodsAnalysisViewModel,
} from "../viewModels";
import { ResultCardShell } from "./ResultCardShell";

export function FiveElementsCard({
  model,
}: {
  model: FiveElementsViewModel;
}): ReactNode {
  if (!model.visible || model.rows.items.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-five-elements-title"
      hasMore={model.hasMore}
      data-card="five-elements"
      data-priority="3"
      className="rp-card--auto"
    >
      <ul className="rp-elements">
        {model.rows.items.map((row) => (
          <li key={row.name} className="rp-elements__row" data-element={row.element}>
            <div className="rp-elements__meta">
              <span className="rp-elements__name">{row.name}</span>
              {row.status ? <span className="rp-elements__status">{row.status}</span> : null}
            </div>
            <div
              className="rp-elements__track"
              role="meter"
              aria-label={`${row.name} ${row.pct}%`}
              aria-valuenow={row.pct}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <span className="rp-elements__fill" style={{ width: `${row.pct}%` }} />
            </div>
            <span className="rp-elements__pct">
              {row.count != null ? row.count : `${row.pct}%`}
            </span>
          </li>
        ))}
      </ul>
      <PresentationText
        typeRole="summary"
        preview={model.summary}
        className="rp-card__summary"
        as="p"
      />
    </ResultCardShell>
  );
}

export function StrengthAnalysisCard({
  model,
}: {
  model: StrengthAnalysisViewModel;
}): ReactNode {
  if (!model.visible) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-strength-title"
      hasMore={model.hasMore}
      data-card="strength"
      data-question="main-strength"
      data-priority="2"
      className="rp-card--auto"
    >
      <div className="rp-strength__hero">
        <PresentationText typeRole="metric" as="div" className="rp-strength__level">
          {model.level}
        </PresentationText>
        <PresentationText typeRole="subtitle" as="div" className="rp-strength__score">
          {model.score}
        </PresentationText>
      </div>
      <div
        className="rp-strength__track"
        role="meter"
        aria-valuenow={model.percent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Sức mạnh ${model.percent}`}
      >
        <span className="rp-strength__fill" style={{ width: `${model.percent}%` }} />
      </div>
      <PresentationText typeRole="summary" preview={model.insight} as="p" />
      <ul className="rp-strength__factors">
        {model.factors.items.map((factor) => (
          <li key={factor.text} className="rp-strength__factor" data-tone={factor.tone}>
            <PresentationText typeRole="summary" clamp="summary" as="span">
              {factor.text}
            </PresentationText>
          </li>
        ))}
      </ul>
    </ResultCardShell>
  );
}

export function TenGodsAnalysisCard({
  model,
}: {
  model: TenGodsAnalysisViewModel;
}): ReactNode {
  if (!model.visible || model.gods.items.length === 0) return null;

  return (
    <ResultCardShell
      title={model.title}
      titleId="rp-ten-gods-title"
      hasMore={model.hasMore}
      data-card="ten-gods"
      data-priority="3"
      className="rp-card--auto"
      footer={null}
    >
      <ul className="rp-ten-gods">
        {model.gods.items.map((god) => (
          <li key={god.name} className="rp-ten-gods__row">
            <span
              className="rp-ten-gods__dot"
              style={{ background: god.color }}
              aria-hidden="true"
            />
            <div>
              <PresentationText typeRole="body" clamp="subtitle" as="span" className="rp-ten-gods__name">
                {god.name}
              </PresentationText>
              {god.score ? (
                <PresentationText typeRole="caption" clamp="description" as="span">
                  {god.score}
                </PresentationText>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
      {model.othersLine ? (
        <PresentationText typeRole="summary" as="p" className="rp-card__summary">
          {model.othersLine}
        </PresentationText>
      ) : null}
    </ResultCardShell>
  );
}
