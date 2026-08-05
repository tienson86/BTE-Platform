import { memo, type ReactNode } from "react";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { Stack } from "../../components/layout/Stack";
import type {
  BaZiInterpretationBlock,
  BaZiResultLabels,
  PresentationStatus,
} from "./mockData";
import { SectionGate } from "./SectionGate";

export type InterpretationCardProps = {
  status: PresentationStatus;
  labels: BaZiResultLabels;
  interpretation: BaZiInterpretationBlock;
  errorMessage?: string;
};

/** Canonical Result — Interpretation tier (same mock facts, reading layout). */
export const InterpretationCard = memo(function InterpretationCard({
  status,
  labels,
  interpretation,
  errorMessage,
}: InterpretationCardProps): ReactNode {
  return (
    <Card
      title={labels.interpretationTitle}
      className="cui-bazi-interpretation"
      aria-label={labels.interpretationTitle}
    >
      <SectionGate
        status={status}
        loadingLabel="Đang tải Luận Giải"
        emptyTitle="Chưa có luận giải"
        emptyDescription="Luận giải sẽ hiển thị sau khi Interpretation Engine được nối."
        errorTitle="Không tải được Luận Giải"
        errorDescription={errorMessage}
      >
        <Stack gap="paragraph" className="cui-bazi-interpretation__body">
          {interpretation.paragraphs.map((paragraph) => (
            <BaseText key={paragraph} variant="body">
              {paragraph}
            </BaseText>
          ))}
        </Stack>
      </SectionGate>
    </Card>
  );
});
