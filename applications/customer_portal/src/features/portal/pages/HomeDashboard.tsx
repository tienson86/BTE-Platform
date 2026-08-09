import { PortalIcon } from "../components/Icon";
import { PvBadge, PvButton, PvCard } from "../components/primitives";
import type { PortalRoute } from "../chrome/routes";

export function HomePage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <section className="pv-page">
      <header className="pv-hero">
        <p className="pv-kicker">Cổng tư vấn BTE</p>
        <h2 className="pv-display">Hiểu nhịp của mình trước khi quyết định lớn.</h2>
        <p className="pv-lede">
          Không gian này giúp bạn lập lá số, đọc định hướng và học thêm — với giọng tư vấn, không phải bảng điều khiển.
        </p>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("analyze")}>Bắt đầu phân tích mới</PvButton>
          <PvButton variant="secondary" onClick={() => onNavigate("dashboard")}>
            Xem việc nên làm hôm nay
          </PvButton>
        </div>
      </header>
    </section>
  );
}

export function DashboardPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <section className="pv-page">
      <header className="pv-hero pv-hero--compact">
        <p className="pv-kicker">Hôm nay</p>
        <h2 className="pv-heading">Bạn nên hoàn tất một định hướng đang dở.</h2>
        <p className="pv-lede">Ưu tiên đọc lại tư vấn sự nghiệp, rồi mới lập lá số mới.</p>
      </header>
      <div className="pv-grid-2">
        <PvCard
          title={<h3 className="pv-card-title">Tiếp tục tư vấn</h3>}
          footer={
            <PvButton onClick={() => onNavigate("result")}>Mở kết quả đang xem</PvButton>
          }
        >
          <p className="pv-prose">Nguyễn Văn An · Ưu tiên môi trường ổn định.</p>
          <PvBadge tone="success">Sẵn sàng tư vấn</PvBadge>
        </PvCard>
        <PvCard
          title={<h3 className="pv-card-title">Bắt đầu nhanh</h3>}
          footer={
            <PvButton variant="secondary" onClick={() => onNavigate("analyze")}>
              Phân tích mới
            </PvButton>
          }
        >
          <p className="pv-prose">Lập lá số với các bước rõ ràng: ngày sinh → lá số → tiến trình.</p>
        </PvCard>
      </div>
      <PvCard title={<h3 className="pv-card-title">Phân tích gần đây</h3>}>
        <ul className="pv-list">
          <li>
            <button type="button" className="pv-list__row" onClick={() => onNavigate("result")}>
              <span>Nguyễn Văn An</span>
              <PvBadge tone="success">Sẵn sàng</PvBadge>
            </button>
          </li>
          <li>
            <button type="button" className="pv-list__row" onClick={() => onNavigate("results")}>
              <span>Trần Thị Bình</span>
              <PvBadge tone="warning">Đang hoàn thiện</PvBadge>
            </button>
          </li>
        </ul>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Báo cáo ghim</h3>}>
        <p className="pv-prose">Chưa có báo cáo được ghim. Bạn có thể ghim sau khi đọc kết quả.</p>
        <PvButton variant="text" onClick={() => onNavigate("results")}>
          Xem danh sách kết quả
        </PvButton>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Gợi ý kiến thức</h3>}>
        <button type="button" className="pv-list__row" onClick={() => onNavigate("knowledge")}>
          <span className="pv-inline">
            <PortalIcon name="knowledge" />
            Nhật chủ — trục nhận diện trong buổi tư vấn
          </span>
        </button>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Hoạt động gần đây</h3>}>
        <p className="pv-note">Hôm nay · Đã mở tư vấn Nguyễn Văn An</p>
        <p className="pv-note">Hôm qua · Đã lưu nháp Trần Thị Bình</p>
      </PvCard>
    </section>
  );
}
