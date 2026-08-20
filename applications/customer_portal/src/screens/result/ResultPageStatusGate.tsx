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
  readonly action?: ReactNode;
};

/**
 * Renders accessible loading, empty, or error state for the Result Page body.
 */
export function ResultPageStatusGate({
  status,
  message,
  action,
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
          title="Chưa có kết quả phân tích"
          description={
            message ??
            "Vui lòng nhập thông tin ngày giờ sinh để bắt đầu."
          }
          action={
            action ?? (
              <a className="rp-status-gate__cta" href="/analyze">
                Nhập ngày giờ sinh
              </a>
            )
          }
        />
      </div>
    );
  }

  const isVersion = Boolean(message && /phiên bản dữ liệu cũ|chưa đủ hợp đồng/i.test(message));
  return (
    <div
      className="rp-status-gate"
      data-status="error"
      data-reason={isVersion ? "contract" : "error"}
    >
      <ErrorState
        title={isVersion ? "Kết quả cần phân tích lại" : "Không tải được kết quả"}
        description={message ?? "Vui lòng thử lại sau."}
        action={
          action ?? (
            <a className="rp-status-gate__cta" href="/analyze">
              Phân tích lại
            </a>
          )
        }
      />
    </div>
  );
}
