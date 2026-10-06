import type { ReactNode } from "react";

import type { MarriageHistoryItemDto } from "./types";

type Props = {
  items: MarriageHistoryItemDto[];
  loading: boolean;
  error: string;
  activeId: string | null;
  onOpen: (consultationId: string) => void;
};

export function MarriageHistoryPanel({ items, loading, error, activeId, onOpen }: Props): ReactNode {
  return (
    <section className="mc-history" data-testid="marriage-history">
      <div className="mc-history__heading">
        <div>
          <h2>Hồ sơ tư vấn hôn nhân</h2>
          <p className="muted">Các cặp đã phân tích được lưu lại để mở và xuất báo cáo khi cần.</p>
        </div>
        <strong>{items.length} hồ sơ</strong>
      </div>
      {loading ? <p className="muted" role="status">Đang tải hồ sơ...</p> : null}
      {error ? <p className="mc-history__error" role="alert">{error}</p> : null}
      {!loading && !error && !items.length ? (
        <p className="muted">Chưa có hồ sơ tư vấn hôn nhân nào.</p>
      ) : null}
      {items.length ? (
        <div className="mc-history__list">
          {items.map((item) => (
            <article className="bte-card mc-history__item" key={item.consultation_id}>
              <div>
                <h3>{item.display_identity || "Cặp đôi chưa đặt tên"}</h3>
                <p className="muted">{formatCreatedAt(item.created_at)}</p>
              </div>
              <div className="mc-history__metrics">
                <span>{item.score === null ? "Chưa chấm điểm" : `${item.score}/100`}</span>
                {item.grade ? <strong>Xếp loại {item.grade}</strong> : null}
              </div>
              <button
                type="button"
                className="secondary"
                aria-current={activeId === item.consultation_id ? "true" : undefined}
                onClick={() => onOpen(item.consultation_id)}
              >
                {activeId === item.consultation_id ? "Đang mở" : "Mở hồ sơ"}
              </button>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}

function formatCreatedAt(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value || "—";
  return date.toLocaleString("vi-VN");
}
