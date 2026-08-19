import { memo, type ReactNode } from "react";
import { Badge } from "../../components/base/Badge";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { BaseTooltip } from "../../components/base/BaseTooltip";
import { ScoreBar } from "../../components/display/ScoreBar";
import type {
  BaZiFiveElement,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type FiveElementsCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  elements: readonly BaZiFiveElement[];
  errorMessage?: string;
};

/** WP07 — Five Elements Card (no chart library). */
export const FiveElementsCard = memo(function FiveElementsCard({
  status,
  labels,
  elements,
  errorMessage,
}: FiveElementsCardProps): ReactNode {
  return (
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
        <div className="cui-bazi-elements__layout">
          <div className="cui-bazi-elements__bars" aria-label="Biểu đồ phân bố">
            {elements.map((element) => (
              <BaseTooltip
                key={element.id}
                content={`${element.name}: ${element.score}${element.strength ? ` · ${element.strength}` : ""}`}
              >
                <div className="cui-bazi-elements__bar-item">
                  <ScoreBar
                    label={element.name}
                    value={element.percentage}
                    max={100}
                  />
                </div>
              </BaseTooltip>
            ))}
          </div>
          <ul className="cui-bazi-elements__legend" aria-label="Chú thích phần trăm">
            {elements.map((element) => (
              <li key={element.id} className="cui-bazi-elements__legend-item">
                <BaseText variant="body">{element.name}</BaseText>
                <Badge tone="info">{element.percentage}%</Badge>
                <BaseText variant="caption" tone="muted">
                  {labels.score}: {element.score}
                </BaseText>
                <Badge tone="neutral">{element.strength}</Badge>
              </li>
            ))}
          </ul>
        </div>
      </SectionGate>
    </Card>
  );
});
