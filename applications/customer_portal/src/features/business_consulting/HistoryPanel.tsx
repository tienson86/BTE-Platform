import type { ReactNode } from "react";
import type { BusinessHistoryItem } from "./api";
import { IconFolder } from "../../screens/canonical_desktop/icons";

type Props = {
  items: BusinessHistoryItem[];
  loading: boolean;
  error: string;
  activeId: string | null;
  disabled: boolean;
  hasMore: boolean;
  onOpen: (id: string) => void;
  onRefresh: () => void;
  onLoadMore: () => void;
};

export function BusinessHistoryPanel({ items, loading, error, activeId, disabled, hasMore, onOpen, onRefresh, onLoadMore }: Props): ReactNode {
  return (
    <section className="mc-history" data-testid="business-history">
      <div className="mc-history__heading">
        <h2>Hồ sơ tư vấn hợp tác</h2>
        <button type="button" className="secondary" disabled={disabled || loading} onClick={onRefresh}>Làm mới danh sách</button>
      </div>
      {loading ? <p role="status">Đang tải hồ sơ...</p> : null}
      {error ? <p role="alert">{error}</p> : null}
      {!loading && !error && !items.length ? <p className="muted">Chưa có hồ sơ tư vấn hợp tác đã lưu.</p> : null}
      <div className="mc-history__list">
        {items.map((item) => (
          <article className="bte-card mc-history__item" key={item.consultation_id}>
            <div>
              <h3>{item.display_identity}</h3>
              <p>{item.occupation_label}</p>
              <p className="muted">{formatDate(item.saved_at || item.created_at)}</p>
            </div>
            <button type="button" className="secondary" disabled={disabled} onClick={() => onOpen(item.consultation_id)} aria-current={item.consultation_id === activeId ? "true" : undefined}>
              <IconFolder size={16} /> {item.consultation_id === activeId ? "Đang xem" : "Mở hồ sơ"}
            </button>
          </article>
        ))}
      </div>
      {hasMore ? <button type="button" className="secondary" disabled={disabled || loading} onClick={onLoadMore}>Xem thêm hồ sơ</button> : null}
    </section>
  );
}

function formatDate(value: string): string {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString("vi-VN");
}
