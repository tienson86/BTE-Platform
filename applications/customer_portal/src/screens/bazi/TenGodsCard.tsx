import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { ScoreBar } from "../../components/display/ScoreBar";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiResultLabels,
  BaZiTenGod,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type TenGodsCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  gods: readonly BaZiTenGod[];
  errorMessage?: string;
};

/** WP08 — Ten Gods Card (presentation only). */
export const TenGodsCard = memo(function TenGodsCard({
  status,
  labels,
  gods,
  errorMessage,
}: TenGodsCardProps): ReactNode {
  const totalCount = gods.reduce((sum, god) => sum + god.count, 0);

  return (
    <Card
      title={labels.tenGodsTitle}
      className="cui-bazi-gods"
      aria-label={labels.tenGodsTitle}
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải Thập Thần"
        emptyTitle="Chưa có dữ liệu Thập Thần"
        emptyDescription="Thập Thần sẽ hiển thị sau khi phân tích."
        errorTitle="Không tải được Thập Thần"
        errorDescription={errorMessage}
      >
        <Stack gap="paragraph">
          <BaseText variant="caption" tone="secondary">
            {labels.distributionSummary}: {totalCount} xuất hiện
          </BaseText>
          <div className="cui-bazi-gods__grid">
            {gods.map((god) => (
              <BaseTooltip
                key={god.id}
                content={`${god.name}: ${god.descriptionPreview}`}
              >
                <article className="cui-bazi-god" aria-label={god.name}>
                  <div className="cui-bazi-god__head">
                    <BaseText variant="subsection">{god.name}</BaseText>
                    <Badge tone="info">×{god.count}</Badge>
                    <Badge tone="neutral">{god.strength}</Badge>
                  </div>
                  <ScoreBar
                    label={labels.score}
                    value={god.score}
                    max={100}
                  />
                </article>
              </BaseTooltip>
            ))}
          </div>
        </Stack>
      </SectionGate>
    </Card>
  );
});
