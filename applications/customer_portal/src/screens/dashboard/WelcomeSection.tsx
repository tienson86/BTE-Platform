import type { ReactNode } from "react";
import { BaseText } from "../../components/base/BaseText";
import { Card } from "../../components/base/Card";

export type WelcomeSectionProps = {
  userName?: string;
};

/** Dashboard welcome block — Canonical hero tier (same copy). */
export function WelcomeSection({ userName }: WelcomeSectionProps): ReactNode {
  const greeting = userName ? `Xin chào, ${userName}` : "Xin chào";
  return (
    <Card className="cui-dashboard-welcome">
      <BaseText variant="section">{greeting}</BaseText>
      <BaseText variant="body" tone="secondary">
        BTE Portal giúp bạn lập lá số, xem kết quả Bát Tự và theo dõi báo cáo —
        tất cả trong một không gian làm việc thống nhất.
      </BaseText>
    </Card>
  );
}
