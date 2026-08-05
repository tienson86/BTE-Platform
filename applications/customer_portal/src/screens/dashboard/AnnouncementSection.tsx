import type { ReactNode } from "react";
import { Alert } from "../../components/feedback/Alert";
import { Card } from "../../components/base/Card";
import { BaseText } from "../../components/base/BaseText";
import { Button } from "../../components/base/Button";
import type { DashboardAnnouncement, DashboardShortcut } from "./mockData";

export type AnnouncementSectionProps = {
  announcement: DashboardAnnouncement;
};

/** Dashboard announcement placeholder (WP04). */
export function AnnouncementSection({
  announcement,
}: AnnouncementSectionProps): ReactNode {
  return (
    <Alert tone="info" title={announcement.title}>
      {announcement.body}
    </Alert>
  );
}

export type ShortcutsSectionProps = {
  shortcuts: readonly DashboardShortcut[];
};

/** Dashboard shortcut cards (WP04). */
export function ShortcutsSection({ shortcuts }: ShortcutsSectionProps): ReactNode {
  return (
    <section className="cui-dashboard__shortcuts" aria-label="Lối tắt">
      {shortcuts.map((item) => (
        <Card
          key={item.id}
          title={item.title}
          footer={
            <Button
              variant="ghost"
              size="sm"
              onClick={() => window.location.assign(item.href)}
            >
              Mở
            </Button>
          }
        >
          <BaseText variant="body" tone="secondary">
            {item.description}
          </BaseText>
        </Card>
      ))}
    </section>
  );
}
