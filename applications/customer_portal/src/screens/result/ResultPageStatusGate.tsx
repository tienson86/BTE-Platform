/**
 * Accessible Result Page gate states — PACK_05 (loading / empty / error).
 * Presentation-only. Does not alter zone architecture.
 */

import type { ReactNode } from "react";
import type { CanonicalDesktopStatus } from "../../adapters";
import { EmptyState } from "../../components/feedback/EmptyState";
import { ErrorState } from "../../components/feedback/ErrorState";
import { Skeleton } from "../../components/feedback/Skeleton";

export type ResultPageStatusGateProps = {
  readonly status: Exclude<CanonicalDesktopStatus, "ready">;
  readonly message?: string | null;
};

/**
 * Renders accessible loading, empty, or error state for the Result Page body.
 */
export function ResultPageStatusGate({
  status,
  message,
}: ResultPageStatusGateProps): ReactNode {
  if (status === "loading") {
    return (
      <div
        className="rp-status-gate"
        role="status"
        aria-live="polite"
        aria-busy="true"
        aria-label="Đang tải kết quả phân tích"
        data-status="loading"
      >
        <Skeleton height="1.5rem" width="36%" />
        <Skeleton height="8rem" width="100%" />
        <Skeleton height="8rem" width="100%" />
        <Skeleton height="6rem" width="100%" />
        <p className="rp-status-gate__sr">{message ?? "Đang tải kết quả…"}</p>
      </div>
    );
  }

  if (status === "empty") {
    return (
      <div
        className="rp-status-gate"
        role="status"
        aria-live="polite"
        data-status="empty"
      >
        <EmptyState
          title="Chưa có kết quả"
          description={message ?? "Nhập thông tin sinh để xem lá số Bát Tự."}
        />
      </div>
    );
  }

  return (
    <div
      className="rp-status-gate"
      data-status="error"
    >
      <ErrorState
        title="Không tải được kết quả"
        description={message ?? "Vui lòng thử lại sau."}
      />
    </div>
  );
}
