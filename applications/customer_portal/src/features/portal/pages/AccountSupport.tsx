import { useState } from "react";
import type { PortalRoute } from "../chrome/routes";
import { PvButton, PvCard, PvCheckbox, PvDialog, PvDrawer, PvInput, PvSelect, PvTextarea } from "../components/primitives";
import { PvEmpty, PvError, PvLoading } from "../components/states";

export function ProfilePage() {
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Thông tin cá nhân</h2>}>
        <div className="pv-form-grid">
          <PvInput label="Họ và tên" defaultValue="Nguyễn Văn An" />
          <PvInput label="Thư điện tử" defaultValue="an@example.vn" />
        </div>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Tùy chọn</h3>}>
        <PvSelect label="Ngôn ngữ" defaultValue="vi">
          <option value="vi">Tiếng Việt</option>
        </PvSelect>
        <p className="pv-note">Giao diện sáng/tối sẽ có ở phiên sau.</p>
      </PvCard>
      <PvCard title={<h3 className="pv-card-title">Riêng tư</h3>}>
        <PvCheckbox label="Cho phép lưu lịch sử tư vấn trên thiết bị này" defaultChecked />
        <p className="pv-note">Chia sẻ tóm tắt chỉ khi bạn chọn Chia sẻ trên trang kết quả.</p>
      </PvCard>
    </section>
  );
}

export function HistoryPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Lịch sử tư vấn</h2>}>
        <p className="pv-prose">Mở lại báo cáo đã lưu hoặc tiếp tục bản nháp.</p>
        <ul className="pv-list">
          <li>
            <button type="button" className="pv-list__row" onClick={() => onNavigate("result")}>
              <span>10/08/2026 · Nguyễn Văn An · Đã lưu</span>
              <span>Mở tư vấn</span>
            </button>
          </li>
          <li>
            <button type="button" className="pv-list__row" onClick={() => onNavigate("analyze-progress")}>
              <span>03/08/2026 · Trần Thị Bình · Nháp</span>
              <span>Tiếp tục phân tích</span>
            </button>
          </li>
        </ul>
      </PvCard>
    </section>
  );
}

export function SettingsPage() {
  const [dialog, setDialog] = useState(false);
  const [drawer, setDrawer] = useState(false);
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Cài đặt</h2>}>
        <PvCheckbox label="Nhận gợi ý kiến thức sau mỗi buổi tư vấn" defaultChecked />
        <PvTextarea label="Ghi chú hiển thị trên hồ sơ" rows={3} defaultValue="" />
        <div className="pv-cta-row">
          <PvButton onClick={() => setDialog(true)}>Lưu tùy chọn</PvButton>
          <PvButton variant="secondary" onClick={() => setDrawer(true)}>
            Xem nhanh quyền riêng tư
          </PvButton>
        </div>
      </PvCard>
      <PvDialog open={dialog} title="Đã ghi nhận" onClose={() => setDialog(false)}>
        <p className="pv-prose">Tùy chọn được lưu trên giao diện này. Chưa gửi lên máy chủ.</p>
      </PvDialog>
      <PvDrawer open={drawer} title="Riêng tư" onClose={() => setDrawer(false)}>
        <p className="pv-prose">Portal không lưu mật khẩu hay mã kỹ thuật trên màn hình này.</p>
        <PvButton variant="text" onClick={() => setDrawer(false)}>
          Đóng
        </PvButton>
      </PvDrawer>
    </section>
  );
}

export function HelpPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Trợ giúp</h2>}>
        <p className="pv-prose">Nếu buổi tư vấn chưa hiện, hãy thử lại, quay về tổng quan, hoặc để lại nhu cầu hỗ trợ.</p>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("dashboard")}>Về tổng quan</PvButton>
          <PvButton variant="secondary" onClick={() => onNavigate("analyze")}>
            Lập phân tích mới
          </PvButton>
          <PvButton variant="text" onClick={() => onNavigate("premium")}>
            Nhờ tư vấn chuyên sâu
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function AboutPage() {
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Giới thiệu BTE</h2>}>
        <p className="pv-prose">
          BTE là nền tảng tư vấn Bát Tự: giúp hiểu nhịp, lý do và việc nên làm — không phải máy tính số mệnh.
        </p>
      </PvCard>
    </section>
  );
}

export function NotFoundPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <PvEmpty
      title="Không tìm thấy trang này"
      body="Đường dẫn không còn hoặc chưa được mở trong cổng tư vấn."
      actionLabel="Về trang chủ"
      onAction={() => onNavigate("home")}
    />
  );
}

export function ErrorPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <PvError
      title="Không thể hiển thị buổi tư vấn"
      body="Đã có sự cố khi mở trang. Hãy thử lại, quay về tổng quan, hoặc mở trợ giúp. Không cần mã kỹ thuật."
      actionLabel="Về tổng quan"
      onAction={() => onNavigate("dashboard")}
    />
  );
}

export function LoadingPage() {
  return <PvLoading label="Đang tải cổng tư vấn" />;
}

export function EmptyPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  return (
    <PvEmpty
      title="Tạo báo cáo đầu tiên"
      body="Chưa có buổi tư vấn nào trên thiết bị này. Bắt đầu khi bạn sẵn sàng."
      actionLabel="Tạo báo cáo đầu tiên"
      onAction={() => onNavigate("analyze")}
    />
  );
}
