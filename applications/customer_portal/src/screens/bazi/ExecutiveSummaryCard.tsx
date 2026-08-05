import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import type {
  BaZiExecutiveSummary,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type ExecutiveSummaryCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  executive: BaZiExecutiveSummary;
  errorMessage?: string;
};

type GlanceItem = {
  readonly id: string;
  readonly label: string;
  readonly value: string;
  readonly hint?: string;
  readonly emphasize?: boolean;
};

/**
 * Round 2 — Executive Summary Hero (ONLY section under review).
 * Answers in ~5 seconds: Nhật Chủ, Ngũ Hành, Âm Dương, Thân,
 * Dụng / Hỷ / Kỵ, Cách Cục, Đánh giá tổng quan.
 */
export const ExecutiveSummaryCard = memo(function ExecutiveSummaryCard({
  status,
  labels,
  executive,
  errorMessage,
}: ExecutiveSummaryCardProps): ReactNode {
  const glance: readonly GlanceItem[] = [
    {
      id: "strength",
      label: "Thân Vượng / Nhược",
      value: executive.strengthGlance,
      hint: executive.strengthHint,
      emphasize: true,
    },
    {
      id: "dung",
      label: "Dụng Thần",
      value: executive.dungThan,
      emphasize: true,
    },
    {
      id: "hy",
      label: "Hỷ Thần",
      value: executive.hyThan,
    },
    {
      id: "ky",
      label: "Kỵ Thần",
      value: executive.kyThan,
    },
    {
      id: "pattern",
      label: "Cách Cục",
      value: executive.pattern,
    },
    {
      id: "grade",
      label: "Đánh giá tổng quan",
      value: executive.overallGrade,
      emphasize: true,
    },
  ];

  return (
    <section
      id="tom-tat"
      className="cui-bazi-level cui-bazi-level--executive cui-bazi-executive-hero"
      aria-labelledby="bazi-executive-heading"
      data-review-section="executive-summary"
    >
      <header className="cui-bazi-level__header">
        <BaseText id="bazi-executive-heading" variant="section">
          {labels.executiveTitle}
        </BaseText>
        <div className="cui-bazi-level__header-meta">
          <Badge tone="success">{executive.level}</Badge>
          <Badge tone="info">
            {labels.confidence}: {executive.confidence}%
          </Badge>
        </div>
      </header>

      <SectionGate
        status={status}
        loadingLabel="Đang tải Tóm Tắt Điều Hành"
        emptyTitle="Chưa có tóm tắt điều hành"
        emptyDescription="Tóm tắt sẽ hiển thị sau khi có kết quả phân tích."
        errorTitle="Không tải được Tóm Tắt Điều Hành"
        errorDescription={errorMessage}
      >
        <Card className="cui-bazi-exec-hero" aria-label="Nhật Chủ — Hero">
          <div className="cui-bazi-exec-hero__identity">
            <div className="cui-bazi-exec-hero__day-master">
              <BaseText variant="caption" tone="muted">
                Nhật Chủ
              </BaseText>
              <p className="cui-bazi-exec-hero__stem">{executive.dayMaster}</p>
              <BaseText variant="body" tone="secondary">
                {executive.dayMasterHint}
              </BaseText>
            </div>
            <div className="cui-bazi-exec-hero__pair">
              <div className="cui-bazi-exec-hero__chip">
                <BaseText variant="caption" tone="muted">
                  Ngũ Hành Nhật Chủ
                </BaseText>
                <BaseText variant="section">{executive.element}</BaseText>
                <BaseText variant="caption" tone="secondary">
                  {executive.elementHint}
                </BaseText>
              </div>
              <div className="cui-bazi-exec-hero__chip">
                <BaseText variant="caption" tone="muted">
                  Âm Dương
                </BaseText>
                <BaseText variant="section">{executive.yinYang}</BaseText>
                <BaseText variant="caption" tone="secondary">
                  {executive.yinYangHint}
                </BaseText>
              </div>
              <div className="cui-bazi-exec-hero__chip cui-bazi-exec-hero__chip--grade">
                <BaseText variant="caption" tone="muted">
                  Đánh giá tổng quan
                </BaseText>
                <BaseText variant="section">{executive.overallGrade}</BaseText>
                <BaseText variant="caption" tone="secondary">
                  {executive.level}
                </BaseText>
              </div>
            </div>
          </div>

          <BaseText variant="body" className="cui-bazi-exec-hero__summary">
            {executive.summary}
          </BaseText>

          <aside
            className="cui-bazi-exec-hero__callout"
            aria-label="Khuyến nghị đầu tiên"
          >
            <BaseText variant="caption" tone="muted">
              Khuyến nghị đầu tiên
            </BaseText>
            <BaseText variant="body">{executive.recommendation}</BaseText>
          </aside>
        </Card>

        <div
          className="cui-bazi-exec-glance"
          aria-label="Chỉ số điều hành nhanh"
        >
          {glance.map((item) => (
            <Card
              key={item.id}
              className="cui-bazi-exec-glance__item"
              data-emphasize={item.emphasize || undefined}
            >
              <BaseText variant="caption" tone="muted">
                {item.label}
              </BaseText>
              <BaseText
                variant="subsection"
                className="cui-bazi-exec-glance__value"
              >
                {item.value}
              </BaseText>
              {item.hint ? (
                <BaseText variant="caption" tone="secondary">
                  {item.hint}
                </BaseText>
              ) : null}
            </Card>
          ))}
        </div>
      </SectionGate>
    </section>
  );
});
