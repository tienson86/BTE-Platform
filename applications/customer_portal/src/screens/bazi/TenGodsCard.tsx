import { memo, type ReactNode } from "react";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
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
  visibleLabels?: readonly string[];
  hiddenLabels?: readonly string[];
  note?: string;
  errorMessage?: string;
};

/**
 * Canonical Level 4 — Ten Gods presence grid.
 * Same god names/counts; check / × for progressive scan.
 */
export const TenGodsCard = memo(function TenGodsCard({
  status,
  labels,
  gods,
  visibleLabels,
  hiddenLabels,
  note,
  errorMessage,
}: TenGodsCardProps): ReactNode {
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
          {visibleLabels && visibleLabels.length ? (
            <BaseText variant="body">
              {labels.visibleGods}: {visibleLabels.join(" · ")}
            </BaseText>
          ) : null}
          {hiddenLabels && hiddenLabels.length ? (
            <BaseText variant="body">
              {labels.hiddenGods}: {hiddenLabels.join(" · ")}
            </BaseText>
          ) : null}
          <ul className="cui-bazi-presence-grid">
            {gods.map((god) => {
              const present = god.count > 0;
              return (
                <li key={god.id}>
                  <BaseTooltip
                    content={`${god.name}: ×${god.count} · ${god.descriptionPreview}`}
                  >
                    <span
                      className="cui-bazi-presence"
                      data-present={present ? "true" : "false"}
                      aria-label={`${god.name}: ${present ? "có" : "không"}`}
                    >
                      <span
                        className="cui-bazi-presence__mark"
                        aria-hidden="true"
                      >
                        {present ? "✓" : "×"}
                      </span>
                      <BaseText variant="body">{god.name}</BaseText>
                    </span>
                  </BaseTooltip>
                </li>
              );
            })}
          </ul>
          <BaseText variant="caption" tone="muted">
            {note || labels.tenGodsNote}
          </BaseText>
          <BaseText variant="caption" tone="muted">
            ✓ Có xuất hiện · × Không có
          </BaseText>
        </Stack>
      </SectionGate>
    </Card>
  );
});
