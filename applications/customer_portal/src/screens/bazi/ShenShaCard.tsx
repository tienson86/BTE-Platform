import { memo, type ReactNode } from "react";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiResultLabels,
  BaZiShenShaItem,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type ShenShaCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  items: readonly BaZiShenShaItem[];
  errorMessage?: string;
};

/** Canonical Level 4 — Thần Sát presence grid. */
export const ShenShaCard = memo(function ShenShaCard({
  status,
  labels,
  items,
  errorMessage,
}: ShenShaCardProps): ReactNode {
  return (
    <Card
      title={labels.shenShaTitle}
      className="cui-bazi-shensha"
      aria-label={labels.shenShaTitle}
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải Thần Sát"
        emptyTitle="Chưa có dữ liệu Thần Sát"
        emptyDescription="Thần Sát sẽ hiển thị sau khi Pattern / Rule sẵn sàng."
        errorTitle="Không tải được Thần Sát"
        errorDescription={errorMessage}
      >
        <Stack gap="paragraph">
          <ul className="cui-bazi-presence-grid">
            {items.map((item) => (
              <li key={item.id}>
                <BaseTooltip content={item.note}>
                  <span
                    className="cui-bazi-presence"
                    data-present={item.present ? "true" : "false"}
                    aria-label={`${item.name}: ${item.present ? "có" : "không"}`}
                  >
                    <span className="cui-bazi-presence__mark" aria-hidden="true">
                      {item.present ? "✓" : "×"}
                    </span>
                    <BaseText variant="body">{item.name}</BaseText>
                  </span>
                </BaseTooltip>
              </li>
            ))}
          </ul>
          <BaseText variant="caption" tone="muted">
            ✓ Có · × Không · ? Chưa xác định (sau Engine)
          </BaseText>
        </Stack>
      </SectionGate>
    </Card>
  );
});
