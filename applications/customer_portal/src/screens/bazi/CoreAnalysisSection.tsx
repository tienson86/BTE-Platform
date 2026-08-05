import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { ProgressBar } from "../../components/display/ProgressBar";
import { ScoreBar } from "../../components/display/ScoreBar";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiFiveElement,
  BaZiResultLabels,
  BaZiSpiritGod,
  BaZiStrength,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type CoreAnalysisSectionProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  strength: BaZiStrength;
  elements: readonly BaZiFiveElement[];
  spiritGods: readonly BaZiSpiritGod[];
  errorMessage?: string;
};

/**
 * Canonical Level 3 — Core Analysis.
 * Strength + Five Elements + Dụng/Kỵ Thần.
 */
export const CoreAnalysisSection = memo(function CoreAnalysisSection({
  status,
  labels,
  strength,
  elements,
  spiritGods,
  errorMessage,
}: CoreAnalysisSectionProps): ReactNode {
  return (
    <section
      id="phan-tich"
      className="cui-bazi-level"
      aria-labelledby="bazi-analysis-heading"
    >
      <header className="cui-bazi-level__header">
        <BaseText id="bazi-analysis-heading" variant="section">
          Phân tích Bát Tự
        </BaseText>
      </header>

      <div className="cui-bazi-core">
        <Card
          className="cui-bazi-strength"
          aria-label={labels.strengthTitle}
          title={labels.strengthTitle}
        >
          <SectionGate
            status={status}
            loadingLabel="Đang tải Thân Vượng Nhược"
            emptyTitle="Chưa có đánh giá Thân Vượng Nhược"
            emptyDescription="Kết quả thân vượng/nhược sẽ hiển thị sau khi phân tích."
            errorTitle="Không tải được Thân Vượng Nhược"
            errorDescription={errorMessage}
          >
            <Stack gap="paragraph">
              <BaseTooltip
                content={`${labels.score}: ${strength.score}/${strength.maxScore}`}
              >
                <BaseText variant="section">
                  {strength.score} / {strength.maxScore}
                </BaseText>
              </BaseTooltip>
              <ProgressBar
                value={strength.score}
                max={strength.maxScore}
                label={labels.strengthTitle}
              />
              <div className="cui-bazi-strength__scale" aria-hidden="true">
                <span>Nhược</span>
                <span>Trung hòa</span>
                <span>Vượng</span>
              </div>
              <div className="cui-bazi-strength__verdict">
                <Badge tone="accent">{strength.label}</Badge>
                <Badge tone="success">{strength.level}</Badge>
                <Badge tone="info">
                  {labels.confidence}: {strength.confidence}%
                </Badge>
              </div>
              <BaseText variant="body">{strength.summary}</BaseText>
            </Stack>
          </SectionGate>
        </Card>

        <Card
          title={labels.fiveElementsTitle}
          className="cui-bazi-elements"
          aria-label={labels.fiveElementsTitle}
        >
          <SectionGate
            status={status}
            loadingLabel="Đang tải Ngũ Hành"
            emptyTitle="Chưa có dữ liệu Ngũ Hành"
            emptyDescription="Phân bố ngũ hành sẽ hiển thị sau khi phân tích."
            errorTitle="Không tải được Ngũ Hành"
            errorDescription={errorMessage}
          >
            <div className="cui-bazi-elements__bars" aria-label="Biểu đồ phân bố">
              {elements.map((element) => (
                <BaseTooltip
                  key={element.id}
                  content={`${element.name}: ${element.percentage}% · ${element.strength}`}
                >
                  <div
                    className="cui-bazi-elements__bar-item"
                    data-element={element.id}
                  >
                    <ScoreBar
                      label={element.name}
                      value={element.percentage}
                      max={100}
                    />
                  </div>
                </BaseTooltip>
              ))}
            </div>
          </SectionGate>
        </Card>

        <div className="cui-bazi-spirits" aria-label="Dụng Thần · Kỵ Thần">
          {spiritGods.map((god) => (
            <Card
              key={god.id}
              className="cui-bazi-spirit"
              data-role={god.role}
              data-element={god.element}
            >
              <BaseText variant="caption" tone="muted">
                {god.roleLabel}
              </BaseText>
              <BaseText variant="section">{god.name}</BaseText>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
});
