import type { ReactNode } from "react";
import { Button } from "../../components/base/Button";
import type { DashboardQuickAction } from "./mockData";

export type QuickActionsSectionProps = {
  actions: readonly DashboardQuickAction[];
};

/** Dashboard quick action buttons (WP04). */
export function QuickActionsSection({ actions }: QuickActionsSectionProps): ReactNode {
  return (
    <section className="cui-dashboard__actions" aria-label="Thao tác nhanh">
      {actions.map((action) => (
        <Button
          key={action.id}
          variant={action.id === "new-chart" ? "primary" : "secondary"}
          onClick={() => {
            if (typeof window !== "undefined") {
              window.location.assign(action.href);
            }
          }}
        >
          {action.label}
        </Button>
      ))}
    </section>
  );
}
