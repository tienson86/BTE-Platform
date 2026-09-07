import { useState, type ReactNode } from "react";

import { warningNotes } from "./adapter";
import { FORBIDDEN_ID_PATTERN, FORBIDDEN_SCORE_PATTERN } from "./labels";
import type { DomainCardVm, MarriageViewModel } from "./types";

type ResultViewProps = {
  view: MarriageViewModel;
  expertMode: boolean;
  onToggleExpert: () => void;
};

export function ResultView({ view, expertMode, onToggleExpert }: ResultViewProps): ReactNode {
  const notes = warningNotes(view.warnings);
  return (
    <div className="mc-result" data-testid="marriage-result">
      <section className="bte-card mc-identity" data-testid="couple-identity">
        <h2>Hồ sơ cặp đôi</h2>
        <p data-testid="couple-names">
          {view.personAName} và {view.personBName}
        </p>
        <p className="muted">{view.identityTitle}</p>
      </section>

      <section className="bte-card mc-hero" data-testid="compatibility-hero" data-semantic-only="true">
        <p className="mc-hero__eyebrow">{view.heroEyebrow}</p>
        <h2 data-testid="hero-headline">{view.heroHeadline}</h2>
        <p data-testid="hero-state">{view.heroStateLabel}</p>
        <p data-testid="hero-summary">{view.heroSummary}</p>
        <p data-testid="hero-confidence">{view.confidenceLabel}</p>
        {view.heroStrengths.length ? (
          <ul data-testid="hero-strengths">
            {view.heroStrengths.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        ) : null}
        {view.heroRisks.length ? (
          <ul data-testid="hero-risks">
            {view.heroRisks.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        ) : null}
        <p className="sr-only" data-testid="hero-score-absent">
          Điểm số tương hợp chưa khả dụng
        </p>
      </section>

      <section className="bte-card" data-testid="executive-summary">
        <h2>Tóm tắt tư vấn</h2>
        <p>{view.executiveSummary}</p>
      </section>

      <section className="bte-card" data-testid="key-strengths">
        <h2>Điểm hỗ trợ then chốt</h2>
        <ul>
          {view.strengths.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section className="bte-card" data-testid="key-risks">
        <h2>Điểm cần lưu ý</h2>
        <ul>
          {view.risks.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section className="mc-domains" data-testid="domain-analysis">
        <h2>Hiểu vì sao</h2>
        <div className="mc-domain-grid">
          {view.domains.map((domain) => (
            <DomainCard key={domain.domain} domain={domain} />
          ))}
        </div>
        {view.unavailableNote ? (
          <p className="mc-limitation" data-testid="unavailable-domains">
            {view.unavailableNote}
          </p>
        ) : null}
      </section>

      {view.timingSummary ? (
        <section className="bte-card" data-testid="timing-section">
          <h2>Nhịp thời điểm</h2>
          <p>{view.timingSummary}</p>
        </section>
      ) : (
        <div data-testid="timing-omitted" hidden />
      )}

      <section className="mc-actions" data-testid="action-plan">
        <h2>Kế hoạch hành động</h2>
        <div className="mc-action-grid">
          {view.actions.map((action) => (
            <article
              key={action.key}
              className="bte-card mc-action"
              data-priority={action.priority || undefined}
              data-testid="action-card"
            >
              <h3>{action.title}</h3>
              <p>
                <strong>Việc nên làm.</strong> {action.what}
              </p>
              {action.objective ? (
                <p>
                  <strong>Mục tiêu.</strong> {action.objective}
                </p>
              ) : null}
              {action.priorityLabel ? (
                <p data-testid="action-priority">
                  <strong>Mức ưu tiên.</strong> {action.priorityLabel}
                </p>
              ) : null}
              {action.when ? (
                <p>
                  <strong>Khi nào áp dụng.</strong> {action.when}
                </p>
              ) : null}
              {action.outcome ? (
                <p>
                  <strong>Kết quả mong đợi.</strong> {action.outcome}
                </p>
              ) : null}
            </article>
          ))}
        </div>
      </section>

      <section className="bte-card mc-confidence" data-testid="confidence-limitations">
        <h2>Độ tin cậy và giới hạn</h2>
        <p data-testid="confidence-label">{view.confidenceLabel}</p>
        <p>{view.confidenceBody}</p>
        {view.limitations.length ? (
          <ul data-testid="limitation-list">
            {view.limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        ) : null}
        {notes.map((note) => (
          <p key={note} className="mc-limitation" data-testid="warning-note">
            {note}
          </p>
        ))}
      </section>

      <section className="bte-card" data-testid="conclusion">
        <h2>Kết luận</h2>
        <p>{view.conclusion}</p>
      </section>

      <section className="bte-card" data-testid="appendix">
        <h2>Phụ lục phương pháp</h2>
        <p>{view.appendix}</p>
      </section>

      <details className="bte-card mc-expert" data-testid="expert-mode">
        <summary>
          <button type="button" className="secondary" onClick={onToggleExpert}>
            {expertMode ? "Ẩn chế độ chuyên gia" : "Xem chế độ chuyên gia"}
          </button>
        </summary>
        {expertMode && view.expertTrace ? (
          <pre data-testid="expert-trace">{view.expertTrace}</pre>
        ) : (
          <p className="muted">Chế độ chuyên gia ẩn theo mặc định.</p>
        )}
      </details>

      <span data-testid="score-grade-guard" hidden>
        {String(view.score)}|{String(view.grade)}|{FORBIDDEN_SCORE_PATTERN.test(JSON.stringify(view))
          ? "score-leak"
          : "ok"}
        {FORBIDDEN_ID_PATTERN.test(customerText(view)) ? "id-leak" : "id-ok"}
      </span>
    </div>
  );
}

function DomainCard({ domain }: { domain: DomainCardVm }): ReactNode {
  const [open, setOpen] = useState(false);
  return (
    <article className="bte-card mc-domain" data-domain={domain.domain} data-testid="domain-card">
      <h3>{domain.title}</h3>
      {domain.stateLabel ? <p className="mc-domain__state">{domain.stateLabel}</p> : null}
      <p>{domain.summary}</p>
      <button type="button" className="secondary" onClick={() => setOpen((value) => !value)}>
        {open ? "Thu gọn" : "Xem chi tiết"}
      </button>
      {open ? (
        <div className="mc-domain__details" data-testid="domain-details">
          <p>{domain.explanation}</p>
        </div>
      ) : null}
    </article>
  );
}

function customerText(view: MarriageViewModel): string {
  return [
    view.identityTitle,
    view.heroHeadline,
    view.heroSummary,
    view.executiveSummary,
    ...view.strengths,
    ...view.risks,
    ...view.domains.map((item) => item.summary),
    ...view.actions.map((item) => item.what),
    view.conclusion,
    view.appendix,
  ].join(" ");
}
