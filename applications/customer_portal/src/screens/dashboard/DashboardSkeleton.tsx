import type { ReactNode } from "react";
import { Skeleton } from "../../components/feedback/Skeleton";
import { Stack } from "../../components/layout/Stack";

/** Dashboard loading skeleton (WP04). */
export function DashboardSkeleton(): ReactNode {
  return (
    <div className="cui-dashboard-skeleton" aria-busy="true" aria-label="Đang tải dashboard">
      <Stack gap="list">
        <Skeleton height="4rem" width="100%" />
        <Skeleton height="2.75rem" width="100%" />
        <Skeleton height="6rem" width="100%" />
        <Skeleton height="8rem" width="100%" />
      </Stack>
    </div>
  );
}
