import type { ReactNode } from "react";

import {
  NO_OCCURRENCES,
  NO_PATTERNS,
  PURPOSE_LABELS,
  STRENGTHS_HEADING,
  WATCHOUTS_HEADING,
} from "./labels";
import type { NumberEnergyData, PurposeContext } from "./types";

function purposeLabel(value: string | undefined): string {
  if (value && value in PURPOSE_LABELS) {
    return PURPOSE_LABELS[value as PurposeContext];
  }
  return value || "—";
}

function textOrDash(value: string | null | undefined): string {
  const trimmed = value?.trim();
  return trimmed ? trimmed : "—";
}

export function NumberEnergyResultView({ data }: { data: NumberEnergyData }): ReactNode {
  const narrative = data.narrative || {};
  const metadata = data.metadata || {};
  const occurrences = data.occurrences || [];
  const patterns = data.patterns || [];
  const patternLabels = metadata.pattern_labels || [];
  const warnings = data.warnings || [];
  const strengths = narrative.strengths || [];
  const watchouts = narrative.watchouts || [];
  return (
    <div className="ne-result" data-testid="number-energy-result">
      <section className="bte-card" data-testid="sequence-state-card">
        <h2>Trạng thái chuỗi</h2>
        <p className="ne-state" data-testid="sequence-state">
          {textOrDash(data.sequence_state)}
        </p>
        {narrative.unknown_notice ? (
          <p className="muted" data-testid="unknown-notice">
            {narrative.unknown_notice}
          </p>
        ) : null}
      </section>

      <section className="bte-card" data-testid="occurrences-card">
        <h2>Trường khí phát hiện</h2>
        {occurrences.length ? (
          <ul className="ne-occurrence-list">
            {occurrences.map((item) => (
              <li key={item.occurrence_id} className="ne-occurrence" data-testid="occurrence-item">
                <p className="ne-occurrence__name">{item.display_name}</p>
                <dl className="ne-kv">
                  <dt>Cặp số</dt>
                  <dd>{item.pair_digits}</dd>
                  <dt>Nguồn</dt>
                  <dd>{item.source_digits}</dd>
                  <dt>Trạng thái</dt>
                  <dd>{item.state}</dd>
                  <dt>Hạng biểu hiện</dt>
                  <dd>{item.strength_rank ?? "—"}</dd>
                  <dt>Phân loại</dt>
                  <dd data-testid="classification-label">
                    {item.classification_label || item.classification}
                  </dd>
                </dl>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted">{NO_OCCURRENCES}</p>
        )}
      </section>

      <section className="bte-card" data-testid="patterns-card">
        <h2>Mẫu đặc biệt</h2>
        {patterns.length ? (
          <ul data-testid="patterns-list">
            {patterns.map((item, index) => (
              <li key={item}>{patternLabels[index] || item}</li>
            ))}
          </ul>
        ) : (
          <p className="muted">{NO_PATTERNS}</p>
        )}
      </section>

      <section className="bte-card" data-testid="narrative-card">
        <h2>Luận giải</h2>
        <p data-testid="narrative-summary">{textOrDash(narrative.summary)}</p>
        {narrative.purpose_focus ? (
          <p className="muted" data-testid="purpose-focus">
            {narrative.purpose_focus}
          </p>
        ) : null}
        {strengths.length ? (
          <div data-testid="narrative-strengths">
            <h3>{STRENGTHS_HEADING}</h3>
            <ul>
              {strengths.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}
        {watchouts.length ? (
          <div data-testid="narrative-watchouts">
            <h3>{WATCHOUTS_HEADING}</h3>
            <ul>
              {watchouts.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null}
        {narrative.compatibility_note ? (
          <p className="muted" data-testid="compatibility-note">
            {narrative.compatibility_note}
          </p>
        ) : null}
        {narrative.health_disclaimer ? (
          <p className="ne-disclaimer" data-testid="health-disclaimer">
            {narrative.health_disclaimer}
          </p>
        ) : null}
      </section>

      {warnings.length ? (
        <section className="bte-card" data-testid="warnings-card">
          <h2>Cảnh báo V1</h2>
          <ul>
            {warnings.map((item) => (
              <li key={`${item.source_digits}-${item.reason}`}>
                {item.code}: {item.customer_reason || item.reason}
                {item.source_digits ? ` (${item.source_digits})` : ""}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className="bte-card ne-meta" data-testid="metadata-card">
        <h2>Phiên bản</h2>
        <dl className="ne-kv">
          <dt>Hệ thống</dt>
          <dd>{textOrDash(metadata.system_name || narrative.system_name)}</dd>
          <dt>Tên hiển thị</dt>
          <dd>{textOrDash(metadata.system_short_name || narrative.system_short_name)}</dd>
          <dt>Knowledge</dt>
          <dd data-testid="knowledge-version">{textOrDash(metadata.knowledge_version)}</dd>
          <dt>Engine</dt>
          <dd>{textOrDash(metadata.engine_version)}</dd>
          <dt>Ngữ cảnh</dt>
          <dd>{purposeLabel(metadata.purpose_context)}</dd>
        </dl>
      </section>
    </div>
  );
}
