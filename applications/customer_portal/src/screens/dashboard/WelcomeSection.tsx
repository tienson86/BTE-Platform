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
        Không gian tư vấn giúp bạn lập lá số, đọc định hướng và theo dõi hồ sơ —
        bình tĩnh, rõ ràng, không phải bảng điều khiển.
      </BaseText>
    </Card>
  );
}
