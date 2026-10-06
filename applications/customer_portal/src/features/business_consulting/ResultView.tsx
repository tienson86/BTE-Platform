import { type ReactNode } from "react";

import { FORBIDDEN_ID_PATTERN } from "../marriage_consulting/labels";
import { CompatibilityMatrix } from "../marriage_consulting/CompatibilityMatrix";
import type { AssessmentCardVm, MarriageViewModel } from "../marriage_consulting/types";
import type { BusinessScoreAudit, BusinessViewModel } from "./types";

type ResultViewProps = {
  view: BusinessViewModel;
  occupation: string;
};

export function ResultView({ view, occupation }: ResultViewProps): ReactNode {
  return (
    <div className="mc-result" data-testid="business-result">
      <section className="bte-card mc-identity" data-testid="business-identity">
        <h2>Hồ sơ hợp tác</h2>
        <p data-testid="business-names">
          {view.personAName} và {view.personBName}
        </p>
        <p className="muted" data-testid="business-occupation">
          Ngành/nghề dự định hợp tác: {occupation}
        </p>
      </section>

      {view.businessScore ? <BusinessScoreSummary score={view.businessScore} /> : null}

      <CompatibilityMatrix
        sections={view.compatibilityMatrix}
        personALabel={view.personAName}
        personBLabel={view.personBName}
        introduction="Đối chiếu dữ liệu hai đối tác theo Dụng thần, Cung Phi, Can Chi, Mệnh Cục và Nhật Chủ. Mỗi hàng nêu kết quả và quy tắc làm căn cứ cho nhận định hợp tác."
      />

      {view.assessmentCards.length ? (
        <section className="mc-assessment" data-testid="business-assessment">
          <h2>Đánh giá hợp tác</h2>
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
      </section>

      <section className="bte-card" data-testid="executive-summary" hidden={view.assessmentCards.length > 0}>
        <h2>Đánh giá hợp tác</h2>
        <p>{view.executiveSummary}</p>
      </section>

      {view.actions.length || view.timingSummary || view.unavailableNote ? (
        <section className="bte-card mc-guidance" data-testid="business-guidance">
          <h2>Gợi ý phối hợp</h2>
          <p className="mc-guidance__intro">
            Từ những điểm bổ trợ và khác biệt đã đối chiếu, hai người nên thống nhất vai trò, quyền quyết định,
            cách chia lợi ích và nguyên tắc xử lý rủi ro trước khi bắt đầu.
          </p>
          {view.timingSummary ? (
            <div className="mc-guidance__timing" data-testid="timing-guidance">
              <h3>Nhịp thời điểm</h3>
              <p>{view.timingSummary}</p>
            </div>
          ) : null}
          {view.actions.length ? (
            <ol className="mc-guidance__list" data-testid="business-actions">
              {view.actions.slice(0, 4).map((action) => (
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
      ) : null}

      <section className="bte-card mc-opinion" data-testid="conclusion">
        <h2>Kết luận hợp tác</h2>
        {view.businessScore ? <p data-testid="conclusion-score"><strong>Điểm hợp tác.</strong> {view.businessScore.score === null ? "Chưa đủ dữ liệu để chấm điểm" : `${formatNumber(view.businessScore.score)} / 100${view.businessScore.provisional ? " (tạm tính)" : ""}`}</p> : null}
        <p data-testid="conclusion-opinion">
          <strong>Nhận định chung.</strong> {view.finalOpinion.overall}
        </p>
        {view.finalOpinion.strongestStrength ? (
          <p data-testid="conclusion-strength">
            <strong>Điểm bổ trợ nổi bật.</strong> {view.finalOpinion.strongestStrength}
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
        {view.businessScore ? <>
          {view.businessScore.reasons.map((reason) => <p className="muted" key={reason}>{reason}</p>)}
          <p className="muted">{view.businessScore.disclaimer}</p>
        </> : null}
      </section>

      <span data-testid="score-grade-guard" hidden>
        {FORBIDDEN_ID_PATTERN.test(customerText(view)) ? "id-leak" : "id-ok"}
      </span>
    </div>
  );
}

function formatNumber(value: number): string {
  return value.toLocaleString("vi-VN", { maximumFractionDigits: 2 });
}

function BusinessScoreSummary({ score }: { score: BusinessScoreAudit }): ReactNode {
  return <section className="bc-score" data-testid="business-score-summary" aria-labelledby="business-score-title">
    <div className="bc-score__heading">
      <div>
        <h2 id="business-score-title">Điểm hợp tác</h2>
        <p className="bc-score__value" data-testid="business-score-value">{score.score === null ? "Chưa đủ dữ liệu" : <>{formatNumber(score.score)} <span>/ 100</span></>}</p>
        {score.score !== null ? <meter className="bc-score__meter" min={0} max={100} low={45} high={75} optimum={100} value={score.score} aria-label="Điểm tương hợp Bát Tự" /> : null}
        {score.provisional && score.score !== null ? <p className="muted">Điểm tạm tính</p> : null}
      </div>
      <div>
        <h3 data-testid="business-score-recommendation">{score.recommendation}</h3>
        <p>{score.advice}</p>
        <p className="muted">Độ phủ dữ liệu: {formatNumber(score.coverage)}% · Độ tin cậy dữ liệu: {formatNumber(score.confidence * 100)}%</p>
      </div>
    </div>
    <p className="muted">{score.disclaimer}</p>
    <details className="bc-score__details">
      <summary>Chi tiết chấm điểm và ngưỡng khuyến nghị</summary>
      <div className="bc-score__table-scroll">
        <table>
          <caption>Đóng góp của từng nhóm đối chiếu</caption>
          <thead><tr><th scope="col">Nhóm</th><th scope="col">Điểm / 100</th><th scope="col">Trọng số quy ước</th><th scope="col">Trọng số thực tính</th><th scope="col">Đóng góp</th></tr></thead>
          <tbody>{score.groups.map((group) => <tr key={group.key}>
            <th scope="row">{group.title}</th>
            <td>{group.score === null ? "Không chấm" : formatNumber(group.score)}</td>
            <td>{formatNumber(group.configured_weight)}%</td>
            <td>{formatNumber(group.effective_weight)}%</td>
            <td>{group.score === null ? "Không chấm" : `${formatNumber(group.contribution)} điểm`}</td>
          </tr>)}</tbody>
        </table>
      </div>
      {score.groups.map((group) => <p key={group.key}><strong>{group.title}.</strong> {group.explanation}</p>)}
      <p>{score.methodology}</p>
      <p>Từ 75 điểm: có thể hợp tác; 60 đến dưới 75: có điều kiện; 45 đến dưới 60: chỉ thử quy mô nhỏ; dưới 45: chưa nên hợp tác dài hạn.</p>
      <p>Chỉ đưa ra khuyến nghị khi có đủ ba nhóm lõi, độ phủ ít nhất 80% và độ tin cậy dữ liệu ít nhất 50%. Nhóm lõi dưới 40 điểm sẽ giới hạn khuyến nghị ở mức thử quy mô nhỏ; độ tin cậy dưới 70% không cho khuyến nghị thuận lợi nhất.</p>
      {score.reasons.map((reason) => <p key={reason}>{reason}</p>)}
    </details>
  </section>;
}

function AssessmentCard({ card }: { card: AssessmentCardVm }): ReactNode {
  const hasBasis = card.supportingFacts.length > 0 || card.limitations.length > 0;
  return (
    <article className="bte-card mc-assessment-card" data-testid={`assessment-card-${card.questionId}`}>
      <p className="mc-assessment-card__question">{card.question}</p>
      <p className="mc-assessment-card__verdict">{card.answer}</p>
      {card.meaning ? <p>{card.meaning}</p> : null}
      {card.quickGuidance ? <p className="mc-assessment-card__guidance">{card.quickGuidance}</p> : null}
      {hasBasis ? (
        <details className="mc-assessment-card__more">
          <summary>Cơ sở đánh giá</summary>
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
          {card.limitations.length ? (
            <ul className="mc-assessment-card__limits">
              {card.limitations.map((item) => <li key={item}>{item}</li>)}
            </ul>
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
    view.finalOpinion.overall,
    view.finalOpinion.strongestStrength,
    view.finalOpinion.mainAttention,
    view.finalOpinion.recommendation,
  ].join(" ");
}
