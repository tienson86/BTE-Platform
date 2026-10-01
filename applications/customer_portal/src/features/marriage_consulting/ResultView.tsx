import { useState, type ReactNode } from "react";

import { FORBIDDEN_ID_PATTERN } from "./labels";
import type {
  AssessmentCardVm,
  MarriageMatrixSectionVm,
  MarriageViewModel,
} from "./types";

type ResultViewProps = {
  view: MarriageViewModel;
};

export function ResultView({ view }: ResultViewProps): ReactNode {
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

      <RelationshipGuidance view={view} />

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

      <span data-testid="score-grade-guard" hidden>
        {String(view.score)}|{String(view.grade)}
        {FORBIDDEN_ID_PATTERN.test(customerText(view)) ? "id-leak" : "id-ok"}
      </span>
    </div>
  );
}

function RelationshipGuidance({ view }: { view: MarriageViewModel }): ReactNode {
  const actions = view.actions.slice(0, 4);
  const hasContent = Boolean(view.timingSummary || actions.length || view.unavailableNote);
  if (!hasContent) return null;
  return (
    <section className="bte-card mc-guidance" data-testid="relationship-guidance">
      <h2>Gợi ý đồng hành</h2>
      <p className="mc-guidance__intro">
        Từ những điểm hòa hợp và khác biệt đã đối chiếu, hai người có thể ưu tiên các việc sau để mối quan hệ
        ổn định và dễ phối hợp hơn.
      </p>
      {view.timingSummary ? (
        <div className="mc-guidance__timing" data-testid="timing-guidance">
          <h3>Nhịp thời điểm</h3>
          <p>{view.timingSummary}</p>
        </div>
      ) : null}
      {actions.length ? (
        <ol className="mc-guidance__list" data-testid="relationship-actions">
          {actions.map((action) => (
            <li key={action.key}>
              <h3>{action.title}</h3>
              {action.objective ? <p>{action.objective}</p> : null}
              {action.outcome && action.outcome !== action.objective ? (
                <p className="muted">Kết quả hướng tới: {action.outcome}</p>
              ) : null}
            </li>
          ))}
        </ol>
      ) : null}
      {view.unavailableNote ? (
        <p className="mc-guidance__scope muted" data-testid="guidance-scope">
          <strong>Phạm vi luận giải.</strong> {view.unavailableNote}
        </p>
      ) : null}
    </section>
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
