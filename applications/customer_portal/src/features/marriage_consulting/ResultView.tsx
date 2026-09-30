import { useState, type ReactNode } from "react";

import { warningNotes } from "./adapter";
import { FORBIDDEN_ID_PATTERN } from "./labels";
import type {
  AssessmentCardVm,
  DomainCardVm,
  MarriageMatrixSectionVm,
  MarriageViewModel,
} from "./types";

type ResultViewProps = {
  view: MarriageViewModel;
  expertMode: boolean;
  onToggleExpert: () => void;
};

export function ResultView({ view, expertMode, onToggleExpert }: ResultViewProps): ReactNode {
  return (
    <div className="mc-result" data-testid="marriage-result">
      <section className="bte-card mc-identity" data-testid="couple-identity">
        <h2>Hồ sơ cặp đôi</h2>
        <p data-testid="couple-names">
          {view.personAName} và {view.personBName}
        </p>
      </section>

      {view.score !== null ? (
        <section className="bte-card mc-score" data-testid="compatibility-score">
          <div className="mc-score__summary">
            <div>
              <p className="mc-score__label">Điểm tương hợp cấu trúc</p>
              <p className="mc-score__value" data-testid="overall-score">
                {view.score}<span>/100</span>
              </p>
            </div>
            <div className="mc-score__grade" data-testid="overall-grade">
              <span>Xếp loại</span>
              <strong>{view.grade || "-"}</strong>
            </div>
          </div>
          <p className="muted">
            Điểm phản ánh mức bổ trợ giữa hai cấu trúc Bát Tự, không phải xác suất hạnh phúc hay quyết định nên cưới.
          </p>
          {view.scoreDomains.length ? (
            <div className="mc-score__domains" data-testid="domain-scores">
              {view.scoreDomains.map((item) => (
                <div className="mc-score__domain" key={item.domain}>
                  <div>
                    <span>{item.title}</span>
                    <small>Trọng số {item.weight}%</small>
                  </div>
                  <progress max="100" value={item.score} aria-label={`${item.title}: ${item.score} trên 100`} />
                  <strong>{item.score}</strong>
                </div>
              ))}
            </div>
          ) : null}
        </section>
      ) : null}

      {view.compatibilityMatrix.length ? (
        <CompatibilityMatrix sections={view.compatibilityMatrix} />
      ) : null}

      {view.assessmentCards.length ? (
        <section className="mc-assessment" data-testid="marriage-assessment">
          <h2>Đánh giá hôn nhân</h2>
          <div className="mc-assessment-grid">
            {view.assessmentCards.map((card) => (
              <AssessmentCard key={card.questionId} card={card} />
            ))}
          </div>
        </section>
      ) : null}

      <section
        className="bte-card mc-hero"
        data-testid="compatibility-hero"
        data-semantic-only="true"
        hidden={view.assessmentCards.length > 0}
      >
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

      <section className="bte-card" data-testid="executive-summary" hidden={view.assessmentCards.length > 0}>
        <h2>Đánh giá hôn nhân</h2>
        <p>{view.executiveSummary}</p>
      </section>

      <details className="mc-details" data-testid="detailed-analysis">
        <summary>Phân tích chi tiết</summary>
        <section className="bte-card" data-testid="key-strengths">
          <h2>Điểm hòa hợp nổi bật</h2>
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

        {view.mutualSupport ? (
          <section className="bte-card mc-mutual" data-testid="mutual-support">
            <h2>{view.mutualSupport.title}</h2>
            {view.mutualSupport.contributions.map((item) => (
              <div key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </div>
            ))}
            {view.mutualSupport.overall ? (
              <p>
                <strong>Nhận định chung.</strong> {view.mutualSupport.overall}
              </p>
            ) : null}
          </section>
        ) : null}

        {view.cungPhi && !view.compatibilityMatrix.some((item) => item.key === "cung_phi") ? (
          <section className="bte-card mc-cung" data-testid="cung-phi">
            <h2>{view.cungPhi.title}</h2>
            {view.cungPhi.people.map((item) => (
              <p key={item.label}>
                <strong>{item.label}</strong>
                <span> — Cung: {item.cung}</span>
              </p>
            ))}
            {view.cungPhi.relation ? (
              <p>
                <strong>Quan hệ.</strong> {view.cungPhi.relation}
              </p>
            ) : null}
            {view.cungPhi.meaning ? (
              <p>
                <strong>Ý nghĩa.</strong> {view.cungPhi.meaning}
              </p>
            ) : null}
            {view.cungPhi.disclaimer ? <p className="muted">{view.cungPhi.disclaimer}</p> : null}
          </section>
        ) : null}
      </details>

      <section className="bte-card mc-opinion" data-testid="conclusion">
        <h2>Kết luận cuối</h2>
        <p data-testid="conclusion-opinion">
          <strong>Nhận định chung.</strong> {view.finalOpinion.overall}
        </p>
        {view.finalOpinion.strongestStrength ? (
          <p data-testid="conclusion-strength">
            <strong>Điểm mạnh nhất.</strong> {view.finalOpinion.strongestStrength}
          </p>
        ) : null}
        {view.finalOpinion.mainAttention ? (
          <p data-testid="conclusion-attention">
            <strong>Điều cần lưu ý.</strong> {view.finalOpinion.mainAttention}
          </p>
        ) : null}
        {view.finalOpinion.recommendation ? (
          <p data-testid="conclusion-recommendation">
            <strong>Khuyến nghị.</strong> {view.finalOpinion.recommendation}
          </p>
        ) : null}
      </section>

      <details className="bte-card mc-expert" data-testid="expert-mode" open={expertMode}>
        <summary>
          <button type="button" className="secondary" data-testid="expert-toggle" onClick={onToggleExpert}>
            {expertMode ? "Ẩn chế độ chuyên gia" : "Xem chế độ chuyên gia"}
          </button>
        </summary>
        {expertMode ? <ExpertPanel view={view} /> : <p className="muted">Chế độ chuyên gia ẩn theo mặc định.</p>}
      </details>

      <span data-testid="score-grade-guard" hidden>
        {String(view.score)}|{String(view.grade)}
        {FORBIDDEN_ID_PATTERN.test(customerText(view)) ? "id-leak" : "id-ok"}
      </span>
    </div>
  );
}

const MATRIX_STATUS_LABEL: Record<string, string> = {
  supportive: "Hỗ trợ",
  balanced: "Cân bằng",
  mixed: "Hai chiều",
  pressured: "Áp lực",
  reference: "Tham khảo",
  unavailable: "Thiếu dữ liệu",
};

function CompatibilityMatrix({ sections }: { sections: MarriageMatrixSectionVm[] }): ReactNode {
  const [activeKey, setActiveKey] = useState(sections[0]?.key || "");
  const active = sections.find((item) => item.key === activeKey) || sections[0];
  if (!active) return null;
  return (
    <section className="mc-matrix" data-testid="compatibility-matrix">
      <div className="mc-matrix__heading">
        <div>
          <h2>Bảng đối chiếu có thể kiểm chứng</h2>
          <p className="muted">
            Mỗi hàng nêu dữ liệu hai người và quy tắc đối chiếu. Đây là mô hình luận giải Bát Tự minh bạch,
            không phải bằng chứng khoa học dự đoán hạnh phúc.
          </p>
        </div>
        <div className="mc-matrix__legend" aria-label="Chú giải trạng thái">
          <span data-status="supportive">Hỗ trợ</span>
          <span data-status="pressured">Áp lực</span>
          <span data-status="reference">Tham khảo</span>
        </div>
      </div>
      <div className="mc-matrix__tabs" role="tablist" aria-label="Nhóm đối chiếu">
        {sections.map((item) => (
          <button
            type="button"
            role="tab"
            aria-selected={item.key === active.key}
            className={item.key === active.key ? "is-active" : ""}
            key={item.key}
            onClick={() => setActiveKey(item.key)}
          >
            {item.title}
          </button>
        ))}
      </div>
      <div className="mc-matrix__panel" role="tabpanel" data-testid={`matrix-section-${active.key}`}>
        <p className="mc-matrix__description">{active.description}</p>
        <div className="mc-matrix__table-wrap">
          <table className="mc-matrix__table">
            <thead>
              <tr>
                <th>Tiêu chí</th>
                <th>{"Người Nữ"}</th>
                <th>{"Người Nam"}</th>
                <th>Kết quả đối chiếu</th>
                <th>Cơ sở</th>
              </tr>
            </thead>
            <tbody>
              {active.rows.map((row) => (
                <tr key={row.key} data-status={row.status}>
                  <th data-label="Tiêu chí" scope="row">{row.label}</th>
                  <td data-label="Người Nữ">{row.personA}</td>
                  <td data-label="Người Nam">{row.personB}</td>
                  <td data-label="Kết quả">
                    <span className="mc-matrix__status" data-status={row.status}>
                      {MATRIX_STATUS_LABEL[row.status] || row.status}
                    </span>
                    <p>{row.relationship}</p>
                    {row.scoreEffect !== null ? (
                      <small>
                        Ảnh hưởng kỹ thuật: {row.scoreEffect > 0 ? "+" : ""}{row.scoreEffect}; được giới hạn khi gộp điểm.
                      </small>
                    ) : null}
                  </td>
                  <td data-label="Cơ sở">
                    <p>{row.basis}</p>
                    <small>Độ tin cậy dữ liệu: {Math.round(row.confidence * 100)}%</small>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

function AssessmentCard({ card }: { card: AssessmentCardVm }): ReactNode {
  const hasBasis =
    Boolean(card.meaning) ||
    card.supportingFacts.length > 0 ||
    Boolean(card.quickGuidance) ||
    card.limitations.length > 0;
  return (
    <article className="bte-card mc-assessment-card" data-testid={`assessment-card-${card.questionId}`}>
      <p className="mc-assessment-card__question">{card.question}</p>
      <p className="mc-assessment-card__verdict">{card.answer}</p>
      {hasBasis ? (
        <details className="mc-assessment-card__more">
          <summary>Cơ sở đánh giá</summary>
          {card.meaning ? (
            <p className="mc-assessment-card__meaning">
              <span className="mc-assessment-card__label">Ý nghĩa</span>
              {card.meaning}
            </p>
          ) : null}
          {card.supportingFacts.length ? (
            <div>
              <p className="mc-assessment-card__label">Cơ sở</p>
              <ul className="mc-assessment-card__facts">
                {card.supportingFacts.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ) : null}
          {card.quickGuidance ? (
            <p className="mc-assessment-card__guidance">{card.quickGuidance}</p>
          ) : null}
          {card.limitations.length ? (
            <div>
              <p className="mc-assessment-card__label mc-assessment-card__label--muted">Lưu ý</p>
              <ul className="mc-assessment-card__limits">
                {card.limitations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </details>
      ) : null}
    </article>
  );
}

function ExpertPanel({ view }: { view: MarriageViewModel }): ReactNode {
  const notes = warningNotes(view.warnings);
  const technicalCards = view.assessmentCards.filter((card) => card.technicalExplanation);
  return (
    <div className="mc-expert-body">
      {technicalCards.length ? (
        <section className="mc-expert-technical">
          {technicalCards.map((card) => (
            <details
              key={card.questionId}
              className="mc-assessment-card__technical"
              data-testid={`assessment-technical-${card.questionId}`}
            >
              <summary>Giải thích kỹ thuật</summary>
              <p>{card.technicalExplanation}</p>
            </details>
          ))}
        </section>
      ) : null}

      <section className="mc-domains" data-testid="domain-analysis">
        <h2>Phân tích chi tiết theo miền</h2>
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

      <section className="bte-card" data-testid="appendix">
        <h2>Phụ lục phương pháp</h2>
        <p>{view.appendix}</p>
      </section>

      {view.expertTrace ? <pre data-testid="expert-trace">{view.expertTrace}</pre> : null}
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
        {open ? "Thu gọn" : "Chi tiết"}
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
    ...view.assessmentCards.flatMap((card) => [
      card.question,
      card.answer,
      card.meaning,
      ...card.supportingFacts,
      card.quickGuidance,
    ]),
    ...view.strengths,
    ...view.risks,
    ...(view.mutualSupport
      ? [...view.mutualSupport.contributions.map((item) => item.body), view.mutualSupport.overall]
      : []),
    view.cungPhi?.relation || "",
    view.cungPhi?.meaning || "",
    view.finalOpinion.overall,
    view.finalOpinion.strongestStrength,
    view.finalOpinion.mainAttention,
    view.finalOpinion.recommendation,
  ].join(" ");
}
