import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { Divider } from "../../components/base/Divider";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { ProgressBar } from "../../components/display/ProgressBar";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiResultLabels,
  BaZiStrength,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type StrengthCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  strength: BaZiStrength;
  errorMessage?: string;
};

/** WP09 — Strength Card (Thân Vượng / Nhược) — presentation only. */
export const StrengthCard = memo(function StrengthCard({
  status,
  labels,
  strength,
  errorMessage,
}: StrengthCardProps): ReactNode {
  return (
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
          <div className="cui-bazi-strength__score">
            <BaseText variant="caption" tone="muted">
              {labels.score}
            </BaseText>
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
          </div>

          <Divider />

          <div className="cui-bazi-strength__verdict">
            <div>
              <BaseText variant="caption" tone="muted">
                Kết luận
              </BaseText>
              <Badge tone="accent">{strength.label}</Badge>
            </div>
            <div>
              <BaseText variant="caption" tone="muted">
                {labels.level}
              </BaseText>
              <Badge tone="success">{strength.level}</Badge>
            </div>
            <div>
              <BaseText variant="caption" tone="muted">
                {labels.confidence}
              </BaseText>
              <BaseTooltip content={`${labels.confidence}: ${strength.confidence}%`}>
                <Badge tone="info">{strength.confidence}%</Badge>
              </BaseTooltip>
            </div>
          </div>

          <Divider />

          <div>
            <BaseText variant="caption" tone="muted">
              {labels.summary}
            </BaseText>
            <BaseText variant="body">{strength.summary}</BaseText>
          </div>
        </Stack>
      </SectionGate>
    </Card>
  );
});
