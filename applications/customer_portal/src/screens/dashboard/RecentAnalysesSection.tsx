import type { ReactNode } from "react";
import { Button } from "../../components/base/Button";
import { BaseText } from "../../components/base/BaseText";
import { Card } from "../../components/base/Card";
import { Badge } from "../../components/base/Badge";
import { EmptyState } from "../../components/feedback/EmptyState";
import type { DashboardRecentAnalysis } from "./mockData";

export type RecentAnalysesSectionProps = {
  items: readonly DashboardRecentAnalysis[];
};

const STATUS_LABEL: Record<DashboardRecentAnalysis["status"], string> = {
  ready: "Sẵn sàng",
  draft: "Nháp",
  processing: "Đang xử lý",
};

/** Dashboard recent analyses list (WP04). */
export function RecentAnalysesSection({
  items,
}: RecentAnalysesSectionProps): ReactNode {
  return (
    <Card title="Phân tích gần đây" className="cui-dashboard-recent">
      {items.length === 0 ? (
        <EmptyState
          title="Chưa có lá số nào"
          description="Bắt đầu bằng cách lập lá số mới."
          action={
            <Button variant="primary" onClick={() => window.location.assign("/analyze")}>
              Lập Lá Số Mới
            </Button>
          }
        />
      ) : (
        <ul className="cui-dashboard-recent__list">
          {items.map((item) => (
            <li key={item.id} className="cui-dashboard-recent__item">
              <div className="cui-dashboard-recent__meta">
                <BaseText variant="subsection">{item.fullName}</BaseText>
                <BaseText variant="caption" tone="muted">
                  {item.createdAt}
                </BaseText>
              </div>
              <Badge>{STATUS_LABEL[item.status]}</Badge>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => window.location.assign(item.href)}
              >
                Mở
              </Button>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
