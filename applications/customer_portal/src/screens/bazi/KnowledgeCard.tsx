import { memo, type ReactNode } from "react";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import type {
  BaZiKnowledgeItem,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type KnowledgeCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  items: readonly BaZiKnowledgeItem[];
  errorMessage?: string;
};

/** Canonical Result — Knowledge tier (references only; no Engine). */
export const KnowledgeCard = memo(function KnowledgeCard({
  status,
  labels,
  items,
  errorMessage,
}: KnowledgeCardProps): ReactNode {
  return (
    <Card
      title={labels.knowledgeTitle}
      className="cui-bazi-knowledge"
      aria-label={labels.knowledgeTitle}
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải Tri Thức"
        emptyTitle="Chưa có liên kết tri thức"
        emptyDescription="Knowledge Pack sẽ được gắn sau UI Freeze."
        errorTitle="Không tải được Tri Thức"
        errorDescription={errorMessage}
      >
        <ul className="cui-bazi-knowledge__list">
          {items.map((item) => (
            <li key={item.id} className="cui-bazi-knowledge__item">
              <BaseText variant="body">{item.title}</BaseText>
              <BaseText variant="caption" tone="muted">
                {item.reference}
              </BaseText>
            </li>
          ))}
        </ul>
      </SectionGate>
    </Card>
  );
});
