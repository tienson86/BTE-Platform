import { useState } from "react";
import type { PortalRoute } from "../chrome/routes";
import { PvButton, PvCard, PvDialog } from "../components/primitives";

const ONBOARDING_STEPS = [
  {
    kicker: "Chào mừng",
    title: "Bạn sắp có một buổi tư vấn có cấu trúc.",
    body: "BTE giúp bạn hiểu nhịp của mình rồi mới quyết định — không phải máy tính số mệnh.",
  },
  {
    kicker: "BTE làm gì",
    title: "Hiểu lý do, rồi biết việc nên làm.",
    body: "Kết quả gồm tóm tắt, định hướng chính và lưu ý. Kiến thức chỉ mở khi bạn muốn đọc thêm.",
  },
  {
    kicker: "Chuẩn bị",
    title: "Ngày sinh càng rõ, tư vấn càng chắc.",
    body: "Cần họ tên, nơi sinh, ngày và giờ sinh nếu nhớ. Không sao nếu thiếu giờ — buổi vẫn mở được.",
  },
  {
    kicker: "Riêng tư",
    title: "Thông tin dùng để tư vấn, không để phô trương.",
    body: "Màn hình chính không hiện mã kỹ thuật. Bạn chỉ chia sẻ khi chủ động chọn Chia sẻ.",
  },
  {
    kicker: "Kết quả kỳ vọng",
    title: "Một buổi đọc được trong vài phút.",
    body: "Bạn sẽ thấy mình là ai trong giai đoạn này, nên làm gì, và điều gì cần thận trọng.",
  },
  {
    kicker: "Thời gian chờ",
    title: "Thường dưới một phút sau khi gửi ngày sinh.",
    body: "Trong lúc chờ, hãy giữ yên — không cần thao tác kỹ thuật.",
  },
] as const;

export function OnboardingPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  const [step, setStep] = useState(0);
  const current = ONBOARDING_STEPS[step];
  const last = step === ONBOARDING_STEPS.length - 1;
  return (
    <section className="pv-page">
      <p className="pv-note">
        Bước {step + 1} / {ONBOARDING_STEPS.length}
      </p>
      <PvCard>
        <p className="pv-kicker">{current.kicker}</p>
        <h2 className="pv-heading">{current.title}</h2>
        <p className="pv-lede">{current.body}</p>
        <div className="pv-cta-row">
          {last ? (
            <PvButton onClick={() => onNavigate("analyze")}>Bắt đầu phân tích</PvButton>
          ) : (
            <PvButton onClick={() => setStep((value) => value + 1)}>Tiếp tục</PvButton>
          )}
          <PvButton variant="text" onClick={() => onNavigate("home")}>
            Tôi đã hiểu — vào trang chủ
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function CompletionPage({
  onNavigate,
}: {
  onNavigate: (route: PortalRoute) => void;
}) {
  return (
    <section className="pv-page" data-state="success">
      <PvCard title={<h2 className="pv-heading">Báo cáo đã được lưu</h2>}>
        <p className="pv-prose">Bạn có thể mở lại từ Lịch sử, đọc kiến thức liên quan, hoặc đặt tư vấn chuyên sâu sau.</p>
        <div className="pv-cta-row">
          <PvButton onClick={() => onNavigate("history")}>Xem lịch sử</PvButton>
          <PvButton variant="secondary" onClick={() => onNavigate("result")}>
            Quay lại tư vấn
          </PvButton>
          <PvButton variant="text" onClick={() => onNavigate("premium")}>
            Đặt tư vấn chuyên sâu
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function PremiumPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  const [sent, setSent] = useState(false);
  return (
    <section className="pv-page">
      <PvCard title={<h2 className="pv-heading">Tư vấn chuyên sâu</h2>}>
        <p className="pv-prose">
          Sau khi đọc định hướng, bạn có thể trao đổi với chuyên gia. Chưa thu phí trong bước này.
        </p>
        {sent ? (
          <p className="pv-prose">Đã ghi nhận nhu cầu. Chúng tôi chưa mở lịch thanh toán.</p>
        ) : (
          <PvButton onClick={() => setSent(true)}>Để lại nhu cầu tư vấn</PvButton>
        )}
        <div className="pv-cta-row">
          <PvButton variant="text" onClick={() => onNavigate("result")}>
            Quay lại tư vấn
          </PvButton>
        </div>
      </PvCard>
    </section>
  );
}

export function KnowledgeArticlePage({
  onBackToResult,
  onNavigate,
}: {
  onBackToResult: () => void;
  onNavigate: (route: PortalRoute) => void;
}) {
  return (
    <section className="pv-page">
      <article className="pv-card pv-article">
        <p className="pv-kicker">Kiến thức bổ sung</p>
        <h2 className="pv-heading">Nhật chủ</h2>
        <p className="pv-prose">
          Nhật chủ là trục nhận diện trong buổi tư vấn. Đọc bài này để hiểu thuật ngữ — rồi quay lại định hướng vừa nhận.
        </p>
        <p className="pv-prose">Kiến thức không thay thế việc cần làm trong báo cáo.</p>
        <div className="pv-cta-row">
          <PvButton onClick={onBackToResult}>Quay lại tư vấn</PvButton>
          <PvButton variant="secondary" onClick={() => onNavigate("knowledge")}>
            Xem thêm bài khác
          </PvButton>
        </div>
      </article>
    </section>
  );
}

export function ShareSheet({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  return (
    <PvDialog open={open} title="Chia sẻ tóm tắt tư vấn" onClose={onClose}>
      <p className="pv-prose">Nguyễn Văn An · Ưu tiên môi trường ổn định trước khi mở rộng trách nhiệm.</p>
      <p className="pv-note">Chỉ chia sẻ khi bạn chủ động. Liên kết chưa gửi lên máy chủ.</p>
      <PvButton variant="secondary" onClick={onClose}>
        Sao chép liên kết (xem trước)
      </PvButton>
    </PvDialog>
  );
}
