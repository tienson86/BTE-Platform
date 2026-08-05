import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { Divider } from "../../components/base/Divider";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiPillar,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type FourPillarsCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  pillars: readonly BaZiPillar[];
  errorMessage?: string;
};

/** WP06 — Four Pillars Card (presentation only). */
export const FourPillarsCard = memo(function FourPillarsCard({
  status,
  labels,
  pillars,
  errorMessage,
}: FourPillarsCardProps): ReactNode {
  return (
    <Card
      title={labels.pillarsTitle}
      className="cui-bazi-pillars"
      aria-label={labels.pillarsTitle}
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải Tứ Trụ"
        emptyTitle="Chưa có dữ liệu Tứ Trụ"
        emptyDescription="Dữ liệu trụ sẽ hiển thị sau khi phân tích."
        errorTitle="Không tải được Tứ Trụ"
        errorDescription={errorMessage}
      >
        <div className="cui-bazi-pillars__grid">
          {pillars.map((pillar) => (
            <PillarPanel key={pillar.kind} pillar={pillar} labels={labels} />
          ))}
        </div>
      </SectionGate>
    </Card>
  );
});

function PillarPanel({
  pillar,
  labels,
}: {
  pillar: BaZiPillar;
  labels: BaZiResultLabels;
}): ReactNode {
  return (
    <article
      className="cui-bazi-pillar"
      data-kind={pillar.kind}
      aria-label={`Trụ ${pillar.label}`}
    >
      <BaseText variant="subsection" className="cui-bazi-pillar__label">
        {pillar.label}
      </BaseText>
      <Divider />
      <Stack gap="list">
        <PillarRow
          label={labels.stem}
          value={pillar.heavenlyStem}
          tooltip={`${labels.stem}: ${pillar.heavenlyStem}`}
        />
        <PillarRow
          label={labels.branch}
          value={pillar.earthlyBranch}
          tooltip={`${labels.branch}: ${pillar.earthlyBranch}`}
        />
        <div className="cui-bazi-pillar__row">
          <BaseText variant="caption" tone="muted">
            {labels.hidden}
          </BaseText>
          <div className="cui-bazi-pillar__tags">
            {pillar.hiddenStems.map((stem) => (
              <BaseTooltip key={stem} content={`${labels.hidden}: ${stem}`}>
                <Badge tone="neutral">{stem}</Badge>
              </BaseTooltip>
            ))}
          </div>
        </div>
        <PillarRow
          label={labels.naYin}
          value={pillar.naYin}
          tooltip={`${labels.naYin}: ${pillar.naYin}`}
        />
        <PillarRow
          label={labels.twelveStage}
          value={pillar.twelveStage}
          tooltip={`${labels.twelveStage}: ${pillar.twelveStage}`}
        />
      </Stack>
    </article>
  );
}

function PillarRow({
  label,
  value,
  tooltip,
}: {
  label: string;
  value: string;
  tooltip: string;
}): ReactNode {
  return (
    <div className="cui-bazi-pillar__row">
      <BaseText variant="caption" tone="muted">
        {label}
      </BaseText>
      <BaseTooltip content={tooltip}>
        <BaseText variant="body">{value}</BaseText>
      </BaseTooltip>
    </div>
  );
}
